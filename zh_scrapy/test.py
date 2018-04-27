def main():
    urls = list()
    with open('./zh_spider/data/question_urls.txt', 'r') as qa_files:
        urls = qa_files.readlines()
    print(urls[:10])


if __name__ == '__main__':
    main()
