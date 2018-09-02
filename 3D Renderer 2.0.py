import Matrix #Custom function for 3D matrix calculations
import pygame
import math
import sys
import time
from pygame import mouse

#Globalised Variables
global sides
global sidesOutline
global objects
global points
global faces
global colours

colours = [] #List of Colours On Objects
faces = [] #List of All The Faces
points = [] #List of All The Points
objects = [] #A List of All The 3d Objects
sides = [] #A List Of All The Render Codes For The Faces
sidesOutline = [] #A List Of All The Render Codes For The Edges

#Following function are for switching from classical to computer cartesian planes
def X(x):
    global display_width
    return (x + (display_width / 2))
def Y(y):
    global display_height
    return (0 - (y - (display_height / 2)))

#Functions used for rendering points and faces in order of back to front
def lowest(list):
    bottomValue = 0
    for i in range(len(list)):
        if list[i] < list[bottomValue]:
            bottomValue = i
    return bottomValue

def heighest(list):
    topValue = 0
    for i in range(len(list)):
        if list[i] > list[topValue]:
            topValue = i
    return topValue

#Class defining a 3D point
class Point():
    def __init__(self,x,y,z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

#Class defining a 3D object
class Object():
    global sides
    global sidesOutline
    global objects
    global points
    global faces
    global colours
    
    def __init__(self,file,x,y,z):
        global sides
        global sidesOutline
        global objects
        global points
        global faces
        global colours
        
        #Read the original obj file
        object = open('Object Files/'+file+'.obj','r').read()
        #Split at every line end, to get every line
        lines = object.split('\n')
        #Deleting all the empty lines and comments
        for o in range(len(lines)-1,-1,-1):
            if len(lines[o]) < 1:
                lines.pop(o)
            elif lines[o][0] in ['#',' ']:
                lines.pop(o)
        #Variable for vertices
        points2 = []
        for i in lines:
            if i[0:6] == 'mtllib': #Getting the mtl file right at the start
                mtlfile = i[7:]
            if i[0] == 'v': #If the line starts with 'v', meaning a veritce command
                points2.append(i[1:].split('\t\t')) #Making the points a list in the form of [x,y,z]
        #Setting up the positional list
        for i in points2:
            points.append(Point(i[0],i[1],i[2]))
        del points2

        """Setting Up Colours, Through The MTL File"""
        colors = {}
        f = open('Object Files/'+mtlfile,'r') #Open The MTL File
        colorlines = f.read().split('\n')

        #Getting rid of unneeded lines
        for o in range(len(colorlines)-1,-1,-1):
            if len(colorlines[o]) < 1:
                colorlines.pop(o)
            elif colorlines[o][0] in ['#',' ']:
                colorlines.pop(o)
            elif colorlines[o][0:2] in ['Ka','d ','il']:
                colorlines.pop(o)

        #Syntaxing the rgb colour recieved, and formatting it        
        catchColor = False
        for i in colorlines:
            if catchColor:
                catchColor = False
                tempColor = [i[3:].split(' ')]
                tempColor2 = tempColor[:]
                num1 = 0
                for q in tempColor:
                    num2 = 0
                    for o in q:
                        tempColor[num1][num2] = float(o)*255
                        num2 += 1
                    num1 += 1
                tempColor2 = tempColor[0]
                colors[tempName] = (tempColor2[0],tempColor2[1],tempColor2[2])
            if i[0:6] == 'newmtl':
                catchColor = True
                tempName = i[7:]

        #Adding the newly found material to the face property
        faceList = []
        for i in lines:
            if i[0:6] == 'usemtl':
                color = colors[i[7:]]
            if i[0] == 'f':
                faces.append(i[1:].split('\t') + [color])
                faceList.append(faces[-1])
                colours.append(color)
        #making sure every number is an integer type variable        
        num1 = 0
        for i in faces:
            num2 = 0
            for q in i:
                if type(q) is str:
                    faces[num1][num2] = int(q)
                    num2 += 1
            num1 += 1            
        #Creatibg custom commands that wil render the face in the order neccesary    
        num1 = 0
        for i in faces:
            listOfPoints = '['
            for o in i:
                if type(o) != tuple:
                    point = points[o-1]
                    listOfPoints += '[X(points['+str(o - 1)+'].x + objects['+str(len(objects))+'].pos.x),Y(points['+str(o - 1)+'].y) + objects['+str(len(objects))+'].pos.y],'
            listOfPoints += ']'
            sides.append('pygame.draw.polygon(screen,'+str(colours[num1])+','+listOfPoints+',0)')
            sidesOutline.append('pygame.draw.polygon(screen, (255,255,255),'+listOfPoints+',1)')
            num1 += 1
        
        #Getting rid of extra empty points on the face lists
        for face in faceList:
            num1 = 0
            face.pop(3)
            for point in face:
                face[num1] = int(face[num1]) - 1
                num1 += 1
        #Final assignment of variables to the parts of the object        
        self.faces = faceList
        self.pos = Point(x,y,z)
        self.offset = []
        self.angleX = 0
        self.angleY = 0
        
        objects.append(self)

#Creating objects
Object('tinker',-20,0,0)
Object('tinker',20,0,0)
    
#Variables regarding rotation
right = False
left = False
up = False
down = False
zplus = False
zminus = False

#Variables regarding movement
stepForwards = False
stepBackwards = False
stepLeft = False
stepRight = False
fly = False
fall = False

#Other variables
lines = True #Toggle Lines
zoomin = False
zoomout = False
pause = False #Pause renderer
perspective = True #Toggle Perspective

camera = Point(0,0,60) #Create a "position" for the camera

#Variables regarding screen height
display_width = 600
display_height = 600

#Initialise the rendering engine
pygame.init()

#Initialise bg colour
black = (0,0,0)

#Set up the screen
screen = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Renderer')

#Rendering loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_RIGHT:
                right = True
                left = False
            if key == pygame.K_LEFT:
                left = True
                right = False
            if key == pygame.K_UP:
                up = True
                down = False
            if key == pygame.K_DOWN:
                down = True
                up = False
            if key == pygame.K_q:
                zminus = True
                zplus = False
            if key == pygame.K_e:
                zplus = True
                zminus = False
            if key == pygame.K_w:
                stepForwards = True
                stepBackwards = False
            if key == pygame.K_s:
                stepBackwards = True
                stepForwards = False
            if key == pygame.K_a:
                stepLeft = True
                stepRight - False
            if key == pygame.K_d:
                stepRight = True
                stepLeft = False
            if key == pygame.K_EQUALS:
                zoomin = True
                zoomout = False
            if key == pygame.K_MINUS:
                zoomout = True
                zoomin = False
            if key == pygame.K_SPACE:
                fly = True
                fall = False
            if key == pygame.K_LSHIFT:
                fall = True
                fly = False
            if key == pygame.K_l:
                if lines:
                    lines = False
                else:
                    lines = True
            if key == pygame.K_ESCAPE:
                if pause:
                    pause = False
                    mouse.set_visible(False)
                    mouse.set_pos(300,300)
                else:
                    pause = True
                    mouse.set_visible(True)
            if key == pygame.K_p:
                if perspective:
                    perspective = False
                else:
                    perspective = True
        if event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_RIGHT:
                right = False
            if key == pygame.K_LEFT:
                left = False
            if key == pygame.K_UP:
                up = False
            if key == pygame.K_DOWN:
                down = False
            if key == pygame.K_q:
                zminus = False
            if key == pygame.K_e:
                zplus = False
            if key == pygame.K_w:
                stepForwards = False
            if key == pygame.K_s:
                stepBackwards = False
            if key == pygame.K_d:
                stepRight = False
            if key == pygame.K_a:
                stepLeft = False
            if key == pygame.K_SPACE:
                fly = False
            if key == pygame.K_LSHIFT:
                fall = False
            if key == pygame.K_MINUS:
                zoomout = False
            if key == pygame.K_EQUALS:
                zoomin = False
    
    if not pause:
        speed = 5
        changeX = 5
        changeZ = 5
        for object in objects:
            for face in object.faces:
                for pointNum in face:
                    point = points[pointNum]
                    if left:
                        rotX = 5
                    if right:
                        rotX = -5
                    if up:
                        rotY = 5
                    if down:
                        rotY = -5
                        
                    if left or right:
                        rotated = Matrix.rotate('y',rotX,point.x,point.y,point.z)
                        point.x = rotated[0]
                        point.y = rotated[1]
                        point.z = rotated[2]
                    if up or down:
                        rotated = Matrix.rotate('x',rotY,point.x,point.y,point.z)
                        point.x = rotated[0]
                        point.y = rotated[1]
                        point.z = rotated[2]
                    
                        
                    if fly:
                        point.y -= speed
                    if fall:
                        point.y += speed
                    if stepRight:
                        point.x -= changeX
                    if stepLeft:
                        point.x += changeX
                    if stepForwards:
                        point.z -= changeZ
                    if stepBackwards:
                        point.z += changeZ

                    if zoomin:
                        newPoint = Matrix.scale(1.1,1.1,1.1,point.x,point.y,point.z)
                        point.x = newPoint[0]
                        point.y = newPoint[1]
                        point.z = newPoint[2]
                    if zoomout:
                        newPoint = Matrix.scale(0.9,0.9,0.9,point.x,point.y,point.z)
                        point.x = newPoint[0]
                        point.y = newPoint[1]
                        point.z = newPoint[2]
    screen.fill((0, 191, 255))

    averageSide = []
    for object in objects:
        for face in object.faces:
            averageSide.append((points[face[0]].z+points[face[1]].z+points[face[2]].z)/3)

    for face in averageSide:
        sideToRender = lowest(averageSide)
        averageSide[sideToRender] = math.inf
        exec(sides[sideToRender])
        if lines:
            exec(sidesOutline[sideToRender])
    
    
    pygame.display.update()
