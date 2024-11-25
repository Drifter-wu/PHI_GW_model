#!/usr/bin/env python
# coding: utf-8

#Codes by Shucheng Yang


import os
import sys

def main():
    try:
        cmd  = sys.argv[1]       #输入运行文件

        try:
            core = int(sys.argv[2]) #使用核数，单一计算节点最多40
        except IndexError:
            print("DEFAULT CORE VALUE USED!")
            core = 10

        try:
            queue = sys.argv[3]    #使用节点名称
        except IndexError:
            print("DEFAULT QUEUE USED!")
            queue = "GW"

        with open("job.s", 'w') as f:
            print('#BSUB -J %s'%(input("PLEASE INPUT JOB NAME:")), file = f)                  #作业名称
            print('#BSUB -q %s'%queue, file = f)                    #节点名(GW, astron, sastron, gold, gold2)
            print('#BSUB -o %J.out', file = f)                      #结果输出
            print('#BSUB -e %J.err', file = f)                      #报错输出
            print('#BSUB -n %d'%core, file = f)                     #节点核数
            print('#BSUB -R span[ptile=%d]'%core, file = f)         #每个计算单位核数
            print('~/anaconda3/envs/igwn-py39/bin/python %s/%s'%(os.getcwd(), cmd), file = f) #运行指令


        print("JOB.S SET!")


        ifrun = input("SUBMIT JOB.S?(Y/N)")

        if ifrun == "Y" or ifrun == "y":
            os.system("bsub<job.s")
            os.system("bjobs")
        else:
            print("EXIT!")

    except IndexError:
        print("PLEASE INPUT CMD!!!")

if __name__ == '__main__':
    main()

