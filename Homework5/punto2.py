#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib as mpl
import matplotlib.animation as animation
from tqdm import tqdm

Nx = 6
Ny = 6
Nt = 11
x = np.linspace(0, 1, Nx)
y = np.linspace(0, 1, Ny)
t = np.linspace(0, 1, Nt)

dx, dy, dt = x[1]-x[0], y[1]-y[0], t[1]-t[0]


def InitialConditions(x, y, t):
    if t == 0:
        return np.sin(np.pi*(x+y))

    if x == 0:
        return np.e**((-2*np.pi**2)*t)*np.sin(np.pi*y)

    if y == 0:
        return np.e**((-2*np.pi**2)*t)*np.sin(np.pi*x)

    if x == 1:
        return np.e**((-2*np.pi**2)*t)*np.sin(np.pi*(1+y))

    if y == 1:
        return np.e**((-2*np.pi**2)*t)*np.sin(np.pi*(1+x))


def InitT():

    T = np.zeros((Nx, Ny, Nt))

    return T


InitT()
