import random
from ship import Ship
from board import Board
from position import Position
import numpy as np


# This is a naive implementation of a Player class that:
# 1. Sets up the same board every time (i.e. a static layout)
# 2. Fires randomly, without remembering which shots were hits and misses
class Player:

    # Each player has a name. There should be no need to change or delete this!
    def __init__(self, name):
        self.__name = name
        self.__results = []
        self.prob_board = np.zeros((10,10)).astype(np.int32)
        self.stat_board = np.zeros((10,10)).astype(np.int32)
        self.hits = []
        self.shot = 0
        self.hustler_flag = True
        self.seeker_flag = False
        self.sinker_flag = False
        self.reverse = False
        self.board_size = [5,4,3,3,2]
        self.seek_list = []
        self.flow = [1,-1]
        self.ship_hit_count = 2
    def get_name(self):
        return self.__name

    def __str__(self):
        return self.get_name()

    # get_board should return a Board object containing 5 ships:
    # 1 aircraft carrier (length = 5)
    # 1 battleship (length = 4)
    # 1 cruiser (length = 3)
    # 1 submarine (length = 3)
    # 1 destroyer (length = 2)
    # You can make your own fun names for the ships, but the number and lengths
    # of the ship will be validated by the framework. Printing the board will
    # show the first letter of each ship's name.

    # This implementation returns the first sample layout from this web page:
    # http://datagenetics.com/blog/december32011/index.html
    def get_board(self):
        ships_list = [Ship('Paach', Position('C', 1), 5, True),
                      Ship('Char', Position(‘F’, 1), 4, True),
                      Ship('Ten', Position('D', 6), 3, False),
                      Ship('Ten', Position('F', 6), 3, True),
                      Ship('Do', Position(‘I’, 3), 2, False)]
        return Board(ships_list)

    # Takes a random shot, making no effort to remember it
    def next_shot(self):
#        row = chr(64 + random.randint(1, 10))  # A - J
#        col = random.randint(1, 10)
        if self.shot != 0:
            self.hit_flag = self.__results[self.shot-1][1]
            self.sink_flag = self.__results[self.shot-1][2]
            if self.hit_flag:
                self.stat_board[self.hit_row,self.hit_column] = 2
            #print(self.hit_flag,self.sink_flag,'h','s')
           # print(self.sinker_flag,self.seeker_flag,self.hustler_flag) 
            #print(self.shot)
            if self.sink_flag:
                self.hustler_flag = True
                self.seeker_flag = False
                self.sinker_flag = False
                #print(self.board_size)
                #self.board_size.remove(self.ship_hit_count)
                #self.ship_hit_count = 2
                self.seek_list = []
            elif self.sinker_flag and self.reverse and not self.hit_flag:
                self.hustler_flag = False
                self.seeker_flag = True
                self.sinker_flag = False
            
            elif (self.sinker_flag or self.seeker_flag) and self.hit_flag:
                self.hustler_flag = False
                self.seeker_flag = False
                self.sinker_flag = True
                self.ship_hit_count +=1
            elif self.sinker_flag and not self.hit_flag :
                self.hustler_flag = False
                self.seeker_flag = False
                self.sinker_flag = True
                self.reverse = True
                
            elif self.seeker_flag or self.hit_flag:
                self.hustler_flag = False
                self.seeker_flag = True
                self.sinker_flag = False
                self.reverse = False
            else:
                self.hustler_flag = True
                
       # print(self.seeker_flag,self.hustler_flag)
        if self.sinker_flag:
            self.sinker()
        elif self.seeker_flag:
           # print('seek')
            self.seeker()
        elif self.hustler_flag: # make else 
            #print('HERE')
            self.hustler()
        #print('he')   
        self.hits.append(str(self.hit_row)+str(self.hit_column))
        self.stat_board[self.hit_row,self.hit_column] += 1
        row = chr(64 + self.hit_row + 1)
        col = self.hit_column+1
        #print([row,col])
        #print(self.hits)
        print('hit',[self.hit_row,self.hit_column])
        self.shot += 1
        return Position(row, col)

    
    def seeker(self):
        print('seeker')
        for i in self.flow:#boundry conditions
                    
            if (self.hus_row + i) not in range(0,9) or self.stat_board[self.hus_row + i,self.hus_column] >0 :
                self.seek_list.append('R'+ str(i))
                
                
            if (self.hus_column + i) not in range(0,9)or self.stat_board[self.hus_row,self.hus_column + i]>0:
                self.seek_list.append('C'+ str(i))
            
        
        if self.hit_row <5:
            
            for j in self.flow:
           
                
                if ('R'+ str(j)) not in self.seek_list:
                    self.seek_row = self.hus_row + j
                    self.seek_list.append('R'+ str(j))
                    self.hit_row = self.seek_row
                    self.hit_column = self.hus_column
                    self.r_direction = j
                    self.c_direction = 0
                    return
                    
                elif ('C'+ str(j)) not in self.seek_list:
                    self.seek_column = self.hus_column + j
                    self.seek_list.append('C'+ str(j))
                    self.hit_column = self.seek_column
                    self.hit_row = self.hus_row
                    self.r_direction = 0
                    self.c_direction = j
                    return
        else: 
            for j in [-1,1]:
                
                if ('R'+ str(j)) not in self.seek_list:
                    self.seek_row = self.hus_row + j
                    self.seek_list.append('R'+ str(j))
                    self.hit_row = self.seek_row
                    self.hit_column = self.hus_column
                    self.r_direction = j
                    self.c_direction = 0
                    return
                    
                elif ('C'+ str(j)) not in self.seek_list:
                    self.seek_column = self.hus_column + j
                    self.seek_list.append('C'+ str(j))
                    self.hit_column = self.seek_column
                    self.hit_row = self.hus_row
                    self.r_direction = 0
                    self.c_direction = j
                    return
            
                
                        
                
    def sinker(self):
        print('sinker')
        
        if self.hit_row +self.r_direction not in range (0,10):
            self.reverse = True
            print('here') 
        if self.hit_column + self.c_direction not in range(0,10):
            self.reverse = True
            print('here') 
        
        if not self.reverse  :  
                self.hit_row = self.hit_row + self.r_direction
           
                self.hit_column = self.hit_column + self.c_direction
                print('not reverse') 
             
        else:
            self.sinker_row = self.hit_row - self.r_direction
            self.sinker_column = self.hit_column - self.c_direction
            self.hit_row = self.sinker_row
            self.hit_column = self.sinker_column
            print(self.reverse)
            if self.stat_board[self.hit_row,self.hit_column] > 0:
                print(self.stat_board)
                print(self.reverse)
                print([self.hit_row,self.hit_column])
                self.sinker()
            print(self.hit_row,self.hit_column)
        
#               

 #self.reverse = False
#            else:
#                self.sinker_row = self.hit_row - self.r_direction 
#                self.sinker_column = self.hit_column - self.c_direction
#              
        
#       # print([self.hit_row,self.hit_column],'sink')
#        if self.stat_board[self.hit_row,self.hit_column] != 0:
#            
#            #print('new sink',[self.hit_row,self.hit_column])
#            #print(self.stat_board)
#            self.sinker()
#            
#            
  
    def hustler(self):
        print('hustling')
        self.prob_board = np.zeros((10,10)).astype(np.int32)
        
        for size in self.board_size:
            for row in range(0,10):
                for col in range(0,10):
                    if (row + size) <= 10:
                        can_place = True
                        for i in range(size):
                            if self.stat_board[row +i,col] > 0:
                                
                                can_place = False
                        if can_place:       
                            for i in range(size):
                                self.prob_board[row +i,col] += 1
                                
                    if (col + size) <= 10:
                        can_place = True
                        for i in range(size):
                            if self.stat_board[row,col+i] > 0:
                                
                                can_place = False
                        if can_place: 
                            for i in range(size):
                            
                                self.prob_board[row,col+i] += 1
        hustle_hit =np.where(self.prob_board == np.max(self.prob_board))
        rand = random.randint(0,len(hustle_hit)-1)
        if np.size(hustle_hit) == 2:
            self.hus_row = hustle_hit[0][0]
            self.hus_column = hustle_hit[1][0]
        else:
            self.hus_row = hustle_hit[0][rand]
            self.hus_column = hustle_hit[1][rand]
            
        self.hit_row = self.hus_row
        self.hit_column = self.hus_column
   
       # print(self.prob_board)
    # result is a tuple consisting of:
    # - the shot location (a Position object)
    # - whether the shot was a hit (True) or a miss (False)
    # - whether a ship was sunk (True) or not (False)
         
    def post_shot_result(self, result):
        self.__results.append(result)
