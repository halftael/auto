import re
import os

def SequenceGet(f1):
       # 提取gb文件中序列并拼接，参数为预处理数据
       f2 = [i for i in f1 if i[0].isdigit()]
       f3 = []
       for j in f2:
              for i in range(10):
                     j = j.replace(str(i), '')
              f3.append(j.replace(' ', ''))
       sequence = ''.join(f3)
       return sequence

def ColDic(f1,sequence):
       # 提取各figure描述，并从完整序列中比对出特征序列，返回一组键值对
       # 所需参数是 预处理数据 完整序列

       # 获得特征序列描述
       s = []
       l = []
       for i,j in enumerate(f1):
              if re.findall('t[0-9]+-[0-9]+\s(A|D)',j)  :
                     s.append(f1[i-1])
                     l.append(j)
              if 'label=HL' in j or 'label=HR' in j:
                     s.append(f1[i-1])
                     l.append(j)
       # 比对出特征序列
       sa = []
       for i in s:
              start,end = re.findall('[0-9]+',i)
              if 'complement' not in i:
                     sa.append(sequence[int(start):int(end)+1])
              else:                                            # HR需求出其互补序列
                     p = sequence[int(start):int(end)+1]
                     p = p.replace('a','1').replace('t','2').replace('c','3').replace('g','4')
                     p = p.replace('1','t').replace('2','a').replace('3','g').replace('4','c')
                     sa.append(p)

       # Label数据进行简单清洗
       la = []
       for i in l:
              p = i.replace('/label=','')
              la.append(p)

       # 键值对生成
       coldic = {}
       for j,k in zip(la,sa):
              coldic[j] = k

       return coldic

def PathGet(folder):
       # 处理的全部文件路径
       paths = []
       names = os.listdir(folder)
       for name in names:
              path = os.path.join(folder, name)  #os.path.join 拼接路径/文件名
              paths.append(path)
       return names,paths




def datapool(folder):
       # 生成数据池
       datapool = []

       names,paths = PathGet(folder)   #需要填写的文件夹路径

       for name,path in zip(names,paths):
              with open(path,'r') as gb:


                     #数据预处理
                     fl = gb.readlines()
                     pre = [i.strip() for i in fl]

                     # 拼接出完整序列
                     sequence = SequenceGet(pre)

                     # 生成特征序列键值对
                     coldic = ColDic(pre,sequence)

                     #生成间隔为逗号的字符串
                     m = []
                     for j,k in coldic.items():
                           m.append(j)
                           m.append(k)
                     m.insert(0,name)
                     m = ','.join(m)
                     datapool.append(m)

       return datapool



def write(datapool,output):
       # 逐行写入csv文件
       if 'output.csv' not in os.listdir(output):
              with open('output.csv','w') as otp:
                     for i in datapool:
                            otp.writelines(i+'\n')
              print('write down')
       else:
              print('Have written')



def main():
       folder = input('输入目录:')
       output = input('输出目录:')
       write(datapool(folder),output)

       a = input('如需再次执行，请输入again;按enter键可以退出程序\n')
       if a == 'again':
              main()
       return 0


main()