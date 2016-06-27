#!/usr/bin/env python
# -*- coding: utf-8 -*
import copy
import os
import random

from bitstring import BitArray

from src.utils import conf
from src.utils.utils import log_runtime, mkdirs


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
    print 'start:' + str(start)
    end = random.randint(0, bit_array.len)
    print 'end:' + str(end)
    if start > end:
        tmp = start
        start = end
        end = tmp
        print 'start:' + str(start) + '   end:' + str(end)
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
    print 'random pos:' + str(pos)
    print 'random len:' + str(length)
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
    print 'random pos:' + str(pos)
    print 'random len:' + str(length)
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


@log_runtime
def fuzz_file(**kwargs):
    # 变异算子
    operators = {0: remove, 1: add, 2: replace, 3: replace_with_1, 4: replace_with_0}
    if kwargs.get('seedfile', False):
        # 读入文件的二进制
        with open(kwargs['seedfile'], 'rb') as f:
            bit_array = BitArray(f)

        format = 'png'
        job_num = kwargs.get('job_num', 0) + 1
        job_case_num = kwargs.get('job_case_num', 0) + 1
        custom_path = kwargs.get('custom_path', conf.MUTANTS_PATH)

        for i in range(1, job_num):
            output_path = custom_path + '/' + format + '/' + str(i)
            log_path = custom_path + '/' + format + '/' + 'logs/'
            mkdirs(output_path)
            mkdirs(log_path)
            log_file = log_path + 'log-' + str(i) + '.txt'
            with open(log_file, 'a') as log:
                log.write("***************job" + str(i) + "***************")
                log.write('\n')

            for j in range(1, job_case_num):
                # 随机选取一种变异算子进行变异
                tmp = copy.deepcopy(bit_array)
                print '**************************************************************************'
                print 'job' + str(i) + '---第' + str(j) + '次'
                print '变异前:' + str(tmp.len)
                mutant_bit_array, start, end = operators.get(random.randint(0, operators.__len__() - 1))(tmp)
                print '变异后:' + str(mutant_bit_array.len)
                # 写入变异后的文件
                output_file = 'test' + str(i) + '-' + str(j) + '.' + format
                with open(output_path + '/' + output_file, 'wb') as output:
                    print '生成' + output.name
                    mutant_bit_array.tofile(output)
                with open(log_file, 'a') as log:
                    log.write(output_file + '|' + str(start) + '|' + str(end) + '|')
                    log.write('\n')
                print '**************************************************************************'


if __name__ == '__main__':
    fuzz_file(seedfile='../res/seeds/Lenna.png', job_num=10, job_case_num=3)
