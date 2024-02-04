from vpython import *
import numpy as np
import polars as pl


# Pendientes tarea

# No imprimir en consola, gráficas energia cinética, potencial,mecánica,momentos angulares
# Demostrar que la fuerza es conservativa con el gradiente en esfericas
# Gráficar momento angular
# Pendiente velocidades aleatorias y unidades
# Cambiar a la fuerza gravitacional
# Generar botones


class CollidingParticles:
    def __init__(self):
        "Start the simulation scenario"
        ########################################################################################################################
        # Title,caption, dimentions of the box , initial range of the random spheres , numbers of spheres , spheres radius
        # graphics
        Choose = input(
            "Enter the planet that do you want to simulate (Jupyter,Earth,Venus,Mars) : \n"
        )
        while Choose not in {"Jupyter", "Venus", "Mars", "Earth"}:
            print("Invalid input put  (Jupyter,Earth,Venus,Mars) ")
            Choose = input(
                "Enter the planet that do you want to simulate (Jupyter,Earth,Venus,Mars) : \n"
            )
        scene.title = "\n Solar systems, cooming soon n bodys, this is a beta UI app, only works run stop button . \n Developer: Github: Ratabart666 \n \n \n"
        scene.caption = "\n Choose the planet: \n \n \n"
        self.BoxSize = 140
        scene.background = color.white

        # Create the box if the users wants, the default is True

        # Create the spheres, define the dt time, the mass of the spheres, and define the rigidity
        self.CreateDataFrameInfo()
        self.GenerateRunOrStopButton()
        self.GenerateStartOrRebootButton()
        self.GenerateGenerateOrCleanSimulationButton()

        # Run simulation
        self.dt = 0.00001
        self.Run = True
        self.t = 0
        self.G = 4 * (np.pi**2)
        # self.CreateGraphics()
        for Planet in ["Jupyter", "Venus", "Mars", "Earth"]:
            if Planet == Choose:
                setattr(self, "Include" + Planet + "ButtonValue", True)
            else:
                setattr(self, "Include" + Planet + "ButtonValue", False)

        self.GenerateRemoveOrRebootSpheres("Generate the Spheres")
        self.ComputeT = False

        while True:
            self.FramesPerSecond = rate((1 / self.dt))
            if self.Run == True:
                self.GenerateOrCleanSimulationButton.disabled = True
                self.ActualizeEuler()
                self.t += self.dt
            else:
                # Only if the simulation is not running the clean button is active
                self.GenerateOrCleanSimulationButton.disabled = False

            if not (
                hasattr(self, str(0))
            ):  # If there is not spheres then the run button is disabled
                self.RunOrStopSimulationButton.disabled = True

            else:
                self.RunOrStopSimulationButton.disabled = False

    ###########################################################################################################
    # Generate Buttons

    def GenerateRunOrStopButton(self):
        self.RunOrStopSimulationButton = button(
            text="Stop simulation",
            pos=scene.title_anchor,
            bind=self.RunOrStopSimulation,
        )

    def GenerateStartOrRebootButton(self):
        self.RebootButton = button(
            text="Reboot simulation",
            pos=scene.title_anchor,
            bind=self.RebootSimulation,
        )

    def GenerateGenerateOrCleanSimulationButton(self):
        self.GenerateOrCleanSimulationButton = button(
            text="Clean simulation",
            pos=scene.title_anchor,
            bind=self.GenerateOrCleanSimulation,
        )

    def GenerateRunOrStopButton(self):
        self.RunOrStopSimulationButton = button(
            text="Stop simulation",
            pos=scene.title_anchor,
            bind=self.RunOrStopSimulation,
        )

    def GenerateIncludeOrExcludeEarthButton(self):
        self.RunOrStopSimulationButton = button(
            text="Excluded earth",
            pos=scene.title_anchor,
            bind=self.IncludeExcludeEarth,
        )

    def GenerateIncludeOrExcludeVenusButton(self):
        self.RunOrStopSimulationButton = button(
            text="Include Venus",
            pos=scene.title_anchor,
            bind=self.IncludeExcludeVenus,
        )

    def GenerateIncludeOrExcludeMarsButton(self):
        self.RunOrStopSimulationButton = button(
            text="Include Mars",
            pos=scene.title_anchor,
            bind=self.IncludeExcludeMars,
        )

    def GenerateIncludeOrExcludeJupyterButton(self):
        self.RunOrStopSimulationButton = button(
            text="Include Jupyter",
            pos=scene.title_anchor,
            bind=self.IncludeExcludeJupyter,
        )

    ###########################################################################################################
    # Instructions

    def CreateDataFrameInfo(self):
        self.SolarSystem = pl.read_csv(
            "Homework1/SolarSystemInfo.txt", skip_rows=2
        ).to_dicts()

    def GenerateRemoveOrRebootSpheres(self, Instruction):
        "Generates randoms spheres"
        RemoveList = []
        if Instruction == "Generate the Spheres":
            for PlanetDict in self.SolarSystem:
                PlanetName = PlanetDict["Planeta"]

                if PlanetName == "Sun":
                    x, y, z = PlanetDict["a(UA)"], 0, 0
                    e, a, m, D, Texture = (
                        PlanetDict["e"],
                        PlanetDict["a(UA)"],
                        PlanetDict["m(MS)"],
                        PlanetDict["D"],
                        PlanetDict["Texture"],
                    )

                    setattr(
                        self,
                        PlanetName,
                        sphere(
                            pos=vector(x, y, z),
                            radius=D / 2,
                            TupleVel=(0, 0, 0),
                            TuplePos=(x, y, z),
                            TupleInitPos=(x, y, z),
                            TupleInitVel=(0, 0, 0),
                            mass=m,
                            texture=Texture,
                        ),
                    )
                elif getattr(self, "Include" + PlanetName + "ButtonValue") == True:
                    x, y, z = PlanetDict["a(UA)"], 0, 0
                    e, a, m, D, Texture = (
                        PlanetDict["e"],
                        PlanetDict["a(UA)"],
                        PlanetDict["m(MS)"],
                        PlanetDict["D"],
                        PlanetDict["Texture"],
                    )

                    vx, vy, vz = (
                        0,
                        0,
                        np.sqrt(self.G * (1 + e) / (a * (1.0 - e))),
                    )

                    setattr(
                        self,
                        PlanetName,
                        sphere(
                            pos=vector(x, y, z),
                            radius=D / 2,
                            TupleVel=(vx, vy, vz),
                            TuplePos=(x, y, z),
                            TupleInitPos=(x, y, z),
                            TupleInitVel=(vx, vy, vz),
                            mass=m,
                            texture=Texture,
                            make_trail=True,
                        ),
                    )
                else:
                    RemoveList.append(PlanetDict)

            for Delete in RemoveList:
                self.SolarSystem.remove(Delete)

        elif Instruction == "Remove the Spheres":
            pass
        elif Instruction == "Reboot the Spheres":
            pass

    def ClearGraphics(self):
        pass

    def CreateGraphics(self):
        pass

    ###########################################################################################################
    # bind functions buttons

    def RunOrStopSimulation(self, button):
        if button.text == "Stop simulation":
            self.Run = False
            button.text = "Run simulation"
        elif button.text == "Run simulation":
            self.Run = True
            button.text = "Stop simulation"

    def IncludeExcludeEarth(self, button):
        if button.text == "Include Earth":
            self.IncludeEarthButtonValue = False
            button.text = "Exclude Earth"

        elif button.text == "Exclude Earth":
            self.IncludeEarthButtonValue = False
            button.text = "Include Earth"

    def IncludeExcludeVenus(self, button):
        if button.text == "Include Venus":
            self.IncludeVenusButtonValue = False
            button.text = "Exclude Venus"

        elif button.text == "Exclude Venus":
            self.IncludeVenusButtonValue = False
            button.text = "Include Venus"

    def IncludeExcludeJupyter(self, button):
        if button.text == "Include Jupyter":
            self.IncludeJupyterButtonValue = False
            button.text = "Exclude Jupyter"

        elif button.text == "Exclude Jupyter":
            self.IncludeJupyterButtonValue = False
            button.text = "Include Jupyter"

    def IncludeExcludeMars(self, button):
        if button.text == "Include Mars":
            self.IncludeMarsButtonValue = False
            button.text = "Exclude Mars"

        elif button.text == "Exclude Mars":
            self.Run = True
            self.IncludeMarsButtonValue = False
            button.text = "Include Mars"

    def RebootSimulation(self):
        self.Run = False
        self.RunOrStopSimulationButton.text = "Run simulation"
        self.t = 0
        self.ClearGraphics()
        self.GenerateRemoveOrRebootSpheres("Reboot the Spheres")
        self.CreateGraphics()

    def GenerateOrCleanSimulation(self, button):
        if button.text == "Generate simulation":
            self.Run = False
            self.RunOrStopSimulationButton.text = "Run simulation"
            self.t = 0
            self.m = self.MassSliderValue
            self.StopTime = self.StopTimeSliderValue
            self.SpeedSimulation = self.SpeedSimulationSliderValue
            self.k = self.RigiditySliderValue
            self.TotalSpheres = self.TotalSpheresSliderValue
            self.CreateGraphics()
            self.GenerateRemoveOrRebootSpheres("Generate the Spheres")
            button.text = "Clean simulation"

        elif button.text == "Clean simulation":
            self.Run = False
            self.RunOrStopSimulationButton.text = "Run simulation"
            self.ClearGraphics()
            self.GenerateRemoveOrRebootSpheres("Remove the Spheres")
            button.text = "Generate simulation"

    ###########################################################################################################
    # Physics

    def ComputeForceOverSphere(self, PlanetName):
        SpherePos = np.array(getattr(self, PlanetName).TuplePos)
        Force = np.array([0, 0, 0])
        mass1 = getattr(self, PlanetName).mass
        for PlanetDict in self.SolarSystem:
            PlanetName2 = PlanetDict["Planeta"]
            if PlanetName2 != PlanetName:
                NeighborSpherePos = np.array(getattr(self, PlanetName2).TuplePos)
                mass2 = getattr(self, PlanetName2).mass
                d = np.linalg.norm(NeighborSpherePos - SpherePos)
                Force2 = (
                    self.G * (mass2 * mass1) * (NeighborSpherePos - SpherePos) / d**3
                )  # Gravitacional force
                Force = Force + Force2

        return tuple(Force)

    def ActualizeEuler(self):
        ActualizeDict = dict()
        for PlanetDict in self.SolarSystem:
            PlanetName = PlanetDict["Planeta"]
            Sphere = getattr(self, PlanetName)
            mass = Sphere.mass
            x, y, z = Sphere.TuplePos
            vx, vy, vz = Sphere.TupleVel
            Fx, Fy, Fz = self.ComputeForceOverSphere(PlanetName)
            ax, ay, az = Fx / mass, Fy / mass, Fz / mass
            OldPositions = x, y, z
            newx, newy, newz = (
                x + vx * self.dt + (1 / 2) * ax * (self.dt**2),
                y + vy * self.dt + (1 / 2) * ay * (self.dt**2),
                z + vz * self.dt + (1 / 2) * az * (self.dt**2),
            )
            NewPositions = newx, newy, newz
            NewVelocities = vx + ax * self.dt, vy + ay * self.dt, vz + az * self.dt
            ActualizeDict[PlanetName] = OldPositions, NewPositions, NewVelocities
            if self.t > 0:
                rnew = np.sqrt(newx**2 + newy**2 + newz**2)
                ractual = np.sqrt(x**2 + y**2 + z**2)
                oldx, oldy, oldz = getattr(self, PlanetName).TuplePosPast
                rold = np.sqrt(oldx**2 + oldy**2 + oldz**2)
                if ractual < rnew and ractual < rold and self.ComputeT == False:
                    scene.append_to_caption(
                        "EL periodo orbital es {T} años".format(T=self.t)
                    )
                    self.ComputeT = True
                    self.Run = False

        for PlanetDict in self.SolarSystem:
            PlanetName = PlanetDict["Planeta"]
            OldPositions, NewPositions, NewVelocities = ActualizeDict[PlanetName]
            x, y, z = OldPositions
            newx, newy, newz = NewPositions
            newvx, newvy, newvz = NewVelocities
            getattr(self, PlanetName).TuplePos = newx, newy, newz
            getattr(self, PlanetName).TupleVel = newvx, newvy, newvz
            getattr(self, PlanetName).pos = vector(newx, newy, newz)
            getattr(self, PlanetName).TuplePosPast = x, y, z


CollidingParticles()
