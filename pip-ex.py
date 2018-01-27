# -*- coding:utf-8 -*-
import os, pip
import shutil
from os.path import expanduser
import errno
import platform
import pip
import time

home = expanduser("~")

pip_config_dir = os.path.join(home, ".pip")
if "windows" in platform.platform().lower() :
    pip_config_dir = os.path.join(home, "pip")

pip_config_file = os.path.join(pip_config_dir, "pip.ini")


testing_pkg = "pandas" # 找了好几个pkg， 这个的大小在10MB 比较合适测试

template = """
[global]
index-url = %(url)s
[install]
trusted-host=%(host)s
"""


source_list = {
    "aliyun": {
        "name" : u"阿里云",
        "url" : "https://mirrors.aliyun.com/pypi/simple",
        "host" : "mirrors.aliyun.com"
    },
    "tsinghua" : {
        "name" : "清华",
        "url" : "https://pypi.tuna.tsinghua.edu.cn/simple",
        "host" : "pypi.tuna.tsinghua.edu.cn"
    },
    "ustc": {
        "name" : u"中科大",
        "url" : "https://pypi.mirrors.ustc.edu.cn/simple/",
        "host" : "pypi.mirrors.ustc.edu.cn"
    }
}


def speed_test(target) :
    """
    对目标源进行速度测试
    :param target: 
    :return: 
    """
    change(target)
    download_pkg = os.path.join(pip_config_dir, "mysql-connector-2.1.6.tar.gz")
    if os.path.exists(download_pkg) :
        os.remove(download_pkg)
    cache_dir = os.path.join(pip_config_dir, "cache")
    mkdir_p(cache_dir)
    shutil.rmtree(cache_dir)
    pip.main(["download", testing_pkg, "--cache-dir", cache_dir , "-d", pip_config_dir])


def recommend() :
    """
    根据当前网络， 自动测试各个源的下载速度。 
    推荐速度最快的
    :return: 
    """
    pass
    import pip


def reset() :
    """
    清楚当前的设定。 即： 删除配置文件
    :return: 
    """
    if os.path.exists(pip_config_file) :
        os.remove(pip_config_file)

def change(target) :
    """
    修改当前的pip的源
    :param target:
    :return:
    """
    data = source_list[target]
    file_content = template % data
    mkdir_p(pip_config_dir)
    with open(pip_config_file, "w") as fobj :
        fobj.write(file_content)

def list(region = None) :
    """
    列出有哪些备选的pip源.
    可以根据region 进行过滤
    :param region:  国家或者地区。 目前这个参数无用，目前主要是国内源
    :return:
    """
    for key in source_list :
        print key , source_list[key]['name']


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass


if __name__ == '__main__':
    # mkdir_p(pip_config_dir)
    # print os.path.exists(pip_config_dir)
    # list()
    # reset()
    speed_test("aliyun")