import requests
import json
import time
import os
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Cookie': 'q_c1=b9665a595464474d9d7caf485bb3fb98|1523961780000|1523961780000; _zap=bd7a9506-3fd2-45ad-850c-f9726a8ac283; l_cap_id="MTk5ZTAxMjk4NzVhNDkyZWFlMmIwMDNkODY2NThjOGI=|1523963322|d0bed2bf91026bec9a9d443b66f4a0b1aa633eeb"; r_cap_id="Mzk2MmFiOWNjZTJlNDExNGFmY2Q2NzM5YmY4YjU3Yzg=|1523963322|dbf05d362dbb3cd3db03ee85cf41b3199d2e3ea0"; cap_id="NmI1ODkwNGUwMzUyNDM2NGEyMjYyNjU4YjA1NDJhZDc=|1523963322|204a770c2ef734c41836525890b3a4be54b4a281"; aliyungf_tc=AQAAAOxX/RE1tQkAwZ8Gt7qUhpwUSVat; _xsrf=65b67084-806e-4e14-b209-46212a83402e; d_c0="AHBvL9TLfg2PTttJO0-Opj08xA9D0bPq8Os=|1524627448"; capsion_ticket="2|1:0|10:1524627513|14:capsion_ticket|44:NTFlZDIzZjcxODViNGI0ODhjMTdjYWM1MjAzYzYzMTE=|a5946b92b9606e35c11eb402c6ca2569423617ffa4440aeb609874581bcf5703"; z_c0="2|1:0|10:1524627528|4:z_c0|92:Mi4xRXNxWEFRQUFBQUFBY0c4djFNdC1EU1lBQUFCZ0FsVk5TRWJOV3dBLW5kVFd3QTFMckdpYl9DX2VfSTFtX2NjYllB|94a499e64d553afa6af4f2fd1337f8b5766a9f80b1b0e8b63dfa02e1208cfe67"; __utma=155987696.315884556.1524646701.1524646701.1524646701.1; __utmc=155987696; __utmz=155987696.1524646701.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
    }
session = requests.session()

def get_answer(url0, qid, headers):
    global  session
    contents = []
    for i in range(0, 1001, 10):
        url = url0.format(qid=qid, offset=i)
        response = session.get(url, headers=headers)
        request_content = json.loads(response.text)
        # 查看网页是否被正确访问
        # print(request_content)
        data0 = request_content['data']
        if data0 != []:
            for j in range(0, len(data0)):
                if 'content' not in data0[j].keys():
                    continue
                content = data0[j]['content']
                # 非贪婪跨行匹配所有<>结构
                pattern = re.compile(r'<.*?>', flags=re.DOTALL)
                content = re.sub(pattern, '', content)
                # 时间戳，自1970纪元年后经过的浮点秒数
                # created_time = data0[j]['created_time']
                contents.append(content)
            time.sleep(2)
        else:
            break
    return  contents

qids = []
topic_url = "https://www.zhihu.com/api/v4/topics/19608566/feeds/essence?limit=10&offset={offset}"
question_url = 'https://www.zhihu.com/api/v4/questions/{qid}/answers?limit=10&offset={offset}&include=data[*].is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp&data[*].author.follower_co'
# 访问"中山大学"topics
for i in range(0, 1001, 10):
    url = topic_url.format(offset=i)
    response = session.get(url, headers=headers)
    # 查看网页是否已被正确获取
    # print(response.text)
    request_content = json.loads(response.text)
    data0 = request_content['data']
    if data0 != []:
        data0 = request_content['data']
        for j in range(0, len(data0)):
            target = data0[j]['target']
            # print(target.keys())
            if 'question' not in target.keys():
                continue
            title = target['question']['title']
            # 匹配所有不是字母，数字，下划线，汉字的字符
            pattern = re.compile(r'\W')
            qid = target['question']['id']
            title = re.sub(pattern, '', title)
            print(title)
            if qid not in qids:
                # 访问这个问题的回答
                answer = get_answer(question_url, qid, headers)
                if answer == []:
                    print('This page is error', qid)
                # print('[EOS]\n' + title + '\n' + "\n".join(answer))
                fw = open('./Setting/zhihu_HotTopics/[{id}]{title}.txt'.format(id=qid, title=title), 'wb+')
                result = title + '\n' + "\n".join(answer)
                # print(result)
                fw.write(result.encode('utf-8', 'ignore'))
                fw.close()
                qids.append(qid)
    else: # 访问结束
        break