
import random
import numpy as np
import torch
import torch.nn as nn 
import torch.nn.functional as F
from Network import (ActorNetwork,CriticNetwork)
from Noise import OUNoise
from ReplayBuffer_mc import ReplayBuffer
from datetime import datetime
from copy import deepcopy

class Sakuro(object):
    def __init__(self,s_len,s_info,n_agent,a_dim,batch_size,gama=0.9):
        self.s_len=s_len
        self.s_info=s_info
        self.n_agent=n_agent
        # agent_id start at 0
        self.discount=gama
        self.batch_size=batch_size
        self.a_dim=a_dim

        self.actorNetwork=[ActorNetwork(self.s_len,self.s_info,self.n_agent,self.a_dim,i).double() for i in range(self.n_agent)]
        self.actorOptim=[torch.optim.RMSprop(self.actorNetwork[i].parameters(),lr=5e-3,weight_decay=0) for i in range(self.n_agent)]
        #self.actorOptim=[torch.optim.Adam(self.actorNetwork[i].parameters(),lr=5e-3,weight_decay=0) for i in range(self.n_agent)]


        self.criticNetwork=CriticNetwork(self.s_len,self.s_info,self.n_agent).double()
        self.criticOptim=torch.optim.RMSprop(self.criticNetwork.parameters(),lr=5e-3,alpha=0.9,eps=1e-10,weight_decay=0)
        #self.criticOptim=torch.optim.Adam(self.criticNetwork.parameters(),lr=5e-3,weight_decay=0)
        # self.noise=OUNoise(self.a_dim)
        self.replayBuffer=ReplayBuffer(512) 
        self.critic_loss_func=nn.MSELoss()
        self.actor_loss=nn.CrossEntropyLoss()
        self.entropy_weight=0.5
        self.entropy_eps=0.9
        self.__cuda()



    def updateNetwork(self,state_batch,action_batch,reward_batch):
        #state_batch,action_batch,reward_batch,next_state_batch = self.replayBuffer.sample_batch(self.batch_size)
        if state_batch.shape[0]<2:
            return 0
        R_batch=np.zeros(reward_batch.shape)
 
        for t in reversed(range(reward_batch.shape[0]-1)):
            R_batch[t]=reward_batch[t] + self.discount*R_batch[t+1]
        R_batch=torch.from_numpy(R_batch).cuda()
        print('up')
        #print(reward_batch)
        #print(R_batch)
        #print(state_batch[:20])



        '''
        state_batch=torch.Tensor(state_batch).cuda()
        action_batch=torch.Tensor(action_batch).cuda()

        v_batch=self.criticNetwork.forward(state_batch)

        td_batch=R_batch-v_batch
        '''

        state_batch=torch.from_numpy(state_batch).cuda()
        action_batch=torch.from_numpy(action_batch).cuda()
        for i in range(self.n_agent):
            #print(state_batch.dtype)
            #print(state_batch[:10])

            v_batch=self.criticNetwork.forward(state_batch)

            td_batch=R_batch-v_batch
     
            self.actorOptim[i].zero_grad()
            td_error=R_batch[:,i:i+1]-v_batch
            probability=self.actorNetwork[i].forward(state_batch)
            #print(action_batch[:,i])
            #print(probability)
            #print(probability.shape)
            #print(torch.sum(probability*action_batch[:,i],1,keepdim=True))
            #print(torch.log(torch.sum(probability*action_batch[:,i],1,keepdim=True))*(-td_error))
            actor_loss=torch.sum(torch.log(torch.sum(probability*action_batch[:,i],1,keepdim=True))*(-td_error))+self.entropy_weight*torch.sum(probability*torch.log(probability+self.entropy_eps))
            #print(probability)
            print(actor_loss)
            
            actor_loss.backward(retain_graph=True)
            par=list(self.actorNetwork[i].parameters())
            print('grad')
            for index,p in enumerate(par):
                if index==len(par)-1:
                    print(p.grad)


            self.actorOptim[i].step()

        self.criticOptim.zero_grad()
        v_batch=self.criticNetwork.forward(state_batch)
        critic_loss=self.critic_loss_func(torch.sum(R_batch,1,keepdim=True),v_batch)
        critic_loss.backward(retain_graph=True)
        self.criticOptim.step()

    def targetUpdate(self):
        for i in range(self.n_agent):
            self.__hardUpdate(self.targetActorNetwork[i],self.actorNetwork[i])
            self.__hardUpdate(self.targetCriticNetwork[i],self.criticNetwork[i])


        
    def add2replaybuff(self,state,action,reward,nstate):
        self.replayBuffer.add(state,action,reward,nstate)

    def actionSelect(self,stateInputs):
        action=[]
        stateInputs=torch.Tensor([stateInputs]).cuda().double()
        for i in range(self.n_agent):
            a=self.actorNetwork[i].forward(stateInputs)
            a=a.view(-1)
            a=a.detach().cpu().numpy()
            action.append(a)
        action=np.clip(action,0,5)
        return np.array(action)
 
    def resetNoise(self):
        for i in range(self.n_agent):
            self.noise[i].reset()
    def loadModel(self,epoch):
        for i in range(self.n_agent):
            self.actorNetwork[i].load_state_dict(torch.load('actor'+str(i)+'_'+str(epoch)+'.pt'))
        self.criticNetwork.load_state_dict(torch.load('critic_'+str(epoch)+'.pt'))
    def saveModel(self,epoch):
        for i in range(self.n_agent):
            torch.save(self.actorNetwork[i].state_dict(),'actor'+str(i)+'_'+str(epoch)+'.pt')
        torch.save(self.criticNetwork.state_dict(),'critic_'+str(epoch)+'.pt')


    def __cuda(self):
        if torch.cuda.is_available():
            torch.cuda.set_device(1)
            self.criticNetwork.cuda()
            for i in range(self.n_agent):
                self.actorNetwork[i].cuda()


    def __hardUpdate(self,target,source):
        for target_param,source_param in zip(target.parameters(),source.parameters()):
            target_param.data.copy_(source_param.data)
 
    def __softUpdate(self,target,source,tau=0.1):
        for target_param,source_param in zip(target.parameters(),source.parameters()):
            target_param.data.copy_(target_param.data * (1.0-tau) + source_param.data*tau)
 

if __name__ =='__main__':
    SINGLE_S_LEN=3

    AGENT_NUM=1
    ACTION_DIM=4

    BATCH_SIZE=1

    S_INFO=3
    S_LEN=6
    discount=0.9


    obj=Sakuro(S_LEN,S_INFO,AGENT_NUM,ACTION_DIM,BATCH_SIZE,discount)
    timenow=datetime.now()

    episode=22

    statebatch=[]
    actionbatch=[]
    rewardbatch=[]
    for i in range(episode):

        state2Select=np.random.randn(S_INFO*AGENT_NUM,S_LEN)
        action=[]
        for a in range(AGENT_NUM):
            a=np.zeros(ACTION_DIM)
            a[np.random.randint(0,ACTION_DIM)]=1
            action.append(a)
        action=np.array(action)

        reward=np.random.randn(AGENT_NUM)*20
        statebatch.append(state2Select)
        actionbatch.append(action)
        rewardbatch.append(reward)
        probability=obj.actionSelect(state2Select)
        print(probability)
        if i %10==0 and i>0:
            #print(np.array(statebatch))
            obj.updateNetwork(np.array(statebatch),np.array(actionbatch),np.array(rewardbatch))
            del statebatch[:]
            del actionbatch[:]
            del rewardbatch[:]

    print('train 48 times use:'+str(datetime.now()-timenow))
    timenow=datetime.now()



