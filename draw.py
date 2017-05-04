from matplotlib import pyplot as plt

def draw_cifar():
    x = [ 12, 24, 32, 48]
    d = {
        'FP_CNNH' : [0.612, 0.639, 0.625, 0.616],
        'CNNH' : [0.438, 0.508, 0.505, 0.519],
        'KSH' : [0.301, 0.331, 0.342, 0.353],
        'ITQ_CCA' : [0.261, 0.280, 0.283, 0.287],
        'MLH' : [0.177, 0.191, 0.205, 0.209],
        'BRE' : [0.153, 0.178, 0.191, 0.193],
        'SH' : [0.125, 0.126, 0.129, 0.127],
        'ITQ' : [0.161, 0.165, 0.170, 0.172],
        'LSH' : [0.120, 0.123, 0.119, 0.118],
    }
    x2 = [12, 32, 48, 64]
    y = [0.837, 0.862, 0.886, 0.898]

    plt.figure()
    for k, v in d.items():
        plt.plot(x, v, label=k)

    plt.plot(x2, y, label='hash')

    plt.legend()
    plt.title('Image Retrieval Precision of CIFAR-10')
    plt.xlabel('length of hashcode')
    plt.ylabel('Precision')
    #plt.show()
    plt.savefig('cifar.jpg')

def draw_mnist():
    x = [ 12, 24, 32, 48]
    d = {
        'FP-CNNH': [0.962, 0.965, 0.968, 0.969],
        'CNNH': [0.951, 0.955, 0.956, 0.959],
        'KSH': [0.869, 0.889, 0.891, 0.896],
        'ITQ-CCA': [0.653, 0.686, 0.712, 0.721],
        'MLH': [0.471, 0.652, 0.650, 0.651],
        'BRE': [0.512, 0.581, 0.601, 0.622],
        'SH': [0.261, 0.265, 0.258, 0.248],
        'ITQ': [0.386, 0.432, 0.421, 0.426],
        'LSH': [0.185, 0.206, 0.233, 0.241],
    }
    x2 = [8, 16, 32, 64]
    y = [0.9594, 0.9741, 0.9548, 0.9589]

    plt.figure()
    for k, v in d.items():
        plt.plot(x, v, label=k)

    plt.plot(x2, y, label='hash')

    plt.legend()
    plt.title('Image Retrieval Precision of MNIST')
    plt.xlabel('length of hashcode')
    plt.ylabel('Precision')
    #plt.show()
    plt.savefig('mnist.jpg')

draw_cifar()
draw_mnist()
