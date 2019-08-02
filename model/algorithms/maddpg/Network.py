
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime



class ActorNetwork(nn.Module):
    # actornetwork pass the test
    def __init__(self,stateLen,hidden1=256,hidden2=128):
        super(ActorNetwork,self).__init__() 
        self.s_len=stateLen
        self.hidden1=hidden1
        self.hidden2=hidden2


        self.fc1=nn.Linear(self.s_len,self.hidden1)
        self.fc2=nn.Linear(self.hidden1,self.hidden1)
        self.fc3=nn.Linear(self.hidden1,self.hidden2)
        self.fc4=nn.Linear(self.hidden2,64)
        self.outputLayer=nn.Linear(64,1)

    def forward(self,inputs):
        inputs=torch.Tensor(inputs)


        fc1Out=F.relu(self.fc1(inputs))
        fc2Out=F.relu(self.fc2(fc1Out))
        fc3Out=F.relu(self.fc3(fc2Out))
        fc4Out=F.relu(self.fc4(fc3Out))
        out=F.sigmoid(self.outputLayer(fc4Out))
        out=out * 6
        return out


class CriticNetwork(nn.Module):
    def __init__(self,stateLen,n_agent,hidden1=512,hidden2=256):
        super(CriticNetwork,self).__init__()
        self.s_len=stateLen
        self.n_agent=n_agent
        self.hidden1=hidden1
        self.hidden2=hidden2
        self.fc1=nn.Linear(self.s_len*self.n_agent+self.n_agent,self.hidden1) # 1 is action
        self.fc2=nn.Linear(self.hidden1,self.hidden2)
        self.fc3=nn.Linear(self.hidden2,self.hidden2)
        self.fc4=nn.Linear(self.hidden2,128)
        self.outputLayer=nn.Linear(128,1)

    def forward(self,inputs,action):
        inputs=torch.Tensor(inputs)
        action=torch.Tensor(action)

        input2network=torch.cat([inputs,action],dim=1)
    
        fc1Out=F.relu(self.fc1(input2network))
        fc2Out=F.relu(self.fc2(fc1Out))
        fc3Out=F.relu(self.fc3(fc2Out))
        fc4Out=F.relu(self.fc4(fc3Out))
        out=self.outputLayer(fc4Out)

        return out


if __name__ =='__main__':
    SINGLE_S_LEN=3

    AGENT_NUM=1
    ACTION_DIM=4

    BATCH_SIZE=10

    discount=0.9


    timenow=datetime.now()
    c_net=CriticNetwork(SINGLE_S_LEN,AGENT_NUM) # agent_num=2

    t_c_net=CriticNetwork(SINGLE_S_LEN,AGENT_NUM)

    a_net=ActorNetwork(SINGLE_S_LEN,ACTION_DIM,AGENT_NUM) # action_dime=4

    a_optim=torch.optim.Adam(a_net.parameters(),lr=0.001)

    c_optim=torch.optim.Adam(c_net.parameters(),lr=0.005)

    loss_func=nn.MSELoss()
    for i in range(48):
        npState=np.random.rand(BATCH_SIZE,SINGLE_S_LEN*AGENT_NUM)*10
        next_npState=np.random.rand(BATCH_SIZE,SINGLE_S_LEN*AGENT_NUM)*10
        reward=torch.randn(BATCH_SIZE)*10
        a=torch.randn(BATCH_SIZE,AGENT_NUM)*10
        t_a=torch.randn(BATCH_SIZE,AGENT_NUM)*10

        
        #print('epi')
        #print(action)
        #print(t_a)
        t_action=a_net.forward(next_npState[:,:SINGLE_S_LEN])

        q=c_net.forward(npState,a)
        t_q_out=t_c_net.forward(next_npState,t_a)

        target_q=reward+discount*t_q_out

        updateCriticLoss=loss_func(target_q,q)

        c_optim.zero_grad()
        updateCriticLoss.backward()
        c_optim.step()

        a_optim.zero_grad()
        # if you don't have 59-60 lines,can't policyloss.backward
        # because action in buffer will be free,q also be free
        # but write like this,c_optim may update the actornetwork or not ?
        # action=a_net.forward(npState[:,0:SINGLE_S_LEN],startinfo)

        action=a_net.forward(npState[:,0:SINGLE_S_LEN])
        #print(action)
        print(npState)
        policyLoss=-c_net.forward(npState,action)
        policyLoss=policyLoss.mean()
        policyLoss.backward()
        a_optim.step()
        par=list(a_net.parameters())
        print('a net')
        #print(par[0][0])


    print('train 4800 times use:'+str(datetime.now()-timenow))





