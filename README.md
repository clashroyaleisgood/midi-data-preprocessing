# midi-data-preprocessing
preprocess midi data for machine learning

## how to execution
~~execute train_output.py / test_output.py to output formated data~~  
New: execute train_output, test_output by main indirectly  
NOTE: it will create 3 txt files (error.txt, success.txt, fail.txt) for logging (in TEST/ or TRAIN/ )

### in /
```
├─── main.py
├─── support/
│   ├─── midi_analysis.py
│   ├─── do_log.py
│   └─── theme.py
├─── TRAIN/
└─── TEST/
```
### in TRAIN/
```
├─── data/
│   ├─── train_jazz/
│   │    ├─── jazz-1.mid
│   │    └─── jazz-2.mid
│   └─── train_non_jazz/
│        ├─── non-jazz-1.mid
│        └─── non-jazz-2.misd
└─── train_output.py
```
### in TEST/
```
├─── data/
│   ├─── test_jazz/
│   │    ├─── jazz-1.mid
│   │    └─── jazz-2.mid
│   ├─── test_non_jazz/
│   │    ├─── non-jazz-1.mid
│   │    └─── non-jazz-2.misd
│   ├─── jazz_label.txt
│   └─── non_jazz_label.txt
└─── test_output.py
```
