import numpy as np
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

def load_train_file(filename):
    with np.load(filename) as f:
        s_tr = f['s_train']
        x_tr = f['x_test']
        y_tr = f['y_test']
        return x_tr, y_tr, s_tr
'''
x_test, y_test, sum_train= load_train_file(dir_path + '\\train.npz')
x_test = x_test.reshape(sum_train, -1, 2)
y_test = y_test.reshape(sum_train, -1)
'''


with np.load(dir_path + '\\newtest.npz') as f:
    x_test = f['x_test']
    y_test = f['y_test']


print(x_test)
print()
print(y_test)
