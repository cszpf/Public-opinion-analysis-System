import os
import re
pattern = re.compile(r'\[(.*?)\]')
def list_dir(dir):
	result=[]
	for fn in os.listdir(dir):
		result.append(fn)
	return result
def fun(filename):
	results = []
	for i in range(7):
		result = list_dir(os.path.join(filename, str(i)))
		counter=0
		for j in result:
			temp = re.findall(pattern, j)
			counter += int(temp[0])
		results.append(counter)		

	return results

def write2file(filename, results):
	with open(filename, 'wb+') as fw:
		for i in results:
			fw.write('\n\n'.encode('utf-8', 'ignore'))
			fw.write('\n'.join(i).encode('utf-8', 'ignore'))
results = fun('./')
print(results)
# write2file('./zhihu_topics.txt', results)