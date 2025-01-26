/*

use-O3 or Ofast but with caution
//ofast- 0.2 sec slower

profile guided opti;  ==1sec faster for 9 ; only 1 run can use multiple runs


g++ -O3 -fprofile-generate your_program.cpp -o your_program
./your_program   # Run with typical input
g++ -O3 -fprofile-use your_program.cpp -o your_program_optimized


g++ -O3 -fprofile-generate test.cc -o testexe
g++ -O3 -fprofile-use test.cc -o testexe
testexe 


//linktime- 0.5 sec faster in 8
g++ -O3 -flto test.cc -o testlto

//autovectorisation 0.2 sec slower
g++ -O3 -ftree-vectorize test.cc -o testvext

//functioninlining 0.01 sec slower
g++ -O3 -finline-functions test.cc -o testinline


//combined
g++ -O3 -flto -ftree-vectorize -finline-functions test.cpp -o test_optimized

//combined+pgo takes 3 sec longer
g++ -O3 -fprofile-generate -ftree-vectorize -finline-functions test.cc -o testcomb
g++ -O3 -flto -fprofile-use -ftree-vectorize -finline-functions test.cc -o testcomb

//combined +pgo only best ones;  1.1 sec faster
g++ -O3 -fprofile-generate test.cc -o testcomb
g++ -O3 -flto -fprofile-use test.cc -o testcomb

//earlier but depth 13, so testcomb takes- normal takes 26sec ,this takes 22.5 sec
.....
*/


#include <iostream>
#include <vector>//dynamic list
#include <unordered_set>//hashset
#include <unordered_map>//hashmap
#include <string>
#include <utility> //for pairs
#include <algorithm>
#include <chrono>

using namespace std;


using coordtype = int;
using scoretype = double;


static int add(int a,int b){
    return a+b;
}

struct coord{
    coordtype row;
    coordtype col;//def val
    bool operator==(const coord& other) const{
        return other.row==row && other.col==col;
    }
    coord():row(-1),col(-1){};
    coord(coordtype row,coordtype col):row(row),col(col){};
    //copy constructor
    coord(const coord& other):row(other.row),col(other.col){};
    //copy assignment
    coord& operator=(const coord& other){
        if(this!=&other){
            row=other.row;
            col=other.col;
        }
        return *this;
    }
};
struct movepos{
    coord fromm;
    coord to;
    bool iskill;
    coord jumpedpos;
    bool operator==(const movepos& other) const{
        return other.fromm==fromm && other.to==to &&other.iskill==iskill&&other.jumpedpos==jumpedpos;
    }
    movepos():iskill(false){};
    movepos(coord fromm,coord to,bool iskill):fromm(fromm),to(to),iskill(iskill),jumpedpos(coord(-1,-1)){};
    movepos(coord fromm,coord to,bool iskill,coord jumpedpos):fromm(fromm),to(to),iskill(iskill),jumpedpos(jumpedpos){};
    movepos(const movepos& other):fromm(other.fromm),to(other.to),iskill(other.iskill),jumpedpos(other.jumpedpos){};
    movepos& operator=(const movepos& other) {
        if (this != &other) {
            fromm = other.fromm;
            to = other.to;
            iskill = other.iskill;
            jumpedpos = other.jumpedpos;
        }
        return *this;
    }
};

namespace std {
    template <>
    struct hash<coord> {
        size_t operator()(const coord& s) const {
            return hash<int>()(s.row) ^ (hash<int>()(s.col) << 1);
        }
    };
    template <>
    struct hash<movepos> {
        size_t operator()(const movepos& s) const {
            return hash<coord>()(s.fromm) ^ (hash<coord>()(s.to) << 1)^ (hash<bool>()(s.iskill) << 2);
        }
    };
}
struct info{
    bool isking=false;
};
struct board{//might can be refrence
    unordered_map<coord,info> white,black;
    int movecnt;
    //board(const board& other):white(other.white),black(other.black),movecnt(other.movecnt){};
    //board() : movecnt(0) {};
    //board(unordered_map<coord,info> white, unordered_map<coord,info> black,int movecnt):white(white),black(black),movecnt(movecnt){};


};


struct mmret{
    scoretype score;
    vector<movepos> path;
};

mmret minimax(const board& boardmm,int depth,bool ismaxplayer,int depthsort,int depthsortmm,scoretype alpha,scoretype beta,bool fullpath=false);
scoretype getscore(const board& board,bool maxplayer);

static bool inbound(const coord& coord);

template<typename hashset,typename U>
static bool isthere(hashset& set,const U& search);

static bool isterminated(const board& boardmm,bool maxplayer);

static int getgamestate(const board& boardmm,bool maxplayer);

static vector<movepos> getpossmoves(const board& board, bool maxplayer);

//check for erro handling
static board simmove(const movepos& move,board board,bool maxplayer); //we need to copy board

static bool isthereanymove(const board& board, bool maxplayer);

static pair<int,int> getposmovessum(const board& board,bool maxplayer,bool onlycheckifmove=false);

//check for error handling
static bool iscapturethere(const board& board,bool maxplayer,const coord& fromcoord= {-1,-1});

string crdstr(const coord& cord){
    return to_string(static_cast<int>(cord.row))+to_string(static_cast<int>(cord.col));
}




static int totalevals=0;
static int timesmallmm=0;




int main(int argc, char* argv[]){
    //string test="hello";
    //std::cout << test << std::endl;
    //cout<<argc<<endl;
    unordered_map<coord,info> white,black;
    int movecnt=0,depth=12,depthsort=6,depthsortmm=7;
    bool whiteturn = true;
    
    for(int i =0;i<argc;i++){
        string st(argv[i]);
        if(i==1 || i==2){
            for(size_t ind = 0;ind<st.size();ind+=3){
                int colst=st[ind+1]-'0',rowst=st[ind]-'0';
                coordtype col=static_cast<coordtype>(colst),row=static_cast<coordtype>(rowst);
                //cout<<row<<col<<endl;
                if(i==1)white[coord(row,col)] =info{st[ind+2]=='T'};
                else black[coord(row,col)] =info{st[ind+2]=='T'};
            }
        }else if(i==3)whiteturn=(st[0]=='T')?true:false;
        else if(i==4) movecnt=stoi(st);
        else if(i==5) depth=stoi(st);
        else if(i==6) depthsort=stoi(st);
        else if(i==7) depthsortmm=stoi(st);

        //cout<<i<<" "<< st<<endl;
    }
    /*
    cout<<movecnt<<" "<<whiteturn<<" "<<depth<<" "<<depthsort<<" "<<depthsortmm<<" "<<endl;
    cout<<white.size()<<"eeeee"<<endl;
    for(const auto&[key,val]:white){
        cout<<static_cast<int>(key.row)<<" "<<key.col<<" "<<val.isking<<endl;
    }
    cout<<"black"<<endl;
    for(const auto&[key,val]:black){
        cout<<key.row<<" "<<key.col<<" "<<val.isking<<endl;
    }
    
    
    unordered_map<coord,info> white={
        {{2, 1}, {true}}, {{2, 3}, {true}} ,{{3, 6}, {true}}, {{6, 7}, {false}}, {{7, 2}, {false}}
    };
    unordered_map<coord,info> black={
        {{0, 7}, {false}}, {{5, 0}, {false}}, {{5, 4}, {true}}, {{6, 5}, {true}}, {{7, 0}, {true}}
    };
white {(1, 2): True, (2, 7): False, (4, 7): False, (7, 2): False, (7, 6): False} blac {(0, 5): False, (2, 5): False, (5, 2): False, (5, 4): False, (6, 5): False}
    
    unordered_map<coord,info> white={
        {{1, 2}, {true}}, {{2, 7}, {false}} ,{{4, 7}, {false}}, {{7, 2}, {false}}, {{7, 6}, {false}}
    };
    unordered_map<coord,info> black={
        {{0, 5}, {false}}, {{2, 5}, {false}}, {{5, 2}, {false}}, {{5, 4}, {false}}, {{6, 5}, {false}}
    };
    white={
        {{2, 1}, {true}}, {{2, 3}, {true}} ,{{3, 6}, {true}}, {{6, 7}, {false}}, {{7, 2}, {false}}
    };
     black={
        {{0, 7}, {false}}, {{5, 0}, {false}}, {{5, 4}, {true}}, {{6, 5}, {true}}, {{7, 0}, {true}}
    };
    */
    board boardmm=board{white,black,movecnt};

    auto curr=chrono::high_resolution_clock::now();
    mmret res = minimax(boardmm,depth,whiteturn,depthsort,depthsortmm,-10000,10000);


    auto end=chrono::high_resolution_clock::now();
    auto took=chrono::duration_cast<chrono::milliseconds>(end-curr);
    //cout<<"took :"  <<took.count()<<endl;
    //cout<<to_string(getscore(boardmm,true))<<endl;
    cout<<to_string(res.score)<<endl;
    cout<<totalevals<<endl;
    cout<<timesmallmm<<endl;

    string ret;
    for(const movepos& move:res.path){
        cout<<crdstr(move.fromm)+crdstr(move.to)+(move.iskill?"T":"F")+crdstr(move.jumpedpos)<<endl;
    }
    return 0;
}
template<typename hashset,typename U>
static bool isthere(hashset& set,const U& search){
    return set.find(search)!=set.end();
}

static bool inbound(const coord& coord){return coord.row<8 && coord.row>=0 && coord.col<8 && coord.col>=0;}
//template<typename map>   const map& white, const map& black
static int getgamestate(const board& boardmm,bool maxplayer){
    if (boardmm.movecnt > 250)return 0;//draw
    if(boardmm.white.size()==0)return -100;
    else if(boardmm.black.size()==0)return +100;
    else if(boardmm.white.size()<=1 && boardmm.black.size()<=1 )return 0;
    else{
        if (!isthereanymove(boardmm,maxplayer)) return maxplayer? -100:100;
    }
    return -1000;
}
static bool isterminated(const board& boardmm,bool maxplayer){
    return getgamestate(boardmm,maxplayer)!=-1000;
}
static const std::pair<coordtype,coordtype> kingcord[]={{1,-1},{-1,-1},{1,1},{-1,1}};
static const std::pair<coordtype,coordtype> bcord[]={{1,-1},{1,1}};
static const std::pair<coordtype,coordtype> wcord[]={{-1,-1},{-1,1}};
static bool iscapturethere(const board& board,bool maxplayer,const coord& fromcoord){//const unordered_map<coord,info>& white,const unordered_map<coord,info>& black,bool maxplayer,coord fromcoord){

    const unordered_map<coord,info>& freind = maxplayer? board.white:board.black;
    const unordered_map<coord,info>& enemy = maxplayer? board.black:board.white;
    if(!isthere(freind,fromcoord) && fromcoord.row!=-1)cout<<"errrrorr"<<endl;
    unordered_map<coord,info> from; 
    if(fromcoord.row!=-1)from[fromcoord]=freind.at(fromcoord);//returns refrence but we are not changingso doesnt matter
    //from[fromcoord] = freind.find(fromcoord)->second;
    /*
    if (it != freind.end()) {
        const info& value = it->second;
    } else{}*/

    for(const auto& [pos ,info]: fromcoord.row==-1?freind:from){
        const std::pair<coordtype, coordtype>* coords=info.isking?kingcord:(maxplayer?wcord:bcord);
        int end = info.isking? 4:2;
        for(int i =0; i<end;i++){
            const coordtype rowadd=coords[i].first; 
            const coordtype coladd =coords[i].second;
            //int rowmove,colmove; rowmove=rowadd+pos.row;  colmove=coladd+pos.col;
            const coord enemycoord=coord(pos.row+rowadd,pos.col+coladd);
            if (isthere(enemy,enemycoord)){
                const coord jumpedpos=coord(enemycoord.row+rowadd, enemycoord.col+coladd);
                if(inbound(jumpedpos)&& !isthere(enemy,jumpedpos)&& !isthere(freind,jumpedpos))return true;
            }
        }
    }
    return false;
}
static bool isthereanymove(const board& board, bool maxplayer){return getposmovessum(board,maxplayer,true).first!=-1;}
static pair<int,int> getposmovessum(const board& board,bool maxplayer,bool onlycheckifmove){

    const unordered_map<coord,info>& freind = maxplayer? board.white:board.black;
    const unordered_map<coord,info>& enemy = maxplayer? board.black:board.white;
    int moves=0,capturemoves=0;
    for(const auto& [pos ,info]: freind){
        const auto* coords=info.isking?kingcord:(maxplayer?wcord:bcord);
        const int end = info.isking? 4:2;
        for(int i =0; i<end;i++){

            const coordtype rowadd=coords[i].first; const coordtype coladd =coords[i].second;

            //cout<<"h"<<end<<" "<<rowadd<<" "<<coladd<<" "<<info.isking<<endl;
            //int rowmove,colmove; rowmove=rowadd+pos.row;  colmove=coladd+pos.col;
            const coord tocoord=coord(pos.row+rowadd,pos.col+coladd);
            if(!inbound(tocoord))continue;
            if(isthere(enemy,tocoord)){
                coord jumpedpos=coord(tocoord.row+rowadd, tocoord.col+coladd);
                if(inbound(jumpedpos) && !isthere(freind,jumpedpos) && !isthere(enemy,jumpedpos))capturemoves++;
            }else if(!isthere(freind,tocoord))moves++;

            if (moves+capturemoves>0 && onlycheckifmove)return {moves,capturemoves};
        }
    }
    if(onlycheckifmove)
        return {-1,-1}; //didnt found any move
    return {moves,capturemoves};
}
static vector<movepos> getpossmoves(const board& board, bool maxplayer){
    vector<movepos> lst={};
    bool killfound=false;
    const unordered_map<coord,info>& freind = maxplayer? board.white:board.black;
    const unordered_map<coord,info>& enemy = maxplayer? board.black:board.white;
    for(const auto& [pos ,info]: freind){
        const auto* coords=info.isking?kingcord:(maxplayer?wcord:bcord);
        int end = info.isking? 4:2;
        for(int i =0; i<end;i++){
            const coordtype rowadd=coords[i].first; 
            const coordtype coladd =coords[i].second;
            //int rowmove,colmove; rowmove=rowadd+pos.row;  colmove=coladd+pos.col;
            const coord tocoord=coord(pos.row+rowadd,pos.col+coladd);
            if(!inbound(tocoord))continue;
            if(isthere(enemy,tocoord)){
                const coord jumpedpos=coord(tocoord.row+rowadd, tocoord.col+coladd);
                if(inbound(jumpedpos)){
                    bool kill =!isthere(freind,jumpedpos) && !isthere(enemy,jumpedpos);
                    if(kill){
                        if(!killfound){
                            killfound=true;
                            lst={};
                        }
                        lst.push_back(movepos(pos,jumpedpos,true,tocoord));//jumped pos is the pos in which its landed
                    }
                }
            }else if(!killfound && !isthere(freind,tocoord)){
                lst.push_back(movepos(pos,tocoord,false));
            }
        }
    }
    return lst;
}
//TODO migt need error handleing
static board simmove(const movepos& move,board board,bool maxplayer){//we need copy of board
    const coord& fromcoord=move.fromm, tocoord=move.to;
    unordered_map<coord,info>& pieces = maxplayer? board.white:board.black;//only refrence to copy of board
    unordered_map<coord,info>& enemypieces = maxplayer? board.black:board.white;//refrence is imp

    if(!isthere(pieces,move.fromm)||(move.iskill && !isthere(enemypieces,move.jumpedpos))){
        cout<<"ERROR MOVE MM";
        return board;
    }

    pieces[move.to]=info{pieces[move.fromm].isking};
    pieces.erase(move.fromm);

    if(move.iskill)enemypieces.erase(move.jumpedpos);

    bool becameking=false;
    if(((maxplayer && tocoord.row==0) || (!maxplayer && tocoord.row==7)) && !pieces[tocoord].isking){
        becameking=true; 
        pieces[tocoord]=info{true};
    }
    if(!becameking && move.iskill){
        if(iscapturethere(board,maxplayer,tocoord))return board;
    }
    board.movecnt++;
    return board;
}
static int normalval=2,kingval=4;
static scoretype scoreadvconst=static_cast<scoretype>(0.08),scoremovecntconst=static_cast<scoretype>(0.4);


scoretype getscore(const board& board,bool maxplayer){
    int state= getgamestate(board,maxplayer);
    scoretype score=0;
    if(state<=-1000){//TODO make it better
        
        int wpieceval=0,bpieceval=0 ; //for total pieceval
        int whiteadv=0,blackadv=0;
        int whitecenter=0,blackcenter=0;

        for(const auto& [pos,info]:board.white){
            //scoretype row=static_cast<scoretype>(pos.row),col=static_cast<scoretype>(pos.col);//doesnt make any diffferenec
            //coordtype row=pos.row,col=pos.col;//doesnt make any diffferenec

            wpieceval+=info.isking?kingval:normalval;// for piece val
            if(!info.isking)
                whiteadv+=7-pos.row;//if not king then row advancement
            else whitecenter+=(pos.row<4? pos.row:  7-pos.row);//only col adv if king 
            whitecenter+=(pos.col<4? pos.col : 7-pos.col); // for center

        }   
        for(const auto& [pos,info]:board.black){
            //scoretype row=static_cast<scoretype>(pos.row),col=static_cast<scoretype>(pos.col);
            //coordtype row=pos.row,col=pos.col;//doesnt make any diffferenec
            bpieceval+=info.isking?kingval:normalval;// for piece val
            if(!info.isking)
                blackadv+=pos.row;//if not king then row advancement
            else blackcenter+=(pos.row<4? pos.row: 7-pos.row);//only col adv if king 
            blackcenter+=(pos.col<4? pos.col : 7-pos.col); // for center
        }
        score+=static_cast<scoretype>(wpieceval-bpieceval);
        score+=(static_cast<scoretype>(whiteadv-blackadv)/7)*scoreadvconst*3 ;
        score+=static_cast<scoretype>(whitecenter-blackcenter)*0.03*5 ;

        pair<int,int> wsummary =getposmovessum(board,true);
        pair<int,int> bsummary =getposmovessum(board,false);

        scoretype wmoves=static_cast<scoretype>(wsummary.first), wcapturemoves= static_cast<scoretype>(wsummary.second);
        scoretype bmoves=static_cast<scoretype>(bsummary.first), bcapturemoves= static_cast<scoretype>(bsummary.second);
        scoretype whitemovesval=((wmoves)+(wcapturemoves*1.5));
        scoretype blackmovesval=((bmoves)+(bcapturemoves*1.5));


        score+=(whitemovesval-blackmovesval)*scoremovecntconst;
        
        return score;
    }else return static_cast<scoretype>(state);
}

//TODO can optimize paths
//alpha = -10000, beta = 10000
mmret minimax(const board& boardmm,int depth,bool ismaxplayer,int depthsort,int depthsortmm,scoretype alpha,scoretype beta,bool fullpath){
    bool isterm=isterminated(boardmm,ismaxplayer);
    /*cout<<ismaxplayer<<depth<<depthsortmm<<"\n";
    
    cout<<isterm<<"\n";*/
    if(depth==0||isterm){
        if(!isterm && depth ==0 &&iscapturethere(boardmm,ismaxplayer))depth++;
        else{
            totalevals++;
            //if (totalevals%10000==0)cout<<totalevals<<"\n";
            scoretype score=getscore(boardmm,ismaxplayer);
            return mmret{score,{}};
        }
    }
    const vector<movepos>& possmoves= getpossmoves(boardmm,ismaxplayer);
    //const vector<movepos>& t= getpossmoves(boardmm,ismaxplayer); unordered_set<movepos> possmove(t.begin(),t.end()); vector<movepos> possmoves;
    //std::copy(possmove.begin(),possmove.end(),std::back_inserter(possmoves));

    vector<movepos> possmovessorted;
    //unordered_map<movepos,board> possgamessorted;//remoove if more memory taking
    bool usesorted=false;
    const int mcnt=boardmm.movecnt;

    vector<movepos> maxpath={};
    const movepos* maxpathcoord=nullptr;

    if(true){
    if(depthsortmm>0){
        usesorted=true;
        vector<pair<movepos,scoretype>> possgames;
        const auto curr=chrono::high_resolution_clock::now();


        for(const auto& move:possmoves){
            const board& boardmoved=simmove(move,boardmm,ismaxplayer);

            //possgamessorted[move]=boardmoved;

            bool samecnt=boardmoved.movecnt==mcnt;
            bool ismax= samecnt?ismaxplayer:!ismaxplayer;
            int depthsmallmm=1;
            if (depthsortmm>5) depthsmallmm=4;
            else if (depthsortmm>4) depthsmallmm=3; //if starting depth then keep more depthsmall
            else if (depthsortmm>3)depthsmallmm=2;

            const auto& res=minimax(boardmoved,depthsmallmm,ismax,0,0,-10000,10000);//#depsmallmm ////////////////////////////////// might need to use copy
            scoretype gamescore=res.score;
            possgames.push_back({move,gamescore});
        }
        
        //unordered_map<movepos,board> possgames;//might be error
        if(ismaxplayer)
            std::sort(possgames.begin(),possgames.end(),
            [](const auto& other,const auto& other2){return other.second>other2.second ; });//if maxplayer then reversed
        else
            std::sort(possgames.begin(),possgames.end(),
            [](const auto& other,const auto& other2){return other.second<other2.second ; });//>is decreasing, < is increaseng

        const auto end=chrono::high_resolution_clock::now();
        timesmallmm+=chrono::duration_cast<chrono::milliseconds>(end-curr).count();
        for(const auto& [move,score]:possgames)possmovessorted.push_back(move);
    }else if(depthsort>0){
        usesorted=true;
        vector<pair<movepos,scoretype>> possgames;
        for(const auto& move:possmoves){
            const board& boardmoved = simmove(move,boardmm,ismaxplayer);
            //possgamessorted[move]=boardmoved;

            possgames.push_back({move,getscore(boardmoved,ismaxplayer)});
        }
        //unordered_map<movepos,board> possgames;//might be error
        if(ismaxplayer)
            std::sort(possgames.begin(),possgames.end(),
            [](const auto& other,const auto& other2){return other.second>other2.second ; });//if maxplayer then reversed
        else
            std::sort(possgames.begin(),possgames.end(),
            [](const auto& other,const auto& other2){return other.second<other2.second ; });//>is decreasing, < is increaseng
        for(const auto& [move,score]:possgames)possmovessorted.push_back(move);
        
    }}
    scoretype maxeval = ismaxplayer?-1000000:+1000000;
    //if(depth>=6)cout<<'e'<<possmoves.size()<<'e'<<possmovessorted.size()<<usesorted<<endl;

    for(const movepos& move:usesorted?possmovessorted:possmoves){
        //if(depth==7)cout<<'e'<<" "<<ismaxplayer<<endl;

        const board& posgame= 
            //usesorted?possgamessorted[move]:
            simmove(move,boardmm,ismaxplayer);

        bool samecnt=posgame.movecnt==mcnt;
        bool ismax=samecnt?ismaxplayer:!ismaxplayer;
        const mmret& minmax= minimax(posgame,depth-1,ismax,depthsort-1,depthsortmm-1,alpha,beta,fullpath);
        const scoretype val=minmax.score;

        if(!fullpath)fullpath=fullpath||abs(maxeval)==100;//for path best

        if((ismaxplayer &&val>maxeval) || (!ismaxplayer &&val<maxeval)){
            
            maxeval=val;
            maxpath=minmax.path;//makes copy
            maxpathcoord=&move;


            //if(!fullpath)fullpath=fullpath||abs(maxeval)==100;//for path best  can be here

        }else if(val==maxeval){
            //only do if its terminated otherwise always its same path right
            bool winning= ismaxplayer?val>0:val<0;
            if(fullpath&&(((winning && maxpath.size()>minmax.path.size())|| (!winning && maxpath.size()<minmax.path.size())))) {
                maxpath=minmax.path;//makes copy
                maxpathcoord=&move;
            }
        }
        if(ismaxplayer)alpha=max(alpha,val);
        else beta=min(beta,val);
        if(alpha>=beta){
            if((fullpath)&& alpha==beta){//to make paths correct
                //maxeval+=0.1*(ismaxplayer?1:-1);
                continue;//ie dont break
            }
            break;
        }
    
    }
    if(abs(maxeval)>=10000)std::cout<<"errrrror"<<possmoves.size()<<" "<<depthsortmm<<std::endl;
    maxpath.insert(maxpath.begin(),*maxpathcoord);//movepos(maxpathcoord->fromm,maxpathcoord->to,maxpathcoord->iskill,maxpathcoord->jumpedpos));
    return mmret{maxeval,maxpath};
}
/*
if u want to profile
first run ->  g++ -O3 -pg test.cc -o test.exe
then 
gprof test.exe gmon.out > analysis.txt

tocompile with highest optimisation wehtn from 50sec to 15
g++ -O3 test.cc -o test.exe
tocompile
torun 
g++ test.cc -o test.exe
test.exe

g++ "D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.cc" -o "D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.exe"
"D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.exe"

or in one command 

g++ "D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.cc" -o "D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.exe" & "D:\Users\Juweriah\Documents\python\tictactoe\fromctest\test.exe"


*/

//