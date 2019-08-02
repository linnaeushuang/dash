
import numpy as np

class OUNoise(object):
    def __init__(self,a_dim,mu=0,theta=0.15,sigma=0.1):
        self.a_dim=a_dim
        self.mu=mu
        self.theta=theta
        self.sigma=sigma

        self.noise=np.ones(self.a_dim)*self.mu

    def reset(self):
        self.noise=np.ones(self.a_dim)*self.mu
    def getNoise(self):
        dx=self.theta*(self.mu-self.noise)+self.sigma*np.random.randn(len(self.noise))
        self.noise=self.noise+dx
        return self.noise

if __name__ =='__main__':
    theta=[0.1,.15,.20,.25,.30,.35]
    sigma=[.1,.2,.3,.4,.5]
    for i in range(5):
        for k in range(5):
            print('theta:'+str(theta[i])+" sigma:"+str(sigma[k]))
            noise=OUNoise(1,theta[i],sigma[k])
            for z in range(5):
                print(noise.getNoise())
