# midi-data-preprocessing
preprocess midi data for machine learning

## TRAIN / TEST folder
execute train_output.py / test_output.py to output formated data  
NOTE: it will create 3 txt files (error.txt, success.txt, fail.txt) for logging

### in TRAIN/
```
├── support/
│   ├─── midi_analysis.py
│   └─── do_log.py
├─── data/
│   ├─── train_jazz/
│   │    ├─── jazz-1.mid
│   │    └─── jazz-2.mid
│   └─── train_non_jazz/
│        ├─── non-jazz-1.mid
│        └─── non-jazz-2.misd
└── train_output.py
```
### in TEST/
```
├── support/
│   ├─── midi_analysis.py
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
└── test_output.py
```
