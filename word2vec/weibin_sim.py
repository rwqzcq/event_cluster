from config import get_config
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import json


class WeiBinSim:
    '''
    谓语宾语分别聚类
    '''

    def __init__(self):
        self.model = Word2Vec.load(get_config()['WORD_2_VEC_PATH'] + '/word2vec_baike')
        # self.model = Word2Vec.load(get_config()['WX_PATH_MODEL'])

    def sim(self, word_1, word_2):
        '''
        比较两个词之间的相似性
        '''
        return self.model.wv.similarity(word_1, word_2)


def weiyu_cluster():
    path = 'I:\\代码\\事理图谱\\event_cluster\\datatset\\全部谓语宾语_不聚类.json'


class DealWord2vec:
    """将词语转化为向量并存入到JSON文件中去
    """
    
    model = None # 模型
    words = [] # 词语
    vector_path = '' # 向量文件保存位置
    vectors = {} # 所有词向量
    not_have_vector_words = [] # 没有向量化的词语
    not_have_vector_path ='' # 没有向量化的词语的存储位置  

    def load_model_from_txt(self, model_path):
        """从词向量中加载文件
        
        Arguments:
            path {[type]} -- [description]
        """
        self.model = KeyedVectors.load_word2vec_format(model_path)
        return self
    
    def load_model_from_model(self, path):
        """从模型文件中载入模型
        
        Arguments:
            path {[type]} -- [description]
        """
        self.model = Word2Vec.load(path)
        return self
    
    def load_data(self, data):
        """加载数据
        
        Arguments:
            data {list} -- word_list
        """
        # print(data)
        self.words = data
        return self
    
    def set_paths(self, paths):
        """设置文件路径
        
        Arguments:
            paths {list} -- {'vector_path' : 1, 'not_have_vector_path' : 2}
        """
        self.vector_path = paths['vector_path']
        self.not_have_vector_path = paths['not_have_vector_path']
        return self
    
    def get_vectors(self):
        """词语转向量
        """
        for word in self.words:
            try:
                # print(word)
                vector = self.model.wv[word].tolist() # ! TypeError: Object of type 'ndarray' is not JSON serializable
                self.vectors[word] = vector
            except Exception as e:
                self.not_have_vector_words.append(word)
                continue
    
    def save_data(self):
        """保存所有的数据，需要在get_vectors的时候调用
        """

        with open(self.vector_path, 'w', encoding='utf-8') as f: # * 向量文件
            json.dump(self.vectors, f, ensure_ascii=False)

        with open(self.not_have_vector_path, 'w', encoding='utf-8') as f: # * 没有向量的词语的保存位置
            json.dump(self.not_have_vector_words, f, ensure_ascii=False)


def deal_binyu():
    """处理所有的宾语
    """
    word_type = "宾语"

    # ! 宾语转向量
    path = 'I:\\代码\\事理图谱\\event_cluster\\dataset\\全部谓语宾语_不聚类.json'

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # data = {
    #     "收复": [
    #     "收复台湾",
    #     "收复功绩",
    #     "收复腾冲"
    #     ],
    #     "攻占": [
    #         "攻占城",
    #         "攻占山头",
    #         "攻占天京",
    #         "攻占扬州"
    #     ],
    #     "定都": [
    #         "定都洛阳",
    #         "定都南京"
    #     ]
    # }
    binyus = []
    for weiyu, weibins in data.items(): # * 去除所有的谓语
        for weibin in weibins:
            binyu = weibin.replace(weiyu, '')
            binyus.append(binyu)
    binyus = list(set(binyus)) # * 去重

    # ! 类处理
    dealer = DealWord2vec()
    model_path = 'I:\\代码\\事理图谱\\训练好的词向量\\\腾讯AI精简版\\1000000-small.txt'
    vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量\\' + word_type + '.json'
    hav_vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量所对应的词语\\' + word_type + '.json'
    not_have_vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\没有向量化的' + word_type + '.json'
    dealer.load_model_from_txt(model_path).load_data(binyus).get_vectors()
    dealer.set_paths({'vector_path' : vector_path, 'not_have_vector_path' : not_have_vector_path}).save_data()


if __name__ == '__main__':
    deal_binyu()

    # path = 'I:\\代码\\事理图谱\\event_cluster\\dataset\\全部谓语宾语_不聚类.json'

    # with open(path, 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    
    # words = list(data.keys())

    # words_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\原始文本\\谓语.json'

    # with open(words_path, 'w', encoding='utf-8') as f:
    #     json.dump(words, f, ensure_ascii=False)

    # # * 找到所有谓语的向量并存入到文件中 宾语需要去重
    # word_type = '谓语'
    # model_path = 'I:\\代码\\事理图谱\\训练好的词向量\\\腾讯AI精简版\\1000000-small.txt'
    # model = KeyedVectors.load_word2vec_format(model_path)

    # vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量\\' + word_type + '.json'
    # hav_vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量所对应的词语\\' + word_type + '.json'
    # not_have_vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\没有向量化的' + word_type + '.json'
    # vectors = {}
    # not_have_vectors = []
    # remain_words = []

    # for word in words:
    #     try:
    #         vector = model.wv[word].tolist() # ! TypeError: Object of type 'ndarray' is not JSON serializable
    #         # vectors.append(vector) # * ndarray添加元素
    #         vectors[word] = vector
    #         remain_words.append(word)
    #     except Exception as e:
    #         not_have_vectors.append(word)
    
    # with open(vector_path, 'w', encoding='utf-8') as f:
    #     json.dump(vectors, f, ensure_ascii=False)

    # with open(not_have_vector_path, 'w', encoding='utf-8') as f:
    #     json.dump(not_have_vectors, f, ensure_ascii=False)

    # with open(hav_vector_path, 'w', encoding='utf-8') as f:
    #     json.dump(remain_words, f, ensure_ascii=False)



    # 
    # path = '''I:\代码\事理图谱\训练好的词向量\维基中文词向量\hanlp-wiki-vec-zh\hanlp-wiki-vec-zh.txt'''
    # # path = '''I:\代码\事理图谱\训练好的词向量\Tencent_AILab_ChineseEmbedding\Tencent_AILab_ChineseEmbedding.txt'''
    # path = '''I:\代码\事理图谱\训练好的词向量\FastText\wiki.zh.vec'''
    # model = KeyedVectors.load_word2vec_format(path)
    
    # word_1 = '交通'
    # word_2 = '汽车'
    # print(type(model.wv[word_1]))
    # try:
    #     s = model.wv.similarity(word_1, word_2)
    #     print(s)
    # except Exception as e:
    #     l = str(e)
    #     begin=l.find("'")

    #     end=l.rfind("'")

    #     ss=l[begin+1:end]
    #     print(ss)
    

    
    