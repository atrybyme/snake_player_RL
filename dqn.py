import random
import numpy as np
from environment import *
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D
import h5py
import time
import sys
from keras.models import load_model

#game_parameters
action_size = 4
state_size = [7,7]


#model
class DQN_net():
    def __init__(self, state_size, action_size,gamma=0.93,minibatch_size=32):
        self.gamma = gamma
        self.minibatch_size = minibatch_size
        #to determine model size
        self.state_size = state_size
        self.action_size = action_size
        try:
            self.dqn_net = load_model("saved_model_v3_42.h5")
        except:


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
max_memory_len = 50000
memory = deque(maxlen=max_memory_len)
avg_scr = deque(maxlen=100)
episode = 1000000
epsilon = 1
epsilon_decay = 0.998
minimum_epsilon = 0.001

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
    avg_scr.append(game.score)
    if epsilon <= minimum_epsilon:
        epsilon = minimum_epsilon
    if e%1000 == 0 :
        if e >0:
            time_span.append([e, np.sum(avg_scr)/100])
            print(" || Avg Scode of 100 episode after episode" ,'%.3f'%((e/episode)*100), "% : ", np.sum(avg_scr)/100 )
            network.train(memory)
    if e % 40000 == 0:
        save_name = "saved_model_v3_" + str(int(e/40000)) + ".h5"
        network.dqn_net.save(save_name)


network.dqn_net.save("trained_mode.h5")
np.save('time_span_1.npy',np.asarray(time_span))




