#!/usr/bin/env python
# -*- coding: utf-8 -*
import random
import time
from bitstring import BitArray
import os
import copy
from utils import utils


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
        # print 'all_1_bit:uint:' + bits.uint.__str__()
        # 生成随机数，0到最大值
        random_num = random.randint(0, bits.uint)
        # print 'random_num:' + random_num.__str__()
        bin_str = bin(random_num)
    # print 'created bit:' + bin_str[2:]

    return bin_str


def remove(bit_array):
    print '---------------remove----------------'
    # print bit_array.len
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
    return bit_array, start, end


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
    return bit_array, pos, pos + length


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
    return bit_array, pos, pos + length


def replace_with_1(bit_array):
    print '---------replace_with_1---------'
    return replace(bit_array, mode=1)


def replace_with_0(bit_array):
    print 'replace_with_0'
    return replace(bit_array, mode=0)


def fuzz(**kwargs):
    # 变异算子
    operators = {0: remove, 1: add, 2: replace, 3: replace_with_1, 4: replace_with_0}
    if kwargs.get('seedfile', False):
        # 读入文件的二进制
        with open(kwargs['seedfile'], 'rb') as f:
            bit_array = BitArray(f)
        format = 'png'
        job_num = kwargs.get('job_num', 0) + 1
        job_case_num = kwargs.get('job_case_num', 0) + 1
        custom_path = kwargs.get('custom_path', '../res/mutants')
        for i in range(1, job_num):
            output_path = custom_path + '/' + format + '/' + i.__str__()
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            with open(custom_path + '/' + format + '/log.txt', 'a') as log:
                log.write("***************job" + i.__str__() + "***************")
                log.write('\n')

            for j in range(1, job_case_num):
                # 随机选取一种变异算子进行变异
                tmp = copy.deepcopy(bit_array)
                print '**************************************************************************'
                print 'job' + i.__str__() + '---第' + j.__str__() + '次'
                print '变异前:' + tmp.len.__str__()
                mutant_bit_array, start, end = operators.get(random.randint(0, operators.__len__() - 1))(tmp)
                print '变异后:' + mutant_bit_array.len.__str__()
                # 写入变异后的文件
                output_file = 'test' + i.__str__() + '-' + j.__str__() + '.' + format
                with open(output_path + '/' + output_file, 'wb') as output:
                    print '生成' + output.name
                    mutant_bit_array.tofile(output)
                with open(custom_path + '/' + format + '/log.txt', 'a') as log:
                    log.write(output_file + '|' + start.__str__() + '|' + end.__str__() + '|')
                    log.write('\n')
                print '**************************************************************************'


if __name__ == '__main__':
    # for i in range(0, 10):
    begintime = time.time()

    fuzz(seedfile='../res/seeds/Lenna.png', job_num=50, job_case_num=3000,
         custom_path='/media/wcx/Ubuntu 14.0/ResearchData')
    print begintime
    print time.time()
    # bit_array = BitArray('0b11')
    # bit_array.overwrite('0b1',pos=1)
    # remove(bit_array)
    # add(bit_array)
