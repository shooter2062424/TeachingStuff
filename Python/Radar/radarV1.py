import serial
import pygame
import math
import sys
import time
from pygame.locals import *
import threading
import numpy as np



#define some color
green=(0,255,0)
yellow=(255,255,0)
red=(255,0,0)

def parseInfo(s):
    valid = False
    dist = 0.0
    deg = 0.0
    s = s.split(",")
    if len(s) != 2:
        return valid, dist, deg
    else:
        valid = True
        dist = float(s[0])
        deg = int(s[1])
        return valid, dist, deg
    
def decodeData(s):
    s.replace(b"'", b"")
    s.replace(b"b", b"")
    s.replace(b"\r", b"")
    s.replace(b"\n", b"")
    s = s.decode("utf-8")
    return s

##convert functions
def to_window(x,y): # coordinate to window
    x,y=int(x),int(y)
    n_x=x + width//2
    n_y=height//2 - y
    return([n_x,n_y])

def to_radian(angle):
    x=(angle*3.14)/180
    return(x)

#save the data for pygame to read
def add_to_list(angle,distance):
    global point_list
    distance*=8 #50cm will reach the outer circle when multiply by 8(linear)
    deg_angle = angle
    angle=to_radian(angle)
    x,y=math.cos(angle)*distance,math.sin(angle)*distance
    pos=to_window(x,y)
    idx = int(deg_angle)
    #calc current value
    dist_list[idx] = distance/8
    point_list[idx] = pos
    #calc all's average
    c = float(avg_count[idx])
    avg_dist[idx] = (c / (c+1)) * avg_dist[idx] + (1/(c+1)) * distance/8
    a_x = int((c / (c+1)) * avg_point[idx][0] + (1/(c+1)) * pos[0])
    a_y = int((c / (c+1)) * avg_point[idx][1] + (1/(c+1)) * pos[1])
    avg_point[idx] = [a_x, a_y]
    avg_count[idx] += int(1)      
    #calc 5 points average
    nextIdx = int(avg_np_nextIdx[idx])
        #set data
    avg_np_dist[idx][nextIdx] = distance/8
    avg_np_point[idx][nextIdx] = pos
        #calc 5p avg
    valid = []
    for i in range(n_points):
        if avg_np_dist[idx][i] >= -0.001:
            valid.append(i)
    an_dist = 0;
    an_x = 0;
    an_y = 0;
    for i in valid:
        an_dist += avg_np_dist[idx][i]
        an_x += avg_np_point[idx][i][0]
        an_y += avg_np_point[idx][i][1]
    l = float(len(valid))
    avg_np_dist[idx][5] = an_dist/l
    avg_np_point[idx][5][0] = int(an_x/l)
    avg_np_point[idx][5][1] = int(an_y/l)
        #update nextIdx
    avg_np_nextIdx[idx] = (nextIdx + 1) % 5
        
        
#draw function    
def draw_point(list_point,disp):
    for point in list_point:
        pygame.draw.circle(disp,red,point,2)

def draw_circles(disp, offset=(0,0)):
    raduis=50
    for x in range(1,width//2):
        n_raduis=((x//raduis)+1)*raduis
        pygame.draw.circle(disp,green,(width//2+offset[0],height//2+offset[1]),n_raduis,2)
        
def draw_line_byAng(angle,disp,color=yellow):
    a=math.tan(to_radian(angle))
    y=height//2
    if a==0:
        y=0
        if angle==0:
            x=width/2
        elif angle==180:
            x=-width/2
    else:
        x=y//a
    pos=to_window(x,y)
    pygame.draw.line(disp, color,(width/2,height/2),pos,2)
    
def draw_line_byPtList(point,disp,color=green, offset=(0,0)):
    for p in point:
        pygame.draw.line(disp, color,(width//2+offset[0],height//2+offset[1]), (p[0]+offset[0],p[1]+offset[1]),2)
    

def angle_distance(ser):
    #ser.reset_input_buffer()
    read_input=ser.readline()
    read_input=read_input.decode()
    read_input=read_input[:len(read_input)-2]
    read_input=read_input.split(",")
    if len(read_input)!=2 or ("" in read_input):
        return(False)
    return(read_input)

def draw_text(disp,text,t_size, offset=(0,0)):
    fontObj = pygame.font.Font('freesansbold.ttf',t_size)
    textSurface=fontObj.render(text, True,(255,255,255))
    disp.blit(textSurface,(0+offset[0],0+offset[1]))

angle = 0
dist = 0    
def rcvData():
    global angle
    global dist
    ser.open()
    for i in range(5):
        ser.readline()
    while running:
        angle_dist=angle_distance(ser)
        if angle_dist==False:
            continue
        try:
            dist = float(angle_dist[0])
            angle = float(angle_dist[1])
            add_to_list(angle,dist)
        except ValueError:
            dist = 0
            angle = 0

    ser.close()
    print("Serial closed!\n")

mode = int(0)
def toggleMode():
    global mode
    mode = int(mode + 1) % 2


if __name__ == '__main__':

    width,height=800,800
    #measured data from arduino and will be used to draw radar
    dataNum = 181
    point_list=[[width//2, height//2]]*dataNum
    dist_list=[0]*dataNum
    avg_dist = [0]*dataNum
    avg_point = [[width//2, height//2]]*dataNum
    avg_count = [int(0)]*dataNum
    n_points = 5
    avg_np_dist = np.zeros([dataNum, n_points+1]) - 1
    avg_np_point = np.zeros([dataNum, n_points+1, 2], dtype=int)
    for i in range(dataNum):
        for j in range(n_points+1):
            avg_np_point[i][j][0] = width//2
            avg_np_point[i][j][1] = height//2
    avg_np_nextIdx = np.zeros([dataNum])
    running = True    
    
    #init GUI
    pygame.init()
    disp=pygame.display.set_mode((width,height))

    #init serial to communication with Arduino
    ser=serial.Serial()
    ser.timeout=1
    ser.baudrate = 115200
    ser.port='com3' # port name where the arduino 
    serThread = threading.Thread(target = rcvData)
    serThread.start()
    
    while True:
        #clear frame
        disp.fill((0,0,0))
        
        #draw current value
        #draw radar circle
        draw_circles(disp)
    
        #draw scan line
        draw_line_byAng(angle, disp)
        
        #draw data and log the current scan info
        draw_line_byPtList(point_list, disp)
        draw_text(disp,"Live Scaning:",15)
        draw_text(disp,"angle = "+str(angle)+", distance = "+str(dist), 15, offset=(0, 16))
        
        #draw avg value
        #clear lower frame
        pygame.draw.rect(disp, (0,0,0), ((0, height//2), (width, height//2)))
        draw_circles(disp, offset=(0, height//2))
        if mode == 0:
            draw_line_byPtList(avg_point, disp, offset=(0, height//2), color=(255,0,255))
            draw_text(disp,"Scanning Avg:",15, offset=(0, height//2))
        elif mode == 1:
            draw_line_byPtList(avg_np_point[:,-1,:], disp, offset=(0, height//2), color=(0,255,255))
            draw_text(disp,"Scanning " + str(n_points) + "-points avg filter:", 15, offset=(0, height//2))           
        
        
        #check if there has further request from user
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                running = False
                serThread.join()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                #draw avg or draw 5-points avg filter
                toggleMode()
                
        #update display
        pygame.display.update()
        #delay to let CPU rest
        pygame.time.delay(15)