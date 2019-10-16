from OpenHowNet.HowNet import Standards
import numpy as np
import json

word = '破产'
# hownet = Standards.HowNetDict()

# 获取破产的完整信息
# full_info = hownet.get(word)
# with open('./' + word + '.json', 'w', encoding='utf-8') as f:
#     json.dump(full_info, f, ensure_ascii=False)

# 获取破产的义原
# yiyuan = hownet.get_sememes_by_word(word)
# print(yiyuan)

# hownet.initialize_sememe_similarity_calculation()
# s = hownet.calculate_word_similarity(word1, word2)


class HowNet:
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
            print(word + "在Hownet中不存在义原描述")
            return False
        
        r = []

        for sememe in sememes:
            r = r + list(sememe['sememes'])
        return list(set(r))
    
    def word_sim_v_dx(self, word1, word2):
        '''
        动词的比较

        计算公式为 2 * 公共部分 / (word1 + word2)

        openHownet自带的方法比这个要好

        比如亏损和破产 这个方法的相似度为0.6 而自带的方法为0.73
        '''
        r1 = self.get_one_word_yiyuan(word1)
        if r1 == False:
            return 0
        r2 = self.get_one_word_yiyuan(word2)
        if r2 == 0:
            return False
        r1 = np.array(r1)
        r2 = np.array(r2)
        common = np.intersect1d(r1, r2)

        sim = 2 * len(common) / (len(r1) + len(r2))
        return sim
        
        



hn = HowNet()
# r = hn.get_one_word_yiyuan(word)
# print(r)
# word = "亏损"
# r = hn.get_one_word_yiyuan(word)
# print(r)
s = hn.word_sim_v_dx('打架了', '打电话')
print(s)

# hownet = Standards.HowNetDict()

# hownet.initialize_sememe_similarity_calculation()
# s = hownet.calculate_word_similarity(word0 = '破产', word1 = '亏损')
# print(s)