import utils as util
class gameboard:#not used for mm
    def __init__(self,board=None,movecnt=0,whiteturn=True,customset=False):
        self.white={}
        self.black={}
        util.initboard(board,self.white,self.black,customdone=customset)
        self.movecnt=movecnt
        self.whiteturn=whiteturn
        self.gameover=False
    def __str__(self) -> str:
        return util.printboard(self.white,self.black,onlyreturn=True)
    def getpossiblemoves(self):
        return getpossiblemovesmm((self.white,self.black,[self.movecnt]),self.whiteturn)
    def move(self,coord): #if double kill its one move
        t=movemm(coord,(self.white,self.black,[self.movecnt]) ,self.whiteturn,True)
        if t[2][0]!=self.movecnt:
            self.movecnt+=1
            self.whiteturn=not self.whiteturn
            #print('now whyyyite',self.whiteturn,t[2])
            return True# true if no more kill left
        #print('now white',self.whiteturn,t[2])
        return False
    def getgamestate(self):
        return getgamestate(self.white,self.black,self.movecnt,self.whiteturn)
    def isended(self):
        gamestate = self.getgamestate()
        if gamestate!= None:
            self.gameover=True
            return True
def tt(lst):lst[0]+=1
def getgamestate(white,black,movecnt,maxplayer): 
    #CRASH FIXED TODO GIVE SCORE WHEN NO MOVES LEFT IE IT LOST but pieces are there
    # used for getting score dont change
    if movecnt>230:return 0 # can lead to crash
    if len(white)==0:return -100
    elif len(black)==0:return+100
    elif len(white)<=1 and len(black)<=1:return 0 # draw both lenth 1
    else:
        if not getpossiblemovesummary((white,black,[movecnt]),maxplayer,True):
            return -100 if maxplayer else 100
        #if not istherepossiblemoves(white,black,movecnt,True):return -100# white lost because no move left for it
        #if not istherepossiblemoves(white,black,movecnt,False):return 100# black lost because no move left for it
    return None # ie game is going on


def inbound(row,col):return 0<=row<8 and 0<=col<8 

def iscapturethere(boardmm,maxplayer,fromcoord=None):#max player is now whose move
    # any capture there, optimized because if one found connected with enemy simply check if enmy kill also there
    kingcord,bcord,wcord=((1,-1),(-1,-1),(1,1),(-1,1)),((1,-1),(1,1)),((-1,-1),(-1,1))#if king or normal piece (rowadd,cadd)
    dct,enemydct=((boardmm[0],boardmm[1]) if maxplayer else (boardmm[1],boardmm[0]))
    #if fromcoord!=None:dct={fromcoord:dct[fromcoord]} #WAISTED2HRSSSSSSSSSSSSSBUGthis is wrong as we are checking if jumpedposnot in dct
    t=((fromcoord,dct[fromcoord]),) if fromcoord else (dct.items())#two tuples required bcs looping
    for (row,col),isking in (t):
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
def movemm(movecoord,boardmm,maxplayer,sameboard=False): # creates and return in copy  of boardmm
    # DOESNT CHANGE WHITE TURN CHANGE IT AFTER CALLING AFTER CHECKING IF MOVECNT INCREASED IE NO DOUBLE KILL LEFT
    # be sure to check if its valid coord before calling
# TODO FIXED    put movecnt in boarddm 2nd elemnt # TODO FIXED    FIX DOESNT CHANGE KING TO TRUE IN MOVEMM
    if not sameboard:boardmm=(boardmm[0].copy(),boardmm[1].copy(),boardmm[2].copy())
    fromcoord,tocoord=movecoord[0],movecoord[1]

    pieces=boardmm[0] if maxplayer else boardmm[1]
    enemypieces= boardmm[0] if not maxplayer else boardmm[1]#what, no its cooreect

    pieces[tocoord]= pieces.pop(fromcoord) # remove from and put in toocord, basically move coord with same king boolean

    if movecoord[2]:# ie kill true
        enemypieces.pop(movecoord[3]) # remove the other colour which is captured

    becameking=False
    if ((maxplayer and tocoord[0]==0)or(not maxplayer and tocoord[0]==7))  and pieces[tocoord]==False: #if already not king and reached there respective row ending
        becameking=True
        pieces[tocoord]=True # ie it became king

    # dont change turn if any more kill is there ,and this move was kill and didnt became king after killing
    if not becameking and movecoord[2]:
        if iscapturethere(boardmm,maxplayer,tocoord):return boardmm#to check if double kill
    boardmm[2][0]+=1# increment move cnt
    return boardmm

