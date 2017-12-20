#kivy conways app
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.clock import Clock

#the size of the grid
SIZE = 40
#the values that need to be added to the row and column values to
#find all the cells in the 8 surrounding cells
NEIGHBOURS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

GRID = []
#makes the grid full of zeros and the right size.
for row in range(SIZE):
    temp = []
    for column in range(SIZE):
        temp.append(0)
    GRID.append(temp)



#the main (root) widget - a box layout that contains
#my grid of circles and the layout holding the buttons

class MyLayout(BoxLayout):
    #one function fills the GRID with 120 randomly placed  living cells
    def random_gen(self):
        global GRID, SIZE
        GRID = [[0 for x in range(SIZE)] for y in range(SIZE)]
        for i in range(120):
            GRID[random.randint(0,SIZE-1)][random.randint(0,SIZE-1)] = 1
        #this line updates the grid of circles according to the new living cells
        self.mywidge.update_canvas()
        
    #this function puts living cells in specific places to make a generator
    #you can alter this (or add another button) to put another stable formation in
    def generator(self):
        global GRID
        GRID = []
        #makes the grid full of zeros again.
        for row in range(SIZE):
            temp = []
            for column in range(SIZE):
                temp.append(0)
            GRID.append(temp)
        gen_coords = [(1,25),
                      (2,23),(2,25),
                      (3,13),(3,14),(3,21),(3,22),(3,35),(3,36),
                      (4,12),(4,16),(4,21),(4,22),(4,35),(4,36),
                      (5,1),(5,2),(5,11),(5,17),(5,21),(5,22),
                      (6,1),(6,2),(6,11),(6,15),(6,17),(6,18),(6,23),(6,25),
                      (7,11),(7,17),(7,25),
                      (8,12),(8,16),
                      (9,13),(9,14)]
        for cell in gen_coords:
            r,c = cell
            GRID[r][c]=1
        #this line updates the grid of circles according to the new living cells
        self.mywidge.update_canvas()
        

        


class MyWidget(Widget):
    #this is the widget that draws the circles on the screen

    def update_canvas(self):
        global GRID, SIZE
        
        #the height of the cell is the height of the widget over the size of the grid rounded down (// takes only the integer bit)
        cellheight = self.height//SIZE
        #cellwidth is the same as height for this implementation but could be changed to different if you want
        cellwidth = cellheight
        start = 0
        #start the circles from the point 0,0
        x = start
        y = start

        #wipe the canvas clean
        self.canvas.clear()
        
        with self.canvas:
            # in the canvas
            for r in range(SIZE):
                #loop through the rows
                for c in range(SIZE):
                    #loop through the columns
                    #if the cell in the GRID is alive the circle should be green
                    if GRID[r][c]==1:
                        #green colour
                        Color(0.13,0.55,0.13)
                    else:
                        #grey colour
                        Color(0.5,0.5,0.5,0.5)
                    #draw a circle 
                    Ellipse(pos = (x,y), size = (cellwidth,cellheight))
                    #add the width to go to the next position to draw the next circle
                    x+=cellwidth
                #go to the next row
                y+=cellheight
                #and set the x value back to the beginning
                x=start

class ConwaysApp(App):
    #this is the app
        
    def build(self):
        #give the app a new attribute called mL which is a new MyLayout object
        self.mL = MyLayout()
        #you used this in the clock app, this sets the delay of .2 of a second and it keeps running the tick function
        Clock.schedule_interval(self.tick, 0.2)
        
        return self.mL

    def getNeighbours(self,r,c):
        #this function counts the number of living neighbours of a cell
        global GRID
        count=0
        for n in NEIGHBOURS:
            nr,nc = n
            if r+nr <SIZE and c+nc < SIZE:
                #this if test that the neighbour is on the board
                count+=GRID[(r+nr)][(c+nc)]
        return count

    def tick(self,dt):
        #this is what happens every time the clock ticks for .2 of a second
        global GRID
        #this next line is solving a problem. we don't want to update the live GRID because the changes we make will influence the rest of the board so nwe need a copy
        #Because of how python does things gridcopy = GRID doesn't actually make a copy of GRID, it points another variable name to the same memory address
        #There are reasons for this which you can learn but don't need to know. This following line does a proper copy.
        gridcopy = [row[:] for row in GRID]
        rowcount = 0
        #this next section checks the current living and dead values in the GRID and updates the copy of the grid
        for row in GRID:
            colcount = 0
            for col in row:
                r = rowcount
                c = colcount
                if self.isAlive(GRID[r][c],r,c):
                    gridcopy[r][c]=1
                else:
                    gridcopy[r][c]=0
                colcount+=1
            rowcount+=1
        #this next line copies the gridcopy back into GRID
        GRID = [row[:] for row in gridcopy]
        #this is the necessary referencing to update the canvas of the widget
        #it means go to self(the App) and then to mL (the MyLayout) and then to the part of the MyLayout that is referenced as mywidge and call the function update_canvas
        self.mL.mywidge.update_canvas()

    def isAlive(self,current,r,c):
        #this function takes the number of neighbours and the living status of the cell and returns whether it is living or dead.
        global GRID
        num = self.getNeighbours(r,c)
        if current==1 and num in (2,3):
            return True
        elif current==0 and num ==3:
            return True
        else:
            return False

if __name__ == '__main__':
    #runit
    ConwaysApp().run()
    
        
