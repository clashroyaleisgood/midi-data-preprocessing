import os
from mido import MidiFile
from midi_analysis import Track, File
dir_path = os.path.dirname(os.path.realpath(__file__))
class Log():
    pass

a= Log()
files = File("123", a)
with MidiFile(dir_path + '\\that_lucky_old_sun_tk.mid') as mf:
    tk = Track(mf.ticks_per_beat//24)
    print('unit: ', tk.unit)
    track = mf.tracks[files.select_track(midifile=mf) ]
    for i, e in enumerate(track):
        tk.event_process(e, i, True)
    tk.left_event()
    tk.to_sort_list()
    b= tk.output_process(5000)
    a=0