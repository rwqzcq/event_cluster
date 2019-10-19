from sklearn.cluster import KMeans
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import json
import os


class KmeansCluster:
    """Kmeans聚类
    """

    vectors = None # 传入的数据
    model = None # 模型


    
    def load_vectors(self, vectors):
        """加载向量
        
        Arguments:
            vectors {list} -- 二维数组
        """
        self.vectors = vectors
        return self
    
    def load_model(self, model_path):
        """加载模型
        
        Arguments:
            model_path {str} -- 模型的路径
        """
        self.model = joblib.load(model_path)
        return self
    
    def save_model(self, model_path):
        """保存模型
        
        Arguments:
            model_path {str} -- 模型的路径
        """
        if self.model == None:
            raise Exception("没有训练出模型")

        joblib.dump(self.model, model_path)


    def cluster(self, k):
        """训练模型
        
        Arguments:
            k {int} -- 类的个数
        """
        estimator = KMeans(n_clusters=k)
        estimator.fit(self.vectors) # * 开始训练
        self.model = estimator
        return self
    
    def get_formatted_clusters(self, orignal_data, k):
        """输入原始数据，返回组织好的聚类的结果
        
        Arguments:
            orignal_data {list} -- 原始的数据，是一个一维list
        
        参考链接:
            1. https://blog.csdn.net/biboshouyu/article/details/62424457
        """

        # ! labels是一个一维数组，返回的是每一个word_id所对应的类标号
        labels = self.model.labels_.tolist() # numpy转化成list
        r = []
        for i in range(0, k):
            r.append([])
        for word_id, lei_id  in enumerate(labels):
            if len(r[lei_id]) == 0:
                r[lei_id] = []
            r[lei_id].append(orignal_data[word_id])

        return r
    
    def get_model(self):

        return self.model







if __name__ == '__main__':
    """使用K-means和Phrase2vec来实现谓宾短语聚类
    """
    
    path = os.path.abspath('./results/过滤后的向量.json')
    with open(path, 'r', encoding='utf-8') as f:
        vectors = json.load(f)
    

    SSE = []  # 存放每次结果的误差平方和
    vec_min = 4000
    vec_max = 7000
    step = 250
    vec_qijian = range(vec_min,vec_max, step)
    for k in vec_qijian:
        print(k)
        estimator = KMeans(n_clusters=k)  # 构造聚类器
        estimator.fit(vectors)
        abs_path = 'I:\\代码\\事理图谱\\event_cluster\\模型文件\\hanlp_FastText\\' + str(k) + '.pkl'
        joblib.dump(estimator, abs_path)
        SSE.append(estimator.inertia_)
    # plt.figure.figsize = []
    plt.rcParams['savefig.dpi'] = 300 #图片像素
    plt.rcParams['figure.dpi'] = 300 #分辨率
    X = vec_qijian
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(X,SSE,'o-')
    plt.savefig('''../手肘图_{}_{}.jpg'''.format(vec_min, vec_max))