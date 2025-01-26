#layout -> gamelogic 
#       -> GUI   ->MINIMAX ALGO   -> MAIN GAME STARTING
# vvvvvvvvvvvvvvvvvv all imports
from threading import Thread
import time
import numpy as np
#^^^^^^^^^^^^^^^^^^^

import guihelper as gui
import utils as util
import minmaxhelper as minmax
import gamelogic as gamelogic
#
#GAME LOGIC 
#
#


def getpossiblemoves():#TODO DONE instead of recursion keep same turn if more captures available # DONE doesnt work for black king captureing 
    return gameboard.getpossiblemoves()#gamelogic.getpossiblemovesmm((white,black,[movecnt]),whiteturn) # using optimized function

def simulatemovegui(coord,updateguiscoreifnokillleft,): # for computer move # changes movecnt and whiteturn
    '''
    global movecnt,white,black,whiteturn
    prevmovecnt=movecnt# prevmovecoutn
    updatedboard=gamelogic.movemm(coord,(white,black,[movecnt]),maxplayer)
    white,black,newmovecnt=updatedboard
    newmovecnt=newmovecnt[0] # move count inside array 
    gui.updateallpieces(white,black)

    if prevmovecnt!=newmovecnt: # ie more kills are not there
        
        whiteturn= not whiteturn 
        movecnt=newmovecnt
        if updateguiscoreifnokillleft:updatescoregui()
        #posmovescoord=getpossiblemoves()#
        #break #return True # no more kills left
    

    checkgamestate()# now white turn has changed but we want to check for now only
    if gameboard.gameover:return
    return prevmovecnt!=newmovecnt # true if no more kiils left
    '''

    nokilleft=gameboard.move(coord)
    gui.updateallpieces(gameboard.white,gameboard.black)

    if updateguiscoreifnokillleft:updatescoregui()
    gui.updateposmovesgui(getpossiblemoves())
    checkgamestate()
    if gameboard.gameover:return
    return nokilleft

def checkgamestate():
    if gameboard.isended():
        print('GAME OVER')
        gui.updategamestategui(gameboard.getgamestate())
'''
def checkgamestate(): # for checking and then displaying
    gamestate = gamelogic.getgamestate(white,black,movecnt,whiteturn)
    if gamestate!= None:
        print('GAME OVER')
        gameboard.gameover=True
        gui.updategamestategui(gamestate)
'''

#blackcomputertime,whitecomputertime=0,0
def computermove(earlierturn,depth ,v2=True,gocompletelyinbestpath=False):# it will update possible moves
    # no need to input copies of white and black because it wont change
    starttime,timetook=time.time(),0
    result=minmax.minimaxv2((gameboard.white,gameboard.black,[gameboard.movecnt]),depth,earlierturn,v2=v2,analysis=True,dynamicdept=True) 
    bestpath=result[1]
    ind=0
    if gocompletelyinbestpath:
        while ind<len(bestpath):
            time.sleep(3)
            simulatemovegui(bestpath[ind],True)
            ind+=1
        return
    while gameboard.whiteturn==earlierturn:#if more double kills
        if gameboard.gameover:break# dont simulate move as thread diff
        if ind>=len(bestpath):
            bestpath=minmax.minimaxv2((gameboard.white,gameboard.black,[gameboard.movecnt]),depth,earlierturn,v2=v2,analysis=True,dynamicdept=True)[1]
        
        re=simulatemovegui(bestpath[ind],True)
        if re:
            timetook=time.time()-starttime
            if not gameboard.whiteturn:analyshelper.whitecomputertime+=timetook# because black moved
            else: analyshelper.blackcomputertime+=timetook
            print('totaltime,','whiteL',round(analyshelper.whitecomputertime,1),' blacktook:',round(analyshelper.blackcomputertime,1))

            if gameboard.gameover:return
        
        ind+=1#missed simple caused bug
    #now white turn is opposite ie for that turn is there if whiteturn true then its the chance of white to move
    print('COMPUTER MOVED ->',not gameboard.whiteturn,'movecnt:',gameboard.movecnt)

    if timetook<0.5: time.sleep(0.2)
    print(gameboard)
    #util.printboard(white,black)
    checkcomputermove()

def checkcomputermove(newthread=True,gocompletelyinbestpath=False):#call only if game not over
    checkgamestate()# as new thread dont check here
    if gameboard.gameover:return
    if gocompletelyinbestpath:#for simulating purposes
        #computermove(gameboard.whiteturn,10,True,gocompletelyinbestpath=True)#tfor debug
        Thread(target=computermove,args=(gameboard.whiteturn,computerdepth,True,True),daemon=True).start()


    #print('COMPUTER MOVING THINKING,',movecnt, whiteturn)
    if gameboard.whiteturn and whitecomputer:
        Thread(target=computermove,args=(gameboard.whiteturn,computerdepth,True),daemon=True).start()
        #computermove(gameboard.whiteturn,10,True)
    elif not gameboard.whiteturn and blackcomputer:
        Thread(target=computermove,args=(gameboard.whiteturn,computerdepth,False),daemon=True).start()
    # now white turn has changed but we want to check for now only
    return True
    # other all things checked in computermove and simulate move

# for guis
###########################

def toggleblackcomputer():
    global blackcomputer
    blackcomputer=not blackcomputer
    print('setting computer',blackcomputer)
    gui.computerbutton.configure(text='Computer: '+('ON' if blackcomputer else 'OFF'))
    return blackcomputer

def startgui():
    gui.updateposmovesgui(getpossiblemoves())
    gui.maingui(gameboard)
    gui.computerbutton.configure(text='Computer: '+('ON' if blackcomputer else 'OFF'),command=toggleblackcomputer)
    gui.canvas.bind('<Button-1>',canvasclick)
    starttime=time.time()
    updatescoregui(start=True)
    print('time took:',(time.time()-starttime))
    checkcomputermove(gocompletelyinbestpath=0)
    gui.root.mainloop()# after this line doesnt run anything bcs of gui loop

def updatescoregui(start=False):
    res=minmax.minimaxv2((gameboard.white,gameboard.black,[gameboard.movecnt]),depthupdategui,gameboard.whiteturn,analysis=gameboard.movecnt==0,v2=True,dynamicdept=start)
    gui.updatescoregui(res)

def canvasclick(event):
    #global clicked,posmovesid,posmovescoord
    if gameboard.gameover:return        
    row,col=(event.y//gui.gridsize,event.x//gui.gridsize)
    
    rectid=gui.boardrects[(row,col)]
    isblack=(row + col) % 2
    if blackcomputer and not gameboard.whiteturn:return
    if whitecomputer and gameboard.whiteturn:return 
    if isblack:
        if (row,col) in gui.posmovesid:
            simulatemovegui(gui.posmovesid[(row,col)][1],True)#,gameboard.whiteturn,not blackcomputer,True)
            #util.printboard(white,black)
            print(gameboard)
            print(gui.posmovescoord)
            gui.delposmoves()
            checkcomputermove()
            return
        gui.canvasclicked(rectid,row,col)
#######################################
#
#MINIMAX
#boardminmax=(white,black,movecntarray), movecntarray for checking if double or triple kill there so same player will play again
#white -> maxplayer
# kingscore -> king val for each king

gameboard=None

toprofile,doliveanylysis=0,0

analyshelper=util.analyshelper(enabled=doliveanylysis)



#whiteturn,movecnt=True,0
#gameover=False # used for stopping gui click function
#white,black={},{}#key is position val is king or not
#BOARD IS NOT USED IN SIMULATION JUST FOR INITIALISATION
#board * if empty w, b if whhite pice or blac, wk ,bk if king
board=[
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'w', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'b', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'b', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', 'wk', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', 'bk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],
#['*', '*', '*', 'b', '*', 'b', '*', 'b'],['b', '*', 'b', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', 'b', '*', '*'],['w', '*', 'w', '*', '*', '*', '*', '*'],['*', '*', '*', 'w', '*', '*', '*', 'b'],['*', '*', 'w', '*', '*', '*', 'w', '*'],
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['bk', '*', 'w', '*', 'bk', '*', '*', '*'],
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],

#['*', '*', '*', 'b', '*', '*', '*', '*'],['b', '*', 'wk', '*', '*', '*', 'b', '*'],['*', 'w', '*', '*', '*', '*', '*', '*'],['w', '*', 'w', '*', '*', '*', '*', '*'],['*', 'w', '*', '*', '*', '*', '*', '*'],['*', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],

#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],



#['*', '*', '*', 'b', '*', 'b', '*', 'b'],['b', '*', '*', '*', 'b', '*', 'b', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', '*', '*', '*', '*', 'b', '*'],['*', 'b', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'w', '*', 'w', '*'],['*', '*', '*', 'w', '*', 'w', '*', 'w'],['w', '*', 'w', '*', 'w', '*', 'w', '*'],
['*', '*', '*', '*', '*', 'b', '*', '*'],['wk', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['*', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],['*', 'bk', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],

#to fix cyclic dept 10
#['*', 'bk', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', '*', '*', '*', '*'],['*', '*', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', 'w', '*'],
#['*', '*', '*', '*', '*', 'b', '*', '*'],['wk', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['*', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],['*', 'bk', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],




]
#board=[['*']*8 for x in range(8)] # dont use 2 multiplication bcs it will link to same array

blackcomputer,whitecomputer=1,0
computerdepth,depthupdategui=12,9
#liveanalys=[]#list of strings( movecnt, whoplayed, depth, shallow1, shallow2, depthsmallmm, depthsort, timetook, timetooksmallmm)
#import traceback
def startgame():
    #print('\n'.join(traceback.format_stack()))
    profiler = None 
    if toprofile:
        import line_profiler
        profiler=line_profiler.LineProfiler()
        profiler.add_function(minmax.minimax)
        profiler.add_function(gamelogic.iscapturethere)
        profiler.add_function(minmax.getscore)
        profiler.add_function(gamelogic.getpossiblemovesmm)
        profiler.add_function(gamelogic.movemm)
        profiler.add_function(gamelogic.getgamestate)

        profiler.enable()
        
    #utils.startlineprofile()
    minmax.setanalysobj(analyshelper)

    global gameboard
    gameboard=gamelogic.gameboard(board,movecnt=0,whiteturn=True,customset=0)

    #minmax.getbestbalancedsmalldeptmm((gameboard.white,gameboard.black,[0]),gameboard.whiteturn,range(12,13),range(4,9))

    '''#endgame
        GOINGTOPLAY:white ,depth 11 , depthsortmm: 6 ,shallow: 9 31 279 , depthtosort: 3 , score: 6.3428571428571425
        total evals: 273268 , time for minmaxsmall: 7 ,calcscore: 7.13
        time took: 0.7797307968139648

        (7, 3) : (0.025, 279, 4857, 0), (7, 4) : (0.026, 279, 6401, 0), (7, 5) : (0.028, 279, 6999, 1), (7, 6) : (0.05, 279, 20537, 7),
        (8, 3) : (0.035, 279, 6077, 0), (8, 4) : (0.036, 279, 8515, 0), (8, 5) : (0.049, 279, 10084, 1), (8, 6) : (0.081, 279, 29784, 7),
        (9, 3) : (0.111, 279, 36877, 0), (9, 4) : (0.199, 279, 35658, 0), (9, 5) : (0.2, 279, 36587, 1), (9, 6) : (0.245, 279, 57564, 7),
        (10, 3) : (0.325, 279, 54616, 0), (10, 4) : (0.286, 279, 49200, 0), (10, 5) : (0.284, 279, 51493, 1), (10, 6) : (0.33, 279, 70489, 7),       
        (11, 3) : (0.854, 279, 291719, 0), (11, 4) : (0.706, 279, 246099, 0), (11, 5) : (0.775, 279, 256597, 1), (11, 6) : (0.775, 279, 273268, 7),  
        (12, 3) : (1.97, 279, 296486, 0), (12, 4) : (1.793, 279, 279246, 0), (12, 5) : (1.777, 279, 279262, 1), (12, 6) : (1.982, 279, 337526, 7), ti    
        ^^^^^^^^^^all suggests should be decreased by 1
        
        
        #endgame
        GOINGTOPLAY:white ,depth 12 , depthsortmm: 7 ,shallow: 11 56 616 , depthtosort: 4 , score: 4.222857142857142
        total evals: 835587 , time for minmaxsmall: 68 ,calcscore: 4.08
        time took: 3.367061138153076
        
        (7, 4) : (0.08, 616, 18255, 2), (7, 5) : (0.121, 616, 34257, 2), (7, 6) : (0.195, 616, 54781, 19), (7, 7) : (0.404, 616, 110022, 67),
        (8, 4) : (0.1, 616, 22148, 1), (8, 5) : (0.13, 616, 28116, 1), (8, 6) : (0.213, 616, 57895, 21), (8, 7) : (0.497, 616, 132007, 67),
        (9, 4) : (1.04, 616, 112419, 1), (9, 5) : (1.288, 616, 147585, 2), (9, 6) : (1.053, 616, 151803, 19), (9, 7) : (1.339, 616, 232190, 80),
        (10, 4) : (1.897, 616, 316643, 1), (10, 5) : (2.142, 616, 393860, 1), (10, 6) : (1.765, 616, 331372, 21), (10, 7) : (1.536, 616, 321799, 78),     
        (11, 4) : (6.212, 616, 1693770, 1), (11, 5) : (7.343, 616, 2080835, 1), (11, 6) : (2.586, 616, 743957, 19), (11, 7) : (2.747, 616, 754994, 70),   
        (12, 4) : (6.092, 616, 1597561, 1), (12, 5) : (7.103, 616, 1833320, 1), (12, 6) : (3.165, 616, 795272, 18), (12, 7) : (3.324, 616, 835587, 64), ti 
        ^^^^^^^^^^^ all suests current is goood


        #start  
        GOINGTOPLAY:white ,depth 12 , depthsortmm: 7 ,shallow: 7 49 343 , depthtosort: 4 , score: -2.220446049250313e-16
        total evals: 412506 , time for minmaxsmall: 913 ,calcscore: -1.29
        time took: 6.876075744628906

        (7, 4) : (0.199, 343, 11091, 13), (7, 5) : (0.29, 343, 18173, 78), (7, 6) : (0.563, 343, 34633, 212), (7, 7) : (1.197, 343, 65192, 728),
        (8, 4) : (0.221, 343, 11657, 4), (8, 5) : (0.249, 343, 14662, 52), (8, 6) : (0.458, 343, 27351, 166), (8, 7) : (1.572, 343, 95108, 833),
        (9, 4) : (0.415, 343, 21462, 6), (9, 5) : (0.402, 343, 22427, 43), (9, 6) : (0.478, 343, 28474, 126), (9, 7) : (2.123, 343, 127129, 963),
        (10, 4) : (1.394, 343, 72381, 11), (10, 5) : (1.226, 343, 66490, 48), (10, 6) : (1.594, 343, 90487, 218), (10, 7) : (2.667, 343, 157721, 958),    
        (11, 4) : (4.13, 343, 247489, 5), (11, 5) : (2.811, 343, 171689, 62), (11, 6) : (3.009, 343, 182121, 193), (11, 7) : (3.08, 343, 183376, 805),    
        (12, 4) : (11.4, 343, 696132, 7), (12, 5) : (9.03, 343, 551072, 67), (12, 6) : (7.743, 343, 479694, 208), (12, 7) : (6.748, 343, 412506, 885), tim        


        #middlegame
        12, white, 12, 7, 45, 315, 4-1, 4, 7, 7.33, 17.76, 393, -0.79, -0.3, 9, 9, ['*', '*', '*', 'b', '*', 'b', '*', 'b'],['b', '*', '*', '*', 'b', '*', 'b', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', '*', '*', '*', '*', 'b', '*'],['*', 'b', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'w', '*', 'w', '*'],['*', '*', '*', 'w', '*', 'w', '*', 'w'],['w', '*', 'w', '*', 'w', '*', 'w', '*'],

        (12, 4) : (9.63, 315, 845813, 5), (12, 5) : (9.07, 315, 806536, 19), (12, 6) : (7.66, 315, 641722, 135), (12, 7) : (7.39, 315, 621181, 397), (12, 8) : (7.004, 315, 580079, 1320), timetook: 40.75


    '''
    
    #util.initboard(board,white,black,False)
    #util.printboard(gameboard.white,gameboard.black)
    print(gameboard)

    startgui()

    if toprofile:
        util.printlineprofile(profiler)
    if doliveanylysis:
        print('LIVE ANALYSS')#,analyshelper.liveanalyslst)
        util.outputanalysfile(analyshelper.liveanalyslst,title='mevsblaccomp , notprofiled, scoresdv*2 , depth13, dynamicdep',sort=True)#sort by time taken for eac move
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
## FIXED (bcs of dct=fromcoord)bug white sacrifising itself depth 10['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', 'wk', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],
# ['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['bk', '*', 'w', '*', 'bk', '*', '*', '*'],
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'wk', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', 'wk', '*', '*'],['b', '*', '*', '*', 'bk', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['bk', '*', 'w', '*', '*', '*', '*', '*'],


#white sac bug
#['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', 'wk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', 'b', '*', 'w'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['*', '*', 'b', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['*', '*', 'w', '*', '*', '*', 'w', '*'],

#white not becoming king
#['*', '*', '*', '*', '*', 'b', '*', 'b'],['b', '*', '*', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['w', '*', 'b', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'w', '*', 'w', '*', '*', '*'],['*', '*', '*', '*', '*', 'b', '*', '*'],['w', '*', 'w', '*', 'w', '*', 'w', '*'],

#stuck in loop black winning
#['*', '*', '*', '*', '*', 'b', '*', 'wk'],['wk', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', 'bk', '*', 'w'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['bk', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'w', '*', '*', '*', '*', '*'],
#one more stuck only in cpp
#['*', '*', '*', 'b', '*', '*', '*', 'b'],['b', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', 'w', '*', '*', '*', '*'],['w', '*', 'w', '*', 'b', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['w', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],
#onemore but its draw not advancing
#['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'wk', '*', 'wk', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', 'bk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', 'w', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],


#white winning totally but looop fixed by findfullpath v3
#['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'wk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', 'w', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'wk', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'bk'],['*', '*', '*', '*', '*', '*', '*', '*'],

#white winnin totally but cant find the win move ,can fix by adding cycle detection maybe or increasing depth certainly
#['*', 'bk', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', 'wk', '*', '*', '*', '*', '*'],['*', '*', '*', 'wk', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'b'],['*', '*', '*', '*', '*', '*', 'w', '*'],

#black winnnig almost ending depth 10 but if depth 13 it finds win
##['*', '*', '*', '*', '*', 'b', '*', '*'],['wk', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', 'w'],['*', '*', 'bk', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', 'bk', '*', '*', '*'],['*', 'bk', '*', '*', '*', '*', '*', '*'],['*', '*', '*', '*', '*', '*', '*', '*'],
