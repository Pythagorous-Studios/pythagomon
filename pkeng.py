import random
import logger
attacks={}
pokemon={}
#all known pokemon types
pktps=['fire','water','electric','plant','normal']
weakness=[('fire','water'),('water','electricity'),('plant','fire')]
strength=[('water','fire'),('electricity','water'),('fire','plant')]
loglvl=1
#IMPORTANT: upon completion of alpha 1.0 incorporate into pythag
def log(msg,lvl=1):
    """wraper for the logger library"""
    if loglvl==lvl:
        print(logger.log(msg,__name__,lvl))
    else:
        logger.log(msg,lvl)
        
def modchk(slf,opp):
  mod=1
  for seq in weakness:
    if seq[0] == slf.typ and seq[1]==opp.typ:
      mod=.5
  for seq in strength:
    if seq[0] == slf.typ and seq[1] ==opp.typ:
      mod=2

def rand(lower,upper):
    """my wrapper for rand.randint()"""
    return ramdom.randint(lower,upper)

"""error class tree"""
class InvalidMoveParam(BaseException):
    """Error class for faulty arguments passed to the attack class"""
    pass

class InvalidMove(BaseException):
  pass

class InvalidMoveType(BaseException):
    """Error class for pokemon using moves of a type not the same as their own"""
    '''
    def __init__(self,name,move):
        self.name=name
        self.move=move
    def log():
        print('Pokemon: '+self.name.nick+'of type '+self.name.typ+'attempted to use move :'+self.move+' of type: '+self.move.typ) '''
class OutOfTurn(BaseException):
  pass


"""class for different types of moves to be used by the pokemon class ie: attack,buff etc...   """
class attack():
    """Base class for all instances of attack (ie different attacks)"""
    def __init__(self,name,dmg,descrip,typ='normal',effect=None):
        if typ not in pktps:
            typ='normal'
        self.name=name
        self.descrip=descrip
        self.dmg=dmg
        self.typ=typ
        self.effect=effect
        #a list of all the params for the new attack to be stored in attacks for reference,and to prevent ghost instances
        CompList=[self.name,dmg,self.descrip,typ,effect]
        attacks[self.name]= CompList
        log('Move: '+name+' initialized {'+str(CompList)+'}')
        
    def calc(self,origin,xmod=1):
        status=origin.status
        if self.effect=='pois' and target.status != 'pois':
            status='pois'
        return ((((self.dmg)+(.5*xmod))*-1),status)
        
        
class pokemon():
    """class for all pokemon"""
    def __init__(self,nick,name,typ,lvl=1):
        hp=90+(int(lvl)*10)
        status='norm' #alternatively: 'pois',poisoned,'uncon',unconcious etc...
        xp=0
        lvlup=[0,10,30,50,75,150,300,500,750,1000] #list of xp needed to level up by level
        duel=False
        self.nick=nick
        self.name=name
        self.typ=typ
        self.lvl=lvl
        self.hp=hp
        self.xp=xp
        self.lvlup=lvlup
        self.status=status
        self.duel=duel
        log('pokemon '+nick+' initialized {'+str([name,typ,lvl])+'}')
    def hpmod(self,amt):
        log('pokemon '+self.nick+' called hpmod; amt='+str(amt))
        self.hp=self.hp+amt
        if self.hp<0:
            self.hp=0
        return (self.hp,self.lvl)
    def lvlupchk(self):
        lvledup=False
        if self.lvlup[self.lvl]<= self.xp:
            self.lvl+=1
            lvledup=True
        self.hp=90+(int(lvl)*10)
        log('pokemon '+nick+' called lvlupchk; lvlup='+str(lvledup))
        return lvledup
    def xpmod(self,amt):
        """method for keeping track of and managing the xp of an instance of pokemon and leveling up management"""
        self.xp=self.xp+amt
        self.lvlupchk()
        log('pokemon '+nick+' called xpmod; amt='+str(amt))
        return self.xp
    def start_battle(self,opp):
        log('pokemon '+self.nick+' started battle; opp='+opp.nick)
        duel.init(self,opp) 
    def attack(self,move):
        log('pokemon '+self.nick+' called attack; move='+move.name)
        if self.status != 'uncon':
            if self.typ == move.typ or move.typ == "normal":
              duel.action(self,move)
              
                             
class battle():
    def init(self,att,defn):
        try:
            if att.status != 'uncon' and defn.status != 'uncon':
                self.att=att
                self.defn=defn
                turn=att
                self.turn=turn
                log('battle (re)initialized; att='+att.nick+' defn.='+defn.nick)
            else:
                pass
        except NameError:
            pass

    def chtur(self):
        if self.turn==self.att:
            self.turn=self.defn
        else:
            self.turn=self.defn
        log('turn changed to: '+self.turn.nick)
    def action(self,name,move):
        if name != self.turn:
            raise OutOfTurn  
        if name == self.att:
            targ=self.defn
        else:
            targ=self.att
        base=move.calc(name,name.xp)
        targ.hpmod(base[0])
        log(name.nick+'used '+move.name+' on '+targ.nick+'dealing '+str(base[0])+' damage')
        self.chtur()


if __name__ =='__main__':
    duel=battle()
    lucy=pokemon('lucy','vulpix','fire')
    ted=pokemon('ted','pikachu','electricity')
    gerald=pokemon('gerald','squirtle','water')
    ivan=pokemon('ivan','dodrio','normal')
    jeff=pokemon('jeff','bulbasor','plant')
    fb=attack('fire ball',10,'A ball of fire doing damage to your opponent','fire')
    zap=attack('zap',10,'A lighting bolt of static electricity','electric')
    scratch=attack('scratch',10,'A flurry of blows directed at your opponent','normal')
    intox=attack('intoxicate',2,'A brew of chemicals perfect for a little poison','plant','pois')
    lucy.start_battle(ted)
    lucy.attack(fb)
