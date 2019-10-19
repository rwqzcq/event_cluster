from pyhanlp import *
from jpype import JClass
import abc
from gensim.models import Doc2Vec, Word2Vec
from gensim.models import KeyedVectors
import numpy as np

class Phrase2Vec(metaclass=abc.ABCMeta):
    """短语向量化的抽象类
    """

    docVectorModel = None
    documents = None

    
    def load_model(self, model_file):
        """加载模型文件
        
        Arguments:
            model_file {[type]} -- [description]
        """
    
    def load_vector(self, vector_path):
        """初始化向量文件
        
        Arguments:
            vector_path {[type]} -- [description]
        """
        
    @abc.abstractmethod
    def load_data(self, documents):
        """加载数据
            
            Arguments:
                data {List} -- 分词好的文档列表 ["word1 word2", "word3 word4"]
        """

    @abc.abstractmethod
    def filter_data(self):
        """数据过滤
        """

class Phrase2vecUseHanlp(Phrase2Vec):
    """
    利用Hanlp的Word2vec来得到短语向量\n
    先是进行数据的过滤，把不能用词向量表示的短语去除
    """

    def __init__(self, vector_path):
        """初始化向量文件
        
        Arguments:
            vector_path {str} -- 向量文件的位置
        """
        WordVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')
        DocVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
        self.docVectorModel = DocVectorModel(WordVectorModel(vector_path))
    
    def load_data(self, documents):
        """加载数据
        
        Arguments:
            data {List} -- 分词好的文档列表
        """
        self.documents = documents
        return self
    
    def filter_data(self):
        """数据过滤
        """
        filter_documents = []
        filter_vectors = []
        no_documents = []
        for document in self.documents:
            vector = self.docVectorModel.query(document)
            if vector == None:
                no_documents.append(document)
                continue
            vector = vector.getElementArray()
            vector = list(vector)
            filter_documents.append(document)
            filter_vectors.append(vector)
        return {
            'filter_documents' : filter_documents,
            'filter_vectors' : filter_vectors,
            'no_documents' : no_documents 
        }
    

class Phrase2VecUseGensim(Phrase2Vec):
    '''
    根据已有的词向量文件使用Gensim进行一次过滤\n
    参考链接: 
        1. https://blog.csdn.net/flyfrommath/article/details/79643233
        2. https://www.zhihu.com/question/29978268?sort=created
    '''

    # def __init__(self, vector_path):
    #     """初始化的时候默认从词向量文件中加载模型
        
    #     Arguments:
    #         vector_path {[type]} -- [description]
    #     """
    #     self.docVectorModel = KeyedVectors.load_word2vec_format(vector_path) # * 从词向量文件中加载模型

    def load_vector(self, vector_path):
        """从词向量文件中加载模型
        
        Arguments:
            vector_path {[type]} -- [description]
        """
        self.docVectorModel = KeyedVectors.load_word2vec_format(vector_path) # * 从词向量文件中加载模型
        return self        

    def load_model(self, model_path):
        """直接加载模型文件
        
        Arguments:
            model_path {str} -- 模型文件位置
        """
        # ! 直接加载模型文件
        self.docVectorModel = Word2Vec.load(model_path)
        return self

    def load_data(self, documents):
        """加载数据
    
        Arguments:
            data {List} -- 分词好的文档列表
        """
        self.documents = documents
        return self

    def filter_data(self):
        """数据过滤
        句子中所有词的word vector求平均，获得sentence embedding\n
        参考链接: https://www.zhihu.com/question/29978268?sort=created
        """
        filter_documents = []
        filter_vectors = []
        no_documents = []
        for document in self.documents:
            # ! 分词
            words = document.split(' ')
            vectors = []
            if_exist = True
            for word in words:
                try:
                    vector = self.docVectorModel.wv[word]
                    vectors.append(vector) # * ndarray添加元素
                except Exception as e:
                    no_documents.append(document)
                    if_exist = False
                    break
            if if_exist == False:
                continue
            # ! 计算Vectors中每一列的平均值
            vectors = np.array(vectors)
            vector = vectors.mean(axis = 0).tolist()

            filter_documents.append(document)
            filter_vectors.append(vector)
        print(len(filter_vectors))
        return {
            'filter_documents' : filter_documents,
            'filter_vectors' : filter_vectors,
            'no_documents' : no_documents 
        }



class PhraseClusterHanlp:
    """
    谓宾聚类
    使用Hanlp自带的方法
    https://github.com/hankcs/HanLP/wiki/%E6%96%87%E6%9C%AC%E8%81%9A%E7%B1%BB
    核心为词袋向量
    """

    def __init__(self):
        ClusterAnalyzer = JClass('com.hankcs.hanlp.mining.cluster.ClusterAnalyzer')
        self.clusterAnalyzer = ClusterAnalyzer()
    
    def load_data(self, data):
        """加载数据
        
        Arguments:
            data {list} -- ['phrase1', 'phrase2']
        """
        self.data = data
    
    def add_data(self):
        """
        往clusterAnalyzer里面装填数据
        """
        for index, words in enumerate(self.data):
            self.clusterAnalyzer.addDocument(index, words)

    def cluster(self):
        """
        开始聚类
        """
        self.add_data()
        cluster = self.clusterAnalyzer.repeatedBisection(1.0) # 自动判断聚类数量k
        return cluster







if __name__ == '__main__':
    # WordVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.WordVectorModel')
    # DocVectorModel = JClass('com.hankcs.hanlp.mining.word2vec.DocVectorModel')
    path = '''I:\代码\事理图谱\训练好的词向量\维基中文词向量\hanlp-wiki-vec-zh\hanlp-wiki-vec-zh.txt''' # 0.46
    path = '''I:\代码\事理图谱\训练好的词向量\word2vec_c_from_weixin\word2vec_c''' # 0.72
    path = '''I:\代码\事理图谱\训练好的词向量\腾讯AI精简版\\500000-small.txt''' # 0.799
    path = '''I:\代码\事理图谱\训练好的词向量\FastText\wiki.zh.vec''' # !0.95 效果最好
    # docVectorModel = DocVectorModel(WordVectorModel(path))
    # # ! 查询某一文档转化为向量 有的话就返回一个com.hankcs.hanlp.mining.word2vec.Vector@759ebb3d 没有就返回None 成功的话就需要调用getElementArray()返回一个tuble 然后转化成List就可以运用
    # document = '订 机票' # ! 需要分词
    # # document = ''
    # # vector = docVectorModel.query(document)
    # vector = docVectorModel.query(document).getElementArray()
    # print(vector)
    # s = docVectorModel.similarity("山西副省长贪污腐败开庭", "陕西村干部受贿违纪") #
    # s = docVectorModel.similarity("订机票", "订火车票") #
    # print(s)
    # documents = [
    #     "治疗痛",
    #     "治疗支气管炎",
    #     "治疗哲学",
    #     "治疗炎症",
    #     "治疗疾病",
    #     "治疗心得"
    # ]
    # for index, document in enumerate(documents):
    #     docVectorModel.addDocument(index, document)
    # entryList = docVectorModel.nearest("疾病") # 农业类
    # for entry in entryList:
    #     print(entry.getKey(), documents[entry.getKey()], entry.getValue())
    # TODO 获取句子向量
    import json


    # path = '''I:\代码\事理图谱\训练好的词向量\FastText\wiki.zh.vec'''
    # path = 'I:\\代码\\事理图谱\\训练好的词向量\\Tencent_AILab_ChineseEmbedding\\Tencent_AILab_ChineseEmbedding.txt' # ! 太大了，加载不了 jpype._jclass.OutOfMemoryError: GC overhead limit exceeded
    # path = 'I:\\代码\\事理图谱\\训练好的词向量\\\腾讯AI精简版\\1000000-small.txt'
    # cluster = Phrase2vecUseHanlp(path)
    path = 'I:\\代码\\事理图谱\\训练好的词向量\\\腾讯AI精简版\\1000000-small.txt' # ! gensim使用百度百科
    path = 'I:\\代码\\事理图谱\\event_cluster\\word2vec\\word2vec_baike'
    path = '''I:\代码\事理图谱\训练好的词向量\FastText\wiki.zh.vec''' # ! gensim直接使用文件
    path = 'I:\\代码\\事理图谱\\训练好的词向量\\\腾讯AI精简版\\1000000-small.txt'
    bao_name = '_gensim'
    houzhui = '_tencent_ai_small_1000000'

    model_path = 'I:\\代码\\事理图谱\\event_cluster\\word2vec\\word2vec_baike\\word2vec_baike'
    houzhui = '_word2vec_baike'
    cluster = Phrase2VecUseGensim()
    vector_path = 'I:\\代码\\事理图谱\\event_cluster\\dataset\\原始谓宾.json'
    with open(vector_path, 'r', encoding='UTF-8') as f:
        documents = json.load(f)
    final_dict = cluster.load_model(model_path).load_data(documents).filter_data()
    # filter_documents = final_dict['filter_documents']
    # filter_vectors = final_dict['filter_vectors']
    # no_documents =   final_dict['no_documents']
    file_map = {
        'filter_documents' : '过滤后的谓宾' + bao_name + houzhui,
        'filter_vectors' : '过滤后的向量' + bao_name + houzhui,
        'no_documents' : '没有向量的谓宾' + bao_name + houzhui
    }
    base_path = 'I:\\代码\\事理图谱\\event_cluster\\results\\'
    for filename, data in final_dict.items():
        file_path = base_path + file_map[filename] + '.json'
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False) 

    