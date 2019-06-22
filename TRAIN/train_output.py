from mido import MidiFile
from support.midi_analysis import Track, File, do_output
from support.theme import select_theme
from support.do_log import Log
import numpy as np
import os
import time
dir_path = os.path.dirname(os.path.realpath(__file__))
COUNT_TIME = True

MIDI_EVENT_MAX = 200
MIDI_EVENT_MIN = 40
MIDI_SEGMENT = 500      # 單位: 1/24 拍(beat)
SEGMENT_DENSITY = 10    # 單位: 單位時間/event
constants={'event_min': MIDI_EVENT_MIN, 'event_max': MIDI_EVENT_MAX, \
          'segment': MIDI_SEGMENT, 'density': SEGMENT_DENSITY}
x_train = []                            # 儲存所有的 midi 資料 (numpy array)
y_train = []                            # 答案
segment_count = 0                       # 總共幾個分段
broken_segment_count = 0                # 取到不好的分段

error = Log(dir_path + '\\', "error_log.txt")
success = Log(dir_path + '\\', "success_log.txt")
fail = Log(dir_path + '\\', "fail_log.txt")
logs={'log_err': error, 'log_suc': success, 'log_fai': fail}
train = {
    'jazz': ('\\data\\train_jazz\\', 1),
    'nonjazz': ('\\data\\train_non_jazz\\', 0)
}

to_process = input("which to process? J/N/A...>")
if to_process == 'J':
    to_process = [train['jazz']]
elif to_process == 'N':
    to_process = [train['nonjazz']]
else:
    to_process = train.values()
now = time.time()
#=========================================== READ JAZZ/NON-JAZZ MIDI ============================================

timer= Log(dir_path + '\\', 'timer.txt')
for data_folder, jz_or_not in to_process:
    files = File(dir_path + data_folder, error_log=error)    # 輸入 midi 所在地的資料夾/ log file name
    files.read_file_names()                 # 進入資料夾 尋找所有 midi 檔
    print(files)
    if COUNT_TIME:
        temp = time.time()
    for mf, file_name in files.read_all_file():        # mf = MidiFile(file_place)
        print('{:04}: {:12}'.format(segment_count, file_name))

        if COUNT_TIME:
            timer.log('open: {:<6.5}'.format(time.time()-temp), end=' -  ')
            temp = time.time()

        tk = Track(segment=MIDI_SEGMENT, unit_size=mf.ticks_per_beat//24)       # 輸入最小單位的大小 (tick)

        if COUNT_TIME:
            temp = time.time()
        
        track_number = files.select_track(mf)
        if track_number:
            track = mf.tracks[track_number]         #select track
        else:
            if COUNT_TIME:
                timer.log('')
            continue

        if COUNT_TIME:
            timer.log('sele: {:<6.5}'.format(time.time()-temp), end=' -  ')
            temp = time.time()

        for i, e in enumerate(track):
            tk.event_process(e)
        tk.left_event()
        tk.to_sort_list()

        '''
# ---------------------
        if tk.valid_output():
            x_train = np.append(x_train, tk.output_process(MIDI_EVENT_MAX))
            y_train = np.append(y_train, jz_or_not)
            s_train += 1
            success.log('msg: {:<5} beat length: {:<7} song: {}'.format(len(tk.output), tk.beat_length, file_name))
        else:
            print('\t\tERROR_{:<8} at: {}'.format('LENGTH', file_name))
            error.log('LENGTH ERROR: {} {}'.format(len(tk.output), file_name))
        '''
# ---------------------
        if tk.valid_output():
            x_train, y_train, seg_count = do_output( \
                ori_data=tk.output, jz_or_not=jz_or_not, x_data=x_train, y_data=y_train, filename=file_name, track_number=track_number, **logs, **constants)
            segment_count += seg_count[0]
            broken_segment_count += seg_count[1]
        else:
            print('\t\tERROR_LENGTH/TIME at: {}'.format(file_name))
            error.log('LENGTH ERROR: {} {}'.format(len(tk.output), file_name))
        if COUNT_TIME:
            timer.log('proc: {:<6.5}'.format(time.time()-temp))
            temp = time.time()
#           succ-> new x_train, fail-> old x_train

# end processing midi
print('end processing midi: ', time.time()-now)
now = time.time()
#=============================================== END ===================================================

x_train = x_train.reshape(-1, MIDI_EVENT_MAX, 2)      # 這樣就不用 s_train 了
np.savez(dir_path + '\\newtrain.npz', x_train = x_train, y_train = y_train)
print('we got {} segments, {} bad segments'.format(segment_count, broken_segment_count))
success.log('we got {} segments, {} bad segments'.format(segment_count, broken_segment_count))
print('end processing npz: ', time.time()-now)