from numpy import *
import os, random


#swapping of 2 columns of a matrix
def swap_cols(arr, frm, to):
    t=copy(arr)
    t[:,[frm, to]] = t[:,[to, frm]]
    return t

#swapping of 2 rows of a matrix
def swap_rows(arr, frm, to):
    t=copy(arr)
    t[[frm, to],:] = t[[to, frm],:]
    return t
#compare a plateau to all given plateaux
def compareAll(p1,p2):
    for plateau in p2:
        if comparePlateaux(p1,plateau):return 1
    return 0

#compare 2 plateaux             
def comparePlateaux(a,b): return allclose(a,b)

#return the number of cells in a row
def getLineCount(plateau):return sqrt(size(plateau))

#return all possible equivalent plateaux
def getTransformedForms(plateau):
    return plateau, plateau.T, swap_cols(plateau,0,2), swap_rows(plateau,0,2),swap_cols(plateau.T,0,2), swap_rows(plateau.T,0,2)

#try find a transfomation to reach plateau  with plateau2
def findTransformation(plateau,plateau2):
    if comparePlateaux(plateau, plateau2): return 0
    if comparePlateaux(plateau, plateau2.T): return 1
    if comparePlateaux(plateau, swap_cols(plateau2,0,2)): return 2
    if comparePlateaux(plateau, swap_rows(plateau2,0,2)): return 3
    if comparePlateaux(plateau, swap_cols(plateau2.T,0,2)): return 4
    if comparePlateaux(plateau, swap_rows(plateau2.T,0,2)): return 5
    return 50

#transforms a plateau using a tansformation ID
def transformBack(plateau,transformationID):
    if transformationID==0:return plateau
    if transformationID==1:return plateau.T
    if transformationID==2:return swap_cols(plateau,0,2)
    if transformationID==3:return swap_rows(plateau,0,2)
    if transformationID==4:return swap_cols(plateau.T,0,2)
    if transformationID==5:return swap_rows(plateau.T,0,2)
    
#looks for lines of cross or circle is the plateau
def checkPlateau(plateau, lineCount):        
    #lines
    temp=plateau.flat
    for i in range(int(lineCount)):
        if checkLine(temp,i*lineCount,lineCount): return 1
    #columns
    temp=plateau.T.flat
    for i in range(int(lineCount)):
        if checkLine(temp,i*lineCount,lineCount): return 1
    #diagonals
    if plateau[0,0]!=2 and plateau[0,0]==plateau[1,1] and plateau[0,0]==plateau[2,2]:
        return 1
    if plateau[2,0]!=2 and plateau[0,2]==plateau[1,1] and plateau[0,2]==plateau[2,0]: 
        return 1
    return 0

#checks if all values of a line between a and a+lineCount are equal
def checkLine(line,a, lineCount):
    a=int(a)
    if line[a]==2: return 0
    ref=line[a]
    b=lineCount+a
    while a<b:
        if line[a]!=ref : return 0
        a+=1
    return 1

#refresh the text output
def clear():
    #pass
    os.system('cls')