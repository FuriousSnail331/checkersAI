import subprocess
import ctypes
import time
#either one use
# for subprocess
'''
g++ -O3 -o test.exe test.cc
g++ -O3 test.cc -o test.exe

for sub
result = subprocess.run(['./mycppfunction'], stdout=subprocess.PIPE)
res=result.stdout.decode()
print(f'Result from C++ function: {res}')


g++ -shared -o test.dll test.cc
for ctype
lib = ctypes.CDLL('./mycppfunction.so')  # Use .dll on Windows

# Call the C++ function
result = lib.my_cpp_function()


white={(2, 1): True, (2, 3): True, (3, 6): True, (6, 7): False, (7, 2): False}
black={(0, 7): False, (5, 0): False, (5, 4): True, (6, 5): True, (7, 0): True}

'''
import sys
sys.path.insert(0,'D:/Users/Juweriah/Documents/python/tictactoe/checkers')
import gamelogic as glogic

def getshallowcount(boardmm,ismaxplayer):# 1rst layer secondlayer count, secondlayer actual branches
    pos=(glogic.getpossiblemovesmm(boardmm,ismaxplayer))
    shallowcount1,shallowcount2=len(pos),0
    posboard=[glogic.movemm(cord,boardmm,ismaxplayer) for cord in pos]
    for board in posboard:
        ismax= ismaxplayer if (board[2][0]==boardmm[2][0]) else not ismaxplayer
        shallowcount2+=len(glogic.getpossiblemovesmm(board,ismax))
    shallowcount3=shallowcount1*shallowcount2#the actual shallow count of depth 2


    return (shallowcount1,shallowcount2,shallowcount3)

white={(2, 1): True, (2, 3): True, (3, 6): True, (6, 7): False, (7, 2): False}
black={(0, 7): False, (5, 0): False, (5, 4): True, (6, 5): True, (7, 0): True}


def getminmaxfromproces(boardmm,whiteturn,depth,depthsort,depthsortmm):
    def converttostr(dct):
        st=''
        for x,y in dct.items():
            st+=str(x[0])+str(x[1])+('T' if y else 'F')
        return st
    white,black,movecnt=boardmm
    movecnt=movecnt[0]
    path=[r"D:\Users\Juweriah\Documents\python\tictactoe\commandlinecpp\test.exe"]
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
    #print(score)
    #print(path)
    return (score,path,totalevals,timetakensmallmm)

start=time.time()

print(getshallowcount((white,black,[0]),True))
res=getminmaxfromproces((white,black,[0]),True,13,4,9)

print("timetoook:",time.time()-start)
print((int(res[2])/10**3),"K")
print((int(res[2])/10**6),"M")

print(int(res[3])/1000)
print(res)