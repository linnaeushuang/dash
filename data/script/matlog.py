
# this code should put in the path same of logfile

import matplotlib.pyplot as plt
import os


def matLog():
    realPath=os.path.realpath(__file__)[:-9]
    logList=sorted([logname for logname in os.listdir(realPath) if logname[:3]=='log'])
    nodeList=['node'+str(i) for i in range(len(logList))]
    Time=[[] for i in range(len(logList))]
    BitRate=[[] for i in range(len(logList))]
    Buffer=[[] for i in range(len(logList))]
    Rebuffer=[[] for i in range(len(logList))]
    ChunkSize=[[] for i in range(len(logList))]
    lastDownloadTime=[[] for i in range(len(logList))]
    reward=[[] for i in range(len(logList))]
    # reward also is qoe
    print(logList)

    for fileindex,filename in enumerate(logList):
        with open(realPath+filename,'rb') as f:
            for line in f:
                par=line.split()
                Time[fileindex].append(float(par[0]))
                BitRate[fileindex].append(float(par[1]))
                Buffer[fileindex].append(float(par[2]))
                Rebuffer[fileindex].append(float(par[3]))
                ChunkSize[fileindex].append(float(par[4]))
                lastDownloadTime[fileindex].append(float(par[5]))
                reward[fileindex].append(float(par[6]))

    
    for b in range(len(Buffer)):
        p,=plt.plot(Time[b],Buffer[b],label=nodeList[b])
    plt.title('buffer')
    plt.legend(loc='best')
    plt.savefig("buffer.png")
    plt.close()

    for b in range(len(BitRate)):
        p,=plt.plot(Time[b],BitRate[b],label=nodeList[b])
    plt.title('BitRate')
    plt.legend(loc='best')
    plt.savefig("BitRate.png")
    plt.close()

    for b in range(len(reward)):
        p,=plt.plot(Time[b],reward[b],label=nodeList[b])
    plt.title('qoe')
    plt.legend(loc='best')
    plt.savefig("qoe.png")
    plt.close()





if __name__ == '__main__' :
    matLog()
