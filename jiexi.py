import re
import chardet
import os
import time

# 判断字符串是否是由数字.%以及英文字母组成
def isNumeric(s):
    """return True if string s is numeric"""
    return all([c in "0123456789.%ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" for c in s])

# 获取一个目录下的所有非目录文件
def file_name(file_dir):
    dir_list, file_list = [], []
    d_num, f_num = 0, 0
    for root, dirs, files in os.walk(file_dir):
        #print(root)
        for subdir in dirs:
            d_num += 1
            #print os.path.join(root,subdir)
            dir_list.append(os.path.join(root, subdir))
        for subfile in files:
            if subfile != '统计.txt':
                #print os.path.join(root,subfile)
                f_num += 1
                file_list.append(os.path.join(root, subfile))
    print(d_num, f_num)
    return file_list

# 对网页结构进行解析
def jiexi(filename, idx):
    def qukong(x):
        if(len(x) > 0):
            lunwen = re.sub(r'&nbsp;', '', x[-1])
            lunwen = re.sub(tag_pattern, '', lunwen)
            lunwen = lunwen.strip()
        else:
            lunwen = ''
        return lunwen
    def zhaiyao(x):
        zhaiyao = ''.join(x.split('\n'))
        if(len(zhaiyao.split(';')) > 0):
            return ' '.join(zhaiyao.split(';')).strip()
        elif((len(zhaiyao.split('；')) > 0)):
            return ' '.join(zhaiyao.split('；')).strip()
    fr = open(filename, 'r+')
    wangye = fr.read()
    fr.close()
    wangye_encode = chardet.detect(wangye)['encoding']
    topic_pattern = re.compile(r'<div class="top-title">.*?<h1>(.*?)</h1>.*?</div>', re.S)
    abstract_pattern = re.compile(r'<div class="data" id="a_abstract">.*?<p>(.*?)</p>.*?</div>', re.S)
    keyword_pattern = re.compile(r'<div class="data" id="a_keywords">.*?<p>(.*?)</p>.*?</div>', re.S)
    content_pattern = re.compile(r'<!--brief end-->(.*?)<!--conten left  end-->', re.S)
    a_pattern = re.compile(r'<a.*?</a>', re.S)
    tag_pattern = re.compile(r'<.*?>', re.S)
    topic = re.findall(topic_pattern, wangye.decode(wangye_encode))
    abstract = re.findall(abstract_pattern, wangye.decode(wangye_encode))
    keyword = re.findall(keyword_pattern, wangye.decode(wangye_encode))
    content = re.findall(content_pattern, wangye.decode(wangye_encode))
    tuple_content = [topic, abstract, keyword, content]
    for i in range(len(tuple_content)):
        temp_content = qukong(tuple_content[i])
        string = ''''''
        for j in temp_content.split('\n'):
            if j.strip() != '':
                string += j.strip()+'\n'
        tuple_content[i] = string
    
    tuple_content[-2] = zhaiyao(tuple_content[-2])
    Content = tuple_content[-1]
    Keyword = tuple_content[-2]
    Summary = '\n'.join([tuple_content[i] for i in range(3)]).strip()
    Paper = '\n'.join(tuple_content).strip()
    
    tuple_path = [Content, Keyword, Summary, Paper]
    tuple_path1 = ['Content', 'Keyword', 'Summary', 'Paper']
    prepath = './data/'
    tuple_path1 = [(prepath+i) for i in tuple_path1]
    for i in range(0,4):
        fw = open(tuple_path1[i]+'/'+filename.split('/')[-1], 'wb+')
        fw.write(tuple_path[i].encode('utf-8'))
        fw.close()

        

def mycopy(filename, path, idx):
    fr = open(filename, 'r+')
    content = fr.read()
    fr.close()
    file = path + '/'+ filename.split('/')[-1]
    fw = open(file, 'w+')
    fw.write(content)
    fw.close()


starttime = time.time()
#解析网页
#创建一遍文件夹
idx = 0
fw = open('./keywords.txt', 'w+')
words = []
file_list = file_name('./data/Keyword')
for file in file_list:
    idx += 1
    fr = open(file, 'r+')
    content = fr.read()
    fr.close()
    words.extend(content.strip().split())
words = list(set(words))
fw.write('\n'.join(words).strip())
fw.close()
endtime = time.time()
print('The program is over and the cost is', endtime - starttime)