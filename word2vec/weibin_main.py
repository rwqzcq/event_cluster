# 谓宾聚类
import abc
import json


def get_class_id(weiyu, binyu):
    pass


class WordClass(metaclass=abc.ABCMeta):

    def __init__(self):
        self.load_cluster()

    @abc.abstractmethod
    def load_cluster(self):
        pass
    
    @abc.abstractmethod
    def get_class_id(self, word):
        pass

class WeiyuClass(WordClass):
    weiyu_cluster = [] # 谓语类

    def load_cluster(self):
        path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/谓语_宾语聚类结果/谓语_400.json'
        with open(path, 'r', encoding='utf-8') as f:
            self.weiyu_cluster = json.load(f)

    def get_class_id(self, word):
        """找到所在的类
        
        Arguments:
            word {str} -- 词语
        
        Raises:
            Exception: 找不到类
        
        Returns:
            [dict] -- {'index' : 1, 'class' : []}
        """
        result = {}
        for index, words in enumerate(self.weiyu_cluster):
            if word in words:
                result['index'] = index
                result['class'] = words
                break
            else:
                continue
        if result == {}:
            raise Exception("找不到"+word+"所在的类")
        return result

class BinyuClass(WordClass):
    binyu_cluster = [] # 谓语类

    def load_cluster(self):
        path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/谓语_宾语聚类结果/宾语_4000.json'
        with open(path, 'r', encoding='utf-8') as f:
            self.binyu_cluster = json.load(f)

    def get_class_id(self, word):
        result = {}
        for index, words in enumerate(self.binyu_cluster):
            if word in words:
                result['index'] = index
                result['class'] = words
                break
            else:
                continue
        if result == {}:
            raise Exception("找不到"+word+"所在的类")
        return result



class WeibinClass:
    """谓语宾语分开聚类
    1. 先对谓语进行聚类
    2. 在于宾语进行聚类
    3. 输入一个谓语宾语组合可以得到谓语和宾语分别属于的类
    """
    weiyu_instance = None # 谓语类
    binyu_instance = None # 宾语类

    def __init__(self):
        self.load_binyu_cluster()
        self.load_weiyu_cluster()

    def load_weiyu_cluster(self):
        """加载谓语聚类结果
        """
        self.weiyu_instance = WeiyuClass()
    
    def load_binyu_cluster(self):
        """加载宾语聚类结果
        """
        self.binyu_instance = BinyuClass()
    
    def get_weibin_class(self, weiyu, binyu):
        """获取一个谓宾短语的聚类结果
        
        Arguments:
            weiyu {str} -- 谓语
            binyu {str} -- 宾语
        
        Returns:
            [dict] -- {'weiyu' : None, 'binyu' : None}
        """
        result = {}
        try:
            weiyu_result = self.weiyu_instance.get_class_id(weiyu)
            result['weiyu'] = weiyu_result
        except Exception as e:
            result['weiyu'] = None
        try:
            binyu_result = self.binyu_instance.get_class_id(binyu)
            result['binyu'] = binyu_result
        except Exception as e:
            result['binyu'] = None
        return result


def main():
    # ! 分别计算谓语和宾语所属于的类标号
    path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/event_cluster/dataset/原始谓宾.json'
    wb  = WeibinClass()
    with open(path, 'r', encoding='utf-8') as f:
        weibins = json.load(f)
    base_path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/谓语_宾语聚类结果/'
    filter_filename = '原始谓宾_过滤后.json'
    filter_data = []
    results = []
    # weibins = [
    #     "吃 草药",
    #     "订 机票"
    # ]
    for weibin in weibins:
        class_id = []
        weibin_new = weibin.split(' ')
        weiyu = weibin_new[0]
        binyu = weibin_new[1]
        result = wb.get_weibin_class(weiyu, binyu)
        if result['weiyu'] == None or result['binyu'] == None: # 没有就过滤掉
            continue 
        class_id.append(result['weiyu']['index'])
        class_id.append(result['binyu']['index'])
        results.append(class_id)
        filter_data.append(weibin)
    
    with open(base_path + filter_filename, 'w', encoding='utf-8') as f:
        json.dump(filter_data, f, ensure_ascii=False)

    with open(base_path + '分别聚类后的ID号.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False)
    
    # ! 对类标号进行聚类
    final_lei = {}
    l = len(results)
    for index, result in enumerate(results):
        weiyu_id = result[0]
        binyu_id = result[1]
        leihao = '''{}_{}'''.format(weiyu_id, binyu_id)
        final_lei[leihao] = [result] # 先创建一个类
        next_index = index + 1
        for index_2 in range(next_index, l):
            weibin_2 = results[index_2]
            weiyu_id_2 = weibin_2[0]
            binyu_id_2 = weibin_2[1]

            if weiyu_id == weiyu_id_2:
                if binyu_id == binyu_id_2: # 都是一个类簇
                    final_lei[leihao].append(weibin_2)
                else: # 加入新的类簇
                    final_lei[leihao] = [weibin_2]
            # else:
            #     final_lei[leihao] = [result]
    with open(base_path + '聚类结果_类号.json', 'w', encoding='utf-8') as f:
        json.dump(final_lei, f, ensure_ascii=False)

def cluster():
    base_path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/谓语_宾语聚类结果/'
    with open(base_path + '分别聚类后的ID号.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    # ! 对类标号进行聚类
    # results = [
    #     [84, 3728], [84, 952], [84, 278], [84, 201], [84, 1931], [84, 2619], [84, 46], [84, 1411], [84, 2114], [161, 1234], [161, 3681], [161, 769], [161, 1411], [161, 292], [161, 447], [166, 1408], [166, 434], [166, 1411], [84, 1948], [84, 1411], [84, 2114], [84, 1411], [84, 550], [245, 2305], [84, 2477], [161, 653], [84, 1672], [84, 2374], [84, 1178]
    # ]
    # results = [
    #     [84, 3728], [84, 952], [84, 278], [84, 278], [84, 3728], [84, 3728], [84, 3728], [84, 3728],
    #     [84, 952],[84, 952],[84, 952],[84, 952],[100, 100]
    # ]
    final_lei = {}
    l = len(results)
    has_assign = [] # ! 把已经分配的类放到这个变量里面
    for index, result in enumerate(results):
        print(len(has_assign))
        weiyu_id = result[0]
        binyu_id = result[1]
        leihao = '''{}_{}'''.format(weiyu_id, binyu_id)
        if leihao not in final_lei.keys(): # 类号存在
            final_lei[leihao] = [index] # 先创建一个类
        next_index = index + 1
        for index_2 in range(next_index, l):
            if index_2 in has_assign:
                continue
            weibin_2 = results[index_2]
            weiyu_id_2 = weibin_2[0]
            binyu_id_2 = weibin_2[1]
            leihao = '''{}_{}'''.format(weiyu_id_2, binyu_id_2)
            if weiyu_id == weiyu_id_2:
                if binyu_id == binyu_id_2: # 都是一个类簇
                    final_lei[leihao].append(index_2)
                    has_assign.append(index_2)
    # print(final_lei)
    with open(base_path + '聚类结果_类号.json', 'w', encoding='utf-8') as f:
        json.dump(final_lei, f, ensure_ascii=False)
    

def format_full_name():
    base_path = '/Users/renweiqiang/Desktop/CaoGaohui/project/基于事理图谱的社会化问答知识组织与服务研究/code/丁校硕士论文事件类型确定/谓语_宾语聚类结果/'
    with open(base_path + '聚类结果_类号.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    results = {}
    binyus = []
    weiyus = []
    format = {}
    orignal = []
    with open(base_path + '原始谓宾_过滤后.json', 'r', encoding='utf-8') as f:
        orignal = json.load(f)
    for index, phrases in results.items():
        index = index.split('_')
        # weiyu = index[0]
        # binyu = index[1]
        # format[weiyu + '_' + binyu] = []
        format[index] = []
        for phrase_id in phrases:
            # format[weiyu + '_' + binyu].append(orignal[phrase_id])
            format[index].append(orignal[phrase_id])
    # with open(base_path + '转化后的聚类')
    with open(base_path + "完整版聚类结果.json", 'w', encoding='utf-8') as f:
        json.dump(format, f, ensure_ascii=False)

if __name__ == "__main__":

    cluster()






        


