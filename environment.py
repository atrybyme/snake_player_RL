import numpy as np
import random

class Env():
    def __init__(self,h,w):
        self.height = h
        self.width = w
        self.snake = [[int((self.height)/2),int((self.width)/2)]]
        self.is_finished=False
        self.last_action = -1
        while 1:
            self.target = [random.randint(0,self.height - 1),random.randint(0,self.width - 1)]
            if self.target!=self.snake:
                break
    def generate_target(self):
        target = [random.randint(0, self.height - 1),
                  random.randint(0, self.width - 1)]
        body = 0
        while body < (len(self.snake)):
            if target == self.snake[body]:
                break
            else:
                body = body+1
        if body == len(self.snake):
            return target
        else:
            return self.generate_target()

    reward = 0


    def reset(self):
        self.snake = [[int((self.height)/2 - 1), int((self.width)/2-1)]]
        self.score = 0
        self.target = self.generate_target()
        self.is_finished = False
        self.reward = 0
        self.last_action  = -1
            
                
    def step(self,action_taken):
        self.reward  = 0.0
        if self.snake !="Terminal":
            #head = self.snake[0]
            #if len(self.snake)==1:
            #    neck = [200,200]
            #else:
             #   neck =self.snake[1]
            end = self.snake[-1]
            if len(self.snake)>1:
                self.snake[1:] = self.snake[0:len(self.snake)-2]
            # w==0==up
            if action_taken == 0:
                if self.last_action==2:
                    self.snake[0] = [(self.snake[0])[0]+1, (self.snake[0])[1]]
                else:
                    self.snake[0] = [(self.snake[0])[0]-1, (self.snake[0])[1]]
                    self.last_action = 0
            # a==1==left
            if action_taken == 1:
                if self.last_action==3:
                    self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]+1]
                else:
                    self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]-1]
                    self.last_action=1
            # s==2==down
            if action_taken == 2:
                if self.last_action==0:
                    self.snake[0] = [(self.snake[0])[0]-1, (self.snake[0])[1]]
                else:
                    self.snake[0] = [(self.snake[0])[0]+1, (self.snake[0])[1]]
                    self.last_action=2
            #self==3==right
            if action_taken == 3:
                if self.last_action==1:
                    self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]-1]
                else:
                    self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]+1]
                    self.last_action=3
            if ((self.snake[0])[0] >= self.height) or ((self.snake[0])[0] < 0) or ((self.snake[0])[1] >= self.width) or ((self.snake[0])[1] < 0):
                self.is_finished = True
            if self.target == self.snake[0]:
                (self.snake).append(end)
                self.target = self.generate_target()
                self.score +=1.0
                self.reward = 1.0
            for body_point in self.snake[1:]:
                if self.snake[0] == body_point:
                    self.is_finished = True
                    break
        if self.is_finished == True:
            self.snake = "Terminal"
            if len(self.snake)< self.height * self.width -3 :
                self.reward = -1.0
    def state(self):
        board = np.zeros((self.height,self.width))
        if self.snake == "Terminal":
            return "Terminal"
        board[(self.snake[0])[0], (self.snake[0])[1]] = 2
        board[self.target[0],self.target[1]] = 3
        if len(self.snake)>1 :
            for point in self.snake[1:]:
                board[point[0],point[1]] = 1
        return board
            


            
        

