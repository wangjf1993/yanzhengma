#!/usr/bin/python
# -*- coding:utf-8 -*-

from tensorflow.examples.tutorials.mnist.input_data import *
import tensorflow as tf

# 读取数据集，read_data_sets是一个已经封装好的方法，会去直接下载数据并且做预处理
mnist = read_data_sets("MNIST_data/", one_hot=True)

# # 定义数据，设置占位符
# 设置特征与标签的占位符，特征集是n×784维，标签集维n×10维，n是可以调节的
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder("float", [None, 10])
# 设置dropout的占位符，dropout用于防止过拟合
keep_pro = tf.placeholder("float")
# 将平铺的特征重构成28×28的图片像素维度，因为使用的是黑白图片，所以颜色通道维1,因为要取出所有数据，所以索引维-1
x_image = tf.reshape(x, [-1, 28, 28, 1])


# # 定义函数以方便构造网络
# 初始化权重,传入大小参数，truncated_normal函数使得w呈正太分布，
# stddev设置标准差为0.1。也就是说输入形状大小，输出正太分布的随机参数作为权重变量矩阵
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


# 初始化偏执项，传入矩阵大小的参数，生成该大小的值全部为0.1的矩阵
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# 定义卷基层，步长为1,周围补0，输入与输出的数据大小一样（可得到补全的圈数）
def conv2d(a, w):
    return tf.nn.conv2d(a, w, strides=[1, 1, 1, 1], padding='SAME')


# 定义池化层,kernel大小为2,步长为2,周围补0，输入与输出的数据大小一样（可得到补全的圈数）
def max_pool_2x2(a):
    return tf.nn.max_pool(a, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding="SAME")

# # 进入卷积层与池化层1
# 初始化权重，传入权重大小，窗口的大小是5×5,所以指向每个卷积层的权重也是5×5,
# 卷积层的神经元的个数是32,总共只有1个面（1个颜色通道）
w_conv1 = weight_variable([5, 5, 1, 32])
# 32个神经元就需要32个偏执项
b_conv1 = bias_variable([32])
# 将卷积层相对应的数据求内积再加上偏执项的这个线性函数，放入激励层relu中做非线性打转换，输出的大小是28×28×32
h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)
# 将卷积层输出的数据传入池化层，根据函的设定，窗口大小维2×2,步长为2,输出的大小就降到来14×14×32
h_pool1 = max_pool_2x2(h_conv1)

# # 进入卷积层与池化层2
# 第2层卷积层由64个神经元，1个神经元要初始化的权重维度是5×5×32
w_conv2 = weight_variable([5, 5, 32, 64])
# 偏执项的数目和神经元的数目一样
b_conv2 = bias_variable([64])
# 将池化层1的输出与卷积层2的权重做内积再加上偏执项，然后进入激励函数relu，输出维度为14×14×64
h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
# 进入池化层，输出减半为7×7×64
h_pool2 = max_pool_2x2(h_conv2)
# # 进入全连接层1
# 初始化全链接层的权重，全了链接层有1024个神经元，每个都与池化层2的输出数据全部连接
w_fc1 = weight_variable([7*7*64, 1024])
# 偏执项也等于神经元的个数1024
b_fc1 = bias_variable([1024])
# 将池化层的输出数据拉平为1行7×7×64列打矩阵，-1表示把所有都拿出来
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
# 全连接计算，线性运算后再输入激励函数中，最后输出1024个数据
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
# 使用dropout防止过拟合
h_fc1_drop = tf.nn.dropout(h_fc1, keep_pro)

# # 进入全连接层2
# 初始化权重，全连接层2有10个神经元，上一层打输入是1024
w_fc2 = weight_variable([1024, 10])
# 偏执项为10
b_fc2 = bias_variable([10])
# 全连接的计算，然后再过一个softmax函数，输出为10个数据（10个概率）
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

# # 损失函数最小的最优化计算
# 交叉熵作为目标函数计算
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
# 目标函数最小训练模型，估计参数，使用的是ADAM优化器来做梯度下降
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# 计算预测正确的个数，tf.argmax是寻找一个tensor中每个维度的最大值所在的索引
# 因为类别是用0，1表示的，所以找出1所在打索引就能找到数字打类别
# tf.equals是检测预测与真实的标签是否一致，返回的是布尔值，true,false
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
# 计算正确率,用tf.cast来将true,false转换成1,0,然后计算正确率
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

# # 创建会话,初始化变量
sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())

# # 执行循环
for i in range(2000):
    # 每批取出50个训练样本
    batch = mnist.train.next_batch(50)
    # 循环次数是100的倍数的时候，打印东东
    if i % 100 == 0:
        # 计算正确率，
        train_accuracy = accuracy.eval(feed_dict={
           x: batch[0], y_: batch[1], keep_pro: 1.0})
        # 打印
        print("step %d, training accuracy %g" % (i, train_accuracy))
    # 执行训练模型
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_pro: 0.5})
# 打印测试集正确率
print("test accuracy %g" % accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_pro: 1.0
    }))
