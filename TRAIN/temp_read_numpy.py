import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def load_train_file(filename):
    with np.load(filename) as f:
        s_tr = f['s_train']
        x_tr = f['x_train']
        y_tr = f['y_train']
        return x_tr, y_tr, s_tr
'''
x_train, y_train, sum_train= load_train_file(dir_path + '\\train.npz')
x_train = x_train.reshape(sum_train, -1, 2)
y_train = y_train.reshape(sum_train, -1)
'''


with np.load(dir_path + '\\newtrain.npz') as f:
    x_train = f['x_train']
    y_train = f['y_train']


print(x_train)
print()
print(y_train)
