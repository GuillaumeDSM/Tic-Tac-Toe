import graphics

#graphic display class
class graphicTTT:

    #class constructor
    def __init__(self,pixelSize,plateau,grid=None):
        self.window=graphics.GraphWin("Tic Tac Toe",pixelSize,pixelSize)
        self.pixelSize=pixelSize
        self.cellSize=pixelSize/3
        self.squares=3
        self.lineWidth=3
        self.game={0:2,
                          1:2,
                          2:2,
                          3:2,
                          4:2,
                          5:2,
                          6:2,
                          7:2,
                          8:2}  #storing of the plateau information
        if grid==None:
            self.drawEmpty()
            self.update(plateau)

    #draw the empty plateau (lines and columns)
    def drawEmpty(self):
        for i in range(self.squares - 1):
            hline = graphics.Line(graphics.Point(0, (self.pixelSize/self.squares) * (i + 1)), graphics.Point(self.pixelSize,  (self.pixelSize/self.squares) * (i + 1)))
            hline.draw(self.window)
            vline = graphics.Line(graphics.Point((self.pixelSize/self.squares) * (i + 1), 0), graphics.Point((self.pixelSize/self.squares) * (i + 1), self.pixelSize))
            vline.draw(self.window)


    #print a text information over the game interface
    def printInfo(self, text,pos=None):
        if pos==None:info=graphics.Text(graphics.Point(self.pixelSize/2,self.pixelSize/2),text)
        else:info=graphics.Text(pos,text)
        info.setSize(10)
        info.setStyle('bold italic')
        info.setTextColor('Black')
        info.draw(self.window)
        return info

    #delete an object from the game interface
    def erase(self, item):return item.undraw()

    #udates the display of the plateau
    def update(self, plateau):
        flat=plateau.flat
        i=0
        for item in plateau.flat:
            if self.game[i]!=item:
                self.game[i]=item+10
            i+=1
        self.updateDisplay()

    #draw the needed new crosses and circles
    def updateDisplay(self):
        for key,val in self.game.items():
            if val>9:
                self.drawItem(key,val)
                self.game[key]-=10

    #draw a circle or a cross
    def drawItem(self, cell, type):
        if type==10:self.drawCross(cell)
        if type==11:self.drawCircle(cell)

    #circle drawing function
    def drawCircle(self,cell):
        circle = graphics.Circle(self.getCenter(cell), self.cellSize/2)
        circle.setOutline('red')
        circle.setWidth(self.lineWidth)
        circle.draw(self.window)

    #cross drawing function
    def drawCross(self,cell):
        center=self.getCenter(cell)
        x=center.getX()
        y=center.getY()
        for i in range(2):
            deltaX = (-1) ** i * (self.cellSize / 2)
            deltaY = (self.cellSize / 2)
            line = graphics.Line(graphics.Point(x - deltaX, y - deltaY),
                     graphics.Point(x + deltaX, y + deltaY))
            line.setFill('blue')
            line.setWidth(self.lineWidth)
            line.draw(self.window)

    #return the centre pixel of a cell
    def getCenter(self,cell):
        y=cell//3*self.cellSize+self.cellSize/2
        x=cell%3*self.cellSize+self.cellSize/2
        return graphics.Point(x,y)

    #stop the graphical display
    def stop(self):
        self.window.close()

    #returns the cliced point x and y
    def getMove(self):
        clickedPoint=self.window.getMouse()
        x=clickedPoint.getX()//self.cellSize
        y=clickedPoint.getY()//self.cellSize
        return y, x

    #return the choice between the two inputs
    def getChoise(self,b1,b2):
        pos1=graphics.Point((self.pixelSize/2),self.pixelSize/4)
        pos2=graphics.Point((self.pixelSize/2),3*self.pixelSize/4)
        t1=self.printInfo(b1,pos1)
        t2=self.printInfo(b2,pos2)
        hline = graphics.Line(graphics.Point(0, (self.pixelSize/2)), graphics.Point(self.pixelSize,  (self.pixelSize/2)))
        hline.setFill('black')
        hline.draw(self.window)
        x,y=self.getMove()
        t1.undraw()
        t2.undraw()
        hline.undraw()
        if x*self.cellSize>self.pixelSize/2: return 0
        else: return 1