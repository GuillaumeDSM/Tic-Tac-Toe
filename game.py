from texttable import Texttable
from gui import graphicTTT
from util import *
import time

class game:

    #class constructor, initialisation of the game interface)
    def __init__(self):
        self.name='Tic-Tac-Toe'
        self.playing=1
        self.ssg=None
        self.root=None
        self.startingState=0
        self.algorithme="MinMax"
        self.AIs=["MinMax",]
        self.pixelSize=250
        self.graphWin=None
        self.launch()

    #initialisation of a new tic tac toe, main screen
    def launch(self):
        while self.playing:
            clear()
            print ("=============================================\n            Welcome in " + self.name +"\n=============================================\n")
            t = Texttable()
            t.set_cols_align(["c","c",])
            title=['Choice','Select what to do']
            t.add_rows ([title,[" 1", "Start a new game"]])
            t.add_rows ([title,[" 2", "Artificial intellignece settings"]])
            t.add_rows ([title,[" 0","Exit"]])
            print t.draw()
            while 1:
                try:
                    a=input("Choice : ")
                    break
                except: print "Please type 1, 2 or 0"
            if a==2:self.displaySettings()
            elif a: self.startGame()
            else: self.playing=0

    #dislay of settings screen
    def displaySettings(self):
        clear()
        print ("============================================================================\n                                Settings: \n============================================================================\n")
        t = Texttable()
        t.set_cols_align(["c","l", "l"])
        title=['Choice','Select what to change','Current value']
        t.add_rows ([title,["0","Artificial intelligence game algorithme",self.algorithme]])
        t.add_rows ([title,["1","Starting state (number of already played moves)",str(self.startingState)]])
        print t.draw()
        while 1:
            try:
                a=input("Choice : ")
                break
            except: print "Please type 1 or 0"
        if a: self.changeStartingState()
        else: self.changeAI()

    #diplay of switch AI screen
    def changeAI(self):
        clear()
        t = Texttable()
        t.set_cols_align(["c","l"])
        title=['Choice','Select AI to use']
        for i in range( len(self.AIs)):
             t.add_rows ([title,[str(i), self.AIs[i]]])
        print t.draw()
        while 1:
            try:
                self.algorithme=self.AIs[input("Choice : ")]
                break
            except: print "Please select an existing AI"

    #diplay of switch strating state screen
    def changeStartingState(self):
        clear()
        t = Texttable()
        t.set_cols_align(["c"])
        title=["Select which starting state to use"]
        max=9
        for i in range(max):
            t.add_rows ([title,[str(i)]])
        print t.draw()
        while 1:
            try:
                a=input("Choice : ")
                if a<0 or a>8: raise Exception("x")
                else:
                    self.startingState=a
                    break
            except: print "Please select an existing starting state"
        
        
    #diplay of first player screen
    def startGame(self):
        clear()
        t = Texttable()
        t.set_cols_align(["c","c"])
        title=["Choice","Do you want to play first ?"]
        t.add_rows ([title,["1","Yes"]])
        t.add_rows ([title,["0","No"]])
        print t.draw()
        g=graphicTTT(self.pixelSize,matrix('2 2 2; 2 2 2; 2 2 2'),1) 
        first=g.getChoise("I play first", "Artificial intelligence plays first")
        g.window.close()
        if first: self.currentPlayer=1
        else: self.currentPlayer=0
        self.createPlateau()    #creation of the game plateau
        self.count=size(self.plateau)
        self.lineCount=getLineCount(self.plateau)
        self.play() #starting to play

    #Creation of the game plateau considering the starting state setting
    def createPlateau(self):
        self.plateau=matrix('2 2 2; 2 2 2; 2 2 2')
        for i in range (self.startingState):
            nok=True
            while nok:  #while the random chosen cell is not a free cell
                a=random.randrange(0,3)
                b=random.randrange(0,3)
                if self.plateau[a,b]==2:    #if it is a free cell: fill it
                    self.plateau[a,b]=self.currentPlayer
                    self.currentPlayer=self.changePlayer(self.currentPlayer)
                    nok=False
                
    #display informations by text and graphicaly
    def display(self):
        self.displayText()
        self.displayGraph()

    #display the game in text format
    def displayText(self):
        column=0
        nbRow=1
        t = Texttable()
        t.set_cols_align(["l","c", "c", "c"])
        title=['/','Tic', 'Tac','Toe']
        endLine=['\\',1,2,3]
        adding=[]
        adding.append(nbRow)
        for i in self.plateau.flat: #reads row by row
            if i==0:  adding.append('X')
            elif i==1: adding.append('O')
            else:  adding.append('')
            column+=1
            if column==self.lineCount:
                t.add_rows([title,adding])
                column=0
                nbRow+=1
                adding=[]
                adding.append(nbRow)
        t.add_rows([title,endLine])
        print t.draw()
        
    #make a move from human player 
    def humanMove(self):
        self.graphicInput() #by graphic interface
        #self.consoleInput()    #by text inteface

    #player input by graphic interface
    def graphicInput(self):
        self.moved=False
        asking=True
        while asking:   #while the selected cell is not free
            print "Player's turn, please clic on a free cell"
            x,y=self.graphWin.getMove()
            if self.plateau[x,y]!=2:
                g=self.graphWin.printInfo("Cell already filled,\n please chose an other one")
                time.sleep(1)
                self.graphWin.erase(g)
            else:
                self.moved=True
                asking=False
        self.plateau[x,y]=self.currentPlayer
        
    #player input by text interface
    def consoleInput(self):
        self.moved=False
        asking=True
        while asking:   #while the selected cell is not free
            try:
                print "Player's turn, please enter a row number"
                row=input("O - Row number : ")
                print "Now, please enter a column number"
                col=input("Column number : ")
                if row==5 or col ==5:
                    asking=False
                    quit()
                if self.plateau[int(row)-1, int(col)-1]!=2: print "Cell already filled, please chose an other one"
                else:
                    self.moved=True
                    asking=False
            except : pass
        self.plateau[row-1 , col-1]=self.currentPlayer

    #returns the other player
    def changePlayer(self,n):
        if n:return 0
        else: return 1

    #Alternates the players and checks if the game is over
    def play(self):
        self.display()
        while not self.checkWinner():   #play while no winner
            if self.gameOver():
                return self.endGame()
            self.display()
            if self.currentPlayer:self.humanMove()  #if it's to the player to move
            else: self.AIMove() #if it is to the computer to move
            self.currentPlayer=self.changePlayer(self.currentPlayer)    #switch current player after each move
        if self.currentPlayer: p = 'Artificial intelligence'
        else: p= 'Player'
        print p+' Wins !'
        self.graphWin.printInfo(p+' Wins !\n Clic to continue')
        self.endGame()

    #checks if there is no more free cell
    def gameOver(self):
        for item in self.plateau.flat:
            if item==2: #if at least one is free
                return 0    
        print 'Game over, no winner !'
        self.graphWin.printInfo('Game over, no winner !\n Clic to continue')
        return 1

    #game reset
    def endGame(self):
        self.display()
        del self.ssg, self.plateau,self.currentPlayer
        self.ssg=None
        self.root=None
        self.graphWin.getMove()
        self.graphWin.stop()
        self.graphWin=None
        g=graphicTTT(self.pixelSize,matrix('2 2 2; 2 2 2; 2 2 2'),1) 
        suite=g.getChoise("New game", "Exit")
        g.window.close()
        if suite==1: self.startGame()
        

    #checks if there is a winner in the game
    def checkWinner(self):
        return checkPlateau(self.plateau,self.lineCount)
    
    #defines the artificial intelligence's moves
    def AIMove(self):
        print 'X - AI MOVE ... '
        if self.ssg==None:  #if the state space graph has not been created
            self.createSSG(self.plateau)    #creation
            self.assignHeuristics()     #heuristic calculation
            self.treeLevel=0    #current level of the game in the tree
            g=self.graphWin.printInfo('X - AI Move ...')
        else:   #if state space graph already generated
            g=self.graphWin.printInfo('X - AI Move ...')
            time.sleep(0.3) #to inform it's AI's that is playing
        currentNode=self.findNode(self.ssg.graphLeveled[self.treeLevel])    #find the current state of the game in the state space graph
        bestChild=self.findMove(currentNode)    #find the best move to do
        self.makeMove(bestChild)    #make this move
        self.graphWin.erase(g)  #stop displaying the "AI Move" message
        self.treeLevel+=2   #preparing the level of the next AI move

    #User the ssg to move to the next state
    def makeMove(self, child):
        max=int(self.lineCount)
        for i in range(max):
            for j in range (max):   #for each cell
                pTemp=copy(child.plateau)   #deep copy of the game plateau for the child that is to say with an additional move
                pTemp[i,j]=2    #repace the cell by an empty one
                transformationID=findTransformation(self.plateau, pTemp)    #try to find a transformation that allows to reach the previous state (that is to say the current game state) The aim is to find the cell that was played by the child
                if transformationID!=50:    #if a transformation is found
                    self.plateau=transformBack(child.plateau,transformationID)  #transform the child to the current game shape and simulate the move
                    return
        raise Exception("Game tree is bugged, impossible to find the current game plateau transformation is state space graph") #if impossible to reach the current game state b y unmoving each cells

    #dertermines the next move by selecting the child with the best heuristic It determines the solution path
    def findMove(self, node):
        maxHeuri=node.childs[0].heuristic   
        bestChild=node.childs[0]
        for child in node.childs:    #find the child with the maximum heuristic
            if child.heuristic>maxHeuri:    
                maxHeuri=child.heuristic  
                bestChild=child
        return bestChild
    
    #find the node in the list that is equivalent the the given one taking into account the transformations
    def findNode(self,nodes):
        for node in nodes:
            if compareAll(self.plateau,node.comparing):return node
        raise Exception("Game tree is bugged, impossible to find the current game plateau is state space graph")

    #high level heuristic calculation function
    def assignHeuristics(self):
        print 'Generating heuristic ...'
        t1=time.time()
        self.assignLeaves() #fist assign leaves
        self.propagateHeuristic()   #then all other nodes
        t2=time.time()
        print "Heuristic generated in "+str(t2-t1)+" secondes."

    #assign the heuristic value of each leaf
    def assignLeaves(self):
        for key in self.ssg.graphLeveled.keys():    #for each ssg level
            for node in self.ssg.graphLeveled[key]: #for each node in this level
                if not node.hasChild(): #if it is a leaf
                    node.heuristic=self.computeLeafHeuristic(node,key)

    #compute leaf heuristic
    def computeLeafHeuristic(self,node,key):
        if self.algorithme=="MinMax":   #case where algorithme is MinMax
            if node.isGoal():   #if the given node is a goal node for any player
                if self.currentPlayer==node.player: return 2*((9-key)*9) #if it's a goal node for the current player: high value and higher if the path is short
                else: return -2*((9-key)*9)  #if it's a goal node for the other player: low value and lower if the path is short
            return 1    #if it's a game over (no winner) node: better that lose but worse than win

    #propagates heuristic in the whole tree usign leave heuristic
    def propagateHeuristic(self):
        currentLevel=max(self.ssg.graphLeveled.keys())
        while currentLevel: #starting form the deepest level and going up
            for node in self.ssg.graphLeveled[currentLevel]:    #for each node
                if node.hasChild(): #if not a leaf
                    if self.currentPlayer==node.player:node.heuristic=min(node.getChildsHeuristic())         #if it's a MIN move
                    else:node.heuristic=max(node.getChildsHeuristic())   #if it's a MAX move
            currentLevel=currentLevel-1
                        
    #class used to build the state space graph's nodes
    class node:

        #class construtor
        def __init__(self,plateau,player,leaf):
            self.plateau=plateau
            self.heuristic=None
            self.player=player
            self.isALeaf=leaf
            self.childs=[]
            self.comparing=getTransformedForms(plateau) #storage of the possible transfomations for optimisation

        #checks if the given plateau exists in one of the node's childs
        def existingChild(self,p):
            for item in self.childs:
                if compareAll(item.plateau,self.comparing):return 1
            return 0

        #checks if the node is a goal node
        def isGoal(self):return self.isALeaf

        #checks if the node has at least a child
        def hasChild(self):return len(self.childs)

        #returns all child's heuristic values
        def getChildsHeuristic(self):
            t=[]
            for child in self.childs:
                t.append(child.heuristic)
            return t

    #state space graph class: contains a dictionary of levels and nodes
    class ssg:

        #class constructor
        def __init__(self, node):
            self.graphLeveled={0:[node,]}

        #checks if for a given level, a node with the same plateau and player is present
        def containedNode(self, node, level):
            try:
                for item in self.graphLeveled[level]:   #for each node is the given level
                    if compareAll(item.plateau,node.comparing) and node.player==item.player:
                            return item
                return None
            except KeyError:    #if the given level is not existing, will be created after
                return None

    #create a state space graph with the given plateau
    def createSSG(self,plateau):
        text='Generating state space graph ...' #inform user
        print text
        g=self.graphWin.printInfo(text) #inform user
        t1=time.time()
        self.root=game.node(plateau,self.changePlayer(self.currentPlayer),0)    #creation of the root node
        self.ssg=game.ssg(self.root)    #creation of the ssg containing the root node
        self.generateChilds(self.root,self.currentPlayer,1) #generating all the possible childs
        t2=time.time()
        self.graphWin.erase(g)
        text= "State space graph generated in:\n"+str(t2-t1)+" secondes."
        print text
        g=self.graphWin.printInfo(text)
        time.sleep(1)
        self.graphWin.erase(g)

    #generates all the possible childs of a node
    def generateChilds(self,node,player,level):
        max=int(self.lineCount)
        for i in range(max):
            for j in range (max):   #for each cell
                if node.plateau[i,j]==2:    #if the cell is free
                    temp=node.plateau.copy()    #deep copy of the plateau
                    temp[i,j]=player    #assign the cell to the player
                    if checkPlateau(temp,max):leaf=1    #if it's a winning position
                    else:leaf=0
                    new=game.node(temp,player,leaf) #creation of the corresponding node
                    test=self.ssg.containedNode(new,level)  #check is this node is already contained is the ssg (thanks to transformations)
                    if test != None:    #if it is already present: just link the previously returned node to the current node
                        node.childs.append(test)
                    else:   #otherwise creation of the new node
                        try:self.ssg.graphLeveled[level].append(new) #add the node to the state space graph
                        except KeyError : #if the level doesn't exist
                            self.ssg.graphLeveled[level]=[new,] # create this level with the node
                        node.childs.append(new) #new node added to the current node childrens
        for item in node.childs:    #for each node's childrens
            if (not item.hasChild()) and (not item.isGoal()): self.generateChilds(item,self.changePlayer(player),level+1)   #if the child node doesn't already have child and is not a goal node, generating of its childrens 

    #display of the graphic interface
    def displayGraph(self):
        if self.graphWin==None:self.graphWin=graphicTTT(self.pixelSize,self.plateau)    #creation
        else: self.graphWin.update(self.plateau)    #update