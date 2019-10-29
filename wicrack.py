import sys
import os
import subprocess
import re


def get_conf():
    conf = open("wicrack.conf", "r")
    conf_str = ""
    for l in conf.readlines():
        conf_str += l
    return conf_str


def get_files(root_dir):
    file_map = {}
    for root, dirs, files in os.walk(root_dir):
        for _file in files:
            file = os.path.join(root, _file)
            size = os.path.getsize(file)
            file_map.setdefault(file, size)
    _file_map = sorted(file_map.items(), key=lambda x: x[1], reverse=False)
    return list(dict(_file_map).keys())


def crack():
    for dic_name in dic_names:
        for cap_name in cap_names:
            #判断字典是否已使用过
            if str(dic_name + "-----" + cap_name) in get_conf():
                continue

            cmd = "aircrack-ng -w " + "\'" + dic_name + "\'" + " " + "\'" + cap_name + "\'"
            print("\n" + "-"*len(cmd))
            print(cmd)
            print("-"*len(cmd))
            popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            while popen.poll() is None:
                result = str(popen.stdout.read(3000))
                #显示进度
                if "%" in result:
                    progress = result[result.index("%") - 6: result.index("%") + 1]
                    print(progress.strip(), end="\r")
                #破解成功
                if "KEY FOUND!" in result:
                    print("--------------KEY FOUND!--------------")
                    result = result[result.index("KEY FOUND!"):]
                    print("KEY:" + result[result.index("[") + 1: result.index("]")].strip())
                    print("--------------------------------------")

                    conf_file.write("--------------KEY FOUND!--------------\n")
                    conf_file.write(dic_name + "-----" + cap_name + "\n")
                    conf_file.write("KEY:" + result[result.index("[") + 1: result.index("]")].strip() + "\n")
                    conf_file.write("--------------------------------------\n")
                    conf_file.flush()

                    while True:
                        inp = input("continue? Y/n\n")
                        if inp is "" or inp is "Y" or inp is "y":
                            break
                        elif inp is "n" or inp is "N":
                            return
            #
            conf_file.write(dic_name + "-----" + cap_name + "\n")
            conf_file.flush()


if len(sys.argv) != 3:
    print("argv error")
    print("usage wicrack dic_root_dir or dic_file cap_root_dir or cap_file")
    exit();
dic = sys.argv[1]
cap = sys.argv[2]

if os.path.isfile(dic):
    dic_names = [dic]
else:
    dic_names = get_files(dic)

if os.path.isfile(cap):
    cap_names = [cap]
else:
    cap_names = get_files(cap)

conf_path = "wicrack.conf"
conf_file = open("wicrack.conf", "a")

crack()

