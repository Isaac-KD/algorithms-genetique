class Snake():
    """
    Classe permettant de gere le serpent. le body represent la pile d'execustion des mouvement de chaque parti du corps.
    
    < Methodes > :
        add_mouvement(self,pos)->None :  ajoute un mouvement a la pile d'execustion des diiferent parti du body, qui ce fera ajuster par refresh par la suite.
        refresh(self)->None : refresh la pile d'execustion des different parti du body
        eat(self)->None: fait grandire le serpend de 1.
        bitten(self ): Verifie si le serpend c'est mordue 
    """
    def __init__(self,pos1,pos2,pos3) -> None:
        self.body = [[pos1],[pos2,pos1],[pos3,pos2,pos1]]
        
    def length(self)->int:   
        return len(self.body) 
    
    def head(self):
        return self.body[0][0] 
    
    def tail(self):
        return self.body[len(self.body)-1][0]
    
    def add_mouvement(self,pos)->None:
        for i in range(len(self.body)):
            self.body[i].append(pos)
        
    def refresh(self)->None:
        for i in range(len(self.body)):
            self.body[i].pop(0)
            
    def left(self)->None:
        x,y = self.head()
        self.add_mouvement((x+1,y))
        self.refresh()
    
    def right(self)->None:
        x,y = self.head()
        self.add_mouvement((x-1,y))
        self.refresh()
            
    def top(self)->None:
        x,y = self.head()
        self.add_mouvement((x,y+1))
        self.refresh()
               
    def bottom(self)->None:
        x,y = self.head()
        self.add_mouvement((x,y-1))   
        self.refresh()
                    
    def print(self)->None:
        print(self.body,"\n")
    
    def eat(self)->None:
        l = self.body[len(self.body)-1].copy()
        x,y=l[0]
        l.insert(0,(x,y-1))
        self.body.append(l)

    def bitten(self ):
        x,y = self.head()
        for i in range(1,len(self.body)):
            if self.body[i][0] == (x,y) : return True
        return False
            
def snake_test():
    """
    Creat a snake for train assert
    """
    return Snake((6,6),(5,6),(4,6))

if __name__ == "__main__":
    snake = snake_test()
    snake.print()
    snake.left()
    snake.left()
    #snake.top()
    #snake.top()
    snake.eat()
    snake.print()