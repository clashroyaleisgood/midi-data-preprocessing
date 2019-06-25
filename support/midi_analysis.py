'''
class Track: 用來管理一個track
    __init__: 初始化 輸入 "最小單位"
    event_process(): 處理一個 event (使用多個函式)
    ---> updata_time(): 更新 self.time_count 時間
    ---> note_on(): on 事件就呼叫他
    ---> note_off(): off 事件
    left_event(): 將 midi 檔忘了關掉的 note note_off()
    sort(): 排序 self.output()
    __str__: print() 格式

class File: 用來管理多個 midi 文件
    __init__: 初始化
    read_file_names(): 將路徑底下所有 midi 檔的名稱 存起來
    read_all_file(): 每次開啟一個 midi file
    ---> 用法 for file in read_all_file():
    ------->      file...
    ---> 相當於多次使用 file = MidiFile(filename)
    __len__: 資料夾內有幾個 midi file
    __str__: 輸出格式
'''
import numpy as np

# DEAL with a track: track -> numpy arr
class Track():
    def __init__(self, segment, unit_size=24):
        self.keyboard = [None]*128
        self.output = set()
        self.time_count = 0
        self.unit = unit_size
        self.segment = segment

    def update_time(self, interval):
        self.time_count += interval

    def event_process(self, event, i= None, debug_mode= False):  # 會往下呼叫 note_on/off'
        if debug_mode:
            print('time_count:', self.time_count)
        
        self.update_time(event.time)
        if event.type == 'note_on':
            if event.velocity == 0:     # 沒有力度的 note_on
                self.note_off(event, i, velo_zero=True)
            else:
                self.note_on(event, i)
        elif event.type == 'note_off':
            self.note_off(event, i)
        else:
            pass

    def left_event(self):
        for e in self.keyboard:
            if e:
                begin = e//self.unit
                length= (self.time_count - e)//self.unit
                if length != 0:
                    self.output.add((begin, length))      # 起始時間 + 持續時間
                # self.event_process(e)

    def to_sort_list(self):
        self.output = sorted(list(self.output))

    def output_process(self, size= 1000):
        temp = self.output
        
        self.beat_length= temp[-1][0] - temp[0][0]      # 維持時間長度(unit size)
        # --------------------------------------
        array=np.array(temp)
        if len(array)<size:
            array=np.pad(array, ((0, size-len(array)), (0, 0)), 'constant')
        else:
            array=array[:size]

        return array
        # ----------------------------------------

    def take_segment(self, output_list):            # 回傳固定時間長度的 List
        pass

    def note_on(self, msg, i= None):
        note = msg.note
        if i and self.keyboard[note] != None:
            print(i, 'on length:', (self.time_count - self.keyboard[note]) )
        if self.keyboard[note] != None:
            begin = self.keyboard[note]//self.unit
            length= (self.time_count - self.keyboard[note])//self.unit
            if length != 0:
                self.output.add((begin, length))     # 起始時間 + 持續時間
        self.keyboard[note] = self.time_count

    def note_off(self, msg, i=None, velo_zero=False):
        note = msg.note
        if i and self.keyboard[note] != None:
            print(i, 'off length:', (self.time_count - self.keyboard[note]) )
        if self.keyboard[note] != None:
            begin = self.keyboard[note]//self.unit
            length= (self.time_count - self.keyboard[note])//self.unit
            if length != 0:
                self.output.add((begin, length))      # 起始時間 + 持續時間

            self.keyboard[note] = None
        '''elif velo_zero: # 無法避免 velocity=0 後的 note_off
            pass
        else:
            raise Exception('invalid note-off!')'''

    def valid_output(self):     # event 數量夠多 而且 總持續時間夠長
        if len(self.output) < 20:  # too short
            print("too short")
            return False
        elif self.output[-1][0] - self.output[0][0] < self.segment:
            print("not long enough")
            return False
        else:
            return True

        # return len(self.output) > 100 and self.output[-1][0] - self.output[0][0] > self.segment

    def __str__(self):
        out_str=[]
        for e in self.output:
            out_str += [' '.join([str(f) for f in e])]
        return '\n'.join(out_str)
    

from os import walk
from os.path import isdir
from mido import MidiFile
from support.theme import select_theme, select_max_len
#======================================================================================

# DEAL with files: label/ midi folders/ open midi
class File():
    def __init__(self, dirpath, error_log):
        self.files = [] # midi file names
        self.sum = 0
        self.dirpath = dirpath
        self.label = {}
        self.error_log = error_log
    
    def read_file_names(self):      # 將路徑底下所有 midi 檔的名稱 存起來
        while not isdir(self.dirpath):  # 如果資料夾不存在
            input("place midi folder to the correct position...\n"+ self.dirpath)

        for root, _, files in walk(self.dirpath):
            print("\n路徑：", root)
            #print("  目錄：", dirs)
            #print("  檔案：", files)
            for f in files:
                if f.rsplit('.', 1)[-1] == 'mid':
                    self.files += [f]
                    self.sum += 1
        print('{} midi file\n'.format(self.sum))
    
    def read_all_file(self):        # 每次開啟一個 midi file
        for file in self.files:
            filename = self.dirpath+ file
            try:
                with MidiFile(filename) as f:
                    yield f, file       # 回傳 MidiFile, filename
            except:
                print('\t\tERROR_{:<8} at: {}'.format('OPEN', file))
                self.error_log.log("OPEN ERROR: {}".format(file))

    def read_label_file(self, file_name):
        try:
            with open(file_name) as f:
                for line in f:
                    line = line.rstrip('\n').rsplit(' ', 1)
                    self.label[line[0]] = int(line[1])
        except:
            raise Exception('no such file: {}'.format(file_name))

    def __len__(self):
        return self.sum

    def __str__(self):
        return '\n'.join(self.files)

    def select_track(self, midifile=None, filename=None):
        if midifile:                      # midifile (for train data)
            return select_theme(midifile)
        elif filename:              # filename (for test data)
            try:
                return self.label[filename]
            except:
                return None
                #raise Exception("can't find file {} in label".format(filename))

#======================================================================================

# DEAL with output (called by Track()): list to sliced numpy arr
# input : list(begin, length), jz_or_not
# attr  : time length, msg length, log files, density, filename
# output: np.arr? -> x_data, y_data

# self.output, 1, x_train, y_train,
# MIDI_EVENT_COUNT, MIDI_SEGMENT,
# success, error, density(隔多遠拿一個音)(segment 的 heuristic)
# filename
def do_output(ori_data, jz_or_not, x_data, y_data, log_suc, log_err, log_fai, filename, track_number, event_min, event_max, segment, density):
    def end_time(i):
        return ori_data[i][0]# + ori_data[i][1]

    MSG_min = event_min

    # begin= ori_data[0][0]                   # [first][begin]
    end= ori_data[-1][0] + ori_data[-1][1]  # [last][begin + length]
    end_i = len(ori_data)

    good_seg_count=0    # 找到幾個好的 segment
    bad_seg_count=0     # 找到幾個不適合的 segment
    buffer = np.array([])
    mode = 'N'  # 還沒找到開頭, 'Y': 找到ㄖ
    heuri_len = 5

    try_i= 0    # msg
    try_begin=0 # time
    try_end=0   # time
    for i, m in enumerate(ori_data):   # index, msg(begin, length)
        if mode == 'N':         # 挑一個好的開頭
            if i < end_i-heuri_len:                                     # 還能跟下個比較
                if ori_data[i+heuri_len][0] - m[0] < density*heuri_len: # 密集的音樂事件
                    if end_i - i > MSG_min:                     # MSG長度
                        if end - m[0] > segment:      # 時間長度
                            try_i = i
                            try_begin = m[0]
                            try_end = try_begin + segment
                            mode = 'Y'
        elif mode == 'Y':
            if m[0] < try_end:
                continue
            else:   # 超過長度了! 查看目前字串
                if i - try_i > MSG_min and ori_data[i-1][0]-try_begin > segment - 100:
                    # MSG 數量合格 && 時間長度合格(上面的) && 整個 segment 最少要有 "segment-100" 長度的時間
                    if good_seg_count == 0:  # succ log
                        log_suc.log('{} - {}'.format(filename, track_number))
                    print('\t segment: {}'.format(good_seg_count+1 ))
                    log_suc.log('\tmsg: {:<4} [{:5}:{:5}] beat length: {:<7}'.format(
                                i-try_i, try_i, i, end_time(i-1) - try_begin))
                    # ----------------------------------------------------------------
                    seg_array = np.array(ori_data[try_i: i])
                    for e in range(len(seg_array)):     # 起點對齊
                        seg_array[e][0] -= try_begin
                    if i- try_i < event_max:
                        seg_array=np.pad(seg_array, ((0, event_max-len(seg_array)), (0, 0)), 'constant')
                    else:
                        seg_array=seg_array[:event_max]
                    # ----------------------------------------------------------------
                    buffer = np.append(buffer, seg_array)
                    good_seg_count += 1
                else:                       # 不好的 segment
                    if bad_seg_count == 0:
                        log_fai.log('{} - {}'.format(filename, track_number))
                    log_fai.log('\tmsg: {:<4} [{:5}:{:5}] beat length: {:<7}'.format(
                                i-try_i, try_i, i, end_time(i-1) - try_begin))
                    print("invalid segment")
                    bad_seg_count += 1
                mode = 'N'
    # ----------------------------------- end ----------------------------------------
    if good_seg_count == 0:
        if bad_seg_count == 0:
            print('No suitable segment: {}'.format(filename))
            log_err.log('No suitable segment(even 0 bad segment): {} - {}'.format(filename, track_number))
        else:
            print('No suitable segment: {}'.format(filename))
            log_err.log('No suitable segment( {} bad segment): {} - {}'.format(bad_seg_count, filename, track_number))
        return x_data, y_data, [0, bad_seg_count]

    else:               # 有找到 segment
        x_data = np.append(x_data, buffer)
        y_data = np.append(y_data, [jz_or_not]*good_seg_count)
        return x_data, y_data, [good_seg_count, bad_seg_count]


if __name__ == "__main__":
    pass