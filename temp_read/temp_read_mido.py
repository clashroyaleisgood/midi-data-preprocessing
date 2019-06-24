import os
from mido import MidiFile
from temp_read.midi_analysis import Track, File, do_output
from support.contant import MIDI_EVENT_MAX, MIDI_EVENT_MIN, MIDI_SEGMENT, SEGMENT_DENSITY
dir_path = os.path.dirname(os.path.realpath(__file__))
class Log():
    def log(self, s):
        pass
    pass

a= Log()
constants={'event_min': MIDI_EVENT_MIN, 'event_max': MIDI_EVENT_MAX, \
          'segment': MIDI_SEGMENT, 'density': SEGMENT_DENSITY}
logs={'log_err': a, 'log_suc': a, 'log_fai': a}
files = File("123", a)

jz_or_not = False
file_name = "Xian_Xinghai_midi-sq-by_Ong_Cmu_-_The_Yellow_River_Piano_Concerto_act-1.mid"
x_train, y_train = [], []
with MidiFile(dir_path + '\\' + file_name) as mf:
    tk = Track(mf.ticks_per_beat//24)
    print('unit: ', tk.unit)
    track_number= files.select_track(midifile=mf)
    if track_number:
        print('select track to', track_number)
        track = mf.tracks[track_number]
    else:
        input('something wrong')

    for i, e in enumerate(track):
        tk.event_process(e)
    tk.left_event()
    tk.to_sort_list()

    if tk.valid_output():
        x_train, y_train, seg_count = do_output( \
            ori_data=tk.output, jz_or_not=jz_or_not, x_data=x_train, y_data=y_train, filename=file_name, track_number=track_number, **logs, **constants)
        #segment_count += seg_count[0]
        #broken_segment_count += seg_count[1]
    else:
        print('\t\tERROR_LENGTH/TIME at: {}'.format(file_name))
x_train = x_train.reshape(-1, MIDI_EVENT_MAX, 2)      # 這樣就不用 s_train 了
a=0