
import random
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from Network_conv import (ActorNetwork,CriticNetwork)
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
        self.actorNetwork=[ActorNetwork(self.s_len,self.s_info,self.n_agent,i) for i in range(self.n_agent)]
        self.actorOptim=[torch.optim.RMSprop(self.actorNetwork[i].parameters(),lr=5e-4,alpha=0.9,eps=1e-10,weight_decay=0) for i in range(self.n_agent)]
        self.targetActorNetwork=deepcopy(self.actorNetwork)

        self.criticNetwork=[CriticNetwork(self.s_len,self.s_info,self.n_agent) for _ in range(self.n_agent)]
        self.criticOptim=[torch.optim.RMSprop(self.criticNetwork[i].parameters(),lr=5e-3,alpha=0.9,eps=1e-10,weight_decay=0) for i in range(self.n_agent)]
        self.targetCriticNetwork=deepcopy(self.criticNetwork)
        # self.noise=OUNoise(self.a_dim)
        self.noise=[OUNoise(1) for _ in range(self.n_agent)]
        self.replayBuffer=ReplayBuffer(512)

        self.critic_loss=nn.MSELoss()
        self.actor_loss=nn.CrossEntropyLoss()



    def updateNetwork(self):
        state_batch,action_batch,reward_batch,next_state_batch = self.replayBuffer.sample_batch(self.batch_size)
        if state_batch.shape[0]<1:
            return 0
        state_batch=torch.Tensor(state_batch)
        action_batch=torch.Tensor(action_batch)
        reward_batch=torch.Tensor(reward_batch)
        next_state_batch=torch.Tensor(next_state_batch)

        next_action=self.targetActorNetwork[0].forward(next_state_batch)
        next_action=next_action.view(next_state_batch.shape[0],-1)
        for i in range(self.n_agent-1):
            a=self.targetActorNetwork[i+1].forward(next_state_batch)
            a=a.view(next_state_batch.shape[0],-1)
            next_action=torch.cat([next_action,a],1)
        action=self.actorNetwork[0].forward(state_batch)
        action=action.view(state_batch.shape[0],-1)
        for z in range(self.n_agent-1):
            a=self.actorNetwork[z+1].forward(state_batch)
            a=a.view(state_batch.shape[0],-1)
            action=torch.cat([action,a],1)
        #print(action)


        for i in range(self.n_agent):
            #print('index:'+str(i))
            #par=list(self.actorNetwork[i].parameters())
            #print(par[0][0])
            #self.criticOptim[i].zero_grad()
            '''
            next_action=self.targetActorNetwork[0].forward(next_state_batch)
            next_action=next_action.view(next_state_batch.shape[0],-1)
            for i in range(self.n_agent-1):
                a=self.targetActorNetwork[i+1].forward(next_state_batch)
                a=a.view(next_state_batch.shape[0],-1)
                next_action=torch.cat([next_action,a],1)
            '''

            next_q_values=self.targetCriticNetwork[i].forward(next_state_batch,next_action).view(state_batch.shape[0],-1)
            q_values=self.criticNetwork[i].forward(state_batch,action_batch).view(state_batch.shape[0],-1)
            value_loss=self.critic_loss(reward_batch[:,i:i+1].double()+self.discount*next_q_values.double(),q_values.double())
            #print('value_loss')
            #print(value_loss)
            value_loss.backward(retain_graph=True)
            self.criticOptim[i].step()

            self.actorOptim[i].zero_grad() 
            '''
            action=self.actorNetwork[0].forward(state_batch)
            action=action.view(state_batch.shape[0],-1)
            for z in range(self.n_agent-1):
                a=self.actorNetwork[z+1].forward(state_batch)
                a=a.view(state_batch.shape[0],-1)
                action=torch.cat([action,a],1)
            '''


            #print(action)
            policy_loss=-self.criticNetwork[i](state_batch,action).double()
            #print(policy_loss)
            policy_loss=policy_loss.mean()
            #print(policy_loss)
            policy_loss.backward(retain_graph=True)
            self.actorOptim[i].step()
            par=list(self.actorNetwork[i].parameters())
            #print('grad')
            #for index,p in enumerate(par):
            #    if index==len(par)-1:
            #        print(p.grad)


            self.__softUpdate(self.targetCriticNetwork[i],self.criticNetwork[i])
            self.__softUpdate(self.targetActorNetwork[i],self.actorNetwork[i])

    def targetUpdate(self):
        for i in range(self.n_agent):
            self.__hardUpdate(self.targetActorNetwork[i],self.actorNetwork[i])
            self.__hardUpdate(self.targetCriticNetwork[i],self.criticNetwork[i])


        
    def add2replaybuff(self,state,action,reward,nstate):
        self.replayBuffer.add(state,action,reward,nstate)

    def actionSelect(self,stateInputs):
        action=[]
        stateInputs=torch.Tensor([stateInputs])
        for i in range(self.n_agent):
            a=self.actorNetwork[i].forward(stateInputs)
            a=a.view(-1)
            a=a.detach().numpy()+self.noise[i].getNoise()
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
    S_LEN=6
    discount=0.9


    obj=Sakuro(S_LEN,S_INFO,AGENT_NUM,BATCH_SIZE,discount)
    timenow=datetime.now()

    episode=2
    for i in range(episode):

        state2Select=np.random.randn(S_INFO*AGENT_NUM,S_LEN)
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
        obj.updateNetwork()
        #print('out')
        #print(out)
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



