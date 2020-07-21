# Name :Gia
# Collaborators :

# This file helps you start making tetris pieces, or tetronimoes.

from graphics import *
from time import sleep
import random
dropped_shapes = []
full_row= []
preview = []
b = None
class Block(Rectangle):
    def __init__(self, z, color):
        self.z = z
        self.color = color
        self.point1= Point((self.z.x) * 30, (self.z.y)*30)
        self.point2= Point(self.point1.x +30 , self.point1.y +30)
        Rectangle.__init__(self, self.point1, self.point2)
        self.setFill(color)
        self.setOutline('white')
        self.setWidth(1)
                
    def move_1(self, dx, dy):
        self.move(dx*30, dy*30)
        self.z.x += dx
        self.z.y += dy
    def can_move(self, dx, dy, col, row):
        for blocks in dropped_shapes:
            if blocks.z.x == self.z.x + dx and\
               blocks.z.y == self.z.y + dy:
                return False
        if 0 <= self.z.x + dx < col and 0< self.z.y + dy < row:
            return True
        else:
            return False
        
        
    
class Shape(object):
    def __init__(self, coords, color):
        self.blocks = [Block(coords[0], color), Block(coords[1], color), Block(coords[2],color), Block(coords[3], color)]
    def move_shape(self, dx, dy):
        self.blocks[0].move_1(dx, dy)
        self.blocks[1].move_1(dx,dy)
        self.blocks[2].move_1(dx,dy)
        self.blocks[3].move_1(dx,dy)
        
    def draw_shape(self, win):
        self.blocks[0].draw(win)
        self.blocks[1].draw(win)
        self.blocks[2].draw(win)
        self.blocks[3].draw(win)
    def can_move(self, dx, dy, col, row):
        if self.blocks[0].can_move(dx, dy, col, row) and  self.blocks[1].can_move(dx, dy, col, row) and self.blocks[2].can_move(dx, dy, col, row) and self.blocks[3].can_move(dx, dy, col, row) == True:
            return True
        else:
            return False

class Game(Shape):
    def __init__(self, col, row):
        self.col= col
        self.row= row
        self.win = GraphWin("Game", self.col*30, self.row*30)
        self.p_window = GraphWin("Preview", self.col*15, self.row*15)
        self.letter = None
        self.key = None
        self.win.bind_all('<Key>', self.key_pressed)
        self.pause = Text(Point((self.col*30)/2, (self.row*30)/2),"The game is paused. Type c to continue")
        self.pause.draw(self.win)
        self.pause.setTextColor("black")
        self.z = 0
    def key_pressed(self, event):
        self.key = event.keysym
        self.handle_keypress()
    def handle_keypress(self):
        if self.key == "Left" and self.letter.can_move(-1, 0, self.col, self.row)==True:
             self.letter.move_shape(-1,0)
             self.key = None
        if self.key == "Right" and self.letter.can_move(1, 0, self.col, self.row)==True:
             self.letter.move_shape(1,0)
             self.key = None
        if self.key == "Down" and self.letter.can_move(0, 3, self.col, self.row)==True:
             self.letter.move_shape(0,3)
             self.key = None
        if self.key =="Up":
            self.letter.rotate(self.col, self.row)
            self.key = None
        if self.key == "p":
            if self.z == 1:
                self.letter.blocks[0].move_1(0,-1)
            self.z+=1
            self.pause.setTextColor("white")
            time.sleep(.2)
            self.win.after(0, self.handle_keypress)
        if self.key == "c":
            self.key = None
            self.z = 0
            self.letter.blocks[0].move_1(0,1)
            self.pause.setTextColor("black")



    def get_letter(self):
        global preview
        if self.z == 0:
            a = random.randint(0, 6)
            b = random.randint(0,6)
            shape_1 = shape_letter_list[a]
            shape_2 = shape_letter_list[b]
            preview.append(shape_1)
            preview.append(shape_2)
            self.z = 1
        elif self.z == 1:
            c = random.randint(0,6)
            shape = shape_letter_list[c]
            preview.append(shape)
        
    def lets_move(self):
        if self.letter.can_move(0, 1, self.col, self.row) == True:
                self.letter.move_shape(0,1)
                self.win.after(300, self.lets_move)
        else:
            global dropped_shapes
            dropped_shapes = dropped_shapes + self.letter.blocks[:]
            self.win.after(100, self.add_drop_shape, preview[0])
    def add_drop_shape(self, shape):
        if self.game_over() == False:
            global shape_dic
            self.letter = shape_dic[shape](Point((self.col)/2, 0))
            self.letter.draw_shape(self.win)
            self.lets_move()
            self.check_row()
            self.get_letter()
            global b
            b = self.preview_block(b)
            preview.pop(0)
        if self.game_over() == True:
            for item in dropped_shapes:
                    item.undraw()
            game_over = Text(Point((self.col*30)/2, (self.row*30)/2), "Game Over")
            game_over.draw(self.win)
            game_over.setTextColor("white")
            game_over.setSize(18)
    def check_row(self):
        for rows in range(self.row):
            empty_row= []
            global dropped_shapes
            for b in dropped_shapes:
                if b.z.y == rows:
                    empty_row.append(b)
            if len(empty_row) == self.col:
                for item in empty_row:
                    item.undraw()
                    dropped_shapes.remove(item)
                for items in dropped_shapes:
                    if items.z.y < rows:
                        items.move_1(0,1)
    def preview_block(self, a):
        global shape_dic
        if a != None:
            for block in a.blocks:
                block.undraw()
        if a == None:
            p_text = Text(Point((self.col*15)/2, (self.row)), "Next Block")
            p_text.setTextColor('white')
            p_text.draw(self.p_window)
        a =shape_dic[preview[1]](Point((2), (2)))
        a.draw_shape(self.p_window)
        self.p_window.setBackground('black')
        return a
    def game_over(self):
        for b in dropped_shapes:
            if b.z.y == 0:
                return True
        return False
        
            
x = 0            
class I_shape(Shape):
   def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x  +  2,  center.y)]
     Shape.__init__(self,  coords,  "cyan")
     self.center_block = self.blocks[1]
     self.x = 0
     
   def rotate(self, col, row):
        if self.x == 0:
            if self.blocks[0].can_move(1, -1, col, row) and self.blocks[2].can_move(-1, 1, col, row) and self.blocks[3].can_move(-2, 2, col, row)== True:
                self.blocks[0].move_1(1, -1)
                self.blocks[2].move_1(-1, 1)
                self.blocks[3].move_1(-2, 2)
                self.x +=1
        elif self.x == 1:
            if self.blocks[0].can_move(-1, 1, col, row) and self.blocks[2].can_move(1, -1, col, row) and self.blocks[3].can_move(2, -2,  col, row) == True:
                self.blocks[0].move_1(-1, 1)
                self.blocks[2].move_1(1, -1)
                self.blocks[3].move_1(2, -2)
                self.x = 0
class J_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  +  1,  center.y),
                 Point(center.x  +  1,  center.y +1)]
     Shape.__init__(self,  coords,  "lightpink")
     self.center_block = self.blocks[1]
     self.x = 0

    def rotate(self, col, row):
        if self.x == 0:
            if self.blocks[0].can_move( 1, -1,  col, row) and self.blocks[2].can_move( -1, 1,  col, row) and self.blocks[3].can_move( -2, 0,  col, row)== True: 
                self.blocks[0].move_1(1,-1)
                self.blocks[2].move_1(-1, 1)
                self.blocks[3].move_1(-2, 0)
                self.x = self.x + 1
        elif self.x == 1:
            if self.blocks[0].can_move( 1, 1,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( 0, -2,  col, row)== True: 
                self.blocks[0].move_1(1,1)
                self.blocks[2].move_1(-1,-1)
                self.blocks[3].move_1(0, -2)
                self.x += 1
        elif self.x==2:
            if self.blocks[0].can_move( -1, 1,  col, row) and self.blocks[2].can_move( 1, -1,  col, row) and self.blocks[3].can_move( 2, 0,  col, row)== True: 
                self.blocks[0].move_1(-1, 1)
                self.blocks[2].move_1(1, -1)
                self.blocks[3].move_1(2, 0)
                self.x += 1
        elif self.x==3:
            if self.blocks[0].can_move( -1, -1,  col, row) and self.blocks[2].can_move( 1, 1,  col, row) and self.blocks[3].can_move( 0, 2,  col, row)== True: 
                self.blocks[0].move_1(-1, -1)
                self.blocks[2].move_1(1, 1)
                self.blocks[3].move_1(0, 2)
                self.x =0
     
class L_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  +  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  -  1,  center.y),
                 Point(center.x  -1,  center.y+1)]
     Shape.__init__(self,  coords,  "lightseagreen")
     self.center_block = self.blocks[1]
     self.x = 0

    def rotate(self, col, row):
        if self.x==0:
            if self.blocks[0].can_move( -1, 1,  col, row) and self.blocks[2].can_move( 1, -1,  col, row) and self.blocks[3].can_move( 0, -2,  col, row)== True: 
                self.blocks[0].move_1(-1,1)
                self.blocks[2].move_1(1,-1)
                self.blocks[3].move_1(0, -2)
                self.x +=1
        elif self.x ==1:
            if self.blocks[0].can_move( -1, -1,  col, row) and self.blocks[2].can_move( 1, 1,  col, row) and self.blocks[3].can_move( 2, 0,  col, row)== True: 
                self.blocks[0].move_1(-1,-1)
                self.blocks[2].move_1(1,1)
                self.blocks[3].move_1(2,0)
                self.x+= 1
        elif self.x == 2:
            if self.blocks[0].can_move( 1, -1,  col, row) and self.blocks[2].can_move( -1, 1,  col, row) and self.blocks[3].can_move( 0, 2,  col, row)== True: 
                self.blocks[0].move_1(1,-1)
                self.blocks[2].move_1(-1,1)
                self.blocks[3].move_1(0, 2)
                self.x+= 1
        elif self.x == 3:
            if self.blocks[0].can_move( 1, 1,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( -2, 0,  col, row)== True: 
                self.blocks[0].move_1(1, 1)
                self.blocks[2].move_1(-1, -1)
                self.blocks[3].move_1(-2, 0)
                self.x = 0
class O_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x  -  1,  center.y +1),
                 Point(center.x  ,  center.y+1)]
     Shape.__init__(self,  coords,  "palevioletred")
     self.center_block = self.blocks[1]
     self.x = 0

    def rotate(self):
        pass
class S_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y+1),
                 Point(center.x  ,  center.y),
                 Point(center.x  ,  center.y+1),
                 Point(center.x  +1,  center.y)]
     Shape.__init__(self,  coords,  "teal")
     self.center_block = self.blocks[1]
     self.x=0

    def rotate(self, col, row):
        if self.x == 0:
            if self.blocks[0].can_move( 0, -2,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( -1, 1,  col, row)== True: 
                self.blocks[0].move_1(0,-2)
                self.blocks[2].move_1(-1, -1)
                self.blocks[3].move_1(-1, 1)
                self.x +=1
        elif self.x ==1:
            if self.blocks[0].can_move( 0, 2,  col, row) and self.blocks[2].can_move( 1, 1,  col, row) and self.blocks[3].can_move( 1, -1,  col, row)== True: 
                self.blocks[0].move_1(0,2)
                self.blocks[2].move_1(1, 1)
                self.blocks[3].move_1(1, -1)
                self.x= 0
class T_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x ,  center.y +1),
                 Point(center.x  +  1,  center.y)]
     Shape.__init__(self,  coords,  "plum")
     self.center_block = self.blocks[1]
     self.x = 0

    def rotate(self, col, row):
        if self.x == 0:
            if self.blocks[0].can_move( 1, -1,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( -1, 1,  col, row)== True: 
                self.blocks[0].move_1(1,-1)
                self.blocks[2].move_1(-1, -1)
                self.blocks[3].move_1(-1, 1)
                self.x += 1
        elif self.x == 1:
            if self.blocks[0].can_move( 1, 1,  col, row) and self.blocks[2].can_move( 1, -1,  col, row) and self.blocks[3].can_move( -1, -1,  col, row)== True: 
                self.blocks[0].move_1(1,1)
                self.blocks[2].move_1(1, -1)
                self.blocks[3].move_1(-1, -1)
                self.x += 1
        elif self.x ==2:
            if self.blocks[0].can_move( -1, 1,  col, row) and self.blocks[2].can_move( 1, 1,  col, row) and self.blocks[3].can_move( 1, -1,  col, row)== True:
                self.blocks[0].move_1(-1,1)
                self.blocks[2].move_1(1, 1)
                self.blocks[3].move_1(1, -1)
                self.x += 1
        elif self.x == 3:
            if self.blocks[0].can_move( -1, -1,  col, row) and self.blocks[2].can_move( -1, 1,  col, row) and self.blocks[3].can_move( 1, 1,  col, row)== True:
                self.blocks[0].move_1(-1,-1)
                self.blocks[2].move_1(-1, 1)
                self.blocks[3].move_1(1, 1)
                self.x = 0 
                
                
class Z_shape(Shape):
    def  __init__(self, center):
     coords  =  [Point(center.x  -  1,  center.y),
                 Point(center.x  ,  center.y),
                 Point(center.x ,  center.y+1),
                 Point(center.x  +  1,  center.y+1)]
     Shape.__init__(self,  coords,  "lightsteelblue")
     self.center_block = self.blocks[1]
     self.x = 0

    def rotate(self, col, row):
        if self.x ==0:
            if self.blocks[0].can_move( 1, -1,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( -2, 0,  col, row)== True:
                self.blocks[0].move_1(1, -1)
                self.blocks[2].move_1(-1, -1)
                self.blocks[3].move_1(-2,0)
                self.x +=1
        elif self.x == 1:
            if self.blocks[0].can_move( 1, -1,  col, row) and self.blocks[2].can_move( -1, -1,  col, row) and self.blocks[3].can_move( 2, 0,  col, row)== True:
                self.blocks[0].move_1(-1, 1)
                self.blocks[2].move_1(1, 1)
                self.blocks[3].move_1(2,0)
                self.x = 0
shape_dic = {"I": I_shape, "J": J_shape, "L": L_shape, "O":O_shape, "S":S_shape, "T":T_shape, "Z":Z_shape}


game = Game(10,18)
game.win.setBackground('black')
shape_letter_list = ["I","J","L","O","S","T","Z"]
a = random.randint(0, 6)
shape = shape_letter_list[a]
game.add_drop_shape(shape)



game.win.mainloop()
