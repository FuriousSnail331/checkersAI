import time 
import gamelogic as glogic
import utils as util
import threading 
mindepthtosort=9
#MINIMAX
#boardminmax=(white,black,movecntarray), movecntarray for checking if double or triple kill there so same player will play again
#white -> maxplayer
# kingscore -> king val for each king

kingscore,peicescore=13,7 #not necessary balance it with so that max score 100 or close to it
piecevalue={False:1,True:2}# false for normal pirce, true for king

analysfile=None
def setanalysobj(obj):
    global analysfile
    analysfile=obj

def isterminated(boardmm,maxplayer):#not returns boolean just score if its terminated else NONE
    return glogic.getgamestate(boardmm[0],boardmm[1],boardmm[2][0],maxplayer)

def getscoresimple(boardmm,maxplayer):
    piecevalue={False:1,True:2}
    white,black=boardmm[0],boardmm[1]
    state = isterminated(boardmm,maxplayer)
    if state==None: #ie game is going on
        #whitekingcnt,blackkingcnt=sum(boardmm[0].values()),sum(boardmm[1].values())
        whitepiecesum=sum(piecevalue[x] for x in white.values())
        blackpiecesum=sum(piecevalue[x] for x in black.values())
        return whitepiecesum-blackpiecesum
    else:return state



scoreadvconst,scoremovecntconst=0.08,0.4

def getscore(boardmm,maxplayer,toround=False): #THE HEART OF THE INTELLIGENCE 
    # simple board evaluatiion for each piec 1 or if king 3
    #TODO ADD DIFFERENT EVALUATION CRITERIAS TO MAKE IT MORE ACCURETE
    # piece POSITION, BOARD CONTROL, PIECE SAFETY,PIECE ADVANCMENT
    # 2)MOBILITY, MOVEOPTIONS, CAPTURING OPURTUNITIES
    # 3)PIECE STRUCTURE, FORMATION-aligned can be more effective. , ISOLATION-Isolated pieces or poorly positioned pieces are less valuable
    # 4)Control of Key Areas, Position of Kings
    piecevalue={False:2,True:4}
    white,black=boardmm[0],boardmm[1]
    state = isterminated(boardmm,maxplayer)
    score=0
    if state==None: #ie game is going on
        #whitekingcnt,blackkingcnt=sum(boardmm[0].values()),sum(boardmm[1].values())
        whitepiecesum=sum(piecevalue[x] for x in white.values())
        blackpiecesum=sum(piecevalue[x] for x in black.values())
        score+= whitepiecesum-blackpiecesum #white want to increase positive black want to increase negative
        # if black more then score will be negative if white more it will be positive

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
        score+=(whiteadv-blackadv)*2

        #print(whiteadv,blackadv)
        #mobility, moveoptions
        #whitemoves,blackmoves=0,0
        wmoves,wcapturemoves=glogic.getpossiblemovesummary(boardmm,True)
        bmoves,bcapturemoves=glogic.getpossiblemovesummary(boardmm,False)
        whitemoves=(wmoves*scoremovecntconst)+(wcapturemoves*scoremovecntconst*1.5)
        blackmoves=(bmoves*scoremovecntconst)+(bcapturemoves*scoremovecntconst*1.5)
        score+=whitemoves-blackmoves
        return round(score,2) if toround else score

    else:return state # already have -100 or 100 or 0    game finished

def getbestbalancedsmalldeptmm(boardmm,ismaxplayer,rangedepth=range(7,12+1),rangesmalldepth=range(4,8)):
    starttime=time.time()
    threadtime={}
    timetaken={}

    for depth in rangedepth:
        for depthsortmm in rangesmalldepth:
            start=time.time()
            #thr= threading.Thread(target=util.getminmaxfromproces,args=(boardmm,ismaxplayer,depth,0,depthsortmm),daemon=True)
            shallowcount1,shallowcount2,shallowcount3=util.getshallowcount(boardmm,ismaxplayer)
            res=util.getminmaxfromproces(boardmm,ismaxplayer,depth,0,depthsortmm)
            took=round(time.time()-start,3)
            timetaken[(depth,depthsortmm)]=(took,shallowcount3,res[2],res[3])
    print('threadcnt:',len(threadtime))
    for x,val in threadtime.items():
        took=val[0]

    #print(timetaken)
    no=7
    for key,val in timetaken.items():
        if no!=key[0]:
            no=key[0]
            print()
        print(key,':',val,end=', ')
    

    timetook=round((time.time()-starttime),2)
    print('timetook:',timetook)


def minimaxv2(boardmm,depth,ismaxplayer=True,depthst=3,v2=True,analysis=None,dynamicdept=False):# to adjust with sorting first and other stuffs depthsort 
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
    depthtosort=None
    starttime=time.time()

    #shallowcount= sum((len(glogic.getpossiblemovesmm(board,not ismaxplayer)) for board in posboard))

    shallowcount1,shallowcount2,shallowcount3=util.getshallowcount(boardmm,ismaxplayer)
    #print('toktimetocountshallow:',(time.time()-starttime))


    if depth>mindepthtosort:
        depthtosort=3
    else:
        depthtosort=2
    if shallowcount2>120:depthtosort+=4
    elif shallowcount2>100:depthtosort+=3
    elif shallowcount2>60:depthtosort+=2
    elif shallowcount2>40:depthtosort+=1
    
    
    if dynamicdept:
        #if shallowcount3<100:depth+=1
        if shallowcount3>500:depth-=2
        elif shallowcount3>300:depth-=1

    
    depthsortmm=5
    if depth>=11:depthsortmm+=depth-10
    elif depth<=5:depthsortmm=3
    

    if shallowcount3>400:depthsortmm+=1

    v2=1
    if not v2:depthsortmm,depthtosort=0,0
    
    #score=getscore((white,black,[movecnt]),whiteturn)
    score=getscore(boardmm,ismaxplayer)

    if analysis:
        print('GOINGTOPLAY:'+('white'if ismaxplayer else 'black'),',depth',depth,', depthsortmm:',depthsortmm,',shallow:',shallowcount1,shallowcount2,shallowcount3,', depthtosort:',depthtosort,', score:',score)
    #print('possmoves,',getpossiblemovesmm(boardmm,ismaxplayer))



    #depthsortmm,depthtosort=0,0

    #result= minimax(boardmm,depth,ismaxplayer=ismaxplayer,depthsort=depthtosort,depthsortminmax=depthsortmm,findbestpath=False)



    #C++ CODE COMMUNICATION WITH CLI(COMMAND LINE INTERFACE)
    result=util.getminmaxfromproces(boardmm,ismaxplayer,depth,depthtosort,depthsortmm)


    #print('path:',t[1])
    #print(getpossiblemovesmm((white,black,[movecnt]),True))
    #analysfile.write('movecnt, whoplayed, depth, shallow1, shallow2, depthsmallmm, depthsort, timetook, cumulativetime , timetooksmallmm, score, minmaxscore, whitepiece, blackpiece\n')

    timetook,played=round((time.time()-starttime),2),'white'if ismaxplayer else'black'

    if dynamicdept:
        if timetook <0.5:
            depth+=2
            depthsortmm+=1
            result=util.getminmaxfromproces(boardmm,ismaxplayer,depth,depthtosort,depthsortmm)
            timetook=round((time.time()-starttime),2)
        elif timetook<2:
            depth+=1
            depthsortmm+=1
            result=util.getminmaxfromproces(boardmm,ismaxplayer,depth,depthtosort,depthsortmm)
            timetook=round((time.time()-starttime),2)

    computerscore=result[0]


    white,black,movecnt=boardmm
    cumulativetime= analysfile.whitecomputertime if ismaxplayer else analysfile.blackcomputertime
    totalevals,smallmmtime=result[2],result[3]

    #print('path:',result[1])
    if analysfile.enabled and analysis:
        analysfile.liveanalyslst.append((movecnt[0],played,depth,shallowcount1,shallowcount2,shallowcount3,'4-1',depthtosort,depthsortmm,timetook,round(cumulativetime,2),round(smallmmtime,2),
                round(score,2),round(computerscore,2), len(white),len(black),util.printboard(white,black,onlyreturn=True)))
        
    if analysis:print('total evals:',totalevals,', time for minmaxsmall:',smallmmtime,',calcscore:',round(result[0],2))#,', paath',t[1])


    return result
smallmmtime=0
totalevals=0
paths={}
#bestpath={}
#PROBLEM WITH BEST PATH SELECTION DUE TO ALPHA BETA PRUNING
def minimax(boardmm,depth,ismaxplayer=True,alpha=-10000,beta=10000,depthsort=0,depthsortminmax=0,path=[],findbestpath=False): # depthsort, to explore first best possible gmaes
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
            glogic.iscapturethere(boardmm,ismaxplayer)): # NOT  NEEDED FOR BOTH PLAYERS BECAUSE IF YOUR MOVE AND CAPTURE MOVE IS THERE THEN ONLY INCREASE DEPTH
            #checkmoredepthifkillleft checkk anylysis in down
            depth+=1 # ie check one more depth
        else:
            score=getscore(boardmm,ismaxplayer)
            #global smallmmtime
            #smallmmtime+=time.time()-st
            global totalevals # removing saves some seconds
            totalevals+=1
            return (score,[])#,path,False)
    possmoves=None
    possmoves=set(glogic.getpossiblemovesmm(boardmm,ismaxplayer))

    # using set, startingboard total evals 160k, time 9sec
    #not using set  not using sorting 500k eval, 25sec
    # not using set and complete sorting, 50sec, evals 240k,, 6 sorting, evals400k 20sec, 3sorting 25sec evals 500k
    possgames=None
    mcnt=boardmm[2][0]
    maxpath=[]
    maxpathcoord=None
    #print(depthsort)
    if depthsortminmax<=0 and depthsort>0:# so that it doesnt sort if depthsortmmm is there
        possmoves=list(possmoves)
        possgames={mo:glogic.movemm(mo,boardmm,ismaxplayer) for mo in possmoves}
        possmoves.sort(key=lambda y:getscore(possgames[y],ismaxplayer,False),reverse= ismaxplayer) 

        #print(ismaxplayer,[getscore(possgames[x]) for x in possmoves])
        # depth 10 getscore takes 3 sec, evals 100k, getscoresimple takes 3.7 sec, evals 120k
        # depth 11 getscore 22 sec evals 770k, simple took 22 sec evals 780k
    else:pass#possmoves=set(possmoves) # somehow orders in such a way that decreases total evals

    if depthsortminmax>0:#IMP MAKE IT SO THAT IT KEEPS SEARCHING IF THERE IS CAPTURE LEFT BECAUSE IT CAN ALTER SCORE # sort with foresight
        #possmoves=list(possmoves)
        possgames={mo:glogic.movemm(mo,boardmm,ismaxplayer) for mo in possmoves}

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
        #if depth==7:print([(posscore[x],x[0]) for x in possmoves])

    #TODO DONE INSTEAD OF CHECKING THEM SEPERATELY AS THEY BOTH ARE ALL COMMON 1 IS ENOUGH
    maxeval=1000000*(-1 if ismaxplayer else 1)# max or min eval
    for x in possmoves:
        posgame=glogic.movemm(x,boardmm,ismaxplayer) #possgames[x] if possgames else movemm(x,boardmm,ismaxplayer) 
        #posgame =movemm(x,boardmm,ismaxplayer) 
        samecnt=posgame[2][0]==mcnt
        ismax=ismaxplayer if samecnt else not ismaxplayer
        #if samecnt:print(mcnt,posgame[2][0])
        #print([x]+path, posgame[2][0],depth)
        minmax=minimax(posgame,depth-1,ismax,alpha,beta,depthsort-1,depthsortminmax-1,findbestpath=findbestpath)#,path+[x])# no need to copy posgame as its already copied
        val=minmax[0]
        if not findbestpath:findbestpath=(findbestpath or abs(val)==100) 
        if depth==10:
            if x[0]==(7,2):print(minmax[1])

        if (ismaxplayer and (val>maxeval) )or(not ismaxplayer and (val<maxeval) ) :
            maxeval=val
            maxpath=minmax[1]
            maxpathcoord=x
        elif val==maxeval: # but if its loosing it takes longest path IMP
            
            # so computer chooses least move path
            #VERYIMP OTHERWISE IT WILL BE STUCK IN LOOP WHEN ITS WINNING COMPLETELY BCS SOMETIMES IT WILL GIVE LONGER PATH AND NEXT MOVE SHORTER AND NEXT MOVE LONGER SO ENDLESS LOOP MAY OCCUR
            #but bug due to this because of alphabetacutoff 
            winning = True
            if ismaxplayer :winning=val>0
            else:winning = val<0
            if (findbestpath and ((winning and len(maxpath)>len(minmax[1])) or (not winning and len(maxpath)<len(minmax[1])))):
                maxpath=minmax[1]
                maxpathcoord=x#is it necessary, can it be wrong
        if ismaxplayer:
            alpha=max(val,alpha)
        else:
            beta=min(val,beta)
        if alpha>=beta: 
            if alpha==beta and findbestpath:continue#maxeval+=1*(1 if ismaxplayer else -1)
            break#common for both
    if abs(maxeval)>100000:
        print('error,',possmoves,ismaxplayer)
    return (maxeval,[maxpathcoord]+maxpath)#,bestpath,isalphacut)#+ auto copies path
