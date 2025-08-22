import array

from bee.osql.logger import Logger


class String:
    '''
    String type.
    '''

    def __init__(self, length):
        self.len = length


class Array:
    '''
    Array type.
    '''

    __array:None
    __size = 0

    def __init__(self, size:int):
        self.__size = size
        self.__array = [None] * size

    def __setitem__(self, index:int, v:str):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return
        self.__array[index] = v

    def __getitem__(self, index):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return None
        return self.__array[index]

    def __str__(self):
        # print(type(self.__array))   #<class 'list'>
        return "array len:" + str(len(self.__array)) + ", value:" + str(self.__array)


class LongArray:
    '''
    unsigned Long Array type.
    unsigned long 64 bit.
    '''

    __array:None
    __size = 0

    def __init__(self, size:int):
        self.__size = size
        self.__array = array.array("Q", [0] * size)  # unsigned Long  64 bit

    def __setitem__(self, index:int, v):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return
        self.__array[index] = v

    def __getitem__(self, index):
        if index >= self.__size:
            Logger.warn("Error index: " + str(index))
            return None
        return self.__array[index]

    def __str__(self):
        return "array len:" + str(len(self.__array)) + ", value:" + str(self.__array)


class Bitmap:
    '''
    Bitmap type base LongArray.
    <br><B>since  1.6.2</B>
    '''

    def __init__(self, num_bits: int):
        """
        Initialize a bitmap, using LongArray as the underlying storage.
        :param num_bits: The total number of bits in a bitmap.
        """
        self.__num_bits = num_bits
        self.__long_array = LongArray((num_bits + 63) // 64)  # 计算需要的 64 位整数个数

    def __setitem__(self, bit_index: int, value: int) -> None:
        """
        通过下标设置指定位的值（0 或 1）。
        :param bit_index: 位的索引（从 0 开始）。
        :param value: 0 或 1。
        """
        if bit_index < 0 or bit_index >= self.__num_bits:
            raise IndexError(f"Bit index {bit_index} out of bounds (size: {self.__num_bits})")
        if value not in (0, 1):
            raise ValueError("Value must be 0 or 1")

        array_index = bit_index // 64
        bit_offset = bit_index % 64
        if value == 1:
            self.__long_array[array_index] |= (1 << bit_offset)  # 设置位为 1
        else:
            self.__long_array[array_index] &= ~(1 << bit_offset)  # 设置位为 0

    def __getitem__(self, bit_index: int) -> int:
        """
        通过下标获取指定位的值（0 或 1）。
        :param bit_index: 位的索引（从 0 开始）。
        :return: 0 或 1。
        """
        return self.get_bit(bit_index)

    def set_bit(self, bit_index: int) -> None:
        """
        将指定位设置为 1。
        :param bit_index: 位的索引（从 0 开始）。
        """
        if bit_index < 0 or bit_index >= self.__num_bits:
            raise IndexError(f"Bit index {bit_index} out of bounds (size: {self.__num_bits})")
        array_index = bit_index // 64
        bit_offset = bit_index % 64
        current_value = self.__long_array[array_index]
        self.__long_array[array_index] = current_value | (1 << bit_offset)

    def clear_bit(self, bit_index: int) -> None:
        """
        将指定位设置为 0。
        :param bit_index: 位的索引（从 0 开始）。
        """
        if bit_index < 0 or bit_index >= self.__num_bits:
            raise IndexError(f"Bit index {bit_index} out of bounds (size: {self.__num_bits})")
        array_index = bit_index // 64
        bit_offset = bit_index % 64
        current_value = self.__long_array[array_index]
        self.__long_array[array_index] = current_value & ~(1 << bit_offset)

    def get_bit(self, bit_index: int) -> int:
        """
        获取指定位的值（0 或 1）。
        :param bit_index: 位的索引（从 0 开始）。
        :return: 0 或 1。
        """
        if bit_index < 0 or bit_index >= self.__num_bits:
            raise IndexError(f"Bit index {bit_index} out of bounds (size: {self.__num_bits})")
        array_index = bit_index // 64
        bit_offset = bit_index % 64

        # binary_str = bin(self.__long_array[array_index])
        # print(binary_str)

        return (self.__long_array[array_index] >> bit_offset) & 1

    def is_bit_set(self, bit_index: int) -> bool:
        """
        判断指定位是否为 1。
        :param bit_index: 位的索引（从 0 开始）。
        :return: True（1）或 False（0）。
        """
        return self.get_bit(bit_index) == 1

    def __len__(self) -> int:
        """
        返回位图的总位数。
        """
        return self.__num_bits

    def __str__(self):
        return f"Bitmap(num_bits={self.__num_bits}, data={self.__long_array})"

