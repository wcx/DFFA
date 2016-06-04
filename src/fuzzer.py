#!/usr/bin/env python
# -*- coding: utf-8 -*
import random

import time
from bitstring import BitArray


def get_bits(length, mode=-1):
    """生成指定长度的位串.
        length -- 位串长度
        mode -- 0 返回全0
                1 返回全1
               -1 返回随机位串
    """
    # 生成指定长度的位串的最大值
    bits = BitArray(length)
    bits.set(1)
    bin_str = ''
    if mode == 0:
        bits.set(0)
        bin_str = '0b' + bits.bin
    elif mode == 1:
        bin_str = '0b' + bits.bin
    else:
        # print 'all_1_bit:bin:' + bits.bin
        print 'all_1_bit:uint:' + bits.uint.__str__()
        # 生成随机数，0到最大值
        random_num = random.randint(0, bits.uint)
        print 'random_num:' + random_num.__str__()
        bin_str = bin(random_num)
    # print 'created bit:' + bin_str[2:]

    return bin_str


def remove(bit_array):
    print '---------------remove----------------'
    print bit_array.len
    start = random.randint(0, bit_array.len)
    print 'start:' + start.__str__()
    end = random.randint(0, bit_array.len)
    print 'end:' + end.__str__()
    if start > end:
        tmp = start
        start = end
        end = tmp
        print 'start:' + start.__str__() + '   end:' + end.__str__()
    elif start == end:
        print 'start==end'
        remove(bit_array)
        return
    # print 'yua:' + bit_array.bin
    del bit_array[start:end]
    # print 'del:' + bit_array.bin
    print '---------------remove----------------'
    return bit_array


def add(bit_array):
    print '-----------add-------------'
    # print 'bit_array:' + bit_array.bin
    # 随机位置
    pos = random.randint(0, bit_array.len)
    # 随机长度的位串
    length = random.randint(1, bit_array.len)
    print 'random pos:' + pos.__str__()
    print 'random len:' + length.__str__()
    # 在随机的位置插入随机长度的随机位串
    bit_array.insert(get_bits(length), pos=pos)
    # print 'added bit_array:' + bit_array.bin
    print '-----------add-------------'
    return bit_array


def replace(bit_array, mode=-1):
    print '-----------change-------------'
    # print 'bit_array:' + bit_array.bin + '||len:' + bit_array.len.__str__()
    # 随机位置
    pos = random.randint(0, bit_array.len - 1)
    # 随机长度的位串
    length = random.randint(1, bit_array.len - pos)
    print 'random pos:' + pos.__str__()
    print 'random len:' + length.__str__()
    bit_array.overwrite(get_bits(length, mode), pos=pos)
    # print 'changed bit_array:' + bit_array.bin
    print '-----------change-------------'
    return bit_array


def replace_with_1(bit_array):
    print '---------replace_with_1---------'
    return replace(bit_array, mode=1)


def replace_with_0(bit_array):
    print 'replace_with_0'
    return replace(bit_array, mode=0)


def fuzz(**kwargs):
    # 变异算子
    operators = {0: remove, 1: add, 2: replace, 3: replace_with_1, 4: replace_with_0}
    if kwargs.get("seedfile", False):
        # 读入文件的二进制
        with open(kwargs["seedfile"], 'rb') as f:
            bit_array = BitArray(f)
        # 随机选取一种变异算子进行变异
        mutant_bit_array = operators.get(random.randint(0, operators.__len__() - 1))(bit_array)
        # 写入变异后的文件
        with open('test' + time.time().__str__() + '.png', 'wb') as output:
            print '生成' + output.name
            mutant_bit_array.tofile(output)
def test(**kwargs):
    operators = {0: remove, 1: add, 2: replace, 3: replace_with_1, 4: replace_with_0}
    if kwargs.get("seedfile", False):
        # 读入文件的二进制
        with open(kwargs["seedfile"], 'rb') as f:
            bit_array = BitArray(f)
        # 随机选取一种变异算子进行变异
        mutant_bit_array = operators.get(random.randint(0, operators.__len__() - 1))(bit_array)
        # 写入变异后的文件
        with open('test' + time.time().__str__() + '.png', 'wb') as output:
            print '生成' + output.name
            mutant_bit_array.tofile(output)

if __name__ == '__main__':
    fuzz(seedfile='Lenna.png')
    # bit_array = BitArray('0b11')
    # bit_array.overwrite('0b1',pos=1)
    # remove(bit_array)
    # add(bit_array)
