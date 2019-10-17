from OpenHowNet.HowNet import Standards
import numpy as np
import json


class HowNetSim:
    '''
    Hownet调用对象
    '''
    
    def __init__(self):
        self.hn = Standards.HowNetDict()
    
    def get_one_word_yiyuan(self, word):
        '''
        获取一个词语的义原
        '''
        sememes = self.hn.get_sememes_by_word(word)
        if len(sememes) == 0:
            # print(word + "在Hownet中不存在义原描述")
            return False
        
        r = []

        for sememe in sememes:
            r = r + list(sememe['sememes'])
        return list(set(r))
    
    def word_sim_v_dx(self, word1, word2):
        '''
        动词的比较

        也可以用来比较动词加宾语

        计算公式为 2 * 公共部分 / (word1 + word2)

        openHownet自带的方法比这个要好

        比如亏损和破产 这个方法的相似度为0.6 而自带的方法为0.73

        如果HowNet里面没有就直接返回一个Tuble，第一个参数为false，第二个参数为dHowNet里面没有的那个词
        '''
        r1 = self.get_one_word_yiyuan(word1)
        if r1 == False:
            raise Exception(word1)
            # return False,r1
        r2 = self.get_one_word_yiyuan(word2)
        if r2 == False:
            raise Exception(word2)
            # return False,r2
        r1 = np.array(r1)
        r2 = np.array(r2)
        common = np.intersect1d(r1, r2)

        sim = 2 * len(common) / (len(r1) + len(r2))

        return sim
        
        