from operator import attrgetter
### 印出所有的midi訊息

########類別，為了接下來要存track的編號和多音重複的數量#########
def select_theme(mid):
    class Select_Track:
        def __init__(self, track_num__, more_than_one__, note_count__):
            self.track_num__ = track_num__
            self.more_than_one__ = more_than_one__
            self.note_count__ = note_count__

    select_track_num = 5 ##要選出的音軌的數目

    select_track = [] ##建立等等要存track的陣列##
    main_melody = 0
    basic_note_count=10
    for i, track in enumerate(mid.tracks):
        note_count=0
        pro_change_count=0
        pro_change_to = 0
        more_than_one = 0
        #print('Track {}: {}'.format(i, track.name))
        for j in range(len(mid.tracks[i])):
            if mid.tracks[i][j].type == 'note_on' and mid.tracks[i][j].velocity != 0 :
                end_j = 0
                for k in range(j,len(mid.tracks[i])):
                    if (mid.tracks[i][k].type == 'note_off' and mid.tracks[i][k].note == mid.tracks[i][j].note) or (mid.tracks[i][k].type == 'note_on' and mid.tracks[i][k].note == mid.tracks[i][j].note and mid.tracks[i][k].velocity == 0):
                        end_j = k
                        break
                    ##找到一個音現持續的區間##
                for k in range(j, end_j):
                    if mid.tracks[i][k].type== 'note_on' and mid.tracks[i][k].note != mid.tracks[i][j].note and mid.tracks[i][j].velocity!=0 and mid.tracks[i][k].velocity !=0 :
                        more_than_one += 1
                    ##看看那個區間裡是否有其他音也在（即兩個音重疊）##
            if mid.tracks[i][j].type == 'note_on' or mid.tracks[i][j].type == 'note_off' :
                note_count+=1
            if mid.tracks[i][j].type == 'program_change' and pro_change_to != track[j].program:
                pro_change_count+=1
                pro_change_to = track[j].program

        if note_count>=basic_note_count and pro_change_count<=5:
            select_track.append(Select_Track(i, more_than_one, note_count)) ##把這些重疊的數量和track的編號加到剛剛的class裡面##
            #print("note_count:",note_count)
        #print("***********")
        #print(more_than_one)

    #for i in range(len(select_track)):
        #print(select_track[i].track_num__," 重疊音->", select_track[i].more_than_one__)

    sorted_select_track = sorted(select_track,reverse = False, key = attrgetter('more_than_one__'))###排序，重疊音最少的往前擺###

    #print("sorted:")

    #for i in range(len(sorted_select_track)):
        #print(sorted_select_track[i].track_num__, sorted_select_track[i].more_than_one__)

    selected_three_track = []
    if len(select_track) < 1:
        #print("音軌數量過少。")
        return None
    else:
        for i in range(min(select_track_num, len(select_track))):
            selected_three_track.append(sorted_select_track[i].track_num__)
            ##print(selected_three_track)
        min_jump_count=2147483647
        main_melody = 0
        for i in range(len(selected_three_track)):
            note_num=0
            ###print('Track {}: {}'.format(i, track.name))
            #print("###",selected_three_track[i])
            note_sum = 0  
            note_list = []
            for j in range(len(mid.tracks[selected_three_track[i]])):
                if mid.tracks[selected_three_track[i]][j].type == 'note_on' or mid.tracks[selected_three_track[i]][j].type == 'note_off':
                    note_num+=1
                    note_sum += mid.tracks[selected_three_track[i]][j].note
                    note_list.append(mid.tracks[selected_three_track[i]][j].note)
            ##print(sorted_select_track[i].note_count__, " is ", note_num)
            note_avg=0
            if sorted_select_track[i].note_count__!=0:
                note_avg = note_sum/sorted_select_track[i].note_count__ 

        ###print(note_avg)
            jump_count=0
            for j in range (len(note_list)-1):
                if note_list[j] < note_avg and note_list[j+1]>note_avg:
                    jump_count+=1
            #print("跳躍的音：",jump_count)
            if jump_count < min_jump_count and jump_count!=0:
                min_jump_count = jump_count
                main_melody = selected_three_track[i]

    #print('***')
    #print( "theme:", main_melody)
    return main_melody

def select_max_len(mid):
    select_first=[]     # 單純的 track
    for index, track in enumerate(mid.tracks):
        program_change_count=0
        program_change_to=0
        for j in range(min(60, len(track))):
            if track[j].type == 'program_change' and track[j].program != program_change_to:
                program_change_to = track[j].program
                program_change_count += 1
        if program_change_count < 3:
            select_first+=[index]

    if len(select_first) > 0:
        track_len = [len(mid.tracks[e]) for e in select_first]
        return select_first[track_len.index(max(track_len))]
    else:
        return None

if __name__ == "__main__":
    import os
    from os import walk
    from do_log import Log
    from mido import MidiFile
    dir_path = os.path.dirname(os.path.realpath(__file__))

    logging = Log(dir_path+'\\' ,  'log.txt')
    
    for root, dirs, files in walk(dir_path+'\\data'):
        print("\n路徑：", root)
        print("  目錄：", dirs)
        print("  檔案：", files)
        for file_name in files:
            fail = 0
            while fail < 3:
                try:
                    with MidiFile(dir_path +'\\data\\'+ file_name) as mf:
                        track_num = select_max_len(mf)
                        if track_num != None:
                            logging.log('select '+ str(track_num) +'  at  ' + file_name)
                            print('success: {} -> {}'.format(track_num, file_name))
                        else:
                            logging.log('CAN\'T select track (None) ' + file_name)
                            print('fail       -> {}'.format(file_name))
                        fail = 3
                except:
                    print('fail open: '+dir_path +'\\data\\'+ file_name)
                    fail += 1
                    #這裡是讀檔錯誤 不用理他
    
####錯誤的原因是因為那時候要把note_count直接記下來，之後就不用再重新算一次
####但後來發現排序的時候沒有排到那個儲存note_count的陣列
####所以在計算平均音高的時候，每個音軌除總音符數的都不是自己的總音符數
####現在我把他加到最上面的那個class裡面當作是一個成員，這樣他在排序的時候就會跟著一起排了然後要用的時候再取出來即可