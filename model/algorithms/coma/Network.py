
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from datetime import datetime



class ActorNetwork(nn.Module):
    # actornetwork pass the test
    def __init__(self,stateLen,stateinfo,n_agent,a_dim,m_id,n_fc=64,n_conv=64):
        super(ActorNetwork,self).__init__() 
        self.s_len=stateLen
        self.s_info=stateinfo
        self.scalarOutDim=n_fc
        self.vectorOutDim=n_conv
        self.m_id=m_id
        self.n_agent=n_agent
        self.a_dim=a_dim
        self.fcinput_dim=(self.s_len-4+1)*self.vectorOutDim+2*self.scalarOutDim

        self.bufferstart=self.n_agent*2+self.m_id
        self.bufferend=self.bufferstart+1
        self.thoughputstart=self.n_agent*1+self.m_id
        self.thoughputend=self.thoughputstart+1
        self.bitratestart=self.m_id
        self.bitrateend=self.bitratestart+1


        self.fc=nn.Linear(1,self.scalarOutDim)
        self.conv1=nn.Conv1d(1,self.vectorOutDim,4)
        self.fc1=nn.Linear(1,self.vectorOutDim,4)
        self.fullyConnected=nn.Linear(self.fcinput_dim,self.scalarOutDim)
        self.drop=nn.Dropout(0)
        self.outputLayer=nn.Linear(self.scalarOutDim,self.a_dim)

    def forward(self,inputs):
        #inputs=torch.Tensor(inputs)

        bufferOut=F.relu(self.fc(inputs[:,self.bufferstart:self.bufferend,-1]))
        thoughputOut=F.relu(self.conv1(inputs[:,self.thoughputstart:self.thoughputend,:]))
        bitrateOut=F.relu(self.fc1(inputs[:,self.bitratestart:self.bitrateend,-1]))
        t_flatten=thoughputOut.view(thoughputOut.shape[0],-1)

        fcInput=torch.cat([bitrateOut,t_flatten,bufferOut],1)


        fcOut=self.drop(self.fullyConnected(fcInput))

        fcOut=F.relu(fcOut)

        out=F.softmax(self.outputLayer(fcOut))
        return out


class CriticNetwork(nn.Module):
    def __init__(self,stateLen,stateinfo,n_agent,n_fc=64,n_conv=64):
        super(CriticNetwork,self).__init__()
        self.s_len=stateLen
        self.s_info=stateinfo
        self.scalarOutDim=n_fc
        self.vectorOutDim=n_conv
        self.n_agent=n_agent
        self.fcinput_dim=(self.s_len-4+1)*self.vectorOutDim+2*self.scalarOutDim

        self.bufferstart=self.n_agent*2
        self.bufferend=self.bufferstart+self.n_agent
        self.thoughputstart=self.n_agent*1
        self.thoughputend=self.thoughputstart+self.n_agent
        self.bitratestart=0
        self.bitrateend=self.bitratestart+self.n_agent


        self.fc=nn.Linear(self.n_agent,self.scalarOutDim)
        self.conv1=nn.Conv1d(self.n_agent,self.vectorOutDim,4)
        self.fc1=nn.Linear(self.n_agent,self.vectorOutDim,4)
        self.fullyConnected=nn.Linear(self.fcinput_dim,self.scalarOutDim)
        self.drop=nn.Dropout(0)
        self.outputLayer=nn.Linear(self.scalarOutDim,1)

    def forward(self,inputs):
        #inputs=torch.Tensor(inputs)

        bufferOut=F.relu(self.fc(inputs[:,self.bufferstart:self.bufferend,-1]))
        thoughputOut=F.relu(self.conv1(inputs[:,self.thoughputstart:self.thoughputend,:]))
        bitrateOut=F.relu(self.fc1(inputs[:,self.bitratestart:self.bitrateend,-1]))

        t_flatten=thoughputOut.view(thoughputOut.shape[0],-1)
        fcInput=torch.cat([bitrateOut,t_flatten,bufferOut],1)

        fcOut=self.drop(self.fullyConnected(fcInput))

        fcOut=F.relu(fcOut)

        out=self.outputLayer(fcOut)
        return out


if __name__ =='__main__':
    SINGLE_S_LEN=3
    S_INFO=3
    S_LEN=6

    AGENT_NUM=1
    ACTION_DIM=4

    BATCH_SIZE=2

    discount=0.9

    entropy_weight=0.5
    entropy_eps=1e-6

    timenow=datetime.now()
    c_net=CriticNetwork(S_LEN,S_INFO,AGENT_NUM) # agent_num=2


    a_net=ActorNetwork(S_LEN,S_INFO,AGENT_NUM,ACTION_DIM,0) # action_dime=4

    a_optim=torch.optim.Adam(a_net.parameters(),lr=0.001)

    c_optim=torch.optim.Adam(c_net.parameters(),lr=0.005)

    loss_func=nn.MSELoss()
    for i in range(1):
        npState=np.random.rand(BATCH_SIZE,S_INFO*AGENT_NUM,S_LEN)
        next_npState=np.random.rand(BATCH_SIZE,S_INFO*AGENT_NUM,S_LEN)
        reward=torch.randn(BATCH_SIZE,AGENT_NUM)

        action=[]
        for k in range(BATCH_SIZE):
            a=np.zeros(ACTION_DIM)
            a[np.random.randint(0,ACTION_DIM)]=1
            action.append(a)
        action=torch.Tensor(action)
        #print(action)

        v=c_net.forward(npState)
        #print(v)
        v_=c_net.forward(next_npState).detach()
        #print(reward)
        #print(v_)
        td_error=reward+discount*v_-v
        #print(td_error)


        a_optim.zero_grad()
        probability=a_net.forward(npState)
        #print(probability*action)
        #print(torch.sum(probability*action,dim=1,keepdim=True))
        actor_loss=torch.sum(torch.log(torch.sum(probability*action,1,keepdim=True)*(-td_error))+entropy_weight*torch.sum(probability*torch.log(probability+entropy_eps)))
        actor_loss.backward(retain_graph=True)
        a_optim.step()

        c_optim.zero_grad()
        par=list(c_net.parameters())
        print('par')
        for index,z in enumerate(par):
            if index ==0:
                print(z)
                #print(z.grad)
        critic_loss=loss_func(reward+discount*v_,v)
        critic_loss.backward()
        par=list(c_net.parameters())
        print('grad')
        for index,z in enumerate(par):
            if index==0:
                print(z.grad)

        c_optim.step()
        print('train 4800 times use:'+str(datetime.now()-timenow))





