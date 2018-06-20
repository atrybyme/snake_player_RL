from environment import *
import sys
game = Env(6,6)

while 1:
    game.reset()
    b = "New Game"
    sys.stdout.write('\r New Game ')
    while game.state() !="Terminal":
        print(game.state())
        print("Length of snake : ", len(game.snake))
        print("Score : ",game.score)
        act = input("next action : ")
        if act=='w':
            ac=0
        if act == 'a':
            ac = 1
        if act=='s':
            ac=2
        if act == 'd':
            ac = 3
        game.step(ac)

