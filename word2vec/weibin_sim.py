from config import get_config
from gensim.models import Word2Vec


class WeiBinSim:
    '''
    谓语宾语聚类
    '''

    def __init__(self):
        self.model = Word2Vec.load(get_config()['WORD_2_VEC_PATH'] + '/word2vec_baike')
        self.model = Word2Vec.load(get_config()['WX_PATH_MODEL'])

    def sim(self, word_1, word_2):
        '''
        比较两个词之间的相似性
        '''
        return self.model.wv.similarity(word_1, word_2)





if __name__ == '__main__':
    # wb_sim = WeiBinSim()
    # word_1 = '火车票'
    # word_2 = '汽车票'
    # try:
    #     s = wb_sim.sim(word_1, word_2)
    #     print(s)
    # except Exception as e:
    #     l = str(e)
    #     begin=l.find("'")

    #     end=l.rfind("'")

    #     ss=l[begin+1:end]
    #     print(ss)
    from gensim.models import KeyedVectors
    path = '''I:\代码\事理图谱\训练好的词向量\维基中文词向量\hanlp-wiki-vec-zh\hanlp-wiki-vec-zh.txt'''
    # path = '''I:\代码\事理图谱\训练好的词向量\Tencent_AILab_ChineseEmbedding\Tencent_AILab_ChineseEmbedding.txt'''
    path = '''I:\代码\事理图谱\训练好的词向量\FastText\wiki.zh.vec'''
    model = KeyedVectors.load_word2vec_format(path)
    
    word_1 = '交通'
    word_2 = '汽车'
    print(type(model.wv[word_1]))
    # try:
    #     s = model.wv.similarity(word_1, word_2)
    #     print(s)
    # except Exception as e:
    #     l = str(e)
    #     begin=l.find("'")

    #     end=l.rfind("'")

    #     ss=l[begin+1:end]
    #     print(ss)
    

    
    