from __future__ import print_function
import random
import sys

## comMove can be better by avoiding [1,7],[7,1]..
## if you enter in your turn, error -->solved
## need a function in case there is no available move
## make user choose X or O
## randomly choose who goes first
## maybe level ?

def drawBoard(board):
    firstrow = '   1  2  3  4  5  6  7  8 '
    secondrow = '--+--+--+--+--+--+--+--+--'

    print (firstrow)
    print (secondrow)
    for i in range(8):
        print (' %s %s' %(i+1,getRow(board,i)) )
 
def getRow(board,row):
    boardRow = ''
    for i in range(8):
        boardRow = boardRow + board[i][row] + '  '
    return boardRow

def getBoard():
    board = []
    for i in range(8):
        board.append([])

    for i in board:
        for j in range(8):
            board[j].append(' ')
    initiated(board)
    return board

def initiated(board):
    board[3][3] = 'O'
    board[3][4] = 'X'
    board[4][3] = 'X'
    board[4][4] = 'O'

def isUserFirst():
    if random.randint(0,1) == 0:
        return True

def userMove(board,Tile):
    while True:
        move = raw_input('Enter your move:(1-8 1-8) (or type quit)\n')
        if move == 'quit':sys.exit()
        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit():
           x = int(move[0])-1
           y = int(move[1])-1
           if not isOnBoard(x,y):
               print('invalid value!\n')
           elif board[x][y] != ' ':
               print('alreay taken!\n')
           elif isValid(board,x,y,Tile):
               for i,j in isValid(board,x,y,Tile):
                   #print('i %s,j %s' %(i,j))
                   board[i][j] = Tile
               break
        else :
            print('invalid value!\n')

def isValid(board,xstart,ystart,Tile):
    board[xstart][ystart] = Tile
    flipTiles = []
    if Tile == 'X':
        otherTile = 'O'
    else :
        otherTile = 'X'
    neighbor = [[1,0],[-1,0],[0,1],[0,-1],[1,1],[1,-1],[-1,1],[-1,-1]]
    for xmove,ymove in neighbor:
        x = xstart + xmove
        y = ystart + ymove
        if isOnBoard(x,y) and board[x][y] == otherTile:
            while board[x][y] == otherTile:
                x += xmove
                y += ymove
            #print ('x %s,y %s' %(x,y))
                if not isOnBoard(x,y):
                    break
            if not isOnBoard(x,y):
                continue
            if board[x][y] == Tile:
                while True:
                    x -= xmove
                    y -= ymove
                    flipTiles.append([x,y])
            #print ('x %s,y %s' %(x,y))
                    if x == xstart and y == ystart:
                        break
    board[xstart][ystart] = ' '
    if len(flipTiles) == 0:
        return False
    else:
        return flipTiles

def isOnBoard(x,y):
    return 0 <= x and x <= 7 and 0 <= y and y <= 7

def getBoardWithValidMoves(board,tile):
    boardValid = []
    for i in range(8):
        for j in range(8):
            if board[i][j] == ' ':
                if isValid(board,i,j,tile) != False:
                    boardValid.append([i,j])
    return boardValid
    
def copyBoard(board):
    dupeboard = []
    for i in range(8):
        dupeboard.append(board[i])
    return dupeboard

def comMove(board,Tile,corners):
    boardValid = getBoardWithValidMoves(board,Tile)
    getPoint = 0
    bestx, besty = 0,0
    cornerTaken = False
    # in case that there are more than two available corners
    random.shuffle(corners)
    
    # take corner first
    for corner in corners:
        if corner in boardValid:
            bestx = corner[0]
            besty = corner[1]
            corners.remove([bestx,besty])
            cornerTaken = True
            break
    # greedy algorithm
    if not cornerTaken:
        for i,j in boardValid:
            flipTiles = isValid(board,i,j,Tile)
            if getPoint <= len(flipTiles):
                getPoint = len(flipTiles)
                bestx = i
                besty = j
    for i,j in isValid(board,bestx,besty,Tile):
            board[i][j] = Tile
    print ('Com moved %s %s' %(bestx, besty))
    
def getPoint(board,Tile,otherTile):
    userpoint = 0
    compoint = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == Tile:
                userpoint += 1
            elif board[i][j] == otherTile:
                compoint += 1
    points = [userpoint,compoint]
    return points

def showPoint(userpoint,compoint):
    print ('Your point is %s, Com\'s point is %s' %(userpoint,compoint))
        
def gameEnd(userPoint,comPoint):
    if userPoint < comPoint:
        print('AI won!')
    elif userPoint > comPoint:
        print('You won!')
    else :
        print('Drawed!')
    
def userWants():
    while True:
        XorO = raw_input('You want X or O?')
        XorO = XorO.upper()
        if XorO in ['X','O']:
            return XorO

def userTurn():
    if random.randint(0,1) == 0:
        return True

def printFirst(player):
    if player == 'user':
        print('%s goes first' %(player))
        print('=======game start=========')
    else:
        print('%s goes first' %(player))
        print('=======game start=========')

corners = [[0,0],[0,7],[7,0],[7,7]]

userTile = userWants()
if userTile == 'X':
    otherTile = 'O'
else: 
    otherTile = 'X'

userTurn = userTurn()
board = getBoard()

if userTurn : 
    printFirst('User')
else :
    printFirst('AI')

while True:
    # draw-showpoint-promptMove
    if userTurn :
        drawBoard(board)
        userPoint = getPoint(board,userTile,otherTile)[0]
        comPoint = getPoint(board,userTile,otherTile)[1]
        if getBoardWithValidMoves(board,userTile) == []:
            showPoint(userPoint,comPoint)
            gameEnd(userPoint,comPoint)
            break
        showPoint(userPoint,comPoint)
        userMove(board,userTile)
        userTurn = False
        
    else:
        drawBoard(board)
        userPoint = getPoint(board,userTile,otherTile)[0]
        comPoint = getPoint(board,userTile,otherTile)[1]
        if getBoardWithValidMoves(board,otherTile) == []:
            showPoint(userPoint,comPoint)
            gameEnd(userPoint,comPoint)
            break       
        showPoint(userPoint,comPoint)
        print('Com\'s turn. Type enter',end = '')
        raw_input()
        comMove(board,otherTile,corners)
        userTurn = True
