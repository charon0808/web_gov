"""t-SNE 对手写数字进行可视化"""
from time import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.manifold import TSNE


def get_data():
    digits = datasets.load_iris()
    # digits = datasets.load_digits(n_class=6)
    data = digits.data
    label = digits.target
    n_samples, n_features = data.shape
    print(type(data))
    return data, label, n_samples, n_features


def plot_embedding(data, label, title):
    x_min, x_max = np.min(data, 0), np.max(data, 0)
    data = (data - x_min) / (x_max - x_min)

    fig = plt.figure()
    ax = plt.subplot(111)
    for i in range(data.shape[0]):
        plt.scatter(data[i, 0], data[i, 1],
                 color=plt.cm.Set1(label[i] / 10.),
                 )
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    return fig


def tsne(data, label):
    print('Computing t-SNE embedding')
    ts = TSNE(n_components=2, init='pca', random_state=0)
    t0 = time()
    result = ts.fit_transform(data)
    fig = plot_embedding(result, label,
                         't-SNE embedding of the data (red is outlier)'
                         )
    return fig
    #fig.savefig("name.png")

