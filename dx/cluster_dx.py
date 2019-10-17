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
                    ],
                '生于' :
                    [
                        '生于武汉',
                        '生于夏花',
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

    def cluster_full(self, word_list):
        '''
        
        :param word_list dict 每一次只传入
            {
                '出生于': 
                    [
                        '出生于湘潭',
                        '出生于湖北'
                    ],
                '生于' :
                    [
                        '生于武汉',
                        '生于夏花',
                    ]
                
            }

        :return
            {
                "types" : [
                    {'出生于湘潭' : '出生', '出生于湘潭' : '出生'},
                    {'出生于湘潭' : '出生', '出生于湘潭' : '出生'},
                ],
                "not_in_hownet" : {
                    '出生于': 
                        [
                            '出生于湘潭',
                            '出生于湖北'
                        ],
                }
            }
        '''
        self.word_list = word_list
        # 数据格式重构 重构成 {'出生于湘潭' : '出生'}
        formatted_data = {}
        binyus = list(word_list.keys()) # key返回一个迭代对象，需要转化为list
        for binyu in binyus:
            weibins = word_list[binyu]
            weibins = list(set(weibins)) # 去重
            for weibin in weibins:
                formatted_data[weibin] = binyu
        # 开始聚类
        words = list(formatted_data.keys())

        event_types = {}

        list_len = len(words)

        not_in_hownet = [] # HowNet中没有的短语都列出来

        for index, word_1 in enumerate(words):
            # 首先进行义原过滤
            if self.hownet.get_one_word_yiyuan(word_1) == False:
                not_in_hownet.append(word_1)
                continue

            # 如果这个词已经归类了就过滤掉
            if self.find_ele(event_types, word_1) == True:
                continue 

            # # 这个词在HowNet中没有的情况下则过滤
            # if word_1 in not_in_hownet[binyu]:
            #     continue

            # 不存在就创建一个类型
            if word_1 not in event_types: 
                # event_types[word_1] = [{word_1 : formatted_data[word_1]}]  
                event_types[word_1] = {word_1 : formatted_data[word_1]}
            
            next_index = index + 1
            for index_2 in range(next_index, list_len): # 左闭右开
                word_2 = words[index_2]
                # 再次进行义原过滤
                if self.hownet.get_one_word_yiyuan(word_2) == False:
                    not_in_hownet.append(word_2)
                    continue
                # # 这个词在HowNet中没有的情况下则过滤
                # if word_2 in not_in_hownet[binyu]:
                #     continue
                try:
                    s = self.sim(word_1, word_2)
                except Exception as e:
                    # HowNet中没有这个组合的义原
                    e = str(e)
                    if e not in not_in_hownet[binyu]:
                        not_in_hownet.append(e)
                    continue
                # print(not_in_hownet[binyu])
                # 两个词都有则计算相似度
                print('''{} - {} -相似度: {}'''.format(word_1, word_2, s))
                if s >= self.threshold:
                    # event_types[word_1].append({word_2 : formatted_data[word_2]}) # 与统计不同
                    event_types[word_1][word_2] =  formatted_data[word_2]
                else:
                    if self.find_ele(event_types, word_2) == True:
                        continue
        # not_in_hownet重构
        new_not_in_hownet = {}
        for weibin in not_in_hownet:
            binyu = formatted_data[weibin]
            if binyu in new_not_in_hownet.keys():
                new_not_in_hownet[binyu].append(weibin)
            else:
                new_not_in_hownet[binyu] = [weibin]
        return {
            "types" : event_types,
            "not_in_hownet" : new_not_in_hownet
        }

    def cluster_all(self, word_list):
        '''
        完全按照DX的方法来，一次一次遍历整个DICT

        :param  word_list
            {
                "订": [
                    "订门票",
                    "订房",
                    "订机票",
                    "订间",
                    "订房",
                    "订酒店",
                ],
                "订": [
                    "订门票",
                    "订房",
                    "订机票",
                    "订间",
                    "订房",
                    "订酒店",
                ]
            }


        '''




    def cluster(self, word_list):
        '''
        谓语相同，宾语不同情况之下的聚类

        :papram word_list
            {
                "订": [
                    "订门票",
                    "订房",
                    "订机票",
                    "订间",
                    "订房",
                    "订酒店",
                ]
            }

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

        not_in_hownet = {} # HowNet中没有的短语都列出来
        not_in_hownet[binyu]  = []

        for index, word_1 in enumerate(words):
            # 首先进行义原过滤
            if self.hownet.get_one_word_yiyuan(word_1) == False:
                not_in_hownet[binyu].append(word_1)
                continue

            # 一个词只有一个结果的情况下则过滤
            if self.find_ele(event_types, word_1) == True:
                continue 

            # # 这个词在HowNet中没有的情况下则过滤
            # if word_1 in not_in_hownet[binyu]:
            #     continue

            # 不存在就创建一个类型
            if word_1 not in event_types: 
                event_types[word_1] = [word_1]  
            
            next_index = index + 1
            for index_2 in range(next_index, list_len): # 左闭右开
                word_2 = words[index_2]
                # 再次进行义原过滤
                if self.hownet.get_one_word_yiyuan(word_2) == False:
                    not_in_hownet[binyu].append(word_2)
                    continue
                # # 这个词在HowNet中没有的情况下则过滤
                # if word_2 in not_in_hownet[binyu]:
                #     continue
                try:
                    s = self.sim(word_1, word_2)
                except Exception as e:
                    # HowNet中没有这个组合的义原
                    e = str(e)
                    if e not in not_in_hownet[binyu]:
                        not_in_hownet[binyu].append(e)
                    continue
                # print(not_in_hownet[binyu])
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
        '''
        过滤
        '''
        # return ele in dic

        for k, v_dict in dic.items():
            if ele in v_dict.keys():
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
     