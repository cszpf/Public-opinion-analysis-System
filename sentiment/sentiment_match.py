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


def main():
    fill_sentiment_set()
    print(len(positive_list), len(negtive_list))

    files_dir_url = '../Data/zhihu_HotTopics_fenci/'
    files = os.listdir(files_dir_url)
    for filename in files:
        file_url = os.path.join(files_dir_url, filename)
        with open(file_url, 'r', encoding='utf-8') as file:
            print(get_cnt(file.read().split()), filename)


if __name__ == '__main__':
    main()
