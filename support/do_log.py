from os.path import isfile
class Log:
    def __init__(self, dirpath, log_file_name):
        mode = 'w'
        if isfile(dirpath + log_file_name):
            mode = input("exist file {}, cover or append? (w/a)...>".format(log_file_name))
            while mode != 'a' and mode != 'w':
                print("invalid way:", mode)
                mode = input("exist file {}, cover or append? (w/a)...>".format(log_file_name))
        else:
            print("create file", dirpath + log_file_name)
        print("log at", dirpath + log_file_name)
        
        self.dirpath = dirpath
        self.log_name= log_file_name

        self.file = open(dirpath + log_file_name, mode)

    def log(self, msg, end='\n'):
        self.file.write(msg + end)

    def __del__(self):
        print("file {} closed".format(self.log_name))
        self.file.close()

if __name__ == "__main__":
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
    
    error = Log(dir_path, "error_log.txt")
    error.log("happy", end=" ")
    error.log("birth")
    print()