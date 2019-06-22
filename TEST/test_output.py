'''
資料夾配置
├── support/
│   ├─── midi_analysis.py   #與 train data 的 midi_analysis.py 略有不同 -> 完全相同
│   └─── do_log.py
├─── data/
│   ├─── test_jazz/
│   │    ├─── jazz-1.mid
│   │    └─── jazz-2.mid
│   ├─── test_non_jazz/
│   │    ├─── non-jazz-1.mid
│   │    └─── non-jazz-2.misd
│   ├─── jazz_label.txt
│   └─── non_jazz_label.txt
└── output_midi.py
'''
from mido import MidiFile
from support.midi_analysis import Track, File, do_output
from support.do_log import Log
import numpy as np
import os
import time
dir_path = os.path.dirname(os.path.realpath(__file__))

MIDI_EVENT_MAX = 200
MIDI_EVENT_MIN = 40
MIDI_SEGMENT = 500      # 單位: 1/24 拍(beat)
SEGMENT_DENSITY = 10
constants={'event_min': MIDI_EVENT_MIN, 'event_max': MIDI_EVENT_MAX, \
          'segment': MIDI_SEGMENT, 'density': SEGMENT_DENSITY}

x_test = []                            # 儲存所有的 midi 資料 (numpy array)
y_test = []                            # 答案
segment_count = 0                       # 總共幾個分段
broken_segment_count = 0                # 取到不好的分段

error = Log(dir_path + '\\', "error_log.txt")
success = Log(dir_path + '\\', "success_log.txt")
fail = Log(dir_path + '\\', "fail_log.txt")
logs={'log_err': error, 'log_suc': success, 'log_fai': fail}

test = {
    'jazz': ('\\data\\test_jazz\\', 1, '\\data\\jazz_label.txt'),
    'nonjazz': ('\\data\\test_non_jazz\\', 0, '\\data\\non_jazz_label.txt')
}

to_process = input("which to process? J/N/A...>")
if to_process == 'J':
    to_process = [test['jazz']]
elif to_process == 'N':
    to_process = [test['nonjazz']]
else:
    to_process = test.values()
now = time.time()
#=========================================== READ JAZZ/NONJAZZ MIDI ============================================

for data_folder, jz_or_not, label_txt in to_process:
    files = File(dir_path + data_folder, error_log=error)    # 輸入 midi 所在地的資料夾/ log file name
    files.read_label_file(dir_path + label_txt) # 讀取 label.txt
    files.read_file_names()                 # 進入資料夾 尋找所有 midi 檔
    print(files)

    for mf, file_name in files.read_all_file():        # mf = MidiFile(file_place)
        print('{:04}: {:12}'.format(segment_count, file_name))

        tk = Track(segment=MIDI_SEGMENT, unit_size=mf.ticks_per_beat//24)       # 輸入最小單位的大小 (tick)

        track_number = files.select_track(filename=file_name)

        if track_number:
            track = mf.tracks[track_number]         #select track
        else:
            continue

        for i, e in enumerate(track):
            tk.event_process(e)
        tk.left_event()
        tk.to_sort_list()
        '''
        if tk.valid_output():
            x_test = np.append(x_test, tk.output_process(MIDI_EVENT_MAX))
            y_test = np.append(y_test, jz_or_not)
            s_test += 1
            success.log('msg: {:<5} beat length: {:<7} song: {}'.format(len(tk.output), tk.beat_length, file_name))
        else:
            print('\t\tERROR_{:<8} at: {}'.format('LENGTH', file_name))
            error.log('LENGTH ERROR: {} {}'.format(len(tk.output), file_name))
        '''
        if tk.valid_output():
            x_test, y_test, seg_count = do_output( \
                ori_data=tk.output, jz_or_not=jz_or_not, x_data=x_test, y_data=y_test, filename=file_name, track_number=track_number, **logs, **constants)
            segment_count += seg_count[0]
            broken_segment_count += seg_count[1]
        else:
            print('\t\tERROR_LENGTH/TIME at: {}'.format(file_name))
            error.log('LENGTH ERROR: {} {}'.format(len(tk.output), file_name))
#           succ-> new x_test, fail-> old x_test

# end processing midi
print('end processing midi: ', time.time()-now)
now = time.time()
#=============================================== END ===================================================

x_test = x_test.reshape(-1, MIDI_EVENT_MAX, 2)      # 這樣就不用 s_train 了
np.savez(dir_path + '\\newtest.npz', x_test = x_test, y_test = y_test)
print('we got {} segments, {} bad segments'.format(segment_count, broken_segment_count))
success.log('we got {} segments, {} bad segments'.format(segment_count, broken_segment_count))
print('end processing npz: ', time.time()-now)