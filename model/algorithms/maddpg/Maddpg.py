
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
    def __init__(self,s_len,s_info,n_agent,batch_size,gama=0.9):
        self.s_len=s_len
        self.s_info=s_info
        self.n_agent=n_agent
        # agent_id start at 0
        self.discount=gama
        self.batch_size=batch_size

        self.actorNetwork=[ActorNetwork(self.s_len) for _ in range(self.n_agent)]
        self.actorOptim=[torch.optim.Adam(self.actorNetwork[i].parameters(),lr=1e-3) for i in range(self.n_agent)]
        self.targetActorNetwork=deepcopy(self.actorNetwork)

        self.criticNetwork=[CriticNetwork(self.s_len,self.n_agent) for _ in range(self.n_agent)]
        self.targetCriticNetwork=deepcopy(self.criticNetwork)
        self.criticOptim=[torch.optim.Adam(self.criticNetwork[i].parameters(),lr=1e-3) for i in range(self.n_agent)]

        # self.noise=OUNoise(self.a_dim)
        self.noise=[OUNoise(1) for _ in range(self.n_agent)]
        self.replayBuffer=ReplayBuffer(300)

        self.critic_loss=nn.MSELoss()
        self.actor_loss=nn.CrossEntropyLoss()



    def updateNetwork(self):
        state_batch,action_batch,reward_batch,next_state_batch = self.replayBuffer.sample_batch(self.batch_size)

        state_batch=torch.Tensor(state_batch)
        action_batch=torch.Tensor(action_batch)
        reward_batch=torch.Tensor(reward_batch)
        next_state_batch=torch.Tensor(next_state_batch)

        next_action=self.targetActorNetwork[0].forward(next_state_batch[:,:self.s_len])
        next_action=next_action.view(next_state_batch.shape[0],-1)
        for i in range(self.n_agent-1):
            a=self.targetActorNetwork[i+1].forward(next_state_batch[:,self.s_len*(i+1):self.s_len*(i+2)])
            a=a.view(next_state_batch.shape[0],-1)
            next_action=torch.cat([next_action,a],1)
        action=self.actorNetwork[0].forward(state_batch[:,:self.s_len])
        action=action.view(state_batch.shape[0],-1)
        for z in range(self.n_agent-1):
            a=self.actorNetwork[z+1].forward(torch.Tensor(state_batch)[:,self.s_len*(z+1):self.s_len*(z+2)])
            a=a.view(state_batch.shape[0],-1)
            action=torch.cat([action,a],1)


        for i in range(self.n_agent):
            par=list(self.actorNetwork[i].parameters())
            print('old par'+str(i))
            print(par[-1])
            self.criticOptim[i].zero_grad()
            next_q_values=self.targetCriticNetwork[i].forward(next_state_batch,next_action).view(state_batch.shape[0],-1)
            q_values=self.criticNetwork[i].forward(state_batch,action_batch).view(state_batch.shape[0],-1)
            value_loss=self.critic_loss(reward_batch[:,i:i+1].double()+self.discount*next_q_values.double(),q_values.double())
            value_loss.backward(retain_graph=True)
            self.criticOptim[i].step()

            self.actorOptim[i].zero_grad()

            policy_loss=-self.criticNetwork[i](state_batch,action)
            policy_loss=policy_loss.mean()
            policy_loss.backward(retain_graph=True)
            self.actorOptim[i].step()
            par=list(self.actorNetwork[i].parameters())
            print('new par')
            print(par[-1])
            print(par[-1].grad)

            self.__softUpdate(self.targetCriticNetwork[i],self.criticNetwork[i])
            self.__softUpdate(self.targetActorNetwork[i],self.actorNetwork[i])



        
    def add2replaybuff(self,state,action,reward,nstate):
        self.replayBuffer.add(state,action,reward,nstate)

    def actionSelect(self,stateInputs):
        action=[]
        for i in range(self.n_agent):
            a=self.actorNetwork[i].forward(torch.Tensor([stateInputs])[:,self.s_len*i:self.s_len*(i+1)])
            a=a.view(-1)
            a=a.detach().numpy()+self.noise[i].getNoise()
            action.append(a)
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


    def cuda(self):
        self.actorNetwork.cuda()
        self.criticNetwork.cuda()
        self.targetCriticNetwork.cuda()


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

    BATCH_SIZE=2

    S_INFO=3
    discount=0.9


    obj=Sakuro(SINGLE_S_LEN,S_INFO,AGENT_NUM,BATCH_SIZE,discount)
    timenow=datetime.now()

    episode=40
    for i in range(episode):

        state2Select=np.random.randn(SINGLE_S_LEN*AGENT_NUM)
        action=np.random.randn(AGENT_NUM)
        reward=np.random.randn(AGENT_NUM)
        '''
        print('state')
        print(state2Select)
        print('startinfo')
        print(startinfo)
        '''
        #reward=np.array([2])
        #reward=2
        out=obj.actionSelect(state2Select)
        obj.add2replaybuff(state2Select,action,reward,state2Select)
        #print('out')
        #print(out)
        if i %10==0 and i>0:
            obj.updateNetwork()
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



