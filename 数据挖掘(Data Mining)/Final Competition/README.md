## 南京大学 NJU 计算机系 CS 数据挖掘2019春季课程 大作业 代码 报告



任务: 短文本多分类, 为短文本推荐合适的`Emoji` :feet: Top `10%`

没有Transformer, 就是简单的`word2vec` + `LSTM`, 此外`tf-idf` + 机器学习的方法似乎效果更不好.

每年大作业题目可能有**差别**.

---

:sob:半年后再回首, 当时还是太青涩了, 如果您需要更进一步, 可以看看Non-BERT-based的SOTA模型, 某些神奇又具有可解释性的网络结构可以让embedding之后的特征获取得非常好, 或者极妙的特征提取方法(比如[Super Characters](https://arxiv.org/abs/1810.07653)). 可以使用`PyTorch`等框架, 直接写`.py`文件吧不需要`jupyter notebook`. 记得炼丹.

:night_with_stars: