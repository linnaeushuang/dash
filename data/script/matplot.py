import matplotlib.pyplot as plt
import os
LOG_FILE_PATH='./../logFile'
oldIndex=6
estIndex=8
nodexIndex=2
timeIndex=0
logFiles=os.listdir(LOG_FILE_PATH)
for logFile in logFiles:
    nodeNum=int(logFile[3])
    oldBitRate=[[] for i in range(nodeNum)]
    estBitRate=[[] for i in range(nodeNum)]
    time=[[] for i in range(nodeNum)]
    with open(LOG_FILE_PATH+'/'+logFile,'rb') as f:
        index=0
        for line in f:
            par=line.split()
            index=int(par[nodexIndex])
            oldBitRate[index].append(float(par[oldIndex])/1000)
            estBitRate[index].append(float(par[estIndex])/1000)
            time[index].append(float(par[timeIndex]))
    oldPlotList=[]
    estPlotList=[]
    for i in range(nodeNum):
        oldPlotList.append(plt.plot(time[i],oldBitRate[i]))
    plt.xlabel('time(s)')
    plt.ylabel('oldbitRate(kbps)')
    plt.legend(oldBitRate,labels=['node:'+str(c) for c in range(nodeNum)],loc='best')
    plt.savefig('old'+logFile[3:-4]+'.png')
    plt.close()
    for i in range(nodeNum):
        estPlotList.append(plt.plot(time[i],estBitRate[i]))
    plt.xlabel('time(s)')
    plt.ylabel('estbitRate(kbps)')
    plt.legend(estBitRate,labels=['node:'+str(c) for c in range(nodeNum)],loc='best')
    plt.savefig('est'+logFile[3:-4]+'.png')
    plt.close()

