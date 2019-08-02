import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import numpy as np
#import matplotlib.pyplot as plt
import sys
import multiprocessing as mp
from Maddpg import Sakuro
import torch


BATCH_SIZE=50
S_LEN = 3  # take how many frames in the past
S_INFO=6
A_DIM = 6
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
BUFFER_NORM_FACTOR = 10.0
CHUNK_TIL_VIDEO_END_CAP = 48
M_IN_K = 1000.0
REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
SMOOTH_PENALTY = 1
DEFAULT_QUALITY = 0  # default video quality without agent
RANDOM_SEED = 42
RAND_RANGE = 1000
SUMMARY_DIR = '../results'
LOG_FILE = '../results/log'
# log in format of time_stamp bit_rate buffer_size rebuffer_time chunk_size download_time reward
NN_MODEL = '../models/pretrain_linear_reward.ckpt'

DATA_PATH = '../data'

ACTION_DIM=1
allTimeStep=2000
updateStep=6

def main( usersnumber,tracename='none',allvideochunk=64):

    np.random.seed(RANDOM_SEED)
    torch.manual_seed(RANDOM_SEED)

    assert len(VIDEO_BIT_RATE) == A_DIM

    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)

    # log_path need to fix

    #log_path = LOG_FILE + '_'+tracename+'_Pensieve_'+str(usersnumber)+'_' + str(m_id)
    #log_file = open(log_path, 'wb')
    bitrate=[VIDEO_BIT_RATE[0]*1000 for _ in range(usersnumber)]
    for m_id in range(usersnumber):
        output_file = open(DATA_PATH + '/predict' + str(m_id),'a')
        output_file.write(str(bitrate[0])+'\n')
        output_file.close()
    time_step=0

    allstatelist=[]
    allactionlist=[]
    allrewardlist=[]

    maddpg=Sakuro(S_LEN,S_INFO,usersnumber,BATCH_SIZE)

    with open(LOG_FILE+'time','wb') as logging:
        while time_step<=allTimeStep:  # serve video forever
            with open(DATA_PATH + '/permission') as enable:
                key = enable.read()
                if key == '1':
                    time_step+=1

                    currRate=[]
                    rebuffer=[]
                    allstate=[]
                    reward=[]
                    for m_id in range(usersnumber):
                        #state=[]
                        count=0
                        #state=buffer,thoughput,lastbitrate
                        with open(DATA_PATH+'/buffer'+str(m_id)) as f:
                            for line in f:
                                count+=1
                                allstate.append(float(line.split()[0]))
                        with open(DATA_PATH+'/thoughput'+str(m_id)) as f:
                            for line in f:
                                allstate.append(float(line.split()[0]))
                        with open(DATA_PATH+'/currRate'+str(m_id)) as f:
                            tmp=[]
                            for line in f:
                                tmp.append(float(line.split()[0]))
                            currRate.append(tmp)
                        with open(DATA_PATH+'/rebufftime'+str(m_id)) as f:
                            for line in f:
                                rebuffer.append(float(line.split()[0]))
                        allstate.append(bitrate[m_id]/1000000.0)
                        #allstate.append(state)

                    if time_step>1:
                        currRate=np.array(currRate)
                        ave=np.mean(currRate)
                        fairness=np.sum(np.sqrt(np.sum(np.power(currRate-ave,2),0)/usersnumber)/np.mean(currRate,0))/5
                        b=np.reshape(maddpg.actionSelect(allstate),usersnumber)
                        print(b)
                        for m_id in range(usersnumber):
                            reward.append(bitrate[m_id]/1000000.0-5*fairness-rebuffer[m_id])
                            output_file = open(DATA_PATH + '/predict' + str(m_id),'a')
                            t=0
                            if b[m_id]>5:
                                t=5
                            elif b[m_id]<0:
                                t=0
                            else:
                                t=int(b[m_id])
                            bitrate[m_id]=VIDEO_BIT_RATE[t]*1000
                            #print(bitrate[m_id])
                            output_file.write(str(bitrate[m_id])+'\n')
                            output_file.close()
                        logging.write('state:'+str(allstate)+'\t'+'rebuffer:'+str(rebuffer)+'\t'+'reward:'+str(reward)+'\t'+'next_bitrate:'+str(bitrate)+'\t'+'networkout:'+str(b)+'\n')
                        logging.flush()
                        allstatelist.append(allstate)
                        allrewardlist.append(reward)
                        allactionlist.append(b)
                        if time_step%updateStep==0:
                            for k in range(len(allstatelist)-1):
                                maddpg.add2replaybuff(allstatelist[k],allactionlist[k],allrewardlist[k+1],allstatelist[k+1])
                            #print('updateNetwork')
                            maddpg.updateNetwork()
                            maddpg.resetNoise()
                            del allstatelist[:]
                            del allrewardlist[:]
                            del allactionlist[:]

                    file_permission = open(DATA_PATH + '/permission','a')
                    file_permission.write('0\n')
                    file_permission.close()



if __name__ == '__main__':
    users = sys.argv[1]
    main(int(users))

    
