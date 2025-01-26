import io
import subprocess
import gamelogic as glogic
class analyshelper:
    def __init__(self,enabled):
        self.whitecomputertime=0
        self.blackcomputertime=0
        self.liveanalyslst=[]
        self.enabled=enabled
    
def getcellcolour(row,col):#board pattern
    return 'white' if ((row+col) %2==0) else 'black'

def initboard(board,white,black,customdone=False):# custom done true if alreayd board initlized
    for row in range(8):
        for col in range(8):
            if customdone :
                if board[row][col][0]=='w':white[(row,col)]=len(board[row][col])>1 # cant use one line because board can be * and one line only else there
                elif board[row][col][0]=='b':black[(row,col)]=len(board[row][col])>1
                continue
            if (row<3 or row>4) and (getcellcolour(row,col)=='black'):
                (black if row<3 else white)[((row,col))]=False#ie its not king
    print('white',white,'blac',black)

def printboard(whitee,blackk,space=False,onlyreturn =False):#uses white and black
    board=[['*']*8 for x in range(8)]
    printt=''
    for x,king in (whitee|blackk).items():
        k='k' if king else ''
        board[x[0]][x[1]]='w'+k if x in whitee else 'b'+k
    for row,x in enumerate(board,0):  printt+=(str(x)+('\n,' if space else','))
    if onlyreturn:return printt
    else:print(printt)

def outputanalysfile(liveanalys,title='whitev2 vs blackv1',sort=False):
    analysfile=open('anlysis.csv','a')
    analysfile.write('\nMatch '+title+':'+str(1)+'\n')
    analysfile.write('movecnt, whoplayed, depth, shallow1, shallow2, shallow3, depthsmallmm, depthsort, depthsortmm, timetook, cumulativetime , timetooksmallmm, score, minmaxscore, whitepiece, blackpiece, board\n')
    for x in liveanalys:#write unsorted
        text=''
        for y in x:text+=str(y)+', '
        analysfile.write(text+'\n')

    if sort:liveanalys.sort(key=lambda x:x[9])# by time took
    for x in liveanalys:
        text=''
        for y in x:text+=str(y)+', '
        #print(text)
        analysfile.write(text+'\n')
    analysfile.close()
def printlineprofile(profiler):
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

# return score, pat,totaleveal,smallmmtiem
def getminmaxfromproces(boardmm,whiteturn,depth,depthsort,depthsortmm):
    def converttostr(dct):
        st=''
        for x,y in dct.items():
            st+=str(x[0])+str(x[1])+('T' if y else 'F')
        return st
    white,black,movecnt=boardmm
    movecnt=movecnt[0]
    path=[r"commandlinecpp\testcomb.exe"]
    whitstr,blackstr=converttostr(white),converttostr(black)

    addconfig=[whitstr,blackstr,(str(whiteturn)[0]),str(movecnt),str(depth),str(depthsort),str(depthsortmm)]
    result=subprocess.run(path+addconfig,stdout=subprocess.PIPE)
    res=result.stdout.decode()
    res=res.replace("\r",'').split("\n")
    score,totalevals,timetakensmallmm=-1,-1,-1
    path=[]
    try:
        score=float(res[0].replace(" ",""))
        totalevals=int(res[1].replace(" ",""))
        timetakensmallmm=int(res[2].replace(" ",""))

        for x in range(3,len(res)):
            if len(res[x])<6:continue
            iskill=res[x][4]=='T'
            fromm=(int(res[x][0]),int(res[x][1]))
            to=(int(res[x][2]),int(res[x][3]))

            if iskill:
                jumped=(int(res[x][5]),int(res[x][6]))
                path.append((fromm,to,iskill,jumped))
            else:
                path.append((fromm,to,iskill))
            #print(path,iskill)

    except:
        print(res)
        print('errorwhileconvertback')
    return (score,path,totalevals,timetakensmallmm)


def getshallowcount(boardmm,ismaxplayer):# 1rst layer secondlayer count, secondlayer actual branches
    pos=(glogic.getpossiblemovesmm(boardmm,ismaxplayer))
    shallowcount1,shallowcount2=len(pos),0
    posboard=[glogic.movemm(cord,boardmm,ismaxplayer) for cord in pos]
    for board in posboard:
        ismax= ismaxplayer if (board[2][0]==boardmm[2][0]) else not ismaxplayer
        shallowcount2+=len(glogic.getpossiblemovesmm(board,ismax))
    shallowcount3=shallowcount1*shallowcount2#the actual shallow count of depth 2


    return (shallowcount1,shallowcount2,shallowcount3)
#res=getminmaxfromproces((white,black,[0]),True,12,6,7)
#print(res)