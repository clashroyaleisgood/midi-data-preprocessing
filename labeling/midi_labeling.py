'''
使用流程...>
1. 更改 python 檔之 buffer, test data 名稱( 或是更改自己的資料夾名稱? )
2. 放一些 midi 進 buffer 裡
3. 執行 midi_labeling.py 然後開始標記

4. 需要注意的是
    4-1. 前面的輸入並不會立即造成 a.改寫 label.txt 或 b.移動 midi 檔
    4-2. 直到 'press enter to continue...' 步驟後!
         如果按下 enter！ txt 檔會被更改，midi 檔也會被移動
    4-3. 所以如果中間有打錯不用擔心，關掉重新打一次就好了
5. txt 的格式很簡單，所以其實有想更改的也是可以直接進去改啦
6. buffer 資料夾中的 midi 檔最後會被移到 test_data 資料夾
'''
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
print('dir:', dir_path)

BUFFER_FOLDER_PATH = dir_path + '\\buffer'
TEST_DATA_FOLDER_PATH = dir_path + '\\test_data'

files = next(os.walk(BUFFER_FOLDER_PATH))[2]            # 取出所有檔案名稱

save = {}
for e in files:
    if e.rsplit('.', 1)[1] == 'mid':
        print("\nread midi file: < " + e + " >")
        inp = input('\t\ttrack number...>')
        save[e] = inp                                   # 將 (檔名: track_num) 的配對暫存起來

print()
print('check...')                                       # 檢查有沒有打錯
print('--------------------------------------------------')
for e in save:
    print('{:<30}'.format(e), save[e])
print('--------------------------------------------------')
input('press enter to continue...')

print('saving...')                                      # 將資料寫入 label.txt 且 移動midi檔案
with open(dir_path + '\\label.txt', 'a') as f:
    for e in save:
        f.write(e + ' ' + save[e] + '\n')               # 寫檔
        os.rename(BUFFER_FOLDER_PATH + '\\' + e, \
                  TEST_DATA_FOLDER_PATH + '\\' + e)     # 移動

