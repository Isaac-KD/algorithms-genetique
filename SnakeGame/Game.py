from SnakeGame.Snake import Snake
#from Snake import Snake
import random
import numpy as np

class Game():
    def __init__(self,length=11):
        self.length = length
        self.score=0
        self.time_not_eat=0
        self.appel_in_map = False
        self.appel_pos =(-1,-1)
        self.map = [ [0 for _ in range(self.length)] for _ in range(self.length)]
        mid = self.length//2
        self.snake = Snake((mid,mid),(mid,mid-1),(mid,mid-2))
        self.refresh_snake()
    
    def add_appel(self)-> None:
        x = random.randint(0,self.length-1)
        y = random.randint(0,self.length-1)
        if self.map[x][y] !=0: return
        self.appel_pos = (x,y)
        self.appel_in_map = True
        self.map[x][y]= 2
        
    def check_snake_eat(self)-> None:    
        if  self.snake.head() == self.appel_pos:
            self.snake.eat()
            self.appel_in_map = False
            self.appel_pos = (-1,-1)
            self.score+=1
            self.time_not_eat = 0
        
        
    def refresh_snake(self)-> None:
        for body in self.snake.body:
            x,y = body[0]
            self.map[x][y] = 1
     
    def delete_snake(self)-> None:
        for body in self.snake.body:
            x,y = body[0]
            self.map[x][y] = 0      
            
    def print_map(self)-> None:
        for x in range(len(self.map)-1, -1, -1):
            for y in range(len(self.map)-1, -1, -1):
                print(self.map[y][x],end = " ")
            print()
    
    def choose(self)-> None:
        value = input()
        if value == "d": self.snake.right()
        elif value == "s": self.snake.bottom()
        elif value == "q": self.snake.left()
        else: self.snake.top()
        
    def model_choose(self,value)-> None:
        if value == 3: self.snake.right()
        elif value == 1: self.snake.bottom()
        elif value == 2: self.snake.left()
        elif value == 0: self.snake.top()
        
    def mouve(self) -> bool:
        self.delete_snake()
        self.choose()
        x,y = self.snake.head()
        if x<=self.length-1 and x>=0 and y<=self.length-1 and y>=0 and not self.snake.bitten():
            self.refresh_snake(); return True
        return False
    
    def model_mouve(self,action) ->bool:
        self.delete_snake()
        self.model_choose(action)
        x,y = self.snake.head()
        if x<=self.length-1 and x>=0 and y<=self.length-1 and y>=0 and not self.snake.bitten():
            self.refresh_snake(); return True
        return False
    
    def run(self)-> int:
        self.print_map()
        alive=1
        while alive:
            alive = self.mouve()
            self.check_snake_eat()
            if not self.appel_in_map: self.add_appel()
            self.print_map()
        
        print("       GAME OVER       ")
        return -1
     
    def run_model(self,model)-> int:
        alive = 1
        self.score = 0
        while alive:
            self.time_not_eat+=1
            if self.time_not_eat>=11*12: return 0
            state = np.array(self.map)
            state = state.flatten()
            action = np.argmax(model.predict(np.array([state])))
            alive = self.model_mouve(action)
            self.check_snake_eat()
            if not self.appel_in_map: self.add_appel()
            self.print_map()
        return self.score
            
                    
if __name__ == "__main__":
    game = Game()
    game.run()