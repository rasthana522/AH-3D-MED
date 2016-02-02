#ALICIA NG
#RUCHI ASTHANA

from __future__ import division, print_function
from visual import *
import wx
import copy
import csv

class Population (object):
    
    def __init__(self):
        self.names = []
        self.fats = []
        self.carbs = []
        self.proteins = []
        self.calories = []
        self.nutrition = (self.fats, self.carbs, self.proteins, self.calories)
        self.nutritionMin = 100
        self.nutritionMax = 130
        self.healthy = []
        self.unhealthy = []
        #graph sets of data in different windows

    def getData(self):
        for d in csv.DictReader(open('excel_import2.csv'), delimiter=','):
            self.names.append(str(d['Names']))
            carb = (float(d['Carb(g)']))
            fat = (float(d['Fat(g)']))
            protein = (float(d['Protein(g)']))
            calories = (float(d['Total Calories']))
            self.carbs.append(carb)
            self.fats.append(fat)
            self.proteins.append(protein)
            self.calories.append(calories)
            assert(len(self.names) == len(self.fats) == len(self.carbs)
                   == len(self.proteins) == len(self.calories))
            self.nutrition = (self.fats, self.carbs, self.proteins,self.calories)
            
    def graph(self):
        #get the axes
        dataSet1 = self.nutrition
        carbs = dataSet1[0]
        fats = dataSet1[1]
        proteins = dataSet1[2]
        calories = dataSet1[3]
        #healthy ranges
        minCarbPercent = 0.5
        maxCarbPercent = 0.6
        minFatPercent = 0.25
        maxFatPercent = 0.35
        minProteinPercent = 0.12
        maxProteinPercent = 0.2
        minNutrition = 1.0
        maxNutrition = 1.2
        carbPercent = (minCarbPercent, maxCarbPercent)
        fatPercent = (minFatPercent, maxFatPercent)
        proteinPercent = (minProteinPercent, maxProteinPercent)
        assert(len(carbs) == len(fats) == len(proteins))
        for i in xrange(len(fats)):
            healthiness = 0
            calor = calories[i]
            carb = carbs[i]*4
            fat = fats[i]*9
            protein = proteins[i]*4
            healthiness = Population.findHealthiness(carb, fat, protein,calor,
                        carbPercent, fatPercent, proteinPercent)
            (x,y,z) = (carb/calor*20,fat/calor*10,protein/calor*70)
            if minNutrition <= healthiness <= maxNutrition:
                self.healthy.append(sphere(pos = (carb/calor*20,fat/calor*10,protein/calor*70),frame=f,
                   radius = rad, color = color.green))
            else:
                self.unhealthy.append(sphere(pos = (carb/calor*20,fat/calor*10,protein/calor*70),frame=f,
                   radius = rad, color = color.red))
            curve(pos=[(x,0,z), (x,y,z)], radius = 0.01)
            curve(pos = [(x,0,z),(0,0,z)], radius = 0.01)
            curve(pos = [(x,0,z),(x,0,0)], radius = 0.01)
            curve(pos = [(0,y,z),(x,y,z)], radius = 0.01)
            curve(pos = [(x,y,0),(x,y,z)], radius = 0.01)


    @staticmethod
    def findHealthiness(carb, fat, protein, calor,
                        carbPercent,fatPercent,proteinPercent):
        healthiness = 0
        if carb/calor < carbPercent[0]:
            healthiness += (carb*(1-((carbPercent[0]-(carb/calor))/2)))/calor
        elif carb/calor > carbPercent[1]:
            healthiness += (carb*(1-(((carb/calor)-carbPercent[1])/2)))/calor
        else:
            assert (carbPercent[0] <= carb/calor <= carbPercent[1])
            healthiness += carb/calor
            
        if fat/calor < fatPercent[0]:
            healthiness += (fat*(1-((fatPercent[0]-(fat/calor))/2)))/calor
        elif fat/calor > fatPercent[1]:
            healthiness += (fat*(1-(((fat/calor)-fatPercent[1])/2)))/calor
        else:
            assert (fatPercent[0] <= fat/calor <= fatPercent[1])
            healthiness += fat/calor
            
        if protein/calor < proteinPercent[0]:
            healthiness += (protein*
                            (1-((proteinPercent[0]-(protein/calor))/2)))/calor
        elif protein/calor > proteinPercent[1]:
            healthiness += (protein*
                            (1-(((protein/calor)-proteinPercent[1])/2)))/calor
        else:
            assert (proteinPercent[0] <= protein/calor <= proteinPercent[1])
            healthiness += protein/calor
            
        return healthiness    
            
class User(object):
    
    def __init__(self):
        self.name = None
        self.fat = 0
        self.carb = 0
        self.protein = 0
        self.calories = 0
        self.pos = None
        disp.closestHealthy = None
        disp.closestUnhealthy = None

    def getData(self):
        for d in csv.DictReader(open('patient_import1.csv'), delimiter = ","):
            self.name = str(d[' Name '])
            self.fat = float(d['Fat(g)'])
            self.carb = float(d['Carb(g)'])
            self.protein = float (d['Protein(g)'])
            self.calories = float(d['Total Calories'])

    def graph(self):
        print(self.fat, self.carb,self.protein,self.calories)
        carb = self.carb*4/self.calories
        fat = self.fat*9/self.calories
        protein = self.protein*4/self.calories
        (x,y,z) = (carb*20,fat*10,protein*70)
        self.pos = (x,y,z)
        disp.textPos = ("(%0.1f, %0.1f, %0.1f)"
                        %(self.carb, self.fat, self.protein))
        disp.thingClicked = sphere(pos = (x,y,z),frame = f,
                   radius = rad*2, color = color.orange)
        disp.name = self.name
        disp.userPos = (carb, fat, protein)
        disp.label = label(pos=(x+(rad*8),y+(rad*8),z+(rad*8)),
                           text=disp.name+disp.textPos,
                           opacity=1,box = False,
                           frame = f)
        curve(pos=[(x,0,z), (x,y,z)], radius = 0.01)
        curve(pos = [(x,0,z),(0,0,z)], radius = 0.01)
        curve(pos = [(x,0,z),(x,0,0)], radius = 0.01)
        self.closestHealthy((x,y,z), sample1)
        self.closestUnhealthy((x,y,z), sample1)

    def closestHealthy(self, (x,y,z), population):
        self.findClosestHealthy(population)
        if disp.closestHealthy != None:
            disp.closestHealthy.visible = False
        #unhealthy, healthy
        disp.closestHealthy = curve(pos = [(self.healthy[0],self.healthy[1],self.healthy[2]),(x,y,z)]
              ,radius = 0.05, color = color.cyan)
        
    def closestUnhealthy(self,(x,y,z), population):
        self.findClosestUnhealthy(population)
        if disp.closestUnhealthy != None:
            disp.closestUnhealthy.visible = False
        disp.closestUnhealthy = curve(pos = [(self.unhealthy[0],self.unhealthy[1],self.unhealthy[2]),(x,y,z)]
              ,radius = 0.05, color = color.magenta)

    def findClosestHealthy(self, population):
        userx = self.pos[0]
        usery = self.pos[1]
        userz = self.pos[2]
        minx = None
        miny = None
        minz = None
        minDistance = sqrt(3*(R**2))
        for point in population.healthy:
            healthyx = point.pos[0]
            healthyy = point.pos[1]
            healthyz = point.pos[2]
            distance = sqrt((userx-healthyx)**2+(usery-healthyy)**2+(userz-healthyz)**2)
            if distance < minDistance:
                minDistance = distance
                minx = healthyx
                miny = healthyy
                minz = healthyz
        self.minToHealthy = minDistance
        self.healthy = (minx,miny,minz)

    def findClosestUnhealthy(self,population):
        userx = self.pos[0]
        usery = self.pos[1]
        userz = self.pos[2]
        minx = None
        miny = None
        minz = None
        minDistance = sqrt(3*(R**2))
        for point in population.unhealthy:
            unhealthyx = point.pos[0]
            unhealthyy = point.pos[1]
            unhealthyz = point.pos[2]
            distance = sqrt((userx-unhealthyx)**2+(usery-unhealthyy)**2+(userz-unhealthyz)**2)
            if distance < minDistance:
                minDistance = distance
                minx = unhealthyx
                miny = unhealthyy
                minz = unhealthyz
        self.minToUnhealthy = minDistance
        self.unhealthy = (minx,miny,minz)

###############################################################################

width = 1000
height = 750
menuWidth = 150
helpWidth = 300
R = 20
rad = .2
scale = .12

w = window(width=width, height=height,menus=True, title='AH(3D)MED')
scale = 3
disp = display(window=w, x=menuWidth, y=2, width=width-menuWidth,
               height=height, range = R)
disp.select
f = frame()
f.pos = (0,0,0)
    
sample1 = Population()
sample1.getData()
sample1.graph()

user1 = User()
user1.getData()
user1.graph()

def createFrame():
    pink = (1.,.8,1.)
    xaxis=arrow(pos=(0,0,0),axis=(.9*R,0,0),shaftwidth=.2,color=color.red,
                visible = True, frame = f)
    yaxis=arrow(pos=(0,0,0),axis=(0,.75*R,0),shaftwidth=.2,color=color.blue,
                visible = True, frame = f)
    zaxis=arrow(pos=(0,0,0),axis=(0,0,.9*R),shaftwidth=.2,color=color.green,
                visible = True, frame = f)
    xlabel=label(pos=(.9*R,0,0),text="Carbs",opacity=0,linecolor=color.red,
                 box = False, frame = f)
    ylabel=label(pos=(0,.75*R,0),text="Fat",opacity=0,linecolor=color.blue,
                 box = False, frame = f)
    zlabel=label(pos=(0,0,.9*R),text="Protein",opacity=0,linecolor=color.green,
                 box = False, frame = f)
    xyplane = box(pos = (.9*R/2,.75*R/2,0),height = .75*R,width = .001,
                     opacity=.5,length=.9*R,
                     frame=f,color = pink,material =materials.unshaded)
    xzplane = box(pos = (.9*R/2,0,.9*R/2),height = .001,width = .9*R,
                     opacity=.5,length=.9*R,
                     frame=f,color = pink,material =materials.unshaded)
    yzplane = box(pos = (0,.75*R/2,.9*R/2),height = .75*R,width = .9*R,
                     opacity=.5,length=.001,
                     frame=f,color = pink,material =materials.unshaded)

def createSliders(p,height,dHeight):
    carbText = wx.StaticText(p, pos=(0,height), label='Set carb value')
    height+=dHeight
    carb = wx.Slider(p,pos=(0,height),minValue = 0, maxValue = .9*R,
                    size = (menuWidth,-1),value = disp.thingClicked.pos[0])
    carb.Bind(wx.EVT_SCROLL, setCarb)
    
    height+=2*dHeight
    fatText = wx.StaticText(p, pos=(0,height), label='Set fat value')
    height+=dHeight
    fat = wx.Slider(p,pos=(0,height),minValue = 0, maxValue = .75*R,
                    size = (menuWidth,-1),value = disp.thingClicked.pos[1])
    fat.Bind(wx.EVT_SCROLL, setFat)
    fatText.label = label='Set carb value (%0.1f)'%disp.thingClicked.pos[0]

    height+=2*dHeight
    proteinText = wx.StaticText(p, pos=(0,height), label='Set protein value')
    height+=dHeight
    protein = wx.Slider(p,pos=(0,height),minValue = 0, maxValue = .9*R,
                    size = (menuWidth,-1),value = disp.thingClicked.pos[2])
    protein.Bind(wx.EVT_SCROLL, setProtein)

    return height

def setCarb(evt):
    carb = evt.GetEventObject()
    carbValue = carb.GetValue()
    print(carbValue)
    (x,y,z) = disp.thingClicked.pos
    disp.thingClicked.pos = (carbValue,y,z)
    disp.label.pos = (carbValue+(rad*8),y+(rad*8),z+(rad*8))
    user1.carb = carbValue/20/4*user1.calories
    disp.textPos = ("(%0.1f, %0.1f, %0.1f)"
                        %(user1.carb, user1.fat, user1.protein))
    disp.label.text = disp.name+disp.textPos
    user1.pos = (carbValue,y,z)
    user1.closestHealthy((carbValue,y,z),sample1)
    user1.closestUnhealthy((carbValue,y,z),sample1)

def setFat(evt):
    fat = evt.GetEventObject()
    fatValue = fat.GetValue()
    (x,y,z) = disp.thingClicked.pos
    user1.fat = fatValue/10/9*user1.calories
    disp.textPos = ("(%0.1f, %0.1f, %0.1f)"
                        %(user1.carb, user1.fat, user1.protein))
    disp.label.text = disp.name+disp.textPos
    disp.thingClicked.pos = (x,fatValue,z)
    disp.label.pos = (x+(rad*8),fatValue+(rad*8),z+(rad*8))
    user1.closestHealthy((x,fatValue,z),sample1)
    user1.closestUnhealthy((x,fatValue,z),sample1)

def setProtein(evt):
    protein = evt.GetEventObject()
    proteinValue = protein.GetValue()
    (x,y,z) = disp.thingClicked.pos
    user1.protein = proteinValue/70/4*user1.calories
    disp.textPos = ("(%0.1f, %0.1f, %0.1f)"
                        %(user1.carb, user1.fat, user1.protein))
    disp.label.text = disp.name+disp.textPos
    disp.thingClicked.pos = (x,y,proteinValue)
    disp.label.pos = (x+(rad*8),y+(rad*8),proteinValue+(rad*8))
    user1.closestHealthy((x,y,proteinValue),sample1)
    user1.closestUnhealthy((x,y,proteinValue),sample1)
    
createFrame()
createSliders(w.panel, 50, 10)

##############################################################################

def clickInit(d):
    d.canClick = True

clickInit(disp)

def click(evt):
    if (disp.mouse.pick == disp.thingClicked):
        print(disp.thingClicked)
        print(evt.pos)
        highlightObject()
        disp.canClick = not(disp.canClick)
    
def onMousePress():
    disp.bind('click', click)
    
def highlightObject():
    if disp.canClick == True:
        disp.thingClicked.color = color.yellow
    else: disp.thingClicked.color = color.orange
    

onMousePress()

#show data values for point
#planes?
#BMI, height, weight, age
#calories burned
#sleep 
