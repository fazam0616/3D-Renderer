import math

def cos(angle):
    return round(math.cos(math.radians(angle)),2)

def sin(angle):
    return round(math.sin(math.radians(angle)),2)

def matrixCreator(line1,line2,line3,line4):
    matrix = [line1,line2,line3,line4]
    return matrix

def matrixVertex(matrix,vertex):
    for i in range(len(matrix)):
        for o in range(len(matrix[i])):
            matrix[i][o] *= vertex[o]
    return matrix

def simplifyMatrix(matrix):    
    lines = [0,0,0,0]    
    for o in range(len(matrix)-1):
        for i in range(len(matrix[o])):
            try:
                lines[o] += matrix[o][i]
            except:
                print(matrix[o][i])
    matrix = matrixCreator(round(lines[0],2),round(lines[1],2),round(lines[2],2),round(lines[3],2))
    return matrix

def scale(scalex,scaley,scalez,posx,posy,posz):
    scale = matrixCreator(
[scalex,0,0,0],
[0,scaley,0,0],
[0,0,scalez,0],
[0,0,0,1]
        )
    scale = simplifyMatrix(matrixVertex(scale,[
round(posx,2),
round(posy,2),
round(posz,2),
1
]))
    return scale

def perspective(x,y,z,ex,ey,ez):
    matrix = matrixCreator(
    [1,0,-(ex/ez),0],
    [0,1,-(ey/ez),0],
    [0,0,1,0],
    [0,0,-(1/ez),1]
        )

    points = simplifyMatrix(matrixVertex(matrix,[x,y,z,1]))
    return points

def translate(x,y,z,posx,posy,posz):
    move = matrixCreator(
[1,0,0,x],
[0,1,0,y],
[0,0,1,z],
[0,0,0,1]
        )
    vertex = [
posx,
posy,
posz,
1
        ]
    move = matrixVertex(move,vertex)
    move = simplifyMatrix(move)
    return move

def rotate(mode,angle,posx,posy,posz):
    if mode == 'x':
        rotate = matrixCreator(
[1,0,0,0],
[0,cos(angle),-sin(angle),0],
[0,sin(angle),cos(angle),0],
[0,0,0,1]
            )

    if mode == 'y':
        rotate = matrixCreator(
[cos(angle),0,sin(angle),0],
[0,1,0,0],
[-sin(angle),0,cos(angle),0],
[0,0,0,1]
            )

    if mode == 'z':
        rotate = matrixCreator(
[cos(angle),-sin(angle),0,0],
[sin(angle),cos(angle),0,0],
[0,0,1,0],
[0,0,0,1]
            )

    rotated = matrixVertex(rotate,[
round(posx,2),
round(posy,2),
round(posz,2),
1
])
    rotated = simplifyMatrix(rotated)
    return rotated
