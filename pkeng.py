import logging
import random
logging.basicConfig(level=logging.INFO)
attacks={}
pokemon={}
#all known pokemon types
pktps=['fire','water','electric','plant','normal']
weakness={'fire':'water','water':'electricity','plant':'fire'}
strength={'water':'fire','electricity':'water','fire':'plant'}

#IMPORTANT: upon completion of alpha 1.0 incorporate into pythag
def rand(lower,upper):
    """my wrapper for rand.randint()"""
    return ramdom.randint(lower,upper)

"""error class tree"""
class InvalidMoveParam(BaseException):
    """Error class for faulty arguments passed to the attack class"""
    pass

class InvalidMoveType(BaseException):
    """Error class for pokemon using moves of a type not the same as their own"""
    '''
    def __init__(self,name,move):
        self.name=name
        self.move=move
    def log():
        print('Pokemon: '+self.name.nick+'of type '+self.name.typ+'attempted to use move :'+self.move+' of type: '+self.move.typ) '''


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
        CompList=[self.name,self.descrip]
        attacks[self.name]= CompList
        
    def action(self,target,origin,mod=1,xmod=1):
        print(mod,xmod)
        if target.hp > 0:
            if self.effect=='pois' and target.status != 'pois':
                target.status='pois'
            form=((self.dmg*mod)*xmod)*-1
            logging.info(str(origin)+' attacked '+str(target.nick)+' with '+self.name+'dealing '+str(form))
            return target.hpmod(form)
        
        else:
            print('target eliminated')
        
class pokemon():
    """class for all pokemon"""
    def __init__(self,nick,name,typ,lvl=1):
        hp=90+(int(lvl)*10)
        status='norm' #alternatively: 'pois',poisoned,'uncon',unconcious etc...
        xp=0
        lvlup=[0,10,30,50,75,150,300,500,750,1000] #list of xp needed to level up by level
        self.nick=nick
        self.name=name
        self.typ=typ
        self.lvl=lvl
        self.hp=hp
        self.xp=xp
        self.lvlup=lvlup
        self.status=status
    def hpmod(self,amt):
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
        return lvledup
    def xpmod(self,amt):
        """method for keeping track of and managing the xp of an instance of pokemon and leveling up management"""
        self.xp=self.xp+amt
        self.lvlupchk()
        return self.xp
    def attack(self,target,move):
        if self.status != 'uncon':
            if move.typ == self.typ:
                mod=1
                xmod=1
                try:
                    if weakness[self.typ]==target.typ:
                        mod=.5
                    if strength[self.typ]==target.typ:
                        mod=2
                except KeyError:
                    pass
                if self.xp != 1:
                    for x in range(0,len(str(self.xp))):
                        xmod=self.xp/10
                    xmod+=1
                ret=move.action(target,self.nick,mod,xmod)
                if ret != None:
                    if ret[0] <= 0:
                        self.xpmod(ret[1]*2)
                return ret,self.xp
            else:
                raise InvalidMoveType#(self.nick,move)
        

if __name__ =='__main__':
    lucy=pokemon('lucy','vulpix','fire')
    ted=pokemon('ted','pikachu','electricity')
    gerald=pokemon('gerald','squirtle','water')
    ivan=pokemon('ivan','dodrio','normal')
    jeff=pokemon('jeff','bulbasor','plant')
    fb=attack('fire ball',10,'A ball of fire doing damage to your opponent','fire')
    zap=attack('zap',10,'A lighting bolt of static electricity','electric')
    scratch=attack('scratch',10,'A flurry of blows directed at your opponent','normal')
    intox=attack('intoxicate',2,'A brew of chemicals perfect for a little poison','plant','pois')
