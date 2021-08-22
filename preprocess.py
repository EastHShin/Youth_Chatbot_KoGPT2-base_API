import json
import csv
import re
from collections import OrderedDict
import pandas as pd
#
# file_data = OrderedDict()
# sentence_List = []
# clf_List = []

with open('감성대화말뭉치(최종데이터)_Training.json', 'r') as f:
    with open('edit_dialog_corpus_training.csv', 'w', newline='\n') as cs:
        json_data = json.load(f)
        wr = csv.writer(cs)
        wr.writerow(['Q', 'A', 'label'])
        for i in range(len(json_data)):
            age_type = gender_type = json_data[i]['profile']['persona']['human'][0]
            if age_type != 'A01' and age_type != 'A02':
                continue
            emotion_type = json_data[i]['profile']['emotion']['type']
            integer_emotion = int(emotion_type[1:3])
            if integer_emotion >= 10 and integer_emotion <= 19:
                emotion = '0'
            elif integer_emotion >= 20 and integer_emotion <= 29:
                emotion = '1'
            elif integer_emotion >= 30 and integer_emotion <= 39:
                emotion = '2'
            elif integer_emotion >= 40 and integer_emotion <= 49:
                emotion = '3'
            elif integer_emotion >= 50 and integer_emotion <= 59:
                emotion = '4'
            elif integer_emotion >= 60 and integer_emotion <= 69:
                emotion = '5'
            human1 = json_data[i]['talk']['content']['HS01']
            system1 = json_data[i]['talk']['content']['SS01']
            wr.writerow([human1, system1, emotion])

            human2 = json_data[i]['talk']['content']['HS02']
            system2 = json_data[i]['talk']['content']['SS02']
            if human2 != '' and system2 != '':
                wr.writerow([human2, system2, emotion])

            human3 = json_data[i]['talk']['content']['HS03']
            system3 = json_data[i]['talk']['content']['SS03']
            if human3 != '' and system3 != '':
                wr.writerow([human3, system3, emotion])


    # gender_type = json_data[0]['profile']['persona']['human'][1]
    # emotion_type = json_data[0]['profile']['emotion']['type']
    # human1 = json_data[0]['talk']['content']['HS01']
    # system1 = json_data[0]['talk']['content']['SS01']
    # human2 = json_data[0]['talk']['content']['HS02']
    # system2 = json_data[0]['talk']['content']['SS02']
    # human3 = json_data[0]['talk']['content']['HS03']
    # system3 = json_data[0]['talk']['content']['SS03']



# with open('lyrics-v5.csv', 'r') as f:
#     with open("edit_lyrics_bts.csv", 'w', encoding='utf-8', newline='') as wf:
#         rdr = csv.reader(f)
#         wr = csv.writer(wf)
#         for row in rdr:
#             if row[0] == "12" or row[0] == "2":
#                 continue
#             data = row[8]
#             edit_data = re.sub('[\n\t]', " ", data)
#             edit_data = re.sub('[^a-zA-Z0-9\',]', " ", edit_data)
#             edit_data = re.sub(' +', ' ', edit_data)
#             print(edit_data)
#             if edit_data == "":
#                 continue
#             wr.writerow([edit_data])
# mystr = ""
# with open('edit_lyrics_bts.csv', 'r') as rd:
#     r = csv.reader(rd)
#     for row in r:
#         mystr += row[0] + '\n'
#
# with open('bts-lyrics.txt', 'w', encoding='utf-8') as f:
#     f.write(mystr)


# with open("dataset.txt", 'r') as f:
#     with open("hate_speech_data_Wammad.csv", 'r') as c:
#         rdr = csv.reader(c)
#         count = 0
#
#         with open("train.tsv", 'w', encoding='utf-8', newline='') as t:
#             wr = csv.writer(t, delimiter='\t')
#             for i in range(5825):
#                 data = f.readline().split('|')
#                 edit_data = re.sub('[\n]', "", data[1])
#                 tmp_data = [data[0], edit_data]
#                 wr.writerow(tmp_data)
#             for row in rdr:
#                 if count == 0:
#                     count += 1
#                     continue
#                 tmp_data = [row[1], row[2]]
#                 wr.writerow(tmp_data)

# with open("train.tsv", 'r') as z:
#     with open("train_r.tsv", 'w', encoding='utf-8', newline='') as tr:
#         with open("test.tsv", 'w', encoding='utf-8', newline='') as ts:
#             rd = csv.reader(z, delimiter='\t')
#             wr = csv.writer(tr, delimiter='\t')
#             twr = csv.writer(ts, delimiter='\t')
#             count = 0
#             for row in rd:
#                 sentence = re.sub('[\n\t]', " ", row[0])
#                 if row[1] != "0" and row[1] != "1":
#                     row[1] = "0"
#                 label = re.sub('[^0-1]', "", row[1])
#                 data = [sentence, label]
#                 if count < 6000:
#                     wr.writerow(data)
#                 else:
#                     twr.writerow(data)
#                 count += 1

# group_data = OrderedDict()
# with open("train_r.tsv", 'r') as read:
#     rd = csv.reader(read, delimiter='\t')
#     for row in rd:
#         sentence_List.append(row[0])
#         clf_List.append(row[1])
#     file_data["sentence"] = sentence_List
#     file_data["corse"] = clf_List
#     group_data["data"] = file_data
#     with open("train.json", 'w', encoding="utf-8") as makefile:
#         json.dump(group_data, makefile, ensure_ascii=False, indent='\t')
#
# test_sentence = []
# test_clf = []
# with open("test.tsv", 'r') as read:
#     rd = csv.reader(read, delimiter='\t')
#     for row in rd:
#         test_sentence.append(row[0])
#         test_clf.append(row[1])
#     file_data["sentence"] = test_sentence
#     file_data["corse"] = test_clf
#     group_data["data"] = file_data
#     with open("test.json", 'w', encoding="utf-8") as makefile:
#         json.dump(group_data, makefile, ensure_ascii=False, indent='\t')