import os

DICT_URL = './dict/hownet_sentiment_dict.txt'
positive_list = list()
negtive_list = list()


def fill_sentiment_set():
    with open(DICT_URL, 'r', encoding='utf-8') as dict_file:
        for line in dict_file.readlines():
            if line[-2] == '1':
                positive_list.append(line[:-3])
            else:
                negtive_list.append(line[:-3])


def get_cnt(word_bag):
    pos_cnt = 0
    neg_cnt = 0
    for word in word_bag:
        # print(word)
        if word in positive_list:
            pos_cnt += 1
        elif word in negtive_list:
            neg_cnt += 1

    return pos_cnt, neg_cnt


def question_sentiment():
    # 以问题为主体进行情感分析
    files_dir_url = '../Setting1/zhihu_HotTopics_fenci/'
    topic_cnt = 7
    out_file_url = './question_sa.txt'
    with open(out_file_url, 'w', encoding='utf-8') as out_file:
        for i in range(topic_cnt):
            dir_url = files_dir_url + str(i) + '/'
            files = os.listdir(dir_url)
            for filename in files:
                file_url = os.path.join(dir_url, filename)
                with open(file_url, 'r', encoding='utf-8') as file:
                    print(i, get_cnt(file.read().split()), filename, file=out_file)


def answer_sentiment():
    # 以每个答案为主体进行情感分析
    files_dir_url = '../Setting1/zhihu_HotTopics_fenci/'
    for i in range(7):
        os.makedirs(str(i), exist_ok=True)
        dir_url = files_dir_url + str(i) + '/'
        files = os.listdir(dir_url)
        for filename in files:
            file_url = os.path.join(dir_url, filename)
            with open(file_url, 'r', encoding='utf-8') as file:
                sent_out_url = './' + str(i) + '/' + filename + '.sent.txt'
                with open(sent_out_url, 'w', encoding='utf-8') as out_file:
                    print(filename + '\n', file=out_file)
                    lines = file.readlines()
                    for line in lines:
                        print(get_cnt(line.split()), file=out_file)
                    out_file.write('\n\n')


def main():
    fill_sentiment_set()
    print(len(positive_list), len(negtive_list))
    # question_sentiment()
    answer_sentiment()


if __name__ == '__main__':
    main()
