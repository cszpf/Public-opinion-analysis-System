import os
import jieba
import numpy as np
INPUTFILE = './Data/Setting/All_Topics_DOC_Topic.csv'
N_TOPIC = 10
THREAD = round(1/N_TOPIC, 4)
OUTPUTFILE = './Data/Setting/All_topic_title.txt'

def Load_File(outfile=OUTPUTFILE, intfile=INPUTFILE, thread=THREAD):
    # titles denotes title_list
    titles = []
    # topic_dict denotes {topic:[arg in titles]}
    topic_dict = {i: [] for i in range(N_TOPIC)}
    with open(intfile, 'rb+') as fr:
        datas = fr.read()
    data = datas.decode('utf-8').strip().split('\n')
    print(len(data))
    for i in range(0, len(data), 2):
        title = data[i]
        titles.append(title)
        vec = data[i+1].split(',')
        vec = [round(float(i), 4) for i in vec]
        # for j in range(-1, -4, -1):
        #     if vec[np.argsort(vec)[j]] > thread:
        topic_dict[np.argsort(vec)[-1]].append(len(titles) - 1)
    with open(outfile, 'wb+') as fw:
        for i in range(N_TOPIC):
            fw.write(('Topic%4s\n'%i).encode('utf-8', 'ignore'))
            fw.write(('\n'.join([titles[j] for j in topic_dict[i]])).encode('utf-8', 'ignore'))
            fw.write('\n'.encode('utf-8', 'ignore'))
    return titles, topic_dict

Load_File()