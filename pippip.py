"""
coding: utf-8
@Software: PyCharm
@Time:  11:24
@Author: Fake77
@Module Name: pippip
"""
import os
import json
import argparse
import time
from urllib import request

"""
name: pippip
Create By Tuzi - 04.06.2024
-------------------------------------
File Struct
|
|---|- pippip.py
    |- config.json

Fill the config to add or remove the src links.

-------------------------------------

Smart to switch src for pip. ez to use
[1] - python pippip.py              switch to the best src.
[2] - python pippip.py --reset      switch to the org src.

-------------------------------------
"""


# utils function
# -------------------------------------
def print_format(msg: str, info: str) -> None:
    """
    Rich text print.
    :param msg: msg
    :param info: mode
    :return: None
    """
    mapping = {
        # white
        "i": "[i] \033[34m{}\033[0m",
        # yellow
        "w": "[!] \033[33m{}\033[0m",
        # red
        "e": "[-] \033[31m{}\033[0m",
        # green
        "s": "[+] \033[32m{}\033[0m",
    }
    print(mapping[info].format(msg))


def count_time(func):
    """
    Time counter
    :param func:
    :return: time(ns), result
    """

    def arg_recv(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        return int(round((end - start) * 1000)), ret

    return arg_recv


def get_header():
    ret = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/125.0.0.0 Safari/537.36"
    }
    return ret


def banner():
    ban = """
 _______   __            _______   __           
/       \ /  |          /       \ /  |          
$$$$$$$  |$$/   ______  $$$$$$$  |$$/   ______  
$$ |__$$ |/  | /      \ $$ |__$$ |/  | /      \ 
$$    $$/ $$ |/$$$$$$  |$$    $$/ $$ |/$$$$$$  |
$$$$$$$/  $$ |$$ |  $$ |$$$$$$$/  $$ |$$ |  $$ |
$$ |      $$ |$$ |__$$ |$$ |      $$ |$$ |__$$ |
$$ |      $$ |$$    $$/ $$ |      $$ |$$    $$/ 
$$/       $$/ $$$$$$$/  $$/       $$/ $$$$$$$/  
              $$ |                    $$ |      
              $$ |                    $$ |      
              $$/                     $$/       
    """
    print(ban)
    print("Create by Tuzi.")


# global usage
# -------------------------------------
# 当前路径
__current_path = os.getcwd()

# 配置文件路径
__config_path = os.path.join(__current_path, "config.json")

__url_timeout = 5


# Imp
# -------------------------------------
def load_config() -> dict:
    """
    Load Config
    :return:  dict
    """
    with open(__config_path, "r", encoding="utf-8") as fp:
        ret = json.load(fp)
    return ret


@count_time
def probe(url: str) -> int:
    """
    Check Src available
    :param url:
    :return:
    """
    try:
        req = request.Request(url, headers=get_header())
        resp = request.urlopen(req, timeout=__url_timeout)

    except Exception as _:
        return -1
    return resp.getcode()


def main():
    """
    Start work
    :return: None
    """
    try:
        config = load_config()
        _url_packs = config["Src"]
        _timeout = config["TIMEOUT"]
    except Exception as _:
        print_format(f"Load Fail at {__config_path}\r\n\treason: {_}", "e")
        return

    print_format(f"Load config at {__config_path}", "i")
    print_format(f"Src list length: {len(_url_packs)}", "i")
    print_format("Src List:", "i")
    # 默认官方源
    _best_url_name = "Org"
    _best_url = "https://pypi.python.org/simple"
    _min_time = 10000

    # 探测源速度和可用性
    for name, url in _url_packs:
        # print(url)
        tm_ms, state_code = probe(url)
        if state_code != -1:
            print_format(f"[{state_code}][{tm_ms} ms] {name}: {url}", "i")
        else:
            print_format(f"[N/A] {name}: {url}", "w")
        if tm_ms < _min_time and state_code != -1:
            _min_time = tm_ms
            _best_url = url
            _best_url_name = name
    print_format(f"Best src switch: {_best_url_name}: {_best_url}", "s")
    ret_set_url = os.popen(f"pip config set global.index-url {_best_url}")
    ret_set_timeout = os.popen(f"pip config set global.timeout {_timeout}")
    print_format(ret_set_url.read(), "i")
    print_format(ret_set_timeout.read(), "i")
    ret_pip_config_lst = os.popen("pip config list").readlines()
    [print_format(line, "s") for line in ret_pip_config_lst]
    print_format("Done!", "s")


if __name__ == "__main__":
    banner()
    parse = argparse.ArgumentParser(description="Smart change Src for pip. create by Tuzi")
    parse.add_argument('--reset', help="Rollback to Org Src.", action="store_true")
    _args = parse.parse_args()
    if _args.reset:
        reset_url = os.popen(f"pip config set global.index-url https://pypi.python.org/simple/")
        print_format(reset_url.read(), "i")
        reset_pip_config_lst = os.popen("pip config list").readlines()
        [print_format(line, "s") for line in reset_pip_config_lst]
        print_format("Done!", "s")
    else:
        main()
