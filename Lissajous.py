#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 15:22:56 2020

@author: andrewsmith
"""

import math as mt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import process_time
plt.rcParams['animation.ffmpeg_path'] = '/Users/andrewsmith/Downloads/ffmpeg'


def Lissajous(A,B,C,D):
    
    x = []
    y = []
    dx = 999
    dy = 999
    ynew = -999
    xnew = -999
    t = 0
    dt = (2/30)*(np.pi)
    k = 0.005 #decay rate, bigger number causes faster decay
    i = 0
    while (mt.sqrt(dx**2 + dy**2) > 0.0001 or abs(xnew) > 0.01 or abs(ynew) > 0.01) and i < 1000:
    # for j in range(1000):
        i = i+1
        # print(i)
        xold = xnew
        yold = ynew
        
        xnew = mt.cos(t/A)*(np.exp(-k*t))
        ynew = mt.sin(t/B)*(np.exp(-k*t))
        
        x.append(xnew)
        y.append(ynew)
        
        dx = xold - xnew
        dy = yold - ynew
        
        t = t + dt
        # if i == 1005:
        #     print('number of frames: ',i)
        #     return(x,y)
    print('number of frames: ',i)
    return(x,y)
    

def Harmonograph(A1, A2, A3, A4, B1, B2, B3, B4, C1,C2,C3,C4,D1,D2,D3,D4):
    
    x = []
    y = []
    dx = 999
    dy = 999
    ynew = -999
    xnew = -999
    t = 0
    dt = (2/50)*(np.pi)
    i = 0
    maxLength = 2501
    while (mt.sqrt(dx**2 + dy**2) > 0.0001 or abs(xnew) > 0.01 or abs(ynew) > 0.01) and i < maxLength:
    # for j in range(1000):
        i = i+1
        # print(i)
        xold = xnew
        yold = ynew
        
        xnew = (A1*mt.sin((t/A2) + A3)*(np.exp(-A4*t))) +(B1*mt.sin((t/B2) + B3)*(np.exp(-B4*t)))
        ynew = (C1*mt.sin((t/C2) + C3)*(np.exp(-C4*t))) +(D1*mt.sin((t/D2) + D3)*(np.exp(-D4*t)))
        
        x.append(xnew)
        y.append(ynew)
        
        dx = xold - xnew
        dy = yold - ynew
        
        t = t + dt
        # if i == 1005:
        #     print('number of frames: ',i)
        #     return(x,y)
    print('number of frames: ',i)
    return(x,y)
    

k = 0.004
t1_start = process_time()
# (x,y) = Lissajous(1, 1, 0, 0)


sin1 = (1,1,0,k)
sin2 = (0,1,0,k)
sin3 = (1,4,0,k)
sin4 = (0,1,0,k)

(x,y) = Harmonograph(10,1,0,k, .0,.02,0,k, 10,1.01,np.pi/2,k, .0,.040,np.pi/2,k)


plt.plot(x,y)
plt.axis('square') 
plt.show

if True:
    FFMpegWriter = animation.writers['ffmpeg']
    metadata = dict(title='Movie Test', artist='Matplotlib',
                    comment='Movie support!')
    writer = FFMpegWriter(fps=60, metadata=metadata)
    
    fig = plt.figure()
    plt.axis('square')
    l, = plt.plot([], [], 'k o')
    m, = plt.plot([], [], 'r .')
    
    lim = 10.1
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    
    x0, y0 = 0, 0
    newColorChangerY = 0
    newColorChangerB = 0
    newColorChangerP = 0
    newColorChangerR = 0
    shape = 'd'
    estimatedTime = (-.553 + (.0222*len(x)) + (.0000598*(len(x)**2)))/60
    # print('estimated total time: ', estimatedTime, ' minutes')
    with writer.saving(fig, "Lissajous.mp4", 100):
        for i in range(len(x)):
            if i%200 == 0:
                print(f'\n\ntime remaining: {int(estimatedTime - (process_time()-t1_start)/60):.0f}:{((estimatedTime - (process_time()-t1_start)/60)%1)*60:2.0f}')
                print(f'percent finished: {100*(process_time()-t1_start)/(estimatedTime*60):3.0f}%')
                print('number of frames remaining: ', len(x) - i, 'out of ', len(x))
            if i < len(x)/5:
                m, = plt.plot([], [], shape, color=[1, (5*i)/len(x), 0 ])
            elif i < (2*len(x))/5:
                newColorChangerY = newColorChangerY + 1
                m, = plt.plot([], [], shape, color=[1 - (5*newColorChangerY)/len(x), 1, 0 ])
            elif i < (3*len(x)/5):
                newColorChangerB = newColorChangerB + 1
                m, = plt.plot([], [], shape, color=[0, 1, 5*newColorChangerB/len(x)])
            elif i < (4*len(x)/5):
                newColorChangerP = newColorChangerP + 1
                m, = plt.plot([], [], shape, color=[0, 1 - (5*newColorChangerP)/len(x), 1])
            else:
                newColorChangerR = newColorChangerR + 1
                m, = plt.plot([], [], shape, color=[5*newColorChangerR/len(x), 0, 1])
                
                
            x0 = x[i]
            y0 = y[i]
            xx = x[0:i]
            yy = y[0:i]
            l.set_data(x0, y0)
            m.set_data(x[i], y[i])
            writer.grab_frame()
            
        
    t1_stop = process_time()
    print('time elapsed: ', (t1_stop - t1_start)/60)
        
        