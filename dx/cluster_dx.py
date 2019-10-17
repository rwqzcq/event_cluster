import requests
import json
from sim.hownet_sim import HowNetSim


class ClusterDX:
    '''
    利用丁校的方法进行相似度计算\n
    谓语加宾语的聚类\n
    '''

    def __init__(self, word_list, threshold):
        '''
        :param word_list dict 每一次只传入
            {
                '出生于': 
                    [
                        '出生于湘潭',
                        '出生于湖北'
                    ]
                
            }
        '''
        self.word_list = word_list # 触发词列表
        self.threshold = threshold # 阈值
        self.hownet = HowNetSim()
    
    def sim(self, vi, vj):
        '''
        计算相似度
        vi {}
        vj {}
        '''

        return self.hownet.word_sim_v_dx(vi, vj)

    def cluster(self):
        '''
        聚类

        :return
            {
                "types" : [],
                "not_in_hownet" : []
            }
        '''
        event_types = {}

        binyu = list(self.word_list.keys())[0]
        words = self.word_list[binyu]

        list_len = len(words)

        not_in_hownet = {} # HowNet中没有的词都列出来
        not_in_hownet[binyu]  = []
        for index, word_1 in enumerate(words):
            # 一个词只有一个结果的情况下则过滤
            if self.find_ele(event_types, word_1) == True:
                continue 
            # 这个词在HowNet中没有的情况下则过滤
            if word_1 in not_in_hownet[binyu]:
                continue
            # 不存在就创建一个类型
            if word_1 not in event_types: 
                event_types[word_1] = [word_1]  
            next_index = index + 1
            for index_2 in range(next_index, list_len): # 左闭右开
                word_2 = words[index_2]
                # 这个词在HowNet中没有的情况下则过滤
                if word_2 in not_in_hownet[binyu]:
                    continue
                try:
                    s = self.sim(word_1, word_2)
                except Exception as e:
                    # HowNet中没有这个组合的义原
                    not_in_hownet[binyu].append(str(e))
                    continue
                # 两个词都有则计算相似度
                print('''{} - {} -相似度: {}'''.format(word_1, word_2, s))
                if s >= self.threshold:
                    event_types[word_1].append(word_2)
                else:
                    if self.find_ele(event_types, word_2) == True:
                        continue
        return {
            "types" : event_types,
            "not_in_hownet" : not_in_hownet
        }
    
    def find_ele(self, dic, ele):
        for (k, v) in dic.items():
            if ele in v:
                return True
        return False



# if __name__ == "__main__":
#     # word1 = "关闭"
#     # word2 = "关门"
#     # r = hownet_word_sim(word1,word2)
#     # print(r)
#     word_list = {"订" : "订票", "订" : "订房"}  
#     # 
#     c = ClusterDX(word_list, 0.6)
#     r = c.cluster()
     