import hashlib
import math
from bee.osql.logger import Logger


class BloomFilter:
    """
    Bloom Filter.布隆过滤器
    <B>since  1.6.2</B>
    """

    __size = 0

    def __init__(self, expected_size: int, false_positive_rate: float, hash_count: int):
        """
        初始化布隆过滤器
        :param expected_size: 预期元素数量
        :param false_positive_rate: 最大误判率
        :param hash_count: 哈希函数个数
        """
        self.bit_size = int(-expected_size * math.log(false_positive_rate) / (math.log(2) ** 2))
        self.hash_count = hash_count

        needInterBitMap = False
        try:
            from bitarray import bitarray
            self.bit_set = bitarray(self.bit_size)
            self.bit_set.setall(0)  # 初始化为全0
        except ImportError:
            Logger.info("If you want to use bitarray in BloomFilter, can install it first!")
            needInterBitMap = True

        if needInterBitMap:
            from bee.typing import Bitmap
            self.bit_set = Bitmap(self.bit_size)

    def add(self, s: str) -> None:
        """
        向布隆过滤器中添加元素
        :param s: 待添加的字符串
        """
        if s is None:
            return
        BloomFilter.__size = BloomFilter.__size + 1
        hashes = self._get_hashes(s)
        for h in hashes:
            index = abs(h % self.bit_size)
            self.bit_set[index] = 1

    def contains(self, s: str) -> bool:
        """
        判断元素是否可能存在于布隆过滤器中
        :param s: 待判断的字符串
        :return: True（可能存在）或 False（一定不存在）
        """
        if s is None:
            return False
        hashes = self._get_hashes(s)
        for h in hashes:
            index = abs(h % self.bit_size)
            if not self.bit_set[index]:
                return False
        return True

    def size(self) -> int:
        return BloomFilter.__size

    # -> list[int]里，list[int]  py3.8有报错
    def _get_hashes(self, s: str):
        """
        生成哈希值数组（模拟Java的hashCode和MD5逻辑）
        :param s: 输入字符串
        :return: 哈希值列表
        """
        hashes = []
        data = s.encode('utf-8')

        # 哈希1：模拟Java的hashCode（取绝对值后取模）
        h_code = hash(s)
        h_code = h_code if h_code >= 0 else -h_code
        hashes.append(h_code % self.bit_size)

        # 哈希2和3：基于MD5的前后4字节
        try:
            md5_hash = hashlib.md5(data).digest()
            # 前4字节
            hashes.append(self._bytes_to_int(md5_hash, 0))
            # 后4字节（如果MD5不足8字节，则复用前4字节）
            if len(md5_hash) >= 8:
                hashes.append(self._bytes_to_int(md5_hash, 4))
            else:
                hashes.append(hashes[1])
        except Exception:
            # print(f"MD5生成异常: {e}")
            # 如果MD5失败，复用第一个哈希值
            hashes.extend([hashes[0]] * (self.hash_count - 1))

        # 确保返回的哈希值数量与hash_count一致
        return hashes[:self.hash_count]

    @staticmethod
    def _bytes_to_int(bytes_data: bytes, start: int) -> int:
        """
        将字节数组转换为整数（取4字节）
        :param bytes_data: 字节数组
        :param start: 起始位置
        :return: 转换后的整数
        """
        result = 0
        for i in range(4):
            result <<= 8
            result |= bytes_data[start + i] & 0xFF
        return result

