from collections import deque
import random
import numpy as np

SINGLE_S_LEN=3

AGENT_NUM=2
ACTION_DIM=1



class ReplayBuffer(object):
    def __init__(self,max_buffersize,random_seed=42):
        self.max_buffer_size=max_buffersize
        random.seed(random_seed)
        self.count=0
        self.buffer=deque()


    def add(self,s,a,r,s1):
        # input list array
        # output numpy.ndarray
        experience = (s,a,r,s1)
        if self.count < self.max_buffer_size:
            self.buffer.append(experience)
            self.count += 1
        else:
            self.buffer.popleft()
            self.buffer.append(experience)
    def size(self):
        return self.count


    def sample_batch(self, batch_size):
        batch = []

        if self.count < batch_size:
            batch = random.sample(self.buffer, self.count)
        else:
            batch = random.sample(self.buffer, batch_size)


        s_batch = np.array([_[0] for _ in batch],dtype=np.float16)
        a_batch = np.array([_[1] for _ in batch],dtype=np.float16)
        r_batch = np.array([_[2] for _ in batch],dtype=np.float16)
        s1_batch = np.array([_[3] for _ in batch],dtype=np.float16)

        return s_batch, a_batch, r_batch, s1_batch
    def clear(self):
        self.deque.clear()
        self.count = 0

if __name__ == '__main__':
    b=ReplayBuffer(10)
    for i in range(20):
        State=np.random.randn(SINGLE_S_LEN*AGENT_NUM)
        startinfo=np.random.randn(AGENT_NUM)
        a=np.random.randn(AGENT_NUM)
        r=np.random.randn(AGENT_NUM)
        nextstate=np.random.randn(SINGLE_S_LEN*AGENT_NUM)

        b.add(State,a,r,nextstate)
    c=b.sample_batch(3)
    print(c[0])
    print(c[0][:,0:3])
    



