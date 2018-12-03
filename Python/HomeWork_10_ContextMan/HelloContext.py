import subprocess
import time

class WorkTimer:
    time_start = 0
    time_finish = 0
    time_work = 0

    def __init__(self, name):
        self.time_start = 0
        self.time_finish = 0
        self.time_work = 0
        self.name = name

    def __enter__(self):
        self.time_start = time.time()
        time_in_format = time.strftime("%H.%M.%S", time.localtime())  # "%Y-%m-%d-%H.%M.%S"
        print(self.name, ': Start operation time: ', time_in_format, sep='')


    def __exit__(self, time_start, time_finish, time_work):
        self.time_finish = time.time()
        time_in_format = time.strftime("%H.%M.%S", time.localtime())  # "%Y-%m-%d-%H.%M.%S"
        print(self.name, ': Finish operation time: ', time_in_format, sep='')
        self.time_work = self.time_finish - self.time_start
        print(self.name, ': Operation lasts: {:.{prec}f} sec'.format(self.time_work, prec = 3), sep = '')

if __name__ == '__main__':
    print('Check network connection to domain.')
    print('Enter domain name for check or "q" to exit')
    while(True):
        str_proc = ['ping', '']
        str_proc[1] = input('\nInput domain name: ')
        if str_proc[1] == 'q':
            print('Exit')
            break
        run_proc = (' ').join(str_proc)
        CheckConTimer = WorkTimer(str_proc[1])

        with CheckConTimer as CheckConn:
            subprocess.call(run_proc, shell=False, stdout=0)

        if CheckConTimer.time_work > 5.0:
            print('-'*10, 'Bad connection', '-'*10)
        elif CheckConTimer.time_work < 5.0:
            print('-'*10, 'Normal connection', '-'*10)
        elif CheckConTimer.time_work < 0.02:
            print('-'*10, 'No connection', '-'*10)

