#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 14:27:53 2021

@author: donutman
@licence: GPL
"""
import numpy as np
from matplotlib import pyplot as plt, rc
from matplotlib.widgets import Button

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

def get_analytic_1(a, w, t):
    '''return the analytic (true) parametric equation (x,y) of order-1 fractal
    with parameter alpha = a and omega = w, over the t parameter'''
    c = np.cos(t)
    s = np.sin(t)
    z  = a*np.cos(w*t)
    
    x = c*(1+z)
    y = s*(1+z)
    return (x,y)

def get_analytic_2(a, w, t):
    '''return the analytic (true) parametric equation (x,y) of order-2 fractal
    with parameter alpha = a and omega = w, over the t parameter'''
    c = np.cos(t)
    s = np.sin(t)
        
    x0 = c
    y0 = s
    
    z1   =  a*np.cos(w*t)
    z1p  = -a*w*np.sin(w*t)
    z1pp = -a*w*w*np.cos(w*t)
    
    z2  =  a*a*np.cos(w*w*t)
    z2p = -a*a*w*w*np.sin(w*w*t)
    
    x1 = c*(1+z1)
    y1 = s*(1+z1)
    
    n1 = np.sqrt(z1p*z1p + (1+z1)*(1+z1))

    x2 = (1+z1)*(1+z2/n1)*c + z2/n1*z1p*s
    y2 = -z2/n1*z1p*c + (1+z1)*(1+z2/n1)*s
    
    return (x2, y2)


def get_fractal(order, a, w):
    '''return the parametric equation (x,y) of order-k fractal 
    with parameter alpha = a and omega = w, over the t parameter
    for k =1 and k=2, the solution is exact
    for higher order, it's an approximation'''
    
    t = np.linspace(0, 2*np.pi, 10000*order)
    dt = t[1]-t[0]
    
    if order==1:
        (xp, yp) = (0,0)
        (x, y) = get_analytic_1(a, w, t)
        
    elif order==2:
        (xp, yp) = get_analytic_1(a, w, t)
        (x, y) = get_analytic_2(a, w, t)
    else:
        (x, y) = get_analytic_2(a, w, t)
    
        for k in range(3, order+1):
            z = np.power(a, k-1)*np.cos(np.power(w, k-1)*t)
            dx = np.diff(x, append=x[0])
            dy = np.diff(y, append=y[0])
            
            nx = +dy/(np.sqrt(dx*dx+dy*dy))
            ny = -dx/(np.sqrt(dx*dx+dy*dy))
            
            xp = x
            yp = y
            
            x = x + nx*z
            y = y + ny*z
    return (x, y, xp, yp)


class Index:
    '''This class contains all the graphic callbacks
    (see : https://matplotlib.org/stable/gallery/widgets/buttons.html)'''
    
    def __init__(self, a, w, order):
        self.a = a
        self.w = w
        self.order = order
        
    def _update(self, x, y, xp, yp):
        '''Update of the plot (called each time a button is pressed'''
        lp.set_xdata(xp)
        lp.set_ydata(yp)
    
        l.set_xdata(x)
        l.set_ydata(y)
        
        plt.sca(ax)
        plt.title(r'Order-%d fractal with $\alpha = %2.1f$ and $\omega = %d$' % (self.order, self.a, self.w),
              fontsize=24)
        
        plt.xlim(1.2*np.abs(x).max()*np.array([-1, 1]))
        plt.ylim(1.2*np.abs(x).max()*np.array([-1, 1]))
        plt.draw()

    def next_w(self, event):
        '''Called when we want to increase omega parameter'''
        self.w += 1
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)
        
    def prev_w(self, event):
        '''Called when we want to decrease omega parameter'''
        self.w -= 1
        
        if self.w <1:
            self.w = 1
        
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)
        
    def next_a(self, event):
        '''Called when we want to increase alpha parameter'''
        self.a += 0.05
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)      
        
    def prev_a(self, event):
        '''Called when we want to decrease alpha parameter'''
        self.a -= 0.05
        
        if self.a < 0.05:
            self.a = 0.05
        
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)
        
    def next_o(self, event):
        '''Called when we want to increase the order of the fractal'''
        self.order += 1
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)      
        
    def prev_o(self, event):
        '''Called when we want to decrease the order of the fractal'''
        self.order -= 1
        
        if self.order < 1:
            self.order = 1
        
        (x, y, xp, yp) = get_fractal(self.order, self.a, self.w)
        self._update(x, y, xp, yp)   



# Intialization of the plot

a = 0.3
w = 4
order = 2

(x, y, xp, yp) = get_fractal(order, a, w)

plt.close('all')
fig, ax = plt.subplots(figsize=(15,15))
plt.subplots_adjust(bottom=0.2)

lp, = plt.plot(xp, yp, '-', color=0.7*np.array([1,1,1]), lw=0.5)
l, = plt.plot(x, y, 'r-', lw = 1)

plt.axis('square')
plt.axis('off')

plt.title(r'Order-%d fractal with $\alpha = %2.1f$ and $\omega = %d$' % (order, a, w),
              fontsize=24)

     
# Setting up the callbacks
callback = Index(a, w, order)

# omega +/- buttons
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'w +')
bnext.on_clicked(callback.next_w)
bprev = Button(axprev, 'w -')
bprev.on_clicked(callback.prev_w)

# alpha +/- buttons
axprev2 = plt.axes([0.4, 0.05, 0.1, 0.075])
axnext2 = plt.axes([0.51, 0.05, 0.1, 0.075])
bnext2 = Button(axnext2, 'a +')
bnext2.on_clicked(callback.next_a)
bprev2 = Button(axprev2, 'a -')
bprev2.on_clicked(callback.prev_a)

# order +/- buttons
axprev3 = plt.axes([0.1, 0.05, 0.1, 0.075])
axnext3 = plt.axes([0.21, 0.05, 0.1, 0.075])
bnext3 = Button(axnext3, 'k +')
bnext3.on_clicked(callback.next_o)
bprev3 = Button(axprev3, 'k -')
bprev3.on_clicked(callback.prev_o)


plt.show()

