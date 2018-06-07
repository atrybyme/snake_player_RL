import numpy as np
import random

class Env():
    height = 6
    width = 6
    snake = [[int((height)/2 - 1),int((width)/2-1)]]
    score = 0
    is_finished=False
    while 1:
        target = [random.randint(0,height - 1),random.randint(0,width - 1)]
        if target!=snake:
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
            
            
                
    def step(self,action_taken):
        self.reward  = 0
        if self.snake !="Terminal":
            end = self.snake[-1]
            if len(self.snake)>1:
                self.snake[1:] = self.snake[0:len(self.snake)-2]
            if action_taken == 'w':
                self.snake[0] = [(self.snake[0])[0]-1, (self.snake[0])[1]]
            elif action_taken == 'a':
                self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]-1]
            elif action_taken == 's':
                self.snake[0] = [(self.snake[0])[0]+1, (self.snake[0])[1]]
            elif action_taken == 'd':
                self.snake[0] = [(self.snake[0])[0], (self.snake[0])[1]+1]
            else:
                act = input("Action taken was invalid.Please take a valid action : 'w,a,s,d' : ")
                return  self.step(act)
            if ((self.snake[0])[0] >= self.height) or ((self.snake[0])[0] < 0) or ((self.snake[0])[1] >= self.width) or ((self.snake[0])[1] < 0):
                self.is_finished = True
            if self.target == self.snake[0]:
                (self.snake).append(end)
                self.target = self.generate_target()
                self.score +=1
                self.reward = 1
            for body_point in self.snake[1:]:
                if self.snake[0] == body_point:
                    self.is_finished = True
                    break
        if self.is_finished == True:
            self.snake = "Terminal"
            if len(self.snake)< self.height * self.width -3 :
                self.reward = -1
    def state(self):
        board = np.zeros((self.height,self.width))
        if self.snake == "Terminal":
            return "Terminal"
        board[(self.snake[0])[0], (self.snake[0])[1]] = 2
        print(self.target)
        board[self.target[0],self.target[1]] = 3
        if len(self.snake)>1 :
            for point in self.snake[1:]:
                board[point[0],point[1]] = 1
        return board
            


            
        

