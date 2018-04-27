import os
import time
import pickle as pk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def load_model(filename='./Data/Setting/model.pk'):
    fr = open(filename, 'rb')
    model = pk.load(fr)
    fr.close()
    return model

def save_model(model, filename='./Data/Setting/model.pk'):
    fw = open(filename, 'wb')
    pk.dump(model, fw)
    fw.close()

#   判断字符串是否全部由数字.%以及英文单词组成
def isNumeric(s):
    """return True if string s is numeric"""
    return all([c in "0123456789.%ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" for c in s])

# 获取一个目录下的所有非目录文件
def file_name(file_dir):
    file_list = []
    f_num = 0
    for root, dirs, files in os.walk(file_dir):
        for subfile in files:
            f_num += 1
            file_list.append(os.path.join(root, subfile))
    print(f_num)
    return file_list

# 引入停用词
def stopwr():
    # 从文件导入停用词表
    stpwrdpath = "./Data/stopwords.txt"
    stpwrd_dic = open(stpwrdpath, 'rb+')
    stpwrd_content = stpwrd_dic.read()
    # 将停用词表转换为list
    stpwrdlst = stpwrd_content.splitlines()
    ''' for i in stpwrdlst:
        print (i)  '''
    stpwrd_dic.close()
    return stpwrdlst

# LDA
def My_LDA(infile, outfile):
    '''
    :param infile:分好词的数据所在的目录
    :param outfile:一个包含四个元素的列表[前两个与模型保存路径,
    第三个参数为文档-主题矩阵保存路径,最后一个是前20个词的词-主题矩阵保存路径]
    :return:
    '''
    # 文件名列表
    res_list = file_name(infile)
    # print([i.split('\\')[-1] for i in res_list])
    stpwrdlst = stopwr()
    corpus, i = [], 0
    for res in res_list:
        i += 1
        exec("""with open(res, 'rb+') as f3:
        \n  res{id} = f3.read()""".format(id=str(i)))
        exec("corpus.append(res{id})".format(id=str(i)))

    # 构建词汇统计向量并保存
    cntVector = CountVectorizer(stop_words=stpwrdlst)
    # tfVector = TfidfVectorizer(stop_words = stpwrdlst)
    # 文档__词稀疏矩阵
    cntTf = cntVector.fit_transform(corpus)
    # print(cntTf, '\nThis is a doc_word_Matrix')
    # 主题个数
    n_topic = 10
    lda = LatentDirichletAllocation(n_components=n_topic, max_iter=100, learning_method='batch', learning_offset=60.)
    # docres是文档主题分布
    lda.fit(cntTf)
    docres = lda.transform(cntTf)
    # print(docres)
    # 保存文档-主题分布矩阵
    with open(outfile[-2], 'wb+') as fw:
        for title, vec in zip([i.split('\\')[-1] for i in res_list], docres):
            fw.write('{}'.format(title).encode('utf-8') + '\n'.encode('utf-8'))
            fw.write(','.join([str(x) for x in vec]).encode('utf-8') + '\n'.encode('utf-8'))

    save_model(model=docres, filename=outfile[0])
    topic_name, topic_data = [], []
    tf_feature_names = cntVector.get_feature_names()
    # return
    # 取主题-词矩阵中前面最高的n_words的单词
    n_words = 30
    temp = -n_words - 1
    # 保存前20个词的词-主题矩阵
    for topic_idx, topic in enumerate(lda.components_):
        print("Topic #%d:" % (topic_idx + 1))
        print(" ".join([tf_feature_names[i] for i in topic.argsort()[:temp:-1]]))
        topic_sum = np.sum(topic)
        topic_name.append([tf_feature_names[i] for i in topic.argsort()[:temp:-1]])
        print([round(topic[i]/topic_sum, 4) for i in topic.argsort()[:temp:-1]])
        topic_data.append([topic[i]/topic_sum for i in topic.argsort()[:temp:-1]])
    save_model(model=lda, filename=outfile[1])
    with open(outfile[-1], 'wb+') as fw:
        for i in range(n_topic):
            fw.write('Topic #{}:'.format(i+1).encode('utf-8') + '\n'.encode('utf-8'))
            fw.write(','.join(topic_name[i]).encode('utf-8') + '\n'.encode('utf-8'))
            fw.write(','.join([str(round(x, 4)) for x in topic_data[i]]).encode('utf-8') + '\n'.encode('utf-8'))

# 利用保存的LDA参数重现实验结果
def rerun():
    # lda = load_model()
    res_list = file_name('./data/NLP_test')
    stpwrdlst = stopwr()
    corpus, i = [], 0
    for res in res_list:
        i += 1
        exec("""with open(res, 'r+') as f3:
        \n  res{id} = f3.read()""".format(id=str(i)))
        exec("corpus.append(res{id})".format(id=str(i)))

    # 构建词汇统计向量并保存
    cntVector = CountVectorizer(stop_words=stpwrdlst)
    # 文档__词稀疏矩阵
    cntTf = cntVector.fit_transform(corpus)
    # docres = load_model('./setting/docres.pk')
    tf_feature_names = cntVector.get_feature_names()
    fw = open('tf_feature_names.csv', 'wb+')
    fw.write(','.join([str(i.encode('utf-8')).strip() for i in tf_feature_names]) + '\n')
    fw.close()

# 统计单个文件中的词频信息
def cipin(filename, dict_word):
    fr = open(filename, 'rb+')
    lines = fr.read().strip()
    words = lines.split()
    fr.close()
    for word in words:
        dict_word[word] = dict_word.get(word, 0) + 1
    return dict_word

# 统计文件夹中所有文件的词频信息
def ciping():
    lunwen_list = file_name('./data/NLP_test')
    dict_word = {}
    for lunwen in lunwen_list:
        dict_word = cipin(lunwen, dict_word)
    sorted_list_word = sorted(dict_word.iteritems(), key=lambda x: x[1], reverse=True)
    fw = open('./data/frequency.txt', 'w+')
    for word, num in sorted_list_word:
        if len(word.decode("utf-8")) > 1:
            fw.write("%s\t%d\n" % (word, num))
    fw.close()


start_time = time.time()
path = './Data/Setting'
if not os.path.exists(path):
    os.makedirs(path)
infile = './Data/zhihu_HotTopics_fenci'
prepath = path + '/zhihu_HotTopics_'
outfile = ['Docres.pk', 'Lda.pk', 'Doc_Topic.csv', 'Word_Topic.csv']
outfile = [prepath + i for i in outfile]
My_LDA(infile, outfile)
end_time = time.time()
print('The program is over and the cost is{}s'.format(end_time - start_time))