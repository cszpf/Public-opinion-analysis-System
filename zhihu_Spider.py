import requests
import json
import time
import os
import re
import numpy as np
FILE = './Setting1/zhihu_HotTopics'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Cookie': 'q_c1=b9665a595464474d9d7caf485bb3fb98|1523961780000|1523961780000; _zap=bd7a9506-3fd2-45ad-850c-f9726a8ac283; l_cap_id="MTk5ZTAxMjk4NzVhNDkyZWFlMmIwMDNkODY2NThjOGI=|1523963322|d0bed2bf91026bec9a9d443b66f4a0b1aa633eeb"; r_cap_id="Mzk2MmFiOWNjZTJlNDExNGFmY2Q2NzM5YmY4YjU3Yzg=|1523963322|dbf05d362dbb3cd3db03ee85cf41b3199d2e3ea0"; cap_id="NmI1ODkwNGUwMzUyNDM2NGEyMjYyNjU4YjA1NDJhZDc=|1523963322|204a770c2ef734c41836525890b3a4be54b4a281"; aliyungf_tc=AQAAAOxX/RE1tQkAwZ8Gt7qUhpwUSVat; _xsrf=65b67084-806e-4e14-b209-46212a83402e; d_c0="AHBvL9TLfg2PTttJO0-Opj08xA9D0bPq8Os=|1524627448"; capsion_ticket="2|1:0|10:1524627513|14:capsion_ticket|44:NTFlZDIzZjcxODViNGI0ODhjMTdjYWM1MjAzYzYzMTE=|a5946b92b9606e35c11eb402c6ca2569423617ffa4440aeb609874581bcf5703"; z_c0="2|1:0|10:1524627528|4:z_c0|92:Mi4xRXNxWEFRQUFBQUFBY0c4djFNdC1EU1lBQUFCZ0FsVk5TRWJOV3dBLW5kVFd3QTFMckdpYl9DX2VfSTFtX2NjYllB|94a499e64d553afa6af4f2fd1337f8b5766a9f80b1b0e8b63dfa02e1208cfe67"; __utma=155987696.315884556.1524646701.1524646701.1524646701.1; __utmc=155987696; __utmz=155987696.1524646701.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    }
topic_url = "https://www.zhihu.com/api/v4/topics/19608566/feeds/essence?limit=20&offset={offset}"
# topic_url = "https://www.zhihu.com/api/v4/topics/19608566/feeds/timeline_question?limit=20&offset={offset}"
question_url = 'https://www.zhihu.com/api/v4/questions/{qid}/answers?limit=20&offset={offset}&include=data[*].is_normal%2Ccomment_count%2Ccontent%2Cvoteup_count'
comment_url = "https://www.zhihu.com/api/v4/answers/{aid}/comments?include=data[*].author,content,limit=40&offset={offset}"
session = requests.session()

# 获取单个qid中的回答
def get_answer(qid, url0=question_url, headers=headers):
    # return:返回二维列表，第二维是每一个回答以及与此回答相应的评论
    global  session
    contents, nums = [], 0
    for i in range(0, 1001, 20):
        url = url0.format(qid=qid, offset=i)
        response = session.get(url, headers=headers)
        request_content = json.loads(response.text)
        nums = request_content['paging']['totals']
        data0 = request_content['data']
        if data0 != []:
            for j in range(0, len(data0)):
                if 'content' not in data0[j].keys():
                    continue
                vote_count = data0[j]["voteup_count"]
                comment_count = data0[j]["comment_count"]
                content = data0[j]['content']
                aid = data0[j]['id']
                # 非贪婪跨行匹配所有<>结构
                pattern = re.compile(r'<.*?>', flags=re.DOTALL)
                content = re.sub(pattern, '', content)
                content1 = [str(vote_count), str(comment_count), content]
                # comment_list = get_comments(aid, comment_url, headers)
                # content1.extend(comment_list)

                contents.append(content1)
            time.sleep(1)
        else:
            break
    return  nums, contents

# 获取单个aid中的所有评论
def get_comments(aid, url0=comment_url, headers=headers):
    # return:返回一个一维数组
    global session
    comments = []
    for i in range(0, 1001, 40):
        url = url0.format(aid=aid, offset=i)
        response = session.get(url, headers=headers)
        request_contents = json.loads(response.text)
        # 查看网页是否被正确访问
        # print(request_content)
        # 查看评论总数
        # nums = request_contents['common_counts']
        data0 = request_contents['data']
        if data0 != []:
            for j in range(len(data0)):
                if 'content' not in data0[j].keys():
                    continue
                # vote_count = data0[j]['vote_count']
                content = data0[j]['content']
                # uid = data0[j]['author']['member']['id']
                # uname = data0[j]['author']['member']['name']
                # comments.extend([uid+uname, str(vote_count), str(content)])
                # return comments
                comments.append(content)
            time.sleep(2)
        else:
            break
    return comments

# 将答案写入文件中
def write_tofile(answers, filename, pathname=FILE):
    if not os.path.exists(pathname):
        os.makedirs(pathname)
    fw = open(os.path.join(pathname, filename), 'wb+')
    # if len(np.shape(answers)) == 1:
    #     result = '\n'.join(answers)
    # else:
    result1 = [','.join(i[:2]) for i in answers]
    result2 = [i[2] for i in answers]
    result3 = [','.join(i[3:]) for i in answers]
    result = ['\n'.join(i) for i in zip(result1, result2, result3)]
    result = '\n'.join(result)
    fw.write(result.encode('utf-8', 'ignore'))
    fw.close()

# 获取qids列表下的所有回答
def get_questions(qid_ls=[], url0=question_url, headers=headers, pathname=FILE):
    flag, qids = True, []
    if qid_ls == []:
        flag == False
    # 访问"中山大学"topics
    for i in range(0, 200001, 20):
        url = topic_url.format(offset=i)
        response = session.get(url, headers=headers)
        request_content = json.loads(response.text)
        data0 = request_content['data']
        if data0 != []:
            data0 = request_content['data']
            for j in range(0, len(data0)):
                target = data0[j]['target']
                if 'question' not in target.keys():
                    continue
                target = target['question']
                qid = str(target['id'])
                if flag is True and qid not in qid_ls:
                    continue
                if qid not in qids:
                    time_stamp = list(time.localtime(int(target['created'])))[0]
                    if time_stamp < 2015:
                        continue
                    title = target['title']
                    # 匹配所有不是字母，数字，下划线，汉字的字符
                    pattern = re.compile(r'\W')
                    title = re.sub(pattern, '', title)
                    title = "[{}][{}]{}".format(time_stamp, qid, title)
                    print(title)
                    # 访问这个问题的回答
                    answer = get_answer(qid)
                    if answer == []:
                        print('This page is error', qid)
                        continue
                    write_tofile(answer[1], '[%s]'%(answer[0])+title+'.txt', pathname)
                    qids.append(qid)
        else: # 访问结束
            break

# 生成qids的列表
def generate_qids(file):
    qids, results = [], []
    pattern = r'\[(.*?)\]'
    with open(file, 'rb+') as fr:
        data = fr.read()
        for i in data.decode('utf-8').split('\n'):
            if i.strip() == '':
                if results == []:
                    continue
                else:
                    qids.append(results)
                    results = []
                    continue
            result = re.findall(pattern, i.strip())
            if len(result) == 1:
                # print(result[0])
                results.extend(result)
    # print(qids)
    return qids

qids = generate_qids('./Data/zhihu.txt')
for i in range(len(qids)):
    get_questions(qids[i], pathname=os.path.join(FILE, str(i)))