from sklearn.cluster import KMeans
from cluster import KmeansCluster
import matplotlib.pyplot as plt
import json
import os
from sklearn.externals import joblib



# ! 下面的是为每一个都生成一个类

def weiyu_cluster():
    # ！ 训练
    word_type = "谓语"
    vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量\\' + word_type + '.json'
    with open(vector_path, 'r', encoding='utf-8') as f:
        binyu_vectors = json.load(f)
    binyus = list(binyu_vectors.keys())
    vectors = list(binyu_vectors.values())
    k = 400
    # estimator = KMeans(n_clusters=k)
    # estimator.fit(vectors)
    model_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\模型文件\\' + word_type + '_' + str(k) + '.pkl'
    # joblib.dump(estimator, model_path)
    kmeans = KmeansCluster()
    kmeans.load_vectors(vectors).cluster(k).save_model(model_path) # ! 训练并模型
    clusters = kmeans.get_formatted_clusters(binyus, k)
    r_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\聚类结果\\' + word_type + '_' + str(k) + '.json'
    with open(r_path, 'w', encoding='utf-8') as f:
        json.dump(clusters, f, ensure_ascii=False)

def word_cluster(word_type, k):
    """宾语分别聚类谓语聚类
    
    Arguments:
        word_type {str} -- 词语类型
        k {int} -- 聚类个数
    """
        # ！ 训练
    # word_type = "谓语"
    vector_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\向量\\' + word_type + '.json'
    with open(vector_path, 'r', encoding='utf-8') as f:
        binyu_vectors = json.load(f)
    binyus = list(binyu_vectors.keys())
    vectors = list(binyu_vectors.values())
    # k = 400
    # estimator = KMeans(n_clusters=k)
    # estimator.fit(vectors)
    model_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\模型文件\\' + word_type + '_' + str(k) + '.pkl'
    # joblib.dump(estimator, model_path)
    kmeans = KmeansCluster()
    kmeans.load_vectors(vectors).cluster(k).save_model(model_path) # ! 训练并模型
    clusters = kmeans.get_formatted_clusters(binyus, k)
    r_path = 'I:\\代码\\事理图谱\\event_cluster\\谓语宾语分别聚类\\聚类结果\\' + word_type + '_' + str(k) + '.json'
    with open(r_path, 'w', encoding='utf-8') as f:
        json.dump(clusters, f, ensure_ascii=False)


if __name__ == '__main__':
    # weiyu_cluster()
    word_cluster(word_type = "宾语", k = 4000)
    # SSE = []  # 存放每次结果的误差平方和
    # vec_min = 4000
    # vec_max = 7000
    # step = 250
    # vec_qijian = range(vec_min,vec_max, step)

    # vec_min = 1000
    # vec_max = 7000
    # vec_qujian = [1000, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000, 6250, 6500, 6750, 7000]
    # for k in vec_qujian:
    #     # print(k)
    #     # estimator = KMeans(n_clusters=k)  # 构造聚类器
    #     # estimator.fit(vectors)
    #     abs_path = 'I:\\代码\\事理图谱\\event_cluster\\模型文件\\hanlp_FastText\\' + str(k) + '.pkl'
    #     estimator = joblib.load(abs_path)
    #     joblib.dump(estimator, abs_path)
    #     SSE.append(estimator.inertia_)
    # # plt.figure.figsize = []
    # plt.rcParams['savefig.dpi'] = 300 #图片像素
    # plt.rcParams['figure.dpi'] = 300 #分辨率
    # X = vec_qujian
    # plt.xlabel('k')
    # plt.ylabel('SSE')
    # plt.plot(X,SSE,'o-')
    
    # plt.savefig('''./手肘图_{}_{}.png'''.format(vec_min, vec_max))
    # plt.show()
    


