# 面向黑客论坛的新词发现
呈现方式：论文+小的在线系统(论文不公开)
## 数据集
爬取的七个黑客论坛的数据，时间跨度从2013年到2019年2月，因为个人原因，数据不作公开
## 数据处理方式
根据词的特征，从四个方面去处理，包括词嵌入、字符嵌入(利用CNN提取字符特征)、特征嵌入、词性嵌入之后进行拼接，再利用双向LSTM去发现
## 结果
精确率：92.86%
召回率：86.43%
F1分数：89.53%

目前只是用论坛中18年以后的数据预测，但是效果表示的是可以发现但是发现的并不是非常的能体现这种有效性，所以我们接下来将爬取twitter的相关话题下的数据进行预测，从而验证我们的模型的性能


