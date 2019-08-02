import os
import math
import sys


'''
this code for varBandWidth
'''
def outputFI(SAMPLE_START=50,SAMPLE_END=150):
    realPath=os.path.realpath(__file__)[:-5]
    #print(realPath)
    docName=[realPath+'bb',realPath+'mpc',realPath+'mpcfast',realPath+'pensieve']
    K=len([name for name in os.listdir(docName[3]) if name[:3]=='log'])
    #print(K)
    bandwidthFile=realPath+[norway for norway in os.listdir(realPath) if norway[:6]=='norway'][0]
    FairIndex=[]
    EfficiencyIndex=[]
    StabilityIndex=[]
    sampleTimeList=[]
    sampleBitrateList=[]
    
    
    FILE_NAME_LIST=[]
    # FILE_NAME_LIST[0] is bb,[1] is mpc..
    for doc in docName:
        FILE_NAME_LIST.append(sorted([name for name in os.listdir(doc) if name[:3]=='log']))
    
    TIME=[[[] for k in FILE_NAME_LIST[i]] for i in range(len(docName))]
    BITRATE=[[[] for k in FILE_NAME_LIST[i]] for i in range(len(docName))]
    SAMPLE_BITRATE=[[[] for k in FILE_NAME_LIST[i]] for i in range(len(docName))]
    SAMPLE_TIME=[[[] for k in FILE_NAME_LIST[i]] for i in range(len(docName))]
    SAMPLE_BANDWIDTH=[]

    BANDWIDTH=[]
    BANDWIDTH_TIME=[]
    timeIndex=0
    while True:
        with open(bandwidthFile,'rb') as f:
            for line in f:
                par=line.split()
                BANDWIDTH_TIME.append(float(par[0])+timeIndex)
                BANDWIDTH.append(float(par[1])*K*1000000)
        if BANDWIDTH_TIME[-1] > SAMPLE_END:
            break
        timeIndex+=BANDWIDTH_TIME[-1]
    
    
    for docindex,docname in enumerate(docName):
        for fileindex,filename in enumerate(FILE_NAME_LIST[docindex]):
            with open(docname+'/'+filename,'rb') as f:
                for line in f:
                    par=line.split()
                    TIME[docindex][fileindex].append(float(par[0]))
                    BITRATE[docindex][fileindex].append(int(par[1]))
    
    
    countBand=0
    for index in range(len(BANDWIDTH)):
        if BANDWIDTH_TIME[index]>=SAMPLE_START and BANDWIDTH_TIME[index]<=SAMPLE_END:
            timelen=int(BANDWIDTH_TIME[index]-SAMPLE_START-countBand)
            for i in range(timelen):
                SAMPLE_BANDWIDTH.append(BANDWIDTH[index])
                countBand+=1
            if BANDWIDTH_TIME[index+1]>SAMPLE_END:
                endlen=SAMPLE_END-countBand-SAMPLE_START
                for i in range(endlen):
                    SAMPLE_BANDWIDTH.append(BANDWIDTH[index+1])
                    countBand+=1
    
    for docindex in range(len(BITRATE)):
        for fileindex in range(len(BITRATE[docindex])):
            count=0
            for segBitrateIndex in range(len(BITRATE[docindex][fileindex])):
                if TIME[docindex][fileindex][segBitrateIndex]>=SAMPLE_START and TIME[docindex][fileindex][segBitrateIndex]<=SAMPLE_END:
                    timelen=int(TIME[docindex][fileindex][segBitrateIndex]-SAMPLE_START-count)
                    for i in range(timelen):
                        SAMPLE_TIME[docindex][fileindex].append(SAMPLE_START+count)
                        #SAMPLE_TIME[docindex][fileindex].append(TIME[docindex][fileindex][segBitrateIndex])
                        SAMPLE_BITRATE[docindex][fileindex].append(BITRATE[docindex][fileindex][segBitrateIndex])
                        count+=1
                    if TIME[docindex][fileindex][segBitrateIndex+1]>SAMPLE_END:
                        endlen=SAMPLE_END-count-SAMPLE_START
                        for i in range(endlen):
                            SAMPLE_TIME[docindex][fileindex].append(SAMPLE_START+count)
                            SAMPLE_BITRATE[docindex][fileindex].append(BITRATE[docindex][fileindex][segBitrateIndex+1])
                            count+=1
    
    
    
    averageAllSampleRateList=[]
    for docindex in range(len(SAMPLE_BITRATE)):
        averageAllSampleRate=0
        for fileindex in range(len(SAMPLE_BITRATE[docindex])):
            averageAllSampleRate+=sum(SAMPLE_BITRATE[docindex][fileindex])
        averageAllSampleRateList.append(averageAllSampleRate/((SAMPLE_END-SAMPLE_START)*K))
    
    
    for docindex in range(len(docName)):
        l=[]
        for sampleIndex in range(SAMPLE_END-SAMPLE_START):
            sumvar=0
            nave=0
            for fileIndex in range(K):
                sumvar+=(SAMPLE_BITRATE[docindex][fileIndex][sampleIndex]-averageAllSampleRateList[docindex])**2/K
                nave+=SAMPLE_BITRATE[docindex][fileIndex][sampleIndex]/K
            sumvar=math.sqrt(sumvar)
            l.append(sumvar/nave)
        FairIndex.append(sum(l)/(SAMPLE_END-SAMPLE_START))
    
    #print("infairness: low is good")
    #print(FairIndex)
    
    for docindex in range(len(docName)):
        l=[]
        for sampleIndex in range(SAMPLE_END-SAMPLE_START):
            sumb_x_t=0
            for fileindex in range(K):
                sumb_x_t+=SAMPLE_BITRATE[docindex][fileindex][sampleIndex]
            sumb_x_t=abs(sumb_x_t-SAMPLE_BANDWIDTH[sampleIndex])/SAMPLE_BANDWIDTH[sampleIndex]
            l.append(sumb_x_t)
        EfficiencyIndex.append(sum(l)/(SAMPLE_END-SAMPLE_START))
    
    #print("inefficiency: low is good")
    #print(EfficiencyIndex)
    
    
    for docindex in range(len(docName)):
        l=[]
        sum_bit_w=[]
        for sampleIndex in range(SAMPLE_END-SAMPLE_START-1):
            sumv=0
            # it maybe error
            w=sampleIndex+1.0
            sumb=0
            for fileindex in range(K):
                sumv+=abs((SAMPLE_BITRATE[docindex][fileindex][sampleIndex+1]-SAMPLE_BITRATE[docindex][fileindex][sampleIndex]))*w
                sumb+=SAMPLE_BITRATE[docindex][fileindex][sampleIndex+1]*w
            l.append(sumv)
            sum_bit_w.append(sumb)
        StabilityIndex.append(sum(l)/sum(sum_bit_w))
    
    #print("instability: low is good")
    #print(StabilityIndex)
    
    
    with open(realPath+'index.txt','wb') as f:
        f.write(str(FairIndex[0])+" "+str(FairIndex[1])+" "+str(FairIndex[2])+" "+str(FairIndex[3])+"\n")
        f.write(str(EfficiencyIndex[0])+" "+str(EfficiencyIndex[1])+" "+str(EfficiencyIndex[2])+" "+str(EfficiencyIndex[3])+"\n")
        f.write(str(StabilityIndex[0])+" "+str(StabilityIndex[1])+" "+str(StabilityIndex[2])+" "+str(StabilityIndex[3])+"\n")

if __name__ == '__main__' :
    samplestart=int(sys.argv[1])
    sampleend=int(sys.argv[2])
    #bandwidth=float(sys.argv[3])
    #outputFI(samplestart,sampleend,bandwidth)
    outputFI(samplestart,sampleend)


    
    
    
