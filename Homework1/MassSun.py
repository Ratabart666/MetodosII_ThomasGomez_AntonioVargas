#!/usr/bin/env python3
import polars as pl
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.constants import e, c, h


# https://www.universoformulas.com/fisica/dinamica/leyes-kepler/ From here we conclude that m = (4pi/(GM)) = (4pi/(4piM)) = 1/M => M = 1/m
# MS is solar mass
plt.style.use("ggplot")


def Model(x, m, b):
    return m * x + b


try:
    Data = pl.read_csv("Homework1/OrbitalDataSimulation.txt", skip_rows=2)
except:
    Data = pl.read_csv("OrbitalDataSimulation.txt", skip_rows=2)


x = Data["T^2"]
y = Data["a^3"]
Coeficients, CovMatrix = curve_fit(Model, x, y)

m = Coeficients[0]
b = Coeficients[1]

plt.plot(x, Model(x, m, b), color="red", label="fit")
plt.scatter(x, y, color="blue", label="data")
plt.legend()
M = 1 / m
print("The aproximate mass of sun in (MS) is {M}".format(M=M))
print("The aproximate mass of sun in the SI is {Msi}".format(Msi=M * 2e30))
plt.show()
