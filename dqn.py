import random
import numpy as np
from environment import *
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D
#game_parameters
action_size = 4
state_size = [10,10]


#model
class DQN_net():
    def __init__(self, state_size, action_size,gamma=0.9,epsilon=1.0,epsilon_decay=0.995,epsilon_min=0.01,minibatch_size=16):

        #hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.minibatch_size = minibatch_size

        #to determine model size
        self.state_size = state_size
        self.action_size = action_size
        #Define model
        self.dqn_net = Sequential()
        self.dqn_net.add(Conv2D(16,(1,1),activation='relu',input_shape=(state_size[0],state_size[1],1)))
        self.dqn_net.add(Conv2D(32,(2,2),activation='relu'))
        self.dqn_net.add(Conv2D(64, (3, 3), activation='relu'))
        self.dqn_net.add(Flatten())
        self.dqn_net.add(Dense(128,activation='relu'))
        self.dqn_net.add(Dense(action_size))
        self.dqn_net.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
    
    def train(self,memory):
        x_train = []
        y_train = []
        if len(memory)<=self.minibatch_size :
            ind = np.arange(len(memory))
        else:
            ind = np.random.randint(len(memory),size  = self.minibatch_size)
        for id in ind:
            #sars (state,action,reward,new state )
            x_train.append([(memory[id])[0]])
            y = list(self.dqn_net.predict(np.reshape(np.asarray(x_train[id]).astype(np.float64),(1,self.state_size[0],self.state_size[1],1)))[0])
            if (memory[id])[3] == "Terminal":
                next_max_q = 0.0
            else:
                next_max_q = np.amax(self.dqn_net.predict(np.reshape(np.asarray((memory[id])[3]).astype(np.float64),(1,10,10,1))))
            y[(memory[id])[1]] = float((memory[id])[2]) + self.gamma*next_max_q
            y_train.append(y)
        x_train = np.reshape(np.asarray(x_train).astype(np.float64),(len(ind),self.state_size[0],self.state_size[1],1))
        self.dqn_net.fit(x_train,np.asarray(y_train),batch_size = self.minibatch_size)


