import hashlib
import os
import time

from bee.osql.logger import Logger


def currentMilliseconds():
    # print(time.time()) 浮点数,精度通常为微秒级
    return int(time.time() * 1000)


def string_to_md5(text):
    # 创建 MD5 哈希对象
    md5_hash = hashlib.md5()

    # 更新哈希对象，需要将字符串编码为字节
    md5_hash.update(text.encode('utf-8'))

    # 获取十六进制格式的哈希值
    return md5_hash.hexdigest()


def write_to_file(file_path: str, file_name:str, content: str) -> None:
    """将字符串内容写入到指定文件中。

    Args:
        file_path (str): 文件的完整路径
        file_name (str)：文件名
        content (str): 要写入文件的字符串内容
    """
    try:
        path_and_name = os.path.join(file_path, file_name)  # 工程根目录下
        with open(path_and_name, 'w') as file:  # 以写入模式打开文件
            file.write(content)  # 写入内容
        Logger.info(f"write successful. {path_and_name}")
    except Exception as e:
        Logger.warn(f"write error: {e}")
