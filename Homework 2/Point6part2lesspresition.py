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
    Data = pl.read_csv("Homework1/SimulationDatalesspresition.txt")
except:
    Data = pl.read_csv("SimulationDatalesspresition.txt")


x = Data["2*Time(years)"]
y = Data["2*DeltaAngle(grades)"]
Coeficients, CovMatrix = curve_fit(Model, x, y)

m = Coeficients[0]
b = Coeficients[1]

phi = m * (3600 / 0.01)  # degrees* (3600sarco/1 degree * (1/(0.01centuries/1year)))

plt.plot(x, Model(x, m, b), color="red", label="fit")
plt.scatter(x, y, color="blue", label="data")
plt.legend()

print("The angular velocity of perihelio is {phi} ".format(phi=phi))

plt.show()
