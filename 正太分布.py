#coding:utf-8
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.special import erfinv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def normalDistribution(sigma,mu,min,max):
    y_max = 1.0/(sigma * np.sqrt(2 * np.pi))
    y_rand = np.random.uniform(1,100)
    y= (y_rand * y_max) / 100
    anti_log = 1.0 / (y * sigma * np.sqrt(2 * np.pi))
    x_min = -1 * np.sqrt(2 * np.power(sigma,2) * np.log(anti_log)) + mu
    x_scope = 2 * np.sqrt(2 * np.power(sigma,2) * np.log(anti_log))
    x_rand = np.random.uniform(1,100)
    x = (x_rand * x_scope)/100 + x_min
    if not str(x).replace('.', '', 1).isdigit():
        x = mu
    if x < min:
        x = min
    if x > max:
        x = max
    return round(x,2)

def boxmullersampling(mu=0, sigma=1, size=1):
    u = np.random.uniform(size=size)
    v = np.random.uniform(size=size)
    #z = mu + np.sqrt(sigma) * np.sqrt(-2 * np.log(u)) * np.sin(2 * np.pi * v)
    z = mu + np.sqrt(sigma) * np.sqrt(-2 * np.log(u)) * np.cos(2 * np.pi * v)
    return z
    
def inverfsampling(mu=0, sigma=1, size=1):
    z = np.sqrt(2)*erfinv(2*np.random.uniform(size=size)-1)
    return mu+z*sigma

if __name__ == '__main__':
    total = 10000 #所分总金额
    num = 500 #拆分红包.
    num_bins = 50
    average = float(total) / float(num) #平均数
    min = 0.5 #最小值
    total = total - min * num
    sigma = 30 #标准差
    nums = []
    for i in range(0,num):
        result  = total
        if i < num - 1 and total > 0:
            while True:
                #result = round(inverfsampling(average,sigma),2)
                result = round(boxmullersampling(average,sigma),2)
                if result >= 0 and result != '':
                    break
            if total > result:
                total = round((total - result),2)
            else:
                result = total
                total = 0
        elif i == (num -1):
            total = 0
        nums.append(round((min+result),2))
        print("第%d个红包金额:%.2f" % ((i+1),round((min+result),2)))
        print("剩余金额:%.2f" % ((min * (num - i -1)) if (i != num -1 and total == 0) else (total + (min * (num -i -1)))))
    print nums,sum(nums)
    '''
    average = 50
    sigma = 1
    numss = []
    for i in range(1,100):
        numss.append(normalDistribution(sigma,average,1,100))
    print numss
    nums = numss
    '''
    n, bins, patches = plt.hist(nums, num_bins, normed=True, facecolor = 'blue', alpha = 0.5)
    y = mlab.normpdf(bins, average, sigma)
    plt.plot(bins, y, 'r--')
    plt.xlabel('Amount of money')
    plt.ylabel('Probability')
    plt.title('Red envelopes: $\mu = %.2f$, $\sigma=%.2f$' % (round(average,2),round(sigma,2)))
    plt.subplots_adjust(left = 0.15)
    plt.show()
