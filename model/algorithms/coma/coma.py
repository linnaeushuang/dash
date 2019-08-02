
import random
import numpy as np
import torch
import torch.nn as nn 
import torch.nn.functional as F
from Network import (ActorNetwork,CriticNetwork)
from Noise import OUNoise
from ReplayBuffer import ReplayBuffer
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

        self.actorNetwork=[ActorNetwork(self.s_len,self.s_info,self.n_agent,self.a_dim,i) for i in range(self.n_agent)]
        self.actorOptim=[torch.optim.RMSprop(self.actorNetwork[i].parameters(),lr=5e-3,weight_decay=5e-4) for i in range(self.n_agent)]

        self.criticNetwork=CriticNetwork(self.s_len,self.s_info,self.n_agent)
        self.criticOptim=torch.optim.RMSprop(self.criticNetwork.parameters(),lr=5e-3,alpha=0.9,eps=1e-10,weight_decay=5e-4)
        # self.noise=OUNoise(self.a_dim)
        self.replayBuffer=ReplayBuffer(1) 
        self.critic_loss_func=nn.MSELoss()
        self.actor_loss=nn.CrossEntropyLoss()
        self.entropy_weight=0.5
        self.entropy_eps=0.9
        print('call cuda')
        self.__cuda()



    def updateNetwork(self):
        state_batch,action_batch,reward_batch,next_state_batch = self.replayBuffer.sample_batch(self.batch_size)
        if state_batch.shape[0]<1:
            return 0
        state_batch=torch.Tensor(state_batch).cuda()
        reward_batch=torch.Tensor(reward_batch).cuda()
        next_state_batch=torch.Tensor(next_state_batch).cuda()
        action_batch=torch.Tensor(action_batch).cuda()


        for i in range(self.n_agent):
              
            v=self.criticNetwork.forward(state_batch)
            v_=self.criticNetwork.forward(next_state_batch).detach()
            self.actorOptim[i].zero_grad()
            td_error=reward_batch[:,i:i+1]+self.discount*v_-v
            probability=self.actorNetwork[i].forward(state_batch)
            actor_loss=torch.sum(torch.log(torch.sum(probability*action_batch[:,i],1,keepdim=True))*(-td_error))+self.entropy_weight*torch.sum(probability*torch.log(probability+self.entropy_eps))

            #actor_loss.backward(retain_graph=True)
            actor_loss.backward()
            self.actorOptim[i].step()

        v=self.criticNetwork.forward(state_batch)
        v_=self.criticNetwork.forward(next_state_batch).detach()
        self.criticOptim.zero_grad()
        critic_loss=self.critic_loss_func(torch.sum(reward_batch,1,keepdim=True)+self.discount*v_,v)
        critic_loss.backward()
        self.criticOptim.step()

    def targetUpdate(self):
        for i in range(self.n_agent):
            self.__hardUpdate(self.targetActorNetwork[i],self.actorNetwork[i])
            self.__hardUpdate(self.targetCriticNetwork[i],self.criticNetwork[i])


        
    def add2replaybuff(self,state,action,reward,nstate):
        self.replayBuffer.add(state,action,reward,nstate)

    def actionSelect(self,stateInputs):
        action=[]
        stateInputs=torch.Tensor([stateInputs]).cuda()
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
    def loadModel(self):
        self.actorNetwork.load_state_dict(torch.load('actor.pt'))
        self.criticNetwork.load_state_dict(torch.load('critic.pt'))
        self.targetCriticNetwork.load_state_dict(torch.load('targetcritic.pt'))
        self.targetActorNetwork.load_state_dict(torch.load('targetactor.pt'))
    def saveModel(self):
        torch.save(self.actorNetwork.state_dict(),'actor.pt')
        torch.save(self.criticNetwork.state_dict(),'critic.pt')
        torch.save(self.targetCriticNetwork.state_dict(),'targetcritic.pt')
        torch.save(self.targetActorNetwork.state_dict(),'targetactor.pt')


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

    AGENT_NUM=2
    ACTION_DIM=4

    BATCH_SIZE=2

    S_INFO=3
    S_LEN=6
    discount=0.9


    obj=Sakuro(S_LEN,S_INFO,AGENT_NUM,ACTION_DIM,BATCH_SIZE,discount)
    timenow=datetime.now()

    episode=2
    for i in range(episode):

        state2Select=np.random.randn(S_INFO*AGENT_NUM,S_LEN)
        action=[]
        for a in range(AGENT_NUM):
            a=np.zeros(ACTION_DIM)
            a[np.random.randint(0,ACTION_DIM)]=1
            action.append(a)
        action=np.array(action)

        reward=np.random.randn(AGENT_NUM)
        '''
        print('state')
        print(state2Select)
        print('startinfo')
        print(startinfo)
        '''
        #reward=np.array([2])
        #reward=2
        probability=obj.actionSelect(state2Select)
        obj.add2replaybuff(state2Select,action,reward,state2Select)
        obj.updateNetwork()
        if i %1==0 and i>0:
            #obj.targetUpdate()
            pass

        '''
        next_state=np.random.randn(SINGLE_S_LEN*AGENT_NUM)
        reward=np.random.randn(1)
        next_startinfo=np.random.randn(AGENT_NUM)
        out=obj.actionSelect(next_state,next_startinfo,reward)
        obj.updateNetwork()
        '''
    print('train 48 times use:'+str(datetime.now()-timenow))
    timenow=datetime.now()



