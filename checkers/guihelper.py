import time
import tkinter as tk

#
#GUI
#
#import checgame as main

def gethex(r, g, b):return f'#{r:02x}{g:02x}{b:02x}'

blackcol,whitecol,blackdarkcol,whitepiece,blackpiece,outline=gethex(222, 152, 87),gethex(255, 244, 201),gethex(170, 112, 52),gethex(230,230,230),gethex(66, 64, 54),gethex(161, 102, 47)
boardrects={} # rectpos->id
pieceid={}# pos->id

posmovesid={} # outlinepos->id
posmovescoord=[] # possible moves
clicked=None

kingcol=gethex(252, 223, 76)

def updateposmovesgui(posmoves):
    global posmovescoord
    posmovescoord=posmoves

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
def movepiece(row,col,torow,tocol): # for gui#not used
    x=tocol * gridsize
    y=torow * gridsize
    canvas.moveto(pieceid[(row,col)],x,y)

    pieceid[(torow,tocol)] = pieceid[(row,col)]  # updating id
    pieceid.pop((row,col))

def canvasclicked(rectid,row,col):
    global clicked
    if clicked!=rectid:#diff cell clicked
        if clicked:delposmoves()
        for coord in posmovescoord:# making all possible moves overlay
            if coord[0]==(row,col):
                movepos=coord[1]
                x,y=movepos[1] * gridsize,movepos[0] * gridsize

                posid= canvas.create_oval(x, y, x + gridsize, y + gridsize, width=gridsize//20, outline=blackpiece,tags='possmoves')
                posmovesid[movepos]=(posid,coord)#0 is id 1 is full coord, key is tomovepos
        canvas.itemconfig(rectid, fill=blackdarkcol)
        clicked=rectid

    else:#same cell clicked again
        delposmoves()

def delposmoves():
    global clicked,posmovesid
    canvas.delete('possmoves')#0 is id 
    posmovesid={}
    canvas.itemconfig(clicked, fill=blackcol)
    clicked=None

def updategamestategui(gamestate): # for checking and then displaying
    #gamestate = main.getgamestate(white,black,movecnt,maxplayer)
    if gamestate!= None:
        #print('GAME OVER')
        #main.gameover=True
        text=''
        if gamestate==-100:text='BLACK WON'
        elif gamestate==+100:text='WHITE WON'
        else: text='ITS DRAW'
        canvas.create_rectangle(220, 220,400, 350,fill=whitecol, width=5,outline=outline)
        canvas.create_text(300,270,text=text,fill='black',width=150,font=("Helvetica", 15))

def converttonotation(coord):
    return (chr(65+coord[0])+str(coord[1]+1))

def updatescoregui(result):# for checking and displaying score and displaying prediction and bestpath
    #result=minimaxv2((white,black,[movecnt]),depth,iswhitemove,analysis=movecnt==0)
    drawscore(result[0]) # draw score

    bestpath=result[1]
    #print('bestpath',bestpath,'\n score,',result[0])
    print(result[0])#,main.getscore((white,black,[movecnt]),iswhitemove))
    drawprediction(result[0]) #draw prediction

    # TODO DONE MAKE GUUI TO DISPLAY BEST PATH
    bestpathnotation=[converttonotation(x[0])+'-'+converttonotation(x[1]) for x in bestpath]
    drawpath(bestpathnotation)
    #print('bestpathinnotation',bestpathnotation)

    drawdepth(len(bestpath))
def canvasmousemove(event):
    row,col=(event.y//gridsize,event.x//gridsize)
def buttonenter(event):
    event.widget.config(bg=blackcol)
def buttonleave(event):
    event.widget.config(bg=whitecol)
def updateallpieces(white,black):#NOW OPTIMIZED (NOW NOT completely updatepieces)
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
def draw_board(white,black):#MADE IT COMPATIBLE WITH KINGs
    for row in range(8):
        for col in range(8):
            color = blackcol if (row+col)%2==1 else whitecol
            x,y=col * gridsize,row * gridsize
            boardrects[(row,col)]= canvas.create_rectangle(x, y,(col + 1) * gridsize, (row + 1) * gridsize,fill=color, outline=outline)
    #OPTIMIZED  seperate loop to maintain pices level on top  on graphic, changes when moving
    updateallpieces(white,black)

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


greyscore=gethex(161, 161, 161)
whitescore=gethex(214, 212, 212)
boardx,boardy,gridsize=40,40,70
canvas,scorepanel,predictpanel,pathpanel,depthpanel,computerbutton=None,None,None,None,None,None
root=None
mainboard=None

def maingui(gameboard): # init board before calling
    global canvas,predictpanel,scorepanel,pathpanel,depthpanel,computerbutton,root
    global mainboard
    mainboard=gameboard
    root = tk.Tk()
    root.title("Checkers Board")
    frame=tk.Frame(root,background=blackdarkcol,width=1200,height=700,borderwidth=5, relief="solid")
    frame.pack_propagate(False) # disable from fitting

    canvas = tk.Canvas(frame, width=gridsize*8, height=gridsize*8)
    #canvas.bind("<Motion>",canvasmousemove)
    #canvas.bind('<Button-1>',canvasclick)
    canvas.place(x=boardx,y=boardy)

    predictpanel = tk.Label(frame, bg=whitecol,fg=outline,width=30,height=3,borderwidth=5, relief="solid",font=("Helvetica", 15))
    predictpanel.place(x=boardx+640, y=boardy+10)

    pathpanel=tk.Label(frame, bg=whitecol,fg=outline,width=15,height=15,borderwidth=5, relief="solid",font=("Helvetica", 15),justify=tk.LEFT,anchor="nw",padx=30,pady=10)#,wraplength=10)
    pathpanel.place(x=boardx+640, y=boardy+140)

    depthpanel=tk.Label(frame, bg=whitecol,fg=outline,width=5,height=3,borderwidth=5, relief="solid",font=("Helvetica", 15,'bold'),justify=tk.LEFT,anchor="nw",padx=30,pady=10)#,wraplength=10)
    depthpanel.place(x=boardx+640+320, y=boardy+180)

    computerbutton=tk.Button(frame,width=12,height=3,font=("Arial", 13,'bold'),relief=tk.RIDGE,borderwidth=13,bg=whitecol,fg=outline)
    #togglecomputer() or togglecomputer() #keeping it enabled
    #computerbutton.configure(text='Computer: '+('ON' if True else 'OFF'))
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
    
    draw_board(gameboard.white,gameboard.black)


    '''starttime=time.time()
    
    updatescoregui(depthupdategui,whiteturn,white,black,movecnt)
    print('time took:',(time.time()-starttime))
    from checgame import checkcomputermove
    checkcomputermove()'''
    frame.pack(padx=10,pady=10)

    #root.mainloop() # do eevrything before it 
    
