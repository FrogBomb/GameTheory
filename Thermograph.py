import Tkinter
import ConwayGames
from ConwayGames import ConwayGame, StarGame, UpPowerGame
#from math import floor, ceil
FRAYDEPTH = -.5
class thermographer:
    def __init__(self):
        self.curGraph = None
        
    def makeNewGraph(self, games, width=500, height=250, plotType = "exact", name=None):
        self.curGraph = \
            tgraph(plotFunc=self._getPlotFunc(plotType),\
                         games=games, width=width, height=height, name=name,)
        self.curGraph.pack()
        self.curGraph.plot()
        Tkinter.mainloop()
        
    def _getPlotFunc(self, plotType):
        return eval(plotType+"TGPlot")

class tgraph(Tkinter.Canvas):
    def __init__(self, plotFunc = None,\
                 games=None, width=200, height=100, name=None):
        Tkinter.Canvas.__init__(self, width=width, height=height)
        if plotFunc:
            self.plotFunc = plotFunc
        else:
            self.plotFunc = exactTGPlot
        self.games = games
        self.name = name
        self.context = None
        self.width = width
        self.height = height
            
    def plot(self):
        self.plotFunc(self, self.games)

class thermoData():
    def __init__(self, game):
        if ConwayGames.isNumber(game):
            value = ConwayGames.asNumber(game)
            self.rcritPoints=[(0, value, 0, 0)] #(height, value, slopeBelow, slopeAbove)
            ###slope is always value/height!!!
            self.lcritPoints = [(0, value, 0, 0)]
            self.mastBase = (0, value)
        else:
            leftThermoData = [thermoData(l)\
                               for l in ConwayGames.leftOptions(game)]
            rightThermoData = [thermoData(r)\
                               for r in ConwayGames.rightOptions(game)]
            self.lcritPoints = _leanRight(_findRightSide(leftThermoData))
            self.rcritPoints = _leanLeft(_findLeftSide(rightThermoData))
            self.mastBase = _findTop(self.lcritPoints, self.rcritPoints)
            self.lcritPoints = _trunc(self.lcritPoints, self.mastBase[0])
            self.rcritPoints = _trunc(self.rcritPoints, self.mastBase[0])
            
    def getLines(self):
        self.lcritPoints.sort()
        self.rcritPoints.sort()
        ret = []
        prvCp = None
        for cp in self.lcritPoints:
            if prvCp != None:
                ret.append((cp[0], cp[1], prvCp[0], prvCp[1]))
            else:
                ret.append((cp[0], cp[1], FRAYDEPTH, cp[2]*(FRAYDEPTH-cp[0])+cp[1]))
            prvCp = cp
        ret.append(("Top", prvCp[1], prvCp[0], prvCp[1]))
        prvCp = None
        for cp in self.rcritPoints:
            if prvCp != None:
                ret.append((cp[0], cp[1], prvCp[0], prvCp[1]))
            else:
                ret.append((cp[0], cp[1], FRAYDEPTH, cp[2]*(FRAYDEPTH-cp[0])+cp[1]))
            prvCp = cp
            
        ret.append(("Top", prvCp[1], prvCp[0], prvCp[1]))

        return ret

    def getValuesAt(self, height):
        lP = max(l for l in self.lcritPoints if l[0]<=height)
        rP = max(r for r in self.rcritPoints if r[0]<=height)
        return lP[3]*height + (lP[1]-lP[3]*lP[0]), rP[3]*height + (rP[1]-rP[3]*rP[0])

    def getWidthCritPoints(self):
        return

    def getLCompoundRB(self, other):
        return

    def getRCompoundLB(self, other):
        return

def _findRightSide(listOfThermoData):
    augRcritPoints = [(rcp[0], -rcp[1], rcp[2], rcp[3], rcp)\
                   for tD in listOfThermoData for rcp in tD.rcritPoints]
    augRcritPoints.sort()
    outCritPoints = []
    curHeight = -1
    for i in range(len(augRcritPoints)):
        rcp = augRcritPoints[i]
        if rcp[0]>curHeight:
            if len(outCritPoints) ==0:
                outCritPoints.append(rcp[-1])
                curHeight = rcp[0]
            elif rcp[-1][1]>outCritPoints[-1][1]:
                prvCp = outCritPoints[-1]
                cp = rcp[-1]
                tmp = None
                try:
                    tmp = _lineIntersect(prvCp[0], prvCp[1], cp[0], cp[1],\
                                    prvCp[3], cp[2] )
                except ValueError:
                    pass
                if tmp:
                    if tmp[0]>curHeight:
                        outCritPoints.append((tmp[0], tmp[1], prvCp[3], cp[2]))
                        outCritPoints.append(rcp[-1])
                        curHeight = rcp[0]
    return outCritPoints
    
    
    
def _findLeftSide(listOfThermoData):
    augRcritPoints = [(rcp[0], rcp[1], -rcp[2], -rcp[3], rcp)\
                   for tD in listOfThermoData for rcp in tD.lcritPoints]
    augRcritPoints.sort()
    outCritPoints = []
    curHeight = -1
    for i in range(len(augRcritPoints)):
        rcp = augRcritPoints[i]
        if rcp[0]>curHeight:
            if len(outCritPoints) ==0:
                outCritPoints.append(rcp[-1])
                curHeight = rcp[0]
            elif rcp[-1][1]<outCritPoints[-1][1]:
                prvCp = outCritPoints[-1]
                cp = rcp[-1]
                tmp = None
                try:
                    tmp = _lineIntersect(prvCp[0], prvCp[1], cp[0], cp[1],\
                                    prvCp[3], cp[2] )
                except ValueError:
                    pass
                if tmp:
                    if tmp[0]>curHeight:
                        outCritPoints.append((tmp[0], tmp[1], prvCp[3], cp[2]))
                        outCritPoints.append(rcp[-1])
                        curHeight = rcp[0]
    return outCritPoints
    
#def _completeCritPoints(critPoints):
#    critPoints.sort()
#    oldcrtpts = critPoints
#    prvi = critPoints[0]
#    critPoints = critPoints[1:]
#    newCrtPts = []
#    for i in critPoints:
#        if prvi[3]!=i[2]:
#            x, y = _lineIntersect(prvi[0], prvi[1], i[0],i[1], prvi[3], i[2])
#            if (x, y) == (i[0], i[1]):
#                oldcrtpts.remove(i)
#                oldcrtpts.append((i[0], i[1], prvi[2], i[3]))
#            else:
#                newCrtPts.append((x, y, prvi[3], i[2]))
#        prvi = i
#    ret = oldcrtpts+newCrtPts
#    ret.sort()
#    return ret
    
def _leanRight(critPoints):
    return [(cps[0], cps[1]-cps[0], cps[2]-1, cps[3]-1) for cps in critPoints]
        
def _leanLeft(critPoints):
    return [(cps[0], cps[1]+cps[0], cps[2]+1, cps[3]+1) for cps in critPoints]

def _findTop(lcritPoints, rcritPoints):
    lcritPoints.sort()
    rcritPoints.sort()
    if lcritPoints[0][1]<rcritPoints[0][1]:
        print lcritPoints, rcritPoints
        raise TypeError("Something went horribly wrong")
    elif lcritPoints[0][1] == rcritPoints[0][1]:
        return lcritPoints[0][0], lcritPoints[0][1]
    else:
        prvLP = None
        prvRP = None
        top = None
        augCps = [(c,'l') for c in lcritPoints]+\
                            [(c,'r') for c in rcritPoints]
        augCps.sort()
        for i in range(len(augCps)):
            acp = augCps[i]
            if acp[-1] == 'l':
                if prvLP == None:
                    prvLP = acp[0]
                else:
                    if prvRP != None:
                        if acp[0][1]<prvRP[1]:
                            top = _lineIntersect(acp[0][0], acp[0][1], prvRP[0], prvRP[1], acp[0][2], prvRP[3])
                        else:
                            prvLP = acp[0]
                    
            elif acp[-1] == 'r':
                if prvRP == None:
                    prvRP = acp[0]
                else:
                    if prvLP != None:
                        if acp[0][1]>prvLP[1]:
                            top = _lineIntersect(acp[0][0], acp[0][1], prvLP[0], prvLP[1], acp[0][2], prvLP[3])
                        else:
                            prvRP = acp[0]
        if top==None:
            top = _lineIntersect(prvRP[0], prvRP[1], prvLP[0], prvLP[1], prvRP[3], prvLP[3])
        return top

def _lineIntersect(x_1, y_1, x_2, y_2, m_1, m_2):
    if m_2 == m_1:
        print (x_1, y_1, m_1), (x_2, y_2, m_2)
        raise ValueError("lines are parallel")
    invDet = 1/float(m_2-m_1)
    x = invDet*((x_2*m_2-y_2)-(x_1*m_1-y_1))
    y = invDet*(((x_2*m_2-y_2)*m_1)-((x_1*m_1-y_1)*m_2))
    return x, y
            
def _trunc(critPoints, top):
    ret = [cp for cp in critPoints if cp[0]<top]
    if len([cp for cp in critPoints if cp[0]==top])!=0:
        k = [cp for cp in critPoints if cp[0]==top]
        ret.append((k[0][0], k[0][1], k[0][2], 0))
        return ret
    ret.sort()
    topPoint = (top, ret[-1][1]+(top-ret[-1][0])*ret[-1][3], ret[-1][3], 0)
    ret.append(topPoint)
    return ret
    

def exactTGPlot(canvas, games, color = "black"):
    lineList = []
    
    for game in games:
        tD = thermoData(game)
        lines = tD.getLines()
        lineList.extend(lines)

    canvas.config(bg="white")
    scaling, translation = _calcScalingTranslation(canvas, lineList)
    #scaling = 30 #Denotes number of pixels for .5 units
    #translation = 0 #Denotes translation along the stop-value axis
    
    for l in lineList:
        if l[0] == "Top":
            l = (canvas.width, l[1], l[2], l[3])
        l = _scaleTransLine(canvas, l, scaling, translation)
        canvas.create_line(*l, fill=color)
    _makeCoord(canvas, scaling, translation)

def _makeCoord(canvas, scaling, translation):
    height = canvas.height
    width = canvas.width
    for notH in range(0, height-scaling, scaling):
        h = height-scaling-notH
        if notH%(scaling*2) == scaling:
            canvas.create_line(0, h, width, h, fill = "red", dash = (2, 2))
        else:
            canvas.create_line(0, h, width, h, fill = "red")
    canvas.create_line(0, height-scaling, width, height-scaling)
    for i in range(-width/(scaling*4), width/(scaling*2)+1):
        canvas.create_text(scaling*2*(i+translation-int(translation))+width/2, height-scaling,\
                           text = str(-i+int(translation)), anchor = "n", activefill = "slate blue")
    return

def _scaleTransLine(canvas, line, scaling, translation):
    height = canvas.height
    width = canvas.width
    line = (scaling*2*(-line[1]+translation)+width/2, height-(scaling*2*line[0]+scaling),\
            scaling*2*(-line[3]+translation)+width/2, height-(scaling*2*line[2]+scaling))
    return line

def _calcScalingTranslation(canvas, lines):
    height = canvas.height
    width = canvas.width
    ys = [l[0] for l in lines if not "Top"==l[0]]+[l[2] for l in lines if not "Top"==l[2]]
    yMax = max(ys)
    xs = [l[1] for l in lines]+[l[3] for l in lines]
    xMax = max(xs)
    xMin = min(xs)
    xsOn0 = [l[1] for l in lines if l[0]==0]+[l[3] for l in lines if l[2]==0]
    xMaxOn0 = max(xsOn0)
    xMinOn0 = min(xsOn0)
    scaling = min((width/(2*(1+xMax-xMin))), height/(yMax*2+2))
    trans = (xMaxOn0+xMinOn0)/2
    return int(scaling), trans
    

##    canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
##
##    canvas.create_line(50, 0, 100, 100)

##    canvas.create_rectangle(50, 25, 150, 75, fill="blue")

def compoundTGPlot(canvas, games):
    canvas.config(bg="white")
    return

def compoundWithContextTGPlot(canvas, games):
    canvas.config(bg="white")
    return

def extendedTGPlot(canvas, games):
    canvas.config(bg="white")
    return

def thermoDissociation(game):
    return

def criticalPoints(game):
    return

def heat(game, t):
    if t<0:
        raise ValueError("t must be >=0")
    elif t == 0:
        return game
    if ConwayGames.isNumber(game):
        return game
    else:
        gameSum = game.getSum()
        leftOptions = []
        rightOptions = []
        for comp in gameSum:
            leftOptions.append([heat(g, t)+t for g in comp.leftOptions()])
            rightOptions.append([heat(g, t)-t for g in comp.rightOptions()])
    return sum(ConwayGames.ConwayGame(leftOptions[i], rightOptions[i])\
               for i in range(len(gameSum)))

def cool(game, t):
    td = thermoData(game)
    if td.mastBase[0]<t:
        return td.mastBase[1]
    else:
        gameSum = game.getSum()
        leftOptions = []
        rightOptions = []
        for comp in gameSum:
            leftOptions.append([cool(g, t)-t for g in comp.leftOptions()])
            rightOptions.append([cool(g, t)+t for g in comp.rightOptions()])
    return sum(ConwayGames.ConwayGame(leftOptions[i], rightOptions[i])\
               for i in range(len(gameSum)))
        

def mast(game):
    td = thermoData(game)
    return td.mastBase[1]

def temperature(game):
    td = thermoData(game)
    return td.mastBase[0]
