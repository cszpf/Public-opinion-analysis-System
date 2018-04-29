# Data文件夹下的文件简介

1.stop_word.txt/stopwords.txt：停用词文档(具有伸缩性，可以根据分次任务进行改变)

2.zhihu_HotTopics：知乎中中山大学话题中的精品问题，其文件夹下面的单个文件的文件名为使用gbk编码格式存储，而其内容为使用utf-8编码格式存储

3.zhihu_HotTopics_fenci:分词之后的中山大学话题中的精品问题

4.Setting文件夹：

​	[1].topic_title.txt:文档主题分布事件表(选择分布频率最高的主题)

​	[2].zhihu_HotTopics_Doc_Topic.csv:文档主题分布分布图

​	[3].zhihu_HotTopics_Word_Topic.csv:词主题分布分布图



#Setting1文件夹下的文件简介

1.zhihu_HotTopics:按照给定的主题，挑选出的文档

2.zhihu_HotTopics_fenci:对zhihu_HotTopics文件夹分词之后的结果

3.stopwords.txt:停用词表



# 源程序文件简介

zhihu_Spider.py：知乎_爬虫程序

/zh_scrapy：使用scrapy的知乎爬虫代码

Lda.py: LDA程序

fenci.py：分词的程序
