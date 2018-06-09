import random
import numpy as np
from environment import *
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D
import h5py
import time
import sys
#game_parameters
action_size = 4
state_size = [5,5]


#model
class DQN_net():
    def __init__(self, state_size, action_size,gamma=0.945,minibatch_size=32):

        #hyperparameters
        self.gamma = gamma
        self.minibatch_size = minibatch_size

        #to determine model size
        self.state_size = state_size
        self.action_size = action_size
        #Define model
        self.dqn_net = Sequential()
        self.dqn_net.add(Conv2D(16,(1,1),activation='relu',input_shape=(state_size[0],state_size[1],1)))
        self.dqn_net.add(Conv2D(32,(2,2),activation='relu'))
        self.dqn_net.add(Conv2D(32, (3, 3), activation='relu'))
        self.dqn_net.add(Flatten())
        self.dqn_net.add(Dense(128,activation='relu'))
        self.dqn_net.add(Dense(64, activation='relu'))
        self.dqn_net.add(Dense(action_size))
        self.dqn_net.compile(loss='mse', optimizer='rmsprop', metrics=['accuracy'])
    
    def train(self,memory):
        x_train = []
        y_train = []
        if len(memory)<=self.minibatch_size :
            ind = np.arange(len(memory))
        else:
            ind = np.random.randint(len(memory),size  = self.minibatch_size)
        tp = 0
        for id in ind:
            #sars (state,action,reward,new state )
            x_train.append([(memory[id])[0]])
            #print((self.dqn_net.predict(np.reshape(np.asarray(x_train[tp]).astype(
             #   np.float64), (1, self.state_size[0], self.state_size[1], 1)))[0]))
            y = list(self.dqn_net.predict(np.reshape(np.asarray(x_train[tp]).astype(np.float64),(1,self.state_size[0],self.state_size[1],1)))[0])
            if (memory[id])[3] == "Terminal":
                next_max_q = 0.0
            else:
                next_max_q = np.amax(self.dqn_net.predict(np.reshape(np.asarray((memory[id])[3]).astype(np.float64), (1,self.state_size[0], self.state_size[1], 1))))
            y[(memory[id])[1]] = float((memory[id])[2]) + self.gamma*next_max_q
            y_train.append(y)
            tp = tp+1
        x_train = np.reshape(np.asarray(x_train).astype(np.float64),(len(ind),self.state_size[0],self.state_size[1],1))
        self.dqn_net.fit(x_train,np.asarray(y_train),batch_size = self.minibatch_size,verbose=0)

game = Env(state_size[0],state_size[1])
max_memory_len = 100000
memory = deque(maxlen=max_memory_len)
episode = 1000000
epsilon = 1.0
epsilon_decay = 0.99
minimum_epsilon = 0.002
network = DQN_net(state_size,action_size)
time_span = []
for e in range(episode):
    game.reset()
    state = game.state()
    t=0
    while np.sum(state !="Terminal"):
        t=t+1
        sars = []
        sars.append(state)
        if random.random()<epsilon:
            action = random.randint(0,3)
        else:
            action = np.argmax(network.dqn_net.predict(np.reshape(np.asarray(state).astype(np.float64), (1,state_size[0],state_size[1] ,1))))
        game.step(action)
        sars.append(action)
        sars.append(game.reward)
        state = game.state()
        sars.append(state)
        memory.append(sars)
        b =  "Time step without dying: " + str(t)
        sys.stdout.write('\r'+b)
    epsilon = epsilon_decay*epsilon
    if epsilon <= minimum_epsilon:
        epsilon = minimum_epsilon
    if e%100 == 0 :
        time_span.append([t,game.score])
        print(" || Total Scode of after episode" ,'%.3f'%((e/episode)*100), "% : ", game.score )
        network.train(memory)
    if e % 40000 == 0:
        save_name = "saved_model" + str(int(e/40000)) + ".h5"
        network.dqn_net.save(save_name)


network.dqn_net.save("trained_mode.h5")
np.save('time_span.npy',np.asarray(time_span))




