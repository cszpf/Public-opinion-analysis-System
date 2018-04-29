"""
将Data/zhihu_HotTopics目录下的每一篇文章分词，并分别存放到Data/zhihu_HotTopics_fenci目录下
"""
import os
import jieba
import platform

sys_info = platform.system()  # 操作系统信息
root_dir = os.getcwd()
data_dir = os.path.join(root_dir, "./Data")

# dict_file = os.path.join(data_dir, "user_dict.txt")
# jieba.load_userdict(dict_file)

# 判断字符串是否由数字.%以及英文字母组成
def isNumeric(s):
    """return True if string s is numeric"""
    return all([c in "0123456789.%ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                for c in s])


# 返回停用词列表
def get_stopwords():
    stopwords = []
    stop_file = os.path.join(data_dir, "stopwords.txt")
    with open(stop_file, 'rb+') as fin:
        for line in fin:
            if line.strip():
                stopwords.append(line.strip().decode('utf-8'))
    # print(stopwords)
    return stopwords


# 单个文件分词
# inFile, outFile为完整路径(unicode)
def fenci_file(inFile, outFile):
    stopwords = get_stopwords()
    all_words = []

    with open(inFile, 'rb+') as fin:
        for line in fin:
            if line.strip():
                line = line.strip().decode("utf-8")
                words = list(jieba.cut(line, cut_all=False))
                words = [word for word in words if len(word) > 1]
                words = [word for word in words if not isNumeric(word) and word not in stopwords]
                if words:
                    all_words.append(words)

    with open(outFile, "wb+") as fout:
        for word in all_words:
            fout.write(" ".join(word).encode('utf-8', 'ignore'))
            fout.write('\n'.encode('utf-8', 'ignore'))


# inDir目录下每个文件分词, 存到outDir目录下
def fenci_dir(inDir, outDir, pre_path=data_dir):
    inDir = os.path.join(pre_path, inDir)
    outDir = os.path.join(pre_path, outDir)
    # 创建outDir目录
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    for fn in os.listdir(inDir):
        print(fn)
        if fn.find('.txt') < 0:
            fenci_dir(os.path.join(inDir, fn), os.path.join(outDir, fn))
            continue
        inFile = os.path.join(inDir, fn)
        outFile = os.path.join(outDir, fn)
        fenci_file(inFile, outFile)

fenci_dir(inDir="All_Topics", outDir="All_Topics_fenci")
