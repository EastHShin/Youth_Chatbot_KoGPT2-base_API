from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
from flask import Flask, request, jsonify, render_template
from queue import Queue, Empty
from threading import Thread
import torch
import time

app = Flask(__name__)
U_TKN = '<usr>'
S_TKN = '<sys>'
MASK = '<unused0>'
SENT = '<unused1>'
tokenizer = PreTrainedTokenizerFast.from_pretrained("EasthShin/Youth_Chatbot_Kogpt2-base",
  bos_token='</s>', eos_token='</s>', unk_token='<unk>',
  pad_token='<pad>', mask_token=MASK)

model = GPT2LMHeadModel.from_pretrained('EasthShin/Youth_Chatbot_Kogpt2-base')
requests_queue = Queue()
BATCH_SIZE = 1
CHECK_INTERVAL = 0.1

print("complete model loading")



def handle_requests_by_batch():
    while True:
        request_batch = []
        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))

            except Empty:
                continue
            for requests in request_batch:
                try:
                    res = make_answer(requests["inputs"][0])
                    requests["output"] = res

                except Exception as e:
                    requests["output"] = e


handler = Thread(target=handle_requests_by_batch).start()

def make_answer(text, sent='0'):
    global U_TKN
    global S_TKN
    try:
        input_ids = tokenizer.encode(U_TKN + text + sent + S_TKN)
        gen_ids = model.generate(torch.tensor([input_ids]),
                                 max_length=128,
                                 repetition_penalty= 2.0,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 use_cache=True)


        generated = tokenizer.decode(gen_ids[0, :].tolist())

        return generated

    except Exception as e:
        print('Error occur in getting label!', e)
        return jsonify({'error': e}), 500

@app.route('/chat', methods=['POST'])
def chat():

    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'message' : 'Invalid request'}), 500

    try:
        args = []
        question = request.form['question']
        args.append(question)
    except Exception as e:
        return jsonify({'message' : 'Invalid request'})
    req = {'inputs': args}
    print(req)
    requests_queue.put(req)
    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)
    res = req['output']
    idx = res.find('<sys>')
    res = res[idx+5:-4]

    return res

@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return 'clear', 200


@app.route('/healthz', methods=['GET'])
def health_check():
    return "Health OK", 200

@app.route('/')
def main():
    return render_template('index.html'), 200

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')