from bee.name.bloom import BloomFilter
from bee.typing import Bitmap, LongArray, Array


if __name__ == '__main__':
    
    print("------test Array-------start")
    keys=Array(10)
    
    keys[1]="select * from orders"
    keys[5]="select * from orders5"
    print(keys[1])
    print(keys[5])
    print(keys)
    
    print("------test Array-------end")
    
    
    print("------test LongArray-------start")
    long_array = LongArray(10)
    long_array[6] = 9223372036854775807
    print(long_array[6])
    binary_str = bin(long_array[6])
    print(binary_str)
    print(long_array)
    
    bit_index=100
    array_index = bit_index // 64
    bit_offset = bit_index % 64
    print(array_index)
    print(bit_offset)
    
    long_array[array_index] |= (1 << bit_offset)
    
    binary_str = bin(long_array[array_index])
    print(binary_str)
    print(long_array)
    
    print("------test LongArray-------end")


# 测试代码
if __name__ == "__main__":
    
    print("------test BloomFilter-------start")
    
    bf = BloomFilter(expected_size=1000, false_positive_rate=0.01, hash_count=3)

    # 添加元素
    bf.add("hello")
    bf.add("world")

    # 检查元素
    print(bf.contains("hello"))  # True
    print(bf.contains("world"))  # True
    print(bf.contains("python"))  # False（可能误判，但概率很低）

    print("------test BloomFilter-------end")

# 使用示例
if __name__ == "__main__":
    
    print("------test Bitmap-------start")
    
    # 创建一个 100 位的位图（需要 2 个 64 位整数存储）
    bitmap = Bitmap(100)

    # 通过下标设置第 5 位为 1
    bitmap[5] = 1

    # 检查第 5 位是否为 1
    if bitmap[5]:
        print("Bit 5 is set")  # 输出: Bit 5 is set

    # 设置第 5 位为 0
    bitmap[5] = 0

    # 检查第 5 位是否为 0
    if not bitmap[5]:
        print("Bit 5 is cleared")  # 输出: Bit 5 is cleared
        
        
        
    bitmap[99] = 1

    # 检查第 99 位是否为 1
    if bitmap[99]:
        print("Bit 99 is set")  # 输出: Bit 99 is set

    # 设置第 99 位为 0
    bitmap[99] = 0

    # 检查第 99 位是否为 0
    if not bitmap[99]:
        print("Bit 99 is cleared")  # 输出: Bit 99 is cleared
    
    
    bitmap = Bitmap(100)  

    # 设置第 5 位为 1  
    bitmap.set_bit(5)  
    print(bitmap.is_bit_set(5))  # 输出: True  

    # 获取第 5 位的值  
    print(bitmap.get_bit(5))  # 

    bitmap.set_bit(99)
    bitmap.set_bit(2)

    print(bitmap.is_bit_set(2))
    print(bitmap.is_bit_set(99))
    print(bitmap.is_bit_set(10))
    
    print("------test Bitmap-------end")