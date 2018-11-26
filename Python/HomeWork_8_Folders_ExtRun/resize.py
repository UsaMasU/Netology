import os
import subprocess

resize_program = 'convert.exe '
resize_param = ' -resize 200 '

current_dir = os.path.dirname(os.path.abspath(__file__))

source_dir =  current_dir + '\\'+'Source' + '\\'
result_dir =  current_dir +'\\'+'Result' + '\\'

if __name__ == '__main__':
    try:
        os.mkdir(result_dir)
    except FileExistsError:
        pass
    finally:
        pass
        for root, dirs, files in os.walk(source_dir):
            for filename in files:
                if filename.endswith('.jpg'):
                    resize_cmd_str = resize_program + source_dir + filename + resize_param + result_dir + filename
                    print(resize_cmd_str)
                    subprocess.run(resize_cmd_str, shell=True)