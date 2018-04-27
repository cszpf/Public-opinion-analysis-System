# import fenci

orig_file_url = './Data/question_titles.txt'
sept_sept_url = './Data/separated_titles.txt'

# fenci.fenci_file(orig_file_url, sept_sept_url)

term_count = dict()
with open(sept_sept_url, 'r', encoding='utf-8') as titles_file:
    line = titles_file.read()
    words = line.split()
    for word in words:
        if word not in term_count:
            term_count[word] = 1
        else:
            term_count[word] += 1

term_count = sorted(term_count.items(), key=lambda x: x[1], reverse=True)
with open('./Data/trem_count.txt', 'w', encoding='utf-8') as tc_file:
    for pair in term_count:
        tc_file.write(pair[0] + ': ' + str(pair[1]) + '\n')

print(term_count[:10])
