#layout -> gamelogic 
#       -> GUI   ->MINIMAX ALGO   -> MAIN GAME STARTING
# vvvvvvvvvvvvvvvvvv all imports
from threading import Thread
import time
import tkinter as tk
import io
from numba import jit

#^^^^^^^^^^^^^^^^^^^
#
#GAME LOGIC 
#
#
white,black={},{}#key is position val is king or not
#BOARD IS NOT USED IN SIMULATION JUST FOR INITIALISATION
#board * if empty w, b if whhite pice or blac, wk ,bk if king
board=[
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'w', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'b', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'b', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'wk', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],
#['*', '*', '*', 'b', '*', 'b', '*', 'b'],['b', '*', 'b', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', 'b', '*', '*'],['w', '*', 'w', '*', '*', '*', '*', '*'],['*', '*', '*', 'w', '*', '*', '*', 'b'],['*', '*', 'w', '*', '*', '*', 'w', '*'],
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['bk', '*', 'w', '*', 'bk', '*', '*', '*'],
['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],
]
#board=[['*']*8 for x in range(8)] # dont use 2 multiplication bcs it will link to same array
#(DONE) all 3 things for complete information of board, possible with first 2
def getcell(row,col):
    if 8>row>=0 and 8>col>=0:return board[row][col] # no error even if out of bound 
def getcellcolour(row,col):#board pattern
    return 'white' if ((row+col) %2==0) else 'black'

def initboard(board,customdone=False):# custom done true if alreayd board initlized
    for row in range(8):
        for col in range(8):
            if customdone :
                if board[row][col][0]=='w':white[((row,col))]=len(board[row][col])>1 # cant use one line because board can be * and one line only else there
                elif board[row][col][0]=='b':black[((row,col))]=len(board[row][col])>1
                continue
            if (row<3 or row>4) and (getcellcolour(row,col)=='black'):
                (black if row<3 else white)[((row,col))]=False#ie its not king
    print('white',white,'blac',black)

def printboard(whitee=None,blackk=None,space=False,onlyreturn =False):#uses white and black
    if not whitee:
        whitee=white
        blackk=black
    board=[['*']*8 for x in range(8)]
    printt=''
    for x,king in (whitee|blackk).items():
        k='k' if king else ''
        board[x[0]][x[1]]='w'+k if x in whitee else 'b'+k
    for row,x in enumerate(board,0):  printt+=(str(x)+('\n' if space else','))
    if onlyreturn:return printt
    else:print(printt)

def getgamestate(white,black,movecnt,maxplayer): 
    #CRASH FIXED TODO GIVE SCORE WHEN NO MOVES LEFT IE IT LOST but pieces are there
    # used for getting score dont change
    if movecnt>230:return 0 # can lead to crash
    if len(white)==0:return -100
    elif len(black)==0:return+100
    elif len(white)<=1 and len(black)<=1:return 0 # draw both lenth 1
    else:
        #if not getpossiblemovesummary((white,black,[movecnt]),maxplayer,True) !=(not istherepossiblemoves(white,black,movecnt,True) or not istherepossiblemoves(white,black,movecnt,False)):
         #   printboard(white,black,True)
        if not getpossiblemovesummary((white,black,[movecnt]),maxplayer,True):
            #print(getpossiblemovesummary((white,black,[movecnt]),maxplayer,True))
            #printboard(white,black,True)
            return -100 if maxplayer else 100
        #if not istherepossiblemoves(white,black,movecnt,True):return -100# white lost because no move left for it
        #if not istherepossiblemoves(white,black,movecnt,False):return 100# black lost because no move left for it
    return None # ie game is going on

#def istherepossiblemoves(white,black,movecnt,whiteturn):return getpossiblemovesmm((white,black,[movecnt]),whiteturn,checkisthereanymoveonly=True)

def getpossiblemoves():#TODO DONE instead of recursion keep same turn if more captures available # DONE doesnt work for black king captureing 
    return getpossiblemovesmm((white,black,[movecnt]),whiteturn) # using optimized function
def move(movecoord):#,board): # for player move # besure check if its valid coord before calling
     #DONE TODO DEPRECATED REMOVE AND UPDATE THE WHOLE BOARD IN GUI
    global posmovescoord
    simulatemovegui(movecoord,whiteturn,not blackcomputer) # ie dont update score if black ocmpur
    posmovescoord=getpossiblemoves()

#
#GUI
#

def gethex(r, g, b):return f'#{r:02x}{g:02x}{b:02x}'

blackcol,whitecol,blackdarkcol,whitepiece,blackpiece,outline=gethex(222, 152, 87),gethex(255, 244, 201),gethex(170, 112, 52),gethex(230,230,230),gethex(66, 64, 54),gethex(161, 102, 47)
boardrects={} # rectpos->id
pieceid={}# pos->id

posmovesid={} # outlinepos->id
posmovescoord=[] # possible moves

clicked=None
kingcol=gethex(252, 223, 76)
def makepiecekinggui(row,col):#TODO DONE KING OUTLINE GOING OUT OF BORDER
    id=pieceid[(row,col)]
    x1, y1, x2, y2 = canvas.coords(id)
    half=(gridsize/10)//2
    canvas.coords(id,x1+half,y1+half,x2-half,y2-half)# so outline remains inside
    canvas.itemconfigure(id,width=gridsize/10,outline=kingcol)
def iskingui(coord): #coord-(row,col) #TODO DEPENDS ON OUTLINE OF PIECE TO FIND IF ITS KING, if chnage outline to image then chnage this
    # NO NEED TOCHECK IF ITS IN PIECEID BEFORE CALLING
    return coord in pieceid and canvas.itemcget(pieceid[coord], 'outline')==kingcol
def removepiece(row,col):
    canvas.delete(pieceid[(row,col)])
    pieceid.pop((row,col))
def movepiece(row,col,torow,tocol): # for gui
    x=tocol * gridsize
    y=torow * gridsize
    canvas.moveto(pieceid[(row,col)],x,y)

    pieceid[(torow,tocol)] = pieceid[(row,col)]  # updating id
    pieceid.pop((row,col))

def simulatemovegui(coord,maxplayer,updateguiscoreifnokillleft): # for computer move # changes movecnt and whiteturn
    global movecnt,white,black,whiteturn
    prevmovecnt=movecnt# prevmovecoutn
    updatedboard=movemm(coord,(white,black,[movecnt]),maxplayer)
    white,black,newmovecnt=updatedboard
    newmovecnt=newmovecnt[0] # move count inside array 
    updateallpieces()

    if prevmovecnt!=newmovecnt: # ie more kills are not there
        
        whiteturn= not whiteturn 
        movecnt=newmovecnt
        if updateguiscoreifnokillleft:updatescoregui(depthupdategui,whiteturn,white,black)
        return True # no more kills left
blackcomputertime,whitecomputertime=0,0
def computermove(earlierturn,depth ,v2=True):# it will update possible moves
    # no need to input copies of white and black because it wont change
    global blackcomputertime,whitecomputertime
    starttime,timetook=time.time(),0
    result=minimaxv2((white,black,[movecnt]),depth,earlierturn,v2=v2,analysis=True) 
    bestpath=result[1]
    print('COMPUTER BESTPATH',bestpath)
    ind=0
    while whiteturn==earlierturn:#if more double kills
        if ind>=len(bestpath):
            #result=(minimaxv2 if v2 else minimax)((white,black,[movecnt]),depth,earlierturn)
            result=minimaxv2((white,black,[movecnt]),depth,earlierturn,v2=v2,analysis=True)
            bestpath=result[1]
        if gameover:break# dont simulate move as thread diff
        re=simulatemovegui(bestpath[ind],earlierturn,False)
        if re:
            turned=not whiteturn
            timetook=time.time()-starttime
            if turned:whitecomputertime+=timetook
            else: blackcomputertime+=timetook
            print('totaltime,','whiteL',round(whitecomputertime,1),' blacktook:',round(blackcomputertime,1))

            updatescoregui(depthupdategui,whiteturn,white,black)# keep up false, dupdating score here
        ind+=1#missed simple caused bug
    #now white turn is opposite ie for that turn is there if whiteturn true then its the chance of white to move
    turned=not whiteturn
    print('COMPUTER MOVED ->',turned,'movecnt:',movecnt)
    
    print('time took:',timetook)
    if timetook<0.5:
        print('sleeping')
        time.sleep(2)
    
    printboard()
    global posmovescoord
    #print(posmovescoord)
    posmovescoord=getpossiblemoves()# for next human movee as done in move()
    checkgamestate(whiteturn)# now white turn has changed but we want to check for now only
    if gameover:return
    checkcomputermove(depth=depth)

def checkcomputermove(newthread=True,depth=7):#call only if game not over
    depth=computerdepth
    if gameover:return
    print('COMPUTER MOVING THINKING,',movecnt, whiteturn)
    if whiteturn and whitecomputer:
        Thread(target=computermove,args=(whiteturn,10,True),daemon=True).start()
    elif not whiteturn and blackcomputer:
        Thread(target=computermove,args=(whiteturn,10,False),daemon=True).start()
    checkgamestate(whiteturn)# now white turn has changed but we want to check for now only
    return True
    # other all things checked in computermove and simulate move

def canvasclick(event):
    global clicked,posmovesid,posmovescoord,gameover
    if gameover:return        
    row,col=(event.y//gridsize,event.x//gridsize)
    
    rectid=boardrects[(row,col)]
    isblack=(row + col) % 2
    if blackcomputer and not whiteturn:return
    if whitecomputer and whiteturn:return 
    if isblack:
        if (row,col) in posmovesid:
            move(posmovesid[(row,col)][1])
            printboard()
            print(posmovescoord)

            checkgamestate(whiteturn)

            canvas.delete('possmoves')#0 is id 
            posmovesid={}
            canvas.itemconfig(clicked, fill=blackcol)
            clicked=None
            t=checkcomputermove()
            
            return
        
        if clicked!=rectid:#diff cell clicked
            if clicked:
                canvas.itemconfig(clicked, fill=blackcol)
                canvas.delete('possmoves')
                posmovesid={}
            for coord in posmovescoord:# making all possible moves overlay
                if coord[0]==(row,col):
                    movepos=coord[1]
                    x,y=movepos[1] * gridsize,movepos[0] * gridsize

                    posid= canvas.create_oval(x, y, x + gridsize, y + gridsize, width=gridsize//20, outline=blackpiece,tags='possmoves')
                    posmovesid[movepos]=(posid,coord)#0 is id 1 is full coord, key is tomovepos
            canvas.itemconfig(rectid, fill=blackdarkcol)
            clicked=rectid

        else:#same cell clicked again
            canvas.delete('possmoves')
            posmovesid={}
            canvas.itemconfig(clicked, fill=blackcol)
            clicked=None

def checkgamestate(maxplayer): # for checking and then displaying
    global gameover,movecnt
    gamestate = getgamestate(white,black,movecnt,maxplayer)
    if gamestate!= None:
        print('GAME OVER')
        gameover=True
        text=''
        if gamestate==-100:text='BLACK WON'
        elif gamestate==+100:text='WHITE WON'
        else: text='ITS DRAW'
        canvas.create_rectangle(220, 220,400, 350,fill=whitecol, width=5,outline=outline)
        canvas.create_text(300,270,text=text,fill='black',width=150,font=("Helvetica", 15))
def converttonotation(coord):
    return (chr(65+coord[0])+str(coord[1]+1))
def updatescoregui(depth,iswhitemove,white,black):# for checking and displaying score and displaying prediction and bestpath
    result=minimaxv2((white,black,[movecnt]),depth,iswhitemove)
    drawscore(result[0]) # draw score

    bestpath=result[1]
    #print('bestpath',bestpath,'\n score,',result[0])
    print(result[0],getscore((white,black,[movecnt]),iswhitemove))
    drawprediction(result[0]) #draw prediction

    # TODO DONE MAKE GUUI TO DISPLAY BEST PATH
    bestpathnotation=[converttonotation(x[0])+'-'+converttonotation(x[1]) for x in bestpath]
    drawpath(bestpathnotation)
    #print('bestpathinnotation',bestpathnotation)

    drawdepth(depth)
def canvasmousemove(event):
    row,col=(event.y//gridsize,event.x//gridsize)
def buttonenter(event):
    event.widget.config(bg=blackcol)
def buttonleave(event):
    event.widget.config(bg=whitecol)
def updateallpieces(complete=True):#NOW OPTIMIZED (NOW NOT completely updatepieces)
    # white and black should be correct and initialized
    #update white and black before calling it
    global pieceid
    #canvas.delete('pieces') # no need
    #pieceid={}
    t=(white|black)
    for x in list(pieceid.keys()):
        if x not in t:
            canvas.delete(pieceid[x])
            pieceid.pop(x)
    for coord,king in t.items():
        if coord in pieceid:
            if king == iskingui(coord):continue # its already drawn and same
            else:
                canvas.delete(pieceid[x])
                pieceid.pop(coord)# else remove it to add new vvvvv
        row,col=coord
        x,y=col * gridsize,row * gridsize
        colour=blackpiece if coord in black else whitepiece
        piece= canvas.create_oval(x, y, x + gridsize, y + gridsize, fill=colour, outline="black",tags='pieces')
        pieceid[coord]=piece
        if king:makepiecekinggui(row,col) # after putting it in pieceid call it
def draw_board(canvas):#MADE IT COMPATIBLE WITH KINGs
    for row in range(8):
        for col in range(8):
            color = blackcol if getcellcolour(row,col)=='black' else whitecol
            x,y=col * gridsize,row * gridsize
            boardrects[(row,col)]= canvas.create_rectangle(x, y,(col + 1) * gridsize, (row + 1) * gridsize,fill=color, outline=outline)
    #OPTIMIZED  seperate loop to maintain pices level on top  on graphic, changes when moving
    updateallpieces()

def drawscore(score): # 100 to -100
    score=round(score,1)
    totalheigth=gridsize*8 +10
    totalwidth=34

    whiterect=(totalheigth//2)+((totalheigth//2)*(score/100))
    blackrect=totalheigth-whiterect

    scorepanel.delete('all')
    scorepanel.create_rectangle(0,0,totalwidth,blackrect,fill=greyscore)
    scorepanel.create_rectangle(0,blackrect,totalwidth,totalheigth,fill=whitescore)

    scorepanel.create_text(totalwidth//2,totalheigth-20,text=str(score),font=('Helvetica', 10, 'bold') )

def drawprediction(score):
    text='White ' if score>0 else 'Black '
    text+='Won' if abs(score)==100 else 'Advanatage'
    text='Draw'if score==0 else text
    predictpanel.configure(text='Predicted Result: '+text)
def drawpath(pathnotation):#pass empty list if nothign ther
    st='   Best Move Path: \n \n'
    while len(pathnotation)<=14:pathnotation.append('          ') #tomake it atleast 12
    for ind,x in enumerate(pathnotation):
        st+=str(ind+1)+'.'+(' '*(ind<10))+x
        st+=('\n\n'if (ind+1)%2==0 else '  '*(ind<10)) # add empty string if more then so layout remains currect
        
    pathpanel.configure(text=st)
def drawdepth(depthsearched):
    depthpanel.configure(text='Depth \n\n   '+str(depthsearched))
def togglecomputer():
    global blackcomputer
    blackcomputer=not blackcomputer
    print('setting computer',blackcomputer)
    computerbutton.configure(text='Computer: '+('ON' if blackcomputer else 'OFF'))

greyscore=gethex(161, 161, 161)
whitescore=gethex(214, 212, 212)
boardx,boardy,gridsize=40,40,70
canvas,scorepanel,predictpanel,pathpanel,depthpanel,computerbutton=None,None,None,None,None,None
def maingui(): # init board before calling
    global canvas,predictpanel,scorepanel,pathpanel,depthpanel,blackcomputer,computerbutton
    root = tk.Tk()
    root.title("Checkers Board")
    frame=tk.Frame(root,background=blackdarkcol,width=1200,height=700,borderwidth=5, relief="solid")
    frame.pack_propagate(False) # disable from fitting

    canvas = tk.Canvas(frame, width=gridsize*8, height=gridsize*8)
    #canvas.bind("<Motion>",canvasmousemove)
    canvas.bind('<Button-1>',canvasclick)
    canvas.place(x=boardx,y=boardy)

    predictpanel = tk.Label(frame, bg=whitecol,fg=outline,width=30,height=3,borderwidth=5, relief="solid",font=("Helvetica", 15))
    predictpanel.place(x=boardx+640, y=boardy+10)

    pathpanel=tk.Label(frame, bg=whitecol,fg=outline,width=15,height=15,borderwidth=5, relief="solid",font=("Helvetica", 15),justify=tk.LEFT,anchor="nw",padx=30,pady=10)#,wraplength=10)
    pathpanel.place(x=boardx+640, y=boardy+140)

    depthpanel=tk.Label(frame, bg=whitecol,fg=outline,width=5,height=3,borderwidth=5, relief="solid",font=("Helvetica", 15,'bold'),justify=tk.LEFT,anchor="nw",padx=30,pady=10)#,wraplength=10)
    depthpanel.place(x=boardx+640+320, y=boardy+180)

    computerbutton=tk.Button(frame,command=togglecomputer,width=12,height=3,font=("Arial", 13,'bold'),relief=tk.RIDGE,borderwidth=13,bg=whitecol,fg=outline)
    togglecomputer() or togglecomputer() #keeping it enabled
    computerbutton.bind('<Enter>',buttonenter)
    computerbutton.bind('<Leave>',buttonleave)
    computerbutton.place(x=boardx+640+305, y=boardy+180+150)
    #drawing coords
    
    rowcoords=tk.Canvas(frame,width=30,height=gridsize*8 ,bg=whitecol)
    rowcoordwidth,rowcoordheight=30,10
    for ind,x in enumerate('abcdefgh'):
        rowcoords.create_rectangle(3,3+ind*gridsize,rowcoordwidth,(ind+1)*gridsize,width=3,outline=outline)
        rowcoords.create_text(15,34+ind*gridsize,text=x,font=('Helvetica', 13, 'bold'))
    rowcoords.place(x=3,y=boardy)

    colcoords=tk.Canvas(frame,width=gridsize*8,height=rowcoordwidth ,bg=whitecol)
    for ind,x in enumerate('12345678'):
        colcoords.create_rectangle(3+ind*gridsize,3,(ind+1)*gridsize,rowcoordwidth,width=3,outline=outline)
        colcoords.create_text(34+ind*gridsize,15,text=x,font=('Helvetica', 13, 'bold'))
    colcoords.place(x=rowcoordwidth+7,y=rowcoordheight-7)

    scorepanel=tk.Canvas(frame,background=greyscore,width=30,height=gridsize*8 ,borderwidth=2, relief="solid")
    scorepanel.place(x=590+boardx,y=boardy)

    draw_board(canvas)
    starttime=time.time()
    updatescoregui(depthupdategui,whiteturn,white,black)
    print('time took:',(time.time()-starttime))

    frame.pack(padx=10,pady=10)

    checkcomputermove()

    root.mainloop() # do eevrything before it 
    


#
#MINIMAX
#boardminmax=(white,black,movecntarray), movecntarray for checking if double or triple kill there so same player will play again
#white -> maxplayer
# kingscore -> king val for each king

kingscore,peicescore=13,7 #not necessary balance it with so that max score 100 or close to it
scoreadvconst,scoremovecntconst=0.08,0.4
piecevalue={False:1,True:2}# false for normal pirce, true for king
def isterminated(boardmm,maxplayer):return getgamestate(boardmm[0],boardmm[1],boardmm[2][0],maxplayer)
def getscoresimple(boardmm,maxplayer):
    piecevalue={False:1,True:2}
    white,black=boardmm[0],boardmm[1]
    state = getgamestate(white,black,boardmm[2][0],maxplayer)
    if state==None: #ie game is going on
        #whitekingcnt,blackkingcnt=sum(boardmm[0].values()),sum(boardmm[1].values())
        whitepiecesum=sum(piecevalue[x] for x in white.values())
        blackpiecesum=sum(piecevalue[x] for x in black.values())
        return whitepiecesum-blackpiecesum
    else:return state
    
@jit(nopython=True)
def getscore(boardmm,maxplayer,toround=False): #THE HEART OF THE INTELLIGENCE 
    # simple board evaluatiion for each piec 1 or if king 3
    #TODO ADD DIFFERENT EVALUATION CRITERIAS TO MAKE IT MORE ACCURETE
    # piece POSITION, BOARD CONTROL, PIECE SAFETY,PIECE ADVANCMENT
    # 2)MOBILITY, MOVEOPTIONS, CAPTURING OPURTUNITIES
    # 3)PIECE STRUCTURE, FORMATION-aligned can be more effective. , ISOLATION-Isolated pieces or poorly positioned pieces are less valuable
    # 4)Control of Key Areas, Position of Kings
    piecevalue={False:2,True:4}
    white,black=boardmm[0],boardmm[1]
    state = getgamestate(white,black,boardmm[2][0],maxplayer)
    score=0
    if state==None: #ie game is going on
        #whitekingcnt,blackkingcnt=sum(boardmm[0].values()),sum(boardmm[1].values())
        whitepiecesum=sum(piecevalue[x] for x in white.values())
        blackpiecesum=sum(piecevalue[x] for x in black.values())
        score+= whitepiecesum-blackpiecesum #white want to increase positive black want to increase negative
        # if black more then score will be negative if white more it will be positive
        #return score
        #pieceadvancment and center control
        whiteadv,blackadv=0,0
        for wpiece in white:
            if not white[wpiece]:# if its not king
                whiteadv+=(1-(wpiece[0]/7))*scoreadvconst# row, 0.04 for each row/ 0.32 for each piece in max row
            else:
                whiteadv+=(wpiece[0] if wpiece[0]<4 else abs(wpiece[0]-7))*0.03 # for row center
            whiteadv+=(wpiece[1] if wpiece[1]<4 else abs(wpiece[1]-7))*0.03 # (3 for center then less as go away)coloumn center 0.1 for center
        for wpiece in black:
            if not black[wpiece]:
                blackadv+=(wpiece[0]/7)*scoreadvconst
            else:
                blackadv+=(wpiece[0] if wpiece[0]<4 else abs(wpiece[0]-7))*0.03 # for row center
            blackadv+=(wpiece[1] if wpiece[1]<4 else abs(wpiece[1]-7))*0.03#for col
        score+=whiteadv-blackadv

        #mobility, moveoptions
        #whitemoves,blackmoves=0,0
        wmoves,wcapturemoves=getpossiblemovesummary(boardmm,True)
        bmoves,bcapturemoves=getpossiblemovesummary(boardmm,False)
        whitemoves=(wmoves*scoremovecntconst)+(wcapturemoves*scoremovecntconst*1.5)
        blackmoves=(bmoves*scoremovecntconst)+(bcapturemoves*scoremovecntconst*1.5)
        score+=whitemoves-blackmoves
        """
        for move in getpossiblemovesmm(boardmm,True,onlycntmoves=True):
            if move[2]:whitemoves+=scoremovecntconst*1.5
            else:whitemoves+=scoremovecntconst# 0.2 per move available
        for move in getpossiblemovesmm(boardmm,False,onlycntmoves=True):
            if move[2]:blackmoves+=scoremovecntconst*1.5
            else:blackmoves+=scoremovecntconst# 0.2 per move available
        score+=whitemoves-blackmoves
        """
        #print(whitemoves,blackmoves)
        #return int(score)
        return round(score,2) if toround else score

    else:return state # already have -100 or 100 or 0    game finished
def inbound(row,col):return 0<=row<8 and 0<=col<8 

def iscapturethere(boardmm,maxplayer,fromcoord=None):#max player is now whose move
    # any capture there, optimized because if one found connected with enemy simply check if enmy kill also there
    kingcord,bcord,wcord=((1,-1),(-1,-1),(1,1),(-1,1)),((1,-1),(1,1)),((-1,-1),(-1,1))#if king or normal piece (rowadd,cadd)
    dct,enemydct=((boardmm[0],boardmm[1]) if maxplayer else (boardmm[1],boardmm[0]))
    if fromcoord!=None:dct={fromcoord:dct[fromcoord]}
    for (row,col),isking in dct.items():
        for radd,cadd in (kingcord if isking else (wcord if maxplayer else bcord)):
            rowmove,colmove=row+radd , col+cadd
            enemycoord=(rowmove,colmove)
            if enemycoord in enemydct:#inside coords and front not same side piece we cant go there
                jumpedpos=(rowmove+radd,colmove+cadd)
                if (inbound(jumpedpos[0],jumpedpos[1]) and jumpedpos not in enemydct and jumpedpos not in dct): return True # if capture is there from that movee
    return False

def getpossiblemovesummary(boardmm,maxplayer,onlycheckifanymove=False):#for getting no of king moves and normal movesfor score
    kingcord,bcord,wcord=((1,-1),(-1,-1),(1,1),(-1,1)),((1,-1),(1,1)),((-1,-1),(-1,1))#if king or normal piece (rowadd,cadd)
    moves,capturemove=0,0
    dct,enemydct=((boardmm[0],boardmm[1]) if maxplayer else (boardmm[1],boardmm[0]))# inside bracets necessary
    for (row,col) ,isking in dct.items():
        for radd,cadd in (kingcord if isking else (wcord if maxplayer else bcord)):
            rowmove,colmove=row+radd , col+cadd
            if not inbound(rowmove,colmove):continue
            movecord=(rowmove,colmove)
            if movecord in enemydct:
                if inbound(rowmove+radd,colmove+cadd):
                    jumpedpos=(rowmove+radd,colmove+cadd)
                    if (jumpedpos not in enemydct and jumpedpos not in dct):capturemove+=1
            elif movecord not in dct:moves+=1
            if onlycheckifanymove and (moves!=0 or capturemove!=0):return True#only check if any move
    if onlycheckifanymove:return False
    return (moves,capturemove)
@jit(nopython=True)
def getpossiblemovesmm(boardmm,maxplayer):#,checkisthereanymoveonly=False):
    #checkifanycapture used in minimax score calc so that it keeps playing if capture left
    #if checkisthereanymoveonly then only to check any move left or not it will return boolean if game over but check before if white and black not empty
    #from coord if only from one coord# only using white and black also shortened 70 lines to 20
    # if only cnt moves there will be normal moves also even if captureing move
    kingcord,bcord,wcord=((1,-1),(-1,-1),(1,1),(-1,1)),((1,-1),(1,1)),((-1,-1),(-1,1))#if king or normal piece (rowadd,cadd)

    lst=[]###################(()frompos ,() topos,ISKILL , capturedpos) # no need set() list is better
    killfound=False
    dct,enemydct=((boardmm[0],boardmm[1]) if maxplayer else (boardmm[1],boardmm[0]))# inside bracets necessary
    for (row,col) ,isking in dct.items():
        
        piececord=(row,col)
        for radd,cadd in (kingcord if isking else (wcord if maxplayer else bcord)):
            rowmove,colmove=row+radd , col+cadd
            if not inbound(rowmove,colmove):continue
            movecord=(rowmove,colmove)
            if movecord in enemydct:
                if inbound(rowmove+radd,colmove+cadd):
                    jumpedpos=(rowmove+radd,colmove+cadd)
                    kill=(jumpedpos not in enemydct and jumpedpos not in dct)
                    if kill:
                        if not killfound:
                            killfound=True
                            lst=[]
                        lst.append((piececord,jumpedpos,True,movecord))
            elif not killfound and movecord not in dct:#movecord not in dct and not in enemy dct
                lst.append((piececord,movecord,False))
    #print(len(set(lst)),len(lst))
    #if len(set(lst))!=len(lst):print(lst)
    return (lst)
def movemm(movecoord,boardmm,maxplayer): # creates and return in copy  of boardmm
    # DOESNT CHANGE WHITE TURN CHANGE IT AFTER CALLING AFTER CHECKING IF MOVECNT INCREASED IE NO DOUBLE KILL LEFT
    # be sure to check if its valid coord before calling
# TODO FIXED    put movecnt in boarddm 2nd elemnt # TODO FIXED    FIX DOESNT CHANGE KING TO TRUE IN MOVEMM
    boardmm=(boardmm[0].copy(),boardmm[1].copy(),boardmm[2].copy())
    fromcoord,tocoord=movecoord[0],movecoord[1]

    pieces=boardmm[0] if maxplayer else boardmm[1]
    enemypieces= boardmm[0] if not maxplayer else boardmm[1]

    pieces[tocoord]= pieces.pop(fromcoord) # remove from and put in toocord, basically move coord with same king boolean

    if movecoord[2]:# ie kill true
        enemypieces.pop(movecoord[3]) # remove the other colour which is captured

    becameking=False
    if ((maxplayer and tocoord[0]==0)or(not maxplayer and tocoord[0]==7))  and pieces[tocoord]==False: #if already not king and reached there respective row ending
        becameking=True
        pieces[tocoord]=True # ie it became king

    # dont change turn if any more kill is there and this move was kill and didnt became king after killing
    if not becameking and movecoord[2]:
        if iscapturethere(boardmm,maxplayer,tocoord):return boardmm
    boardmm[2][0]+=1# increment move cnt
    return boardmm
mindepthtosort=9
def minimaxv2(boardmm,depth,ismaxplayer=True,depthst=3,v2=True,analysis=False):# to adjust with sorting first and other stuffs depthsort 
    # depth sort examples
    # first board 
    #1)normal 13 depth took 36 sec, depth sort 3 took 10 sec, depth sort 4 took 9 sec, depth sort 4 took 10 sec from here sorting is taking its toll
    #2)normal 9 depth took 9 sec, depsort 1- 8 sec, depsort 2- 15 sec
    #3)normal 14 depth took 33sec, depsort 4-9 secs, 5 -9secs
    #depth 7 from start move 30 no significant diff, depthtosort 1 whitev2, blackv1  whiteL 36.009886264801025  blacktook: 34.87621021270752
    # for dpethtosort 2 5 sec diff
    #done TODO determin some way to MEasure shallowness
    #4)depth 10,depthst4 from start in sstarting white took more time in ending black toook more time, (whitev2) move 20 totaltime, whiteL 84.51373362541199  blacktook: 129.34555840492249
    #^^^move 65 totaltime, whiteL 116.98742246627808  blacktook: 200.87102222442627
    #5)depth 10 depthsort(4)(endgame) time 15, for deptsort5 time 12sec, for 6-13sec, for 3sort,20sec, without-25 sec
    #6)endgame depth 10, depthsort(getscore2) 3 whiteL 64.58  blacktook: 89.2 8 moves, for getscoresimple totaltime, whiteL 64.9  blacktook: 99.3 MOVE 4, totaltime, whiteL 34.6  blacktook: 42.0 move 5

    #^^^^^ all before deprthsortmm
    #match witout deptsortsmm 24move totaltime, whiteL 100.1  blacktook: 119.5
    #with  depthsortmm 5
    global totalevals,smallmmtime
    totalevals,smallmmtime=0,0
    depthtosort=None
    starttime=time.time()

    pos=(getpossiblemovesmm(boardmm,ismaxplayer))
    posboard=[movemm(cord,boardmm,ismaxplayer) for cord in pos]
    shallowcount1=len(pos)
    shallowcount= sum((len(getpossiblemovesmm(board,not ismaxplayer)) for board in posboard))
    
    #print('toktimetocountshallow:',(time.time()-starttime))
    if depth>mindepthtosort:
        depthtosort=3
    else:
        depthtosort=1
    if shallowcount>120:depthtosort+=4
    elif shallowcount>100:depthtosort+=3
    elif shallowcount>60:depthtosort+=2
    elif shallowcount>40:depthtosort+=1
    
    depthsortmm=5
    if depth>=11:depthsortmm+=depth-10
    elif depth<=5:depthsortmm=3
    
    if not v2:depthsortmm,depthtosort=0,0
    score=getscore((white,black,[movecnt]),whiteturn)
    print('GOINGTOPLAY:'+('white'if whiteturn else 'black'),ismaxplayer,', depthsortmm:',depthsortmm,',shallow:',shallowcount1,shallowcount,', depthtosort:',depthtosort,', score:',score)
    print('possmoves,',getpossiblemovesmm(boardmm,ismaxplayer))
    t= minimax(boardmm,depth,ismaxplayer=ismaxplayer,depthsort=depthtosort,depthsortminmax=depthsortmm)
    #print('path:',t[1])
    #print(getpossiblemovesmm((white,black,[movecnt]),True))
    #    analysfile.write('movecnt, whoplayed, depth, shallow1, shallow2, depthsmallmm, depthsort, timetook, cumulativetime , timetooksmallmm, score, minmaxscore, whitepiece, blackpiece\n')

    timetook,played=round((time.time()-starttime),2),'white'if ismaxplayer else'black'
    computerscore=t[0]
    cumulativetime=whitecomputertime if ismaxplayer else blackcomputertime
    if analysis:
        liveanalys.append((movecnt,played,depth,shallowcount1,shallowcount,'4-1',depthsortmm,timetook,round(cumulativetime,2),round(smallmmtime,2),
                round(score,2),round(computerscore,2), len(white),len(black),printboard(white,black,onlyreturn=True)))
    print('total evals:',totalevals,', time for minmaxsmall:',smallmmtime,',calcscore:',round(t[0],2),', paath',t[1])

    return t
smallmmtime=0
totalevals=0

@jit(nopython=True)
def minimax(boardmm,depth,ismaxplayer=True,alpha=-10000,beta=10000,depthsort=0,depthsortminmax=0):#,path=[]): # depthsort, to explore first best possible gmaes
    #TODO IMP Cycle Detection: If the game state allows for repeating positions (cycles), ensure that your algorithm handles such scenarios to avoid infinite loops.
    #TODO MAKE BETTER Heuristic Evaluation Function 
    #TODO DONE starting 8 depth went from 5 sec to 0.19 sec (add alpa beta pruning to mae it faster)
    # can add path if u want evry path seperately for displaying or debug
    #TODO DONE (DOESNT SAVAE MUCH TIME)->( REMOVE PATH NOT NEEDED AS IT DOES SPERATELY FOR EVERY)
    #TODO MULTITHREADING FOR MORE DEPTHS SEARCH
    #(done 2 ways, one with foresight score calc using mnmax and onlyscorecalc sort)TODO  SORT BEFORE EXPLORING (for starting negatively impacst have to check in middle game)
    
    #if total%100000==0:print(total,depth,boardmm[2][0],path)
    #total+=1
    #IMP DONT PUT GLOBAL IT TAKES MUCH TIME EXTRA VERIFIED
    isterm=isterminated(boardmm,ismaxplayer)!=None
    if depth==0 or isterm :
        #if not isterm and iscapturethere(boardmm,ismaxplayer) != (getpossiblemovesmm(boardmm,ismaxplayer,checkifanycapture=True)):print(printboard(boardmm[0],boardmm[1],True))
        if not isterm and depth==0 and (
            #getpossiblemovesmm(boardmm,ismaxplayer,checkifanycapture=True)):#slower 5 secs
            iscapturethere(boardmm,ismaxplayer)): # NOT  NEEDED FOR BOTH PLAYERS BECAUSE IF YOUR MOVE AND CAPTURE MOVE IS THERE THEN ONLY INCREASE DEPTH
            #checkmoredepthifkillleft checkk anylysis in down
            depth+=1 # ie check one more depth
        else:
            #st=time.time()
            score=getscore(boardmm,ismaxplayer)
            #global smallmmtime
            #smallmmtime+=time.time()-st
            global total,totalevals # removing saves some seconds
            totalevals+=1
            return (score,[])
    possmoves=None
    #possmoves=getpossiblemovesmm(boardmm,ismaxplayer)
    possmoves=set(getpossiblemovesmm(boardmm,ismaxplayer))

    #if depthsortminmax>0 or depthsort>0: possmoves=getpossiblemovesmm(boardmm,ismaxplayer)
    #else:possmoves=set(getpossiblemovesmm(boardmm,ismaxplayer))
    #print(set(possmoves),'t',possmoves)
    # using set, startingboard total evals 160k, time 9sec
    #not using set  not using sorting 500k eval, 25sec
    # not using set and complete sorting, 50sec, evals 240k,, 6 sorting, evals400k 20sec, 3sorting 25sec evals 500k
    #if len(set(possmoves))!=len(possmoves):print(possmoves) #prints nothign
    #possmoves=set(possmoves)
    #possmoves=list(possmoves)
    possgames=None
    mcnt=boardmm[2][0]
    maxpath=[]
    maxpathcoord=None
    #print(depthsort)
    if depthsortminmax<=0 and depthsort>0:# so that it doesnt sort if depthsortmmm is there
        possmoves=list(possmoves)
        possgames={mo:movemm(mo,boardmm,ismaxplayer) for mo in possmoves}
        possmoves.sort(key=lambda y:getscore(possgames[y],ismaxplayer,False),reverse= ismaxplayer) 

        #print(ismaxplayer,[getscore(possgames[x]) for x in possmoves])
        # depth 10 getscore takes 3 sec, evals 100k, getscoresimple takes 3.7 sec, evals 120k
        # depth 11 getscore 22 sec evals 770k, simple took 22 sec evals 780k
    else:pass#possmoves=set(possmoves) # somehow orders in such a way that decreases total evals

    if depthsortminmax>0:#IMP MAKE IT SO THAT IT KEEPS SEARCHING IF THERE IS CAPTURE LEFT BECAUSE IT CAN ALTER SCORE # sort with foresight
        #possmoves=list(possmoves)
        possgames={mo:movemm(mo,boardmm,ismaxplayer) for mo in possmoves}

        posscore={}# move: minmaxscore

        
        #print('sortingforesight',depthsortminmax)
        #analysis examples
        # 0) with onlyyy minimaxv1 starting board time, 26s            with bestconfigs
        # 1) in endgame shallow120, depth11,depsort6,
        # without depthsortmm evals 1.9M time60sec, 
        #  with depthsortmm^^^ depthsortminmax 2,depth ofsmallminmax 3,  totalevals 1.3M time40s
        # if depthsortmm 1, deptsmallmm 5, evals 1.9M time60s
        # if depsortmm 2, deptsmallmm 5, evals 1.75M ,time 48s
        # if depsortmm 1, deptsmallmm 3, evals 1.65M ,time 46s
        # depsortmm 2, depsmalmm 4, evals 1.5M, time 45s, totaltimethesortingtook 1sec
        # depsortmm 3, depsmalmm 4, evals 1.5M, time 44s, totaltimethesortingtook 5sec
        # depsortmm 3, depsmalmm 3, evals 1.1M, time 32s, totaltimethesortingtook 3sec
        # depsortmm 4, depsmalmm 3, evals 1M, time 31s, totaltimethesortingtook 5sec
        # 2) in startboard, shallow 50,depth 11 ,depttosrto3
        #without, eval 160k, time 9s
        #with depthsortmm, depsortmm 4, depsmallmm 3, eval 70k, time 4s

        # all this^^^^ before adding checkmoredepthifkillleft
        # after         adding          ^^^^^^^^^^^^^^^

        # 2) in startboard, shallow 50,depth 11 ,depttosrto3
        #without, eval 240k, time 22s
        #with depthsortmm, depsortmm 3, depsmallmm 3, eval 180k, time 17s, doe depsortmm4, depsmallmm3 its same
        # if depsortmm 4, depsmallmm 2, eval 140k, time 13s
        # if depsortmm 5, depsmallmm 2, eval 115k, time 11s, ,if depsortmm 6, depsmallmm 2, takesmore time
        #1)    without, eval 2.2M, time 85s,  with,depsortmm 5, depsmallmm 2, eval 1M, time 40s
        #if depsortmm 6, depsmallmm 1(dynamic) , eval 100k, time 9s
        #now with dynamic depthsmallmm,  for 1st2 depth depthsmallmm=4, ITS A LITTLE BETTER 

        #3)middlegame board(4) deothsortmm 6, depthsmallmm(5-1) 7sec 101k eval,  if depthsmallmm(4-3-1) 5sec 90k eval
        st=time.time()

        for move,game in possgames.items():
            samecnt=game[2][0]==mcnt
            ismax=ismaxplayer if samecnt else not ismaxplayer
            depthsmallmm=1
            if depthsortminmax>5: depthsmallmm=4
            elif depthsortminmax>4: depthsmallmm=3 #if starting depth then keep more depthsmall
            elif depthsortminmax>3:depthsmallmm=2
            res=minimax(game,depthsmallmm,ismax)#depsmallmm
            gamescore=res[0]
            #print(depthsmallmm,len(res[1]))
            #print(move,gamescore)

            posscore[move]=gamescore
        #possmoves=set(possmoves)
        possmoves=list(possmoves)
        #print('time for minmaxsmall:',time.time()-st)
        possmoves.sort(key=lambda y:posscore[y],reverse= ismaxplayer) 
        global smallmmtime
        smallmmtime+=time.time()-st

    #TODO DONE INSTEAD OF CHECKING THEM SEPERATELY AS THEY BOTH ARE ALL COMMON 1 IS ENOUGH
    maxeval=1000000*(-1 if ismaxplayer else 1)# max or min eval
    for x in possmoves:
        posgame=movemm(x,boardmm,ismaxplayer) #possgames[x] if possgames else movemm(x,boardmm,ismaxplayer) 
        #posgame =movemm(x,boardmm,ismaxplayer) 
        #if len(possmoves)==1 and maxeval==-1000000:print(posgame)
        samecnt=posgame[2][0]==mcnt
        ismax=ismaxplayer if samecnt else not ismaxplayer
        #if samecnt:print(mcnt,posgame[2][0])
        #print([x]+path, posgame[2][0],depth)
        minmax=minimax(posgame,depth-1,ismax,alpha,beta,depthsort-1,depthsortminmax-1)#,[x]+path)# no need to copy posgame as its already copied
        #if x[0]==(4,3) and x[1]==(5,2):print('founddddddddddd',minmax[0],maxpath)

        val=minmax[0]
            
        if (ismaxplayer and (val>maxeval) )or(not ismaxplayer and (val<maxeval) ) :
            maxeval=val
            maxpath=minmax[1]
            maxpathcoord=x
        elif val==maxeval: # but if its loosing it takes longest path IMP
            # so computer chooses least move path
            #VERYIMP OTHERWISE IT WILL BE STUCK IN LOOP WHEN ITS WINNING COMPLETELY BCS SOMETIMES IT WILL GIVE LONGER PATH AND NEXT MOVE SHORTER AND NEXT MOVE LONGER SO ENDLESS LOOP MAY OCCUR
            winning = True
            if ismaxplayer :winning=val>0
            else:winning = val<0
            if (winning and len(maxpath)>len(minmax[1])) or (not winning and len(maxpath)<len(minmax[1])):
                maxpath=minmax[1]
                maxpathcoord=x
        if ismaxplayer:
            alpha=max(val,alpha)
        else:
            beta=min(val,beta)
        if str([maxpathcoord]+maxpath)=='[((3, 6), (4, 5), False), ((5, 4), (3, 6), True, (4, 5)), ((2, 3), (3, 2), False), ((7, 0), (6, 1), False), ((3, 2), (4, 1), False), ((6, 1), (5, 2), False), ((4, 1), (6, 3), True, (5, 2)), ((3, 6), (4, 5), False), ((6, 3), (5, 2), False), ((6, 5), (5, 4), False)]':
            print(val,maxeval,x,depth,depthsortminmax,samecnt,ismax,ismaxplayer)
            printboard(posgame[0],posgame[1],True)
        if alpha>=beta: break#common for both
    if abs(maxeval)>100000:
        print('error,',possmoves,ismaxplayer)
    return (maxeval,[maxpathcoord]+maxpath)#+ auto copies path

whiteturn,movecnt=True,0
gameover=False # used for stopping gui click function
blackcomputer,whitecomputer=bool(0),bool(0)
computerdepth,depthupdategui=9,10

liveanalys=[]#list of strings( movecnt, whoplayed, depth, shallow1, shallow2, depthsmallmm, depthsort, timetook, timetooksmallmm)
analysfile=open('anlysis.csv','a')

def startgame():
    toprofile,doliveanylysis=0,0
    profiler = None 
    '''
    if toprofile:
        import line_profiler
        profiler.add_function(minimax)
        profiler.add_function(iscapturethere)
        profiler.add_function(getscore)
        profiler.add_function(getpossiblemovesmm)
        profiler.add_function(movemm)
        profiler.add_function(getgamestate)

        profiler.enable()
    '''

    
    global posmovescoord
    initboard(board,True)
    printboard()
    posmovescoord=getpossiblemoves() # for gui
    maingui()# after this line doesnt run anything bcs of gui loop
    '''
    if toprofile:
        

        profiler=line_profiler.LineProfiler()
        profiler.disable()
        stream = io.StringIO()
        profiler.print_stats(stream=stream)
        res = stream.getvalue()
        res=res.split('\n')
        ret=''
        #'   612    205510   46953711.0    228.5     12.3      isterm=isterminated(boardmm)!=None'
        #'   612    205510   46953711.0    228.5     12.0'
        for x in res:
            if len(x)>48 and (x[46]==' ' or x[45]==' ' or x[44]==' '):continue
            add=True
            if len(x)>29:
                try:
                    no=round(float(x[17:29].replace(' ',''))/10000000,2)
                    x=x[:17:]+'         '+str(no)+x[29::]
                    #if no==0:add=False
                except:
                    print(x[17:29].replace(' ',''))
            if add:ret+=x+'\n'
        print(ret)
        '''
    if doliveanylysis:
        analysfile.write('\nMatch whitev2 vs blackv1:'+str(1)+'\n')
        analysfile.write('movecnt, whoplayed, depth, shallow1, shallow2, depthsmallmm, depthsort, timetook, cumulativetime , timetooksmallmm, score, minmaxscore, whitepiece, blackpiece, board\n')
        for x in liveanalys:
            text=''
            for y in x:text+=str(y)+', '
            #print(text)
            analysfile.write(text+'\n')
        analysfile.close()
# for useing custom board change board and whiteturn accordingly
total=0
startgame()

#matches
#depth 10 white vs depth 6 move cnt 20 totaltime, whiteL 107.  blacktook: 1. score:1


#matches issues
# stuck in loop
#white winning completey but not doing best move and stuck in loop FIXED# because it was winning so it kept talking longer paths even though smaller paths available, changed code to accomadate it
#white not doing optimal move
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'b', '*', '*', '*', '*', '*'],

#boards (whitetomove)
#endgame
#1) .2 score (draw)totaltime, whiteL 131.0464973449707  blacktook: 216.8417263031006 white v2 sort4
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'w', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'b', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'b', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],
#2) .02 score ,totaltime, whiteL 101.6  blacktook: 204.9 white v2,  120 shallow, total evals 760k, 5 depthtosort
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'wk', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],

#3)black winning -3,totaltime, whiteL 108.1  blacktook: 119.5
#['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', 'w', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', '*', '*', '*', '*', 'b', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'w', '*', '*', '*'],['*', 'b', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', 'w', '*'],

#4) -1 
#['*', '*', '*', 'b', '*', 'b', '*', 'b'],['b', '*', 'b', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', 'b', '*', '*'],['w', '*', 'w', '*', '*', '*', '*', '*'],['*', '*', '*', 'w', '*', '*', '*', 'b'],['*', '*', 'w', '*', '*', '*', 'w', '*'],

#5)2 score v2totalevals 750k shallow 113,  otaltime, whiteL 364.7  blacktook: 1357.7
## bug white sacrifising itself depth 10['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],
# ['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['bk', '*', 'w', '*', 'bk', '*', '*', '*'],
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', 'wk', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],