
class ConwayGame(object):
    """This is a Conway Game class.
    Conway games are each structurally two sets: a set of
    right options and a set of left options, where all
    options are Conway Games (that is, a Conway Game looks like
    {L|R} where L are the left options, and R are the right options).

    As an abstract concept, a Conway Game may be concidered a "game" with
    a left player and a right player. The moves the left player can make
    are to the games in the left set, while the right player may make
    moves to the right game. The game ends when a player cannot make a move,
    in which case the other player wins. 
    
    Any number is considered a Conway Game (Which may be defined
    entirely as a (potentially infinite) Conway Game as well.)
    
    There is an ordering to Conway Games, and a notion of equality and "confusion"
    in Conway Games. Recursively, A>=B iff A is greater than or confused
    with all left options of B and all right options of A are greater than or
    confused with B. We say that A is greater than or confused with B when
    there exists a left option of A that is >=B, or there is a right option
    of B which is <=A. We then simply say that A == B iff A>=B and B>=A,
    and we say A is confused with B iff A is greater than or
    confused with B and B is greater than or confused with A.
    A>B when A is greater than or equal to B and A is greater than or confused with B.
    For numbers, it is true that two numbers are never "confused" with each other. 
    
    The sum of two Conway Games may be defined recursively as
    A+B = {Al|Ar}+{Bl|Br} = {A+Bl, Al+B|A+Br, Ar+B}.

    The negation of a Conway Game may also be defined recursively:
    -{L|R} = {-R|-L}

    The orderings are preserved under sums of equal components.
    That is, if A == B, if C>D, C==D, or C is confused with D,
    then A+C>B+D, A+C==B+D, or A+C is confused with B+D, respecitvely.
    It is also true that if A>B and C>D, then A+C>B+D.

    In relation to the "as a game" abstraction, a Conway Game
    G is always a left player win iff G>0,
    G is a right player win iff G<0, G is always a
    win for the player who goes second iff G==0,
    and G is always a first player win iff G is confused with 0.
    """

##    A Conway Game G is a number x if all left options of G are less
##    than with x and all right options of G are
##    greater than x,
##    and x is the "simplest" x such that this is true.
##    (that is, x = k/(2**n) such that n>=0 is minimal. If n = 0, then make k minimal.)
##    By simply replacing x with G in the above statement, G = {L|R} is a number if L<G<R
##
##    cache = {}
##    def __new__(cls, l = tuple(), r = tuple(), sign = 0, addList = tuple(), shift = 0, **kwargs):
##        if cls == StarGame:
##            key = ("star", l)
##        elif cls == UpPowerGame:
##            key = ("up", l)
##        elif cls == ConwayGame:
##            key = tuple([tuple(l), tuple(r), sign, tuple(addList), shift])
##        if key not in cls.cache:
##            cls.cache[key] = [object.__new__(cls), True]##flag as true when first made
##        return cls.cache[key][0]

    def __init__(self, l = tuple(), r = tuple(), sign = 0, addList = tuple(), shift = 0, **kwargs):
#        key = tuple([tuple(l), tuple(r), sign, tuple(addList), shift])
        doinit = True
##        if key in ConwayGame.cache:
##            if ConwayGame.cache[key][1]:##Don't remake if already made
##                ConwayGame.cache[key][1] = False ##Means this has now been initialized
##            else:
##                doinit = False
        if doinit:
            self._addList = [{'l':frozenset(), 'r':frozenset(), 'sign':sign}]
            if l == None:
                l = []
            if r == None:
                r = []
            if len(l) == 0 and len(r) == 0 and len(addList)!=0:
                self._addList = []
            else:
                self._addList[0]["l"]=\
                        frozenset(i for i in l\
                              if isinstance(i, (int, float, long, ConwayGame)))
                self._addList[0]["r"]=\
                        frozenset(i for i in r\
                              if isinstance(i, (int, float, long, ConwayGame)))
            for i in addList:
                self._addList.extend(i._addList)
            self._key = tuple([tuple(l), tuple(r), sign, tuple(addList), shift])
            self._curShift = shift

    def __str__(self):
        ret = ""
        for opts in self._addList:
            if "starOrder" in opts:
                ret += " + *"+str(opts["starOrder"])
            else:
                ret += " - "*opts["sign"]+" + "*(1-opts["sign"]) +"{"+", ".join(str(lO) for lO in opts['l'])+"|"+\
                            ", ".join(str(rO) for rO in opts['r'])+"}"
        if ret[1] == "+":
            ret = ret[3:]
        elif ret[1] == "-":
            ret = ret[1:]
##        ret = " + ".join(["-"*opts["sign"]+"{"+", ".join(str(lO) for lO in opts['l'])+"|"+\
##                            ", ".join(str(rO) for rO in opts['r'])+"}" for opts in self._addList])
        if self._curShift != 0:
            if self._curShift>0:
                ret += " + " + str(self._curShift)
            elif self._curShift<0:
                ret += " - " + str(-self._curShift)
        return ret

    def getSum(self):
        return [ConwayGame(**i) for i in self._addList] + [self._curShift]

##    def _negate(self):
##        for i in self._addList:
##            i["sign"]=1-i["sign"]

##    def copy(self):
##        return sum(self.getSum())

    def confusedWithOrGreaterThan(self, other):
        return any(other<=lO for lO in self.leftOptions())\
            or any(self>=rO for rO in rightOptions(other))
    
    def confusedWithOrLessThan(self, other):
        return any(other>=rO for rO in self.rightOptions())\
            or any(self<=lO for lO in leftOptions(other))
    
    def confusedWith(self, other):
        return self.confusedWithOrGreaterThan(other) and\
               self.confusedWithOrLessThan(other)

    def __ge__(self, other):
        selfROpts = self.rightOptions()
##        if isinstance(other, (int, float, long)):
##            other = numeric2ConwayGame(other)
####            ret = all(rO.confusedWithOrLessThan(other) for rO in selfROpts\
####                      if isinstance(rO, ConwayGame))
####            if ret == False:
####                return ret
####            for rO in selfROpts:
####                if isinstance(rO, (int, float, long)):
####                    if rO<other:
####                        addList = tuple()
####                        return False
####            return ret
##        if isinstance(other, ConwayGame):
        otherLOpts = leftOptions(other)
        return all(self.confusedWithOrGreaterThan(lO) for lO in otherLOpts)\
               and all(confusedWithOrLessThan(other,rO) for rO in selfROpts)

    def __gt__(self, other):
        return self>=other and not self<=other

    def __lt__(self, other):
        return self<=other and not self>=other

    def __le__(self, other):
        otherROpts = rightOptions(other)
        selfLOpts = leftOptions(self)
##        for i in selfLOpts:
##            print other, "|>", i, confusedWithOrGreaterThan(other,i)
##        for j in otherROpts:
##            print self, "<|", j, confusedWithOrLessThan(self,j)
        return all(confusedWithOrGreaterThan(other,lO) for lO in selfLOpts)\
               and all(confusedWithOrLessThan(self,rO) for rO in otherROpts)

    def __eq__(self, other):
        return self<=other and self>=other
    
    def __hash__(self):
        ret = 0
        signaccu = 0
        for opt in self._addList:
            ret ^= ((2**signaccu)*opt['sign'])
            signaccu +=1
        ret^=(2**len(self._addList))*hash(tuple((opt['l'],opt['r']) for opt in self._addList))
        return ret
    
    def __add__(self, other):
        if isinstance(other, ConwayGame):
            return ConwayGame(addList = [self, other])
        elif isinstance(other, (int, float, long)):
            if other == 0:
                return self
            if self.isNumber():
                return ConwayGame(addList = [self, numeric2ConwayGame(other)])
            else:
                return ConwayGame(self._key[0], self._key[1], self._key[2], self._key[3], shift = self._key[4]+other)

    def __radd__(self, other):
        return self+other

    def __sub__(self, other):
        negother = -other
        retGame = self+negother
        return retGame
            
    def __rsub__(self, other):
        negself = -self
        retGame = negself+other
        return retGame
    

    def __neg__(self):
        newAddList = [i.copy() for i in self._addList]
        for i in newAddList:
            i["sign"] = 1-i["sign"]
        return sum(ConwayGame(i['l'], i['r'], i['sign']) for i in newAddList)

    def __xor__(self, other):
        return join(self, other)
    
    def rightOptions(self):
        retList = []
        _addList = self.getSum()
        for i in range(len(_addList)):
            if isinstance(_addList[i], (int, float, long)):
                rO = rightOptions(_addList[i])
                if len(rO)!=0:
                    rO = rO.pop()
                    retList.append(sum(_addList[:i]+_addList[i+1:]\
                                       +[rO]))
            else:
                sign = _addList[i]._addList[0]["sign"]
                for rO in self._addList[i]["r"*(1-sign)+"l"*sign]:
                    retList.append(sum(_addList[:i]+_addList[i+1:]\
                                       +[rO]*(1-sign)\
                                       +[-rO]*(sign)))
        return set(retList)
                
    def leftOptions(self):
        retList = []
        _addList = self.getSum()
        for i in range(len(_addList)):
            if isinstance(_addList[i], (int, float, long)):
                lO = leftOptions(_addList[i])
                if len(lO)!=0:
                    lO = lO.pop()    
                    retList.append(sum(_addList[:i]+_addList[i+1:]\
                                       +[lO]))
            else:
                sign = _addList[i]._addList[0]["sign"]
                for lO in self._addList[i]["l"*(1-sign)+"r"*sign]:
                    retList.append(sum(_addList[:i]+_addList[i+1:]\
                                       +[lO]*(1-sign)\
                                       +[-lO]*(sign)))
        return set(retList)

    def leftStop(self):
        if self.isNumber():
            return self
        lO = self.leftOptions()
        firstLO = lO.pop()
        if isinstance(firstLO, (int, float, long)):
            ret = firstLO
        else:
            ret = firstLO.rightStop()
        for option in lO:
            if isinstance(option, (int, float, long)):
                if option>ret:
                    ret = option
            elif isinstance(option, ConwayGame):
                opRS = option.rightStop()
                if opRS>ret:
                    ret= opRS
        return ret

    def rightStop(self):
        if self.isNumber():
            return self
        rO = self.rightOptions()
        firstRO = rO.pop()
        if isinstance(firstRO, (int, float, long)):
            ret = firstRO
        else:
            ret = firstRO.leftStop()
        for option in rO:
            if isinstance(option, (int, float, long)):
                if option<ret:
                    ret = option
            elif isinstance(option, ConwayGame):
                opRS = option.leftStop()
                if opRS<ret:
                    ret= opRS
        return ret

    def isNumber(self):
        lO = self.leftOptions()
        rO = self.rightOptions()
        if len(self.leftOptions()) == 0 and len(self.rightOptions()) == 0:
            return True
        if all(isNumber(opt) for opt in lO) and all(isNumber(opt) for opt in rO):
            try:
                if max(lO)<min(rO):
                    return True
            except ValueError:
                return True
        lS = max(rightStop(opt) for opt in lO)
        rS = min(leftStop(opt) for opt in rO)
        if lS == rS:
            if self == lS:
                return True
        elif lS<rS:
            return True
        return False

    def asNumber(self):
        lO = self.leftOptions()
        rO = self.rightOptions()
        if len(lO) == 0 and len(rO) == 0:
            return 0
        if all(isNumber(opt) for opt in lO) and all(isNumber(opt) for opt in rO):
            try:
                maxlO = max(lO)
                maxlO = asNumber(maxlO)
            except ValueError:
                minrO = min(rO)
                ret = 0
                while ret>=minrO:
                    ret-=1
                return ret
            try:
                minrO = min(rO)
                minrO = asNumber(minrO)
            except ValueError:
                ret = 0
                while ret<=maxlO:
                    ret+=1
                return ret
            return simplestNumber(maxlO, minrO)
        lS = max(rightStop(opt) for opt in lO)
        rS = min(leftStop(opt) for opt in rO)
        if lS == rS:
            if self == lS:
                if isinstance(lS, ConwayGame):
                    return lS.asNumber()  
                return lS
        elif lS<rS:
            if self == rS:
                return asNumber(rS)
            elif self == lS:
                return asNumber(lS)
            elif self == simplestNumber(lS, rS):
                return simplestNumber(lS, rS)
            
        raise ValueError("The game is not a number!")

    def canonical(self):
        if self.isNumber():
            return self.asNumber()
        leftCan = set([canonical(i) for i in self.leftOptions()])
        rightCan = set([canonical(i) for i in self.rightOptions()])
        #eliminating dominated options
        if len(leftCan)!= 0:
            maxLOpt = max(leftCan)
            leftCan = leftCan - set([i for i in leftCan if i<=maxLOpt])
            leftCan.add(maxLOpt)
        if len(rightCan)!= 0:
            minROpt = min(rightCan)
            rightCan = rightCan - set([i for i in rightCan if i>=minROpt])
            rightCan.add(minROpt)

        #eliminating reversable options, then dominated options as they appear
        existsRevOptsL = True
        while(existsRevOptsL):
            toRev = None
            rightRevOpt = None
            existsRevOptsL = False
            for lOpt in leftCan:
                for r in rightOptions(lOpt):
                    if self>=r:
                        toRev = lOpt
                        rightRevOpt = r
                        existsRevOptsL = True
                        break
            if existsRevOptsL:
                leftCan.remove(toRev)
                leftCan.update(set([canonical(i) for i in leftOptions(rightRevOpt)]))
                if len(leftCan)!= 0:
                    maxLOpt = max(leftCan)
                    leftCan = leftCan - set([i for i in leftCan if i<=maxLOpt])
                    leftCan.add(maxLOpt)
        existsRevOptsR = True
        while(existsRevOptsR):
            existsRevOptsR = False
            toRev = None
            leftRevOpt = None
            for rOpt in rightCan:
                for l in leftOptions(rOpt):
                    if self<=l:
                        toRev = rOpt
                        leftRevOpt = l
                        existsRevOptsR = True
                        break
            if existsRevOptsR:
                rightCan.remove(toRev)
                rightCan.update(set([canonical(i) for i in rightOptions(leftRevOpt)]))
                if len(rightCan)!= 0:
                    minROpt = min(rightCan)
                    rightCan = rightCan - set([i for i in rightCan if i>=minROpt])
                    rightCan.add(minROpt)
        return ConwayGame(leftCan, rightCan)
        
                    
            

class StarGame(ConwayGame):
    """A Star Game is a special kind of Conway Game that acts like a single pile in Nim.
        Star games may be written as *n, although this will only appear in print statements
        in this library.

        Formally, any move in a star game is to any other star game of a lesser order. That is,
        moves in *3 are to *2, *1 (which also called "star") and *0 (which is the same as 0)
        for both left and right players. 

        Any impartial game is equivilent to some Star Game. (via the Sprague-Grundy Theorem)

        Addition of star games leads to a game which is equal to the star game
        of order equal to the xor of the orders of the summands. (That is,
        *9+*12 = *(9^12) = *6)"""
    
    def __init__(self, n):
##        if StarGame.cache[("star", n)][1]:
##            StarGame.cache[("star", n)][1] = False
        Options = [StarGame(i) for i in range(n)]
        ConwayGame.__init__(self, Options, Options)
        self.starOrder = n
        self._addList[0]["starOrder"] = n

    def __str__(self):
        return "*"+str(self.starOrder)

    def canonical(self):
        if self.starOrder == 0:
            return ConwayGame()
        return self

    def __add__(self, other):
        if isinstance(other, StarGame):
            return StarGame(self.starOrder^other.starOrder)
        else:
            return ConwayGame.__add__(self, other)
    def getSum(self):
        return [self]


class UpPowerGame(ConwayGame):
    def __init__(self, power):
##        if UpPowerGame.cache[("up", power)][1]:
##            UpPowerGame.cache[("up", power)][1] = False
        left = [0]
        if power != 0:
            right = [StarGame(1)-sum([UpPowerGame(i) for i in range(1, power)])]
        else:
            right = [0]
        ConwayGame.__init__(self, left, right)
    def isNumber(self):
        return False
    def asNumber(self):
        raise ValueError("UpPowerGames are never numbers!")
    def rightStop(self):
        return 0
    def leftStop(self):
        return 0
    def getSum(self):
        return [self]
        
##def distance(game):
##    """Returns the left and right distances of the game."""
##    if isinstance(game, float):
##        ratio_game = game.as_integer_ratio()
##        if ratio_game[1] == 1:
##            if ratio_game[0]>0:
##                return 1, 0
##            elif ratio_game[0]<0:
##                return 0, 1
##            else:
##                return 0, 0
##        gameL = (ratio_game[0]-1)/float(ratio_game[1])
##        gameR = (ratio_game[0]+1)/float(ratio_game[1])
##        return distance(gameL)[1], distance(gameR)[0]
##    if isinstance(game, (int, long)):
##        if game>0:
##            return 1, 0
##        elif game<0:
##            return 0, 1
##        else:
##            return 0, 0
##        
##    if isinstance(game, ConwayGame):
##        return ####TO DO####
def simplestNumber(lowerBound, upperBound):
    if lowerBound<upperBound:
        ret = 0
        curDen = 1
        if lowerBound>=ret:
            while(lowerBound>=ret):
                ret+=1
        elif upperBound<=ret:
            while(upperBound<=ret):
                ret-=1
        while(lowerBound>=ret or upperBound<=ret):
            curDen  = curDen*2.0
            if lowerBound>=ret:
                ret+=1/curDen
            elif upperBound<=ret:
                ret-=1/curDen
        return ret
    else:
        raise ValueError("lower bound must be less than upper bound")

def asNumber(game):
    if isinstance(game, (int, float, long)):
        return game
    elif isinstance(game, ConwayGame):
        return game.asNumber()
    raise TypeError

def isNumber(game):
    if isinstance(game, (int, float, long)):
        return True
    elif isinstance(game, ConwayGame):
        return game.isNumber()
    else:
        return False

def leftStop(game):
    if isinstance(game, (int, float, long)):
        return game
    elif isinstance(game, ConwayGame):
        return game.leftStop()
    else:
        raise TypeError
        
def rightStop(game):
    if isinstance(game, (int, float, long)):
        return game
    elif isinstance(game, ConwayGame):
        return game.rightStop()
    else:
        raise TypeError
        
def rightOptions(game):
    if isinstance(game, ConwayGame):
        return game.rightOptions()
    elif isinstance(game, (int, long)):
        if game<0:
            return set([game+1])
        else:
            return set()
    elif isinstance(game, float):
        ratio_game = game.as_integer_ratio()
        if ratio_game[1] == 1:
            if ratio_game[0]<0:
                return set([game+1])
            else:
                return set()
        gameR = (ratio_game[0]+1)/float(ratio_game[1])
        return set([gameR])

def leftOptions(game):
    if isinstance(game, ConwayGame):
        return game.leftOptions()
    elif isinstance(game, (int, long)):
        if game>0:
            return set([game-1])
        else:
            return set()
    elif isinstance(game, float):
        ratio_game = game.as_integer_ratio()
        if ratio_game[1] == 1:
            if ratio_game[0]>0:
                return set([game-1])
            else:
                return set()
        gameR = (ratio_game[0]-1)/float(ratio_game[1])
        return set([gameR])
    
    
def confusedWithOrGreaterThan(a, b):
    if isinstance(a, (int, float, long)):
        if isinstance(b, (int, float, long)):
            return a>b
        elif isinstance(b, ConwayGame):
            return confusedWithOrLessThan(b, a)
    elif isinstance(a, ConwayGame):
        return a.confusedWithOrGreaterThan(b)

def confusedWithOrLessThan(a, b):
    if isinstance(a, (int, float, long)):
        if isinstance(b, (int, float, long)):
            return a<b
        elif isinstance(b, ConwayGame):
            return confusedWithOrGreaterThan(b, a)
    elif isinstance(a, ConwayGame):
        return a.confusedWithOrLessThan(b)

def numeric2ConwayGame(numeric):
    """Converts a float, int, or long into a pure Conway Game."""
    if numeric == 0:
        return ConwayGame()
    if isinstance(numeric, (int, long, float)):
        return ConwayGame(l = [numeric2ConwayGame(i) for i in leftOptions(numeric)],\
                           r =[numeric2ConwayGame(i) for i in rightOptions(numeric)])
def birthday(game):
    """Returns the birthday (depth) of the game."""
    leftOpts = leftOptions(game)
    rightOpts = rightOptions(game)
    if len(leftOpts) == 0 and len(rightOpts)==0:
        return 0
    return 1+max(max(birthday(lO) for lO in leftOpts),\
                max(birthday(rO) for rO in rightOpts))         
    
def join(a, b):
    """Joins games a and b."""
    return ConwayGame([join(aL, bL) for aL in leftOptions(a) for bL in leftOptions(b)],\
                        [join(aR, bR) for aR in rightOptions(a) for bR in rightOptions(b)])

def slowJoin(a, b):
    """Slow joins games a and b"""
    lOa = leftOptions(a)
    rOa = rightOptions(a)
    lOb = leftOptions(b)
    rOb = rightOptions(b)
    if len(lOb) == 0:
        left = [slowJoin(aL, b) for aL in lOa]
    elif len(lOa) == 0:
        left = [slowJoin(a, bL) for bL in lOb]
    else:
        left = [slowJoin(aL, bL) for aL in lOa for bL in lOb]
    if len(rOb) == 0:
        right = [slowJoin(aR, b) for aR in rOa]
    elif len(rOa) == 0:
        right = [slowJoin(a, aR) for aR in rOa]
    else:
        right = [slowJoin(aR, bR) for aR in rOa for bR in rOb]
    return ConwayGame(left, right)

def canonical(game):
    if isinstance(game, (int, float, long)):
        return game
    elif isinstance(game, ConwayGame):
        return game.canonical()
    raise ValueError

    
