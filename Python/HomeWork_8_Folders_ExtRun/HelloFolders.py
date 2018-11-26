import os
import subprocess

external_program = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

search_files_list = []
find_str_files_list = []
search_count = 0
migrations = 'Migrations'
current_dir = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    print('Запускаем браузер и ждем завершение его работы...')
    subprocess.run(external_program, shell=False)
    print('Продолжаем работу\n')

    for root, dirs, files in os.walk(current_dir +'\\'+ migrations):
        for filename in files:
            if filename.endswith('.sql'):
                search_files_list.append(filename)

    cycle_search_files_list = search_files_list[:]
    while(True):
        search_count = 0
        find_str_files_list.clear()
        search_str = input('Введите строку для пойска:')
        for onefile in cycle_search_files_list:
            with open(current_dir +'\\'+ migrations + '\\' + onefile, encoding='utf-8') as file:
                for line in file:
                    if search_str in line:
                        find_str_files_list.append(onefile)
                        search_count += 1
                        #print(search_count, ') ', '-' * 10, onefile, '-' * 10)
                        #print(line)
                        break
        for num, file in enumerate(find_str_files_list):
            print(num + 1, ') ', file, sep='')
        print('\nНайденных файлов:', search_count)
        cycle_search_files_list = find_str_files_list[:]

