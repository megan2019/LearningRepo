# -*- coding: utf-8 -*-
import os
from lxml import etree
import csv
import pickle
import time
import sys
import datetime
firstRun = False
errorCount = 0
# 如果没有数据，创建 header
logger = open(sys.path[0] + '/solverlog.log', 'a+', encoding='utf_8_sig')
if not os.path.exists(sys.path[0] + '/result'):
    os.makedirs(sys.path[0] + '/result')
    firstRun = True
head = ['分类号', '申请人', '发明人', '申请号', '申请日', '发明名称', '申请国家',
        '邮编', '联系地址', '国家/省市', '专利公开号', '主分类号', '公开/公告日', '法律状态']
csvDst = []
year = 1995
while year<= 2018:
    f = open(sys.path[0] + '/result/%d.csv' % year, 'a+', newline='', encoding='utf_8_sig')
    tempwriter = csv.writer(f, dialect='excel')
    if firstRun == True:
        tempwriter.writerow(head)
    csvDst.append(tempwriter)
    year = year + 1

def toCSV(out_txt):
    global errorCount
    thisErrorCount1 = 0
    thisErrorCount2 = 0
    out_str = str(out_txt)
    a = []
    b = []
    c = []
    d = []
    e = []
    f = []
    g = []
    h = []
    i = []
    j = []
    k = []
    l = []
    m = []
    n = []
    xcontent = etree.HTML(out_str)
    num1 = 1   
    while num1 < 101:
        strnum = str(num1)
        tempk = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[1]/td[2]/text()') 
        tempa = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[10]/td[2]/text()')
        tempb = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[3]/td[2]/text()')
        tempc = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[4]/td[2]/text()')
        tempd = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[1]/td[2]/a/text()')
        tempe = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[7]/td[2]/text()')
        tempf = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[2]/td[2]/text()')
        tempg = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[8]/td[2]/text()')
        temph = xcontent.xpath( '//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[12]/td[1]/text()')
        temphh = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[12]/td[2]/text()')
        # 舍弃垃圾数据
        if (len(temph) == 0 or len(temphh) == 0) and len(tempa) != 0:
            errorCount = errorCount + 1
            print('!!! 警告：数据异常，已舍弃当前异常数据。目前已累计异常数据 %d 条。' % errorCount)
            logger.write(datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + ': !!! 警告：数据异常，已舍弃当前异常数据。目前已累计异常数据 %d 条。\n' % errorCount)
            logger.flush()
            num1 = num1 + 1
            continue
        if not len(tempk) == 0:
            if temph[0][0] == "邮":
                h.append(temphh[0][0:-1])
                tempnn = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[13]/td[2]/text()')
                if len(tempnn) == 0:
                    n.append('N/A')
                    thisErrorCount1 = thisErrorCount1 + 1
                    
                else:
                    n.append(tempnn[0])
            else:
                thisErrorCount2 = thisErrorCount2 + 1
                
                h.append('N/A')
                n.append(temphh[0])
        tempi = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[5]/td[2]/text()')
        tempj = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[11]/td[2]/text()')
        
        tempm = xcontent.xpath('//*[@id="tab"]/tbody/tr[' + strnum + ']/td/table/tbody/tr[6]/td[2]/text()')
        if not len(tempk) == 0:
            templ = list(filter(lambda x: x, tempa[0].split(';')))[0]
            m.append(tempm[0][0:-1])
            l.append(templ)
            j.append(tempj[0][0:-1])
            i.append(tempi[0][0:-1])
            g.append(tempg[0][0:-1])
            f.append(tempf[0][0:-1])
            e.append(tempe[0][0:-1])
            d.append(tempd[0][0:-1])
            c.append(tempc[0][0:-1])
            b.append(tempb[0][0:-1])
            a.append(tempa[0][0:-1])
            k.append(list(filter(lambda x: x, tempk[0].split(' ')))[1])
        num1 = num1+1
    label = zip(a, b, c, d, e, f, g, h, i, j, k, l, m, n)    
    w=0
    for v in label:
        stry = list(v)[4][0:4]
        inty = int(stry)
        csv_write=csvDst[inty-1995]
        csv_write.writerow(v)
        w = w + 1
    if thisErrorCount1 != 0 :
        print("  ! 提示：出现法律信息缺失的不完整数据 %d 条，已经用 N/A 代替。" % thisErrorCount1)
        logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                     ":   ! 提示：出现法律信息缺失的不完整数据 %d 条，已经用 N/A 代替。\n" % thisErrorCount1)
        logger.flush()
    if thisErrorCount2 != 0:
        print("  ! 提示：出现邮政编码缺失的不完整数据 %d 条，已经用 N/A 代替。" % thisErrorCount2)
        logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                     ":   ! 提示：出现邮政编码缺失的不完整数据 %d 条，已经用 N/A 代替。\n" % thisErrorCount2)
        logger.flush()
    return w

starttime = time.time()

pickleList = []
pickleList = os.listdir(sys.path[0] + '/output')
for a in pickleList:
    if a[0] == '.':
        pickleList.remove(a)
totalPickles = 0
totalCount = 0
totalPickles = len(pickleList)
pickleList.sort()
print( "即将开始解析数据...")
logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": 即将开始解析数据...\n")
logger.flush()
print("output 文件夹下共有 %d 条 pickle 待解析。" % totalPickles)
logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
             ": output 文件夹下共有 %d 条 pickle 待解析。\n" % totalPickles)
logger.flush()
startIndex = int(input('请输入开始 index：'))
endIndex = int(input('请输入结束 index：'))
for onePickle in pickleList[startIndex:endIndex]:
    timepicklestart = time.time()
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": 正在解析 [%d]: " % pickleList.index(onePickle) +
            onePickle + "...(%d/%d)" % (pickleList.index(onePickle) - startIndex + 1, endIndex - startIndex))
    logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": 正在解析 [%d]: " % pickleList.index(onePickle) +
                 onePickle + "...(%d/%d)\n" % (pickleList.index(onePickle) - startIndex + 1, endIndex - startIndex))
    logger.flush()
    with open(sys.path[0] + '/output/' + onePickle, 'rb') as f:
        source = pickle.load(f)
    thisCount = toCSV(source)
    totalCount = thisCount + totalCount
    timepickleend = time.time()
    print("本条解析用时 %.2fs，共解析 %d 条数据，累计已解析 %d 条数据。" % ((timepickleend - timepicklestart), thisCount, totalCount))
    logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
                 ": 本条解析用时 %.2fs，共解析 %d 条数据，累计已解析 %d 条数据。\n" % ((timepickleend - timepicklestart), thisCount, totalCount))
    logger.flush()
endtime = time.time()
print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": %d 条 pickles 解析完成，耗时 %.2fmin" % (endIndex - startIndex, (endtime - starttime) / 60.0))
logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": %d 条 pickles 解析完成，耗时 %.2fmin\n" % (endIndex - startIndex, (endtime - starttime) / 60.0))
logger.flush()
print('共解析 %d 条数据，有 %d 条异常数据已被丢弃。' % (totalCount, errorCount))
logger.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': 共解析 %d 条数据，有 %d 条异常数据已被丢弃。\n' % (totalCount, errorCount))
logger.flush()
