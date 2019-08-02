import os
import numpy as np
#import matplotlib.pyplot as plt
import sys
import multiprocessing as mp
from coma_mc import Sakuro
import torch


BATCH_SIZE=32
S_LEN = 6  # take how many frames in the past
S_INFO =3
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
allTimeStep=600
updateStep=50
targetUpdate=21

def main( usersnumber,p1=1,p2=1,p3=1,epoch=50):

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
    state=np.zeros((S_INFO*usersnumber,S_LEN))

    maddpg=Sakuro(S_LEN,S_INFO,usersnumber,A_DIM,BATCH_SIZE)
    maddpg.loadModel(epoch)
    rebuffer=np.zeros(usersnumber)

    logging=[open(LOG_FILE+'time'+str(i)+'_'+str(p1)+'_'+str(p2)+'_'+str(p3)+'_'+str(epoch),'wb') for i in range(usersnumber)]
    while time_step<=allTimeStep:  # serve video forever
        with open(DATA_PATH + '/permission') as enable:
            key = enable.read()
            if key == '1':
                time_step+=1

                currRate=[]
                #allstate=[]
                reward=[]
                state=np.roll(state,-1,axis=1)
                for m_id in range(usersnumber):
                    #state=[]
                    #state=buffer,thoughput,lastbitrate
                    with open(DATA_PATH+'/buffer'+str(m_id)) as f:
                        for line in f:
                            state[usersnumber*(2)+m_id,-1]=float(line.split()[0])
                    with open(DATA_PATH+'/thoughput'+str(m_id)) as f:
                        for line in f:
                            state[usersnumber*(1)+m_id,-1]=float(line.split()[0])
                    with open(DATA_PATH+'/currRate'+str(m_id)) as f:
                        tmp=[]
                        for line in f:
                            tmp.append(float(line.split()[0]))
                        currRate.append(tmp)
                    with open(DATA_PATH+'/rebufftime'+str(m_id)) as f:
                        for index,line in enumerate(f):
                            r=float(line.split()[0])
                            if r==0:
                                rebuffer[index]=0
                            else:
                                rebuffer[index]=r
                    state[usersnumber*(0)+m_id,-1]=bitrate[m_id]/4300000.0

                if time_step>1:
                    currRate=np.array(currRate)
                    ave=np.mean(currRate)
                    fairness=np.sum(np.sqrt(np.sum(np.power(currRate-ave,2),0)/usersnumber)/np.mean(currRate,0))/5.0
                    action=maddpg.actionSelect(state)
                    #print(action)
                    read_action=np.zeros(action.shape)
                    for m_id in range(usersnumber):
                        reward.append(p1*bitrate[m_id]/1000000.0-p2*fairness-p3*rebuffer[m_id])
                        output_file = open(DATA_PATH + '/predict' + str(m_id),'a')

                        action_cumsum=np.cumsum(action[m_id])
                        bit_rate=(action_cumsum > np.random.randint(1,RAND_RANGE)/float(RAND_RANGE)).argmax()
                        bitrate[m_id]=VIDEO_BIT_RATE[bit_rate]*1000
                        #print(bitrate[m_id])
                        read_action[m_id,bit_rate]=1
                        #print(read_action)
                        output_file.write(str(bitrate[m_id])+'\n')
                        output_file.close()
                        logging[m_id].write(str(time_step)+'\t'+str(VIDEO_BIT_RATE[bit_rate]*1000)+'\t'+str(state[usersnumber*2+m_id,-1])+'\t'+str(state[usersnumber*1+m_id,-1])+'\t'+str(rebuffer[m_id])+'\t'+str(reward[m_id])+'\n')
                        logging[m_id].flush()
                file_permission = open(DATA_PATH + '/permission','a')
                file_permission.write('0\n')
                file_permission.close()



if __name__ == '__main__':
    users = sys.argv[1]
    main(int(users),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]))

    
