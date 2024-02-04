from vpython import *
import numpy as np


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

        scene.title = "\n Particles in colitions and interacting only between them. Version 1.0.0, the program is in developing and is  unstable in some situations and for now the numerical methods (Euler) is some bad for some cases . \n Developer: Github: Ratabart666 \n \n \n"
        scene.caption = "\n Choose the parameteres: \n \n \n"
        self.BoxSize = 140
        self.SpheresInitialRange = (
            20  # maximum range to left or right of the origin of the box
        )
        scene.background = color.white
        self.SphereRadius = 2.5
        self.TotalSpheres = 10

        # Create the box if the users wants, the default is True

        # Create the spheres, define the dt time, the mass of the spheres, and define the rigidity
        self.GenerateRunOrStopButton()
        self.GenerateStartOrRebootButton()
        self.GenerateGenerateOrCleanSimulationButton()
        self.GenerateTotalSpheresSlider()
        self.GenerateMassSlider()
        self.GenerateSpeedSimulationSlider()
        self.GenerateStopTimeSlider()
        self.GenerateRigiditySlider()

        # Run simulation
        self.dt = 0.001
        self.Run = True
        self.t = 0
        self.m = self.MassSliderValue
        self.StopTime = self.StopTimeSliderValue
        self.SpeedSimulation = self.SpeedSimulationSliderValue
        self.k = self.RigiditySliderValue
        self.TotalSpheres = self.TotalSpheresSliderValue
        self.CreateGraphics()
        self.GenerateRemoveOrRebootSpheres("Generate the Spheres")

        while True:
            self.FramesPerSecond = rate(self.SpeedSimulation * (1 / self.dt))
            if self.t <= self.StopTime and self.Run == True:
                self.GenerateOrCleanSimulationButton.disabled = True
                self.ComputeEnergySystem()
                self.ComputeLinearMomentSystem()
                self.ComputeAngularMomentSystem()
                self.t += self.dt
                self.Actualize()
            else:
                # Only if the simulation is not running the clean button is active
                self.GenerateOrCleanSimulationButton.disabled = False

            if not (
                hasattr(self, str(0))
            ):  # If there is not spheres then the run button is disabled
                self.RunOrStopSimulationButton.disabled = True
                self.TotalSpheresSlider.disabled = False
                self.MassSlider.disabled = False
                self.SpeedSimulationSlider.disabled = False
                self.StopTimeSlider.disabled = False
                self.RigiditySlider.disabled = False

            else:
                self.RunOrStopSimulationButton.disabled = False
                self.TotalSpheresSlider.disabled = True
                self.MassSlider.disabled = True
                self.SpeedSimulationSlider.disabled = True
                self.StopTimeSlider.disabled = True
                self.RigiditySlider.disabled = True

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

    def GenerateTotalSpheresSlider(self):
        wtext(text="Total spheres ")
        self.TotalSpheresSlider = slider(
            min=2,
            max=30,
            step=1,
            value=10,
            bind=self.PutTotalSpheresSliderValue,
        )
        self.TotalSpheresText = wtext(text=10)
        self.TotalSpheresSliderValue = 10

    def GenerateMassSlider(self):
        wtext(text="\t \t \t Mass(kg)")
        self.MassSlider = slider(
            min=1,
            max=5,
            step=1,
            value=1,
            bind=self.PutMassSliderValue,
        )
        self.MassText = wtext(text=1)
        self.MassSliderValue = 1

    def GenerateSpeedSimulationSlider(self):
        wtext(text="\t \t \t Speed simulation")
        self.SpeedSimulationSlider = slider(
            min=0.1,
            max=5,
            step=0.1,
            value=1,
            bind=self.PutSpeedSimulationSliderValue,
        )
        self.SpeedSimulationText = wtext(text=1)
        self.SpeedSimulationSliderValue = 1
        scene.append_to_caption(3 * "\n")

    def GenerateStopTimeSlider(self):
        wtext(text="Stop time (s)")
        self.StopTimeSlider = slider(
            min=10,
            max=30,
            step=1,
            value=10,
            bind=self.PutStopTimeSliderValue,
        )
        self.StopTimeText = wtext(text=10)
        self.StopTimeSliderValue = 10

    def GenerateRigiditySlider(self):
        wtext(text="\t \t \t Rigidity (N/m^3)")
        self.RigiditySlider = slider(
            min=1,
            max=10,
            step=1,
            value=5,
            bind=self.PutRigiditySliderValue,
        )
        self.RigidityText = wtext(text=5)
        self.RigiditySliderValue = 5
        scene.append_to_caption(3 * "\n")

    ###########################################################################################################
    # Instructions

    def GenerateOrRemoveBox(self, Instruction):
        if Instruction == "Generate Box":
            self.Floor = box(
                pos=vector(0, -self.BoxSize / 2, 0),
                size=vector(self.BoxSize, 0.01 * self.BoxSize, self.BoxSize),
                color=color.red,
                texture=textures.wood_old,
            )

            self.Ceiling = box(
                pos=vector(0, 1 / 2 * self.BoxSize, 0),
                size=vector(self.BoxSize, 0.01 * self.BoxSize, self.BoxSize),
                color=color.red,
                texture=textures.wood_old,
            )

            self.Left = box(
                pos=vector(-1 / 2 * self.BoxSize, 0, 0),
                size=vector(0.01 * self.BoxSize, self.BoxSize, self.BoxSize),
                color=color.red,
                texture=textures.wood_old,
            )

            self.Rigth = box(
                pos=vector(1 / 2 * self.BoxSize, 0, 0),
                size=vector(0.01 * self.BoxSize, self.BoxSize, self.BoxSize),
                color=color.red,
                texture=textures.wood_old,
            )

            self.Back = box(
                pos=vector(0, 0, -self.BoxSize / 2),
                size=vector(self.BoxSize, self.BoxSize, 0.01 * self.BoxSize),
                color=color.red,
                texture=textures.wood_old,
            )
        if Instruction == "Remove Box":
            self.Floor.delete()

    def GenerateRemoveOrRebootSpheres(self, Instruction):
        "Generates randoms spheres"
        if Instruction == "Generate the Spheres":
            self.SpheresDict = dict()
            Id = 0
            for Id in range(self.TotalSpheres):
                x, y, z = self.GenerateRandomPos()
                vx, vy, vz = self.GenerateRandomVel()
                setattr(
                    self,
                    str(Id),
                    sphere(
                        pos=vector(x, y, z),
                        radius=self.SphereRadius,
                        TupleVel=(vx, vy, vz),
                        TuplePos=(x, y, z),
                        texture=textures.wood,
                        TupleInitPos=(x, y, z),
                        TupleInitVel=(vx, vy, vz),
                    ),
                )

        elif Instruction == "Remove the Spheres":
            for Id in range(self.TotalSpheres):
                getattr(self, str(Id)).visible = False

            for Id in range(self.TotalSpheres):
                delattr(self, str(Id))

        elif Instruction == "Reboot the Spheres":
            for Id in range(self.TotalSpheres):
                Sphere = getattr(self, str(Id))
                x, y, z = Sphere.TupleInitPos
                vx, vy, vz = Sphere.TupleInitVel
                getattr(self, str(Id)).TupleVel = vx, vy, vz
                getattr(self, str(Id)).TuplePos = x, y, z
                getattr(self, str(Id)).pos = vector(x, y, z)

    def ClearGraphics(self):
        self.LinearMomentxPlot.delete()
        self.LinearMomentyPlot.delete()
        self.LinearMomentzPlot.delete()
        self.KinetEnergyPlot.delete()
        self.PotentialEnergyPlot.delete()
        self.MechanicEnergyPlot.delete()
        self.EnergyGraphics.delete()
        self.LinearMomentGraphics.delete()
        self.AngularMomentGraphics.delete()

    def CreateGraphics(self):
        self.LinearMomentGraphics = graph(
            title="Linear Moment (N*s) vs Time (s)",
            xtitle="t (s)",
            ytitle="P (N*s)",
            fast=False,
        )
        self.EnergyGraphics = graph(
            title="Energy (J) vs Time (s)",
            xtitle="t (s)",
            ytitle="E (J)",
            fast=False,
        )
        self.AngularMomentGraphics = graph(
            title="Angular Moment (kg*m^2/s) vs Time (s)",
            xtitle="t (s)",
            ytitle="L (kg*m^2/s)",
            fast=False,
        )

        self.LinearMomentxPlot = gcurve(
            color=color.blue,
            label="px",
            graph=self.LinearMomentGraphics,
        )

        self.LinearMomentyPlot = gcurve(
            color=color.red, label="py", graph=self.LinearMomentGraphics
        )
        self.LinearMomentzPlot = gcurve(
            color=color.green, label="pz", graph=self.LinearMomentGraphics
        )
        self.KinetEnergyPlot = gcurve(
            color=color.red, label="K", graph=self.EnergyGraphics
        )

        self.PotentialEnergyPlot = gcurve(
            color=color.blue, label="U", graph=self.EnergyGraphics
        )

        self.MechanicEnergyPlot = gcurve(
            color=color.green, label="E", graph=self.EnergyGraphics
        )
        self.AngularMomentxPlot = gcurve(
            color=color.red, label="Lx", graph=self.AngularMomentGraphics
        )

        self.AngularMomentyPlot = gcurve(
            color=color.blue, label="Ly", graph=self.AngularMomentGraphics
        )

        self.AngularMomentzPlot = gcurve(
            color=color.green, label="Lz", graph=self.AngularMomentGraphics
        )

    ###########################################################################################################
    # bind functions buttons

    def RunOrStopSimulation(self, button):
        if button.text == "Stop simulation":
            self.Run = False
            button.text = "Run simulation"

        elif button.text == "Run simulation":
            self.Run = True
            button.text = "Stop simulation"

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

    def PutTotalSpheresSliderValue(self, slider):
        self.TotalSpheresSliderValue = int(slider.value)
        self.TotalSpheresText.text = str(self.TotalSpheresSliderValue)

    def PutMassSliderValue(self, slider):
        self.MassSliderValue = int(slider.value)
        self.MassText.text = str(self.MassSliderValue)

    def PutStopTimeSliderValue(self, slider):
        self.StopTimeSliderValue = int(slider.value)
        self.StopTimeText.text = str(self.StopTimeSliderValue)

    def PutSpeedSimulationSliderValue(self, slider):
        self.SpeedSimulationSliderValue = float(slider.value)
        self.SpeedSimulationText.text = str(self.SpeedSimulationSliderValue)

    def PutRigiditySliderValue(self, slider):
        self.RigiditySliderValue = int(slider.value)
        self.RigidityText.text = str(self.RigiditySliderValue)

    ###########################################################################################################
    # Physics
    def GenerateRandomVel(self):
        x, y, z = tuple(np.random.uniform(-1, 1, size=3))
        norm = np.sqrt(x**2 + y**2 + z**2)
        x, y, z = x / norm, y / norm, z / norm  # Vector of direction
        vel = np.random.uniform(-5, 5)
        v_x, v_y, v_z = x * vel, y * vel, z * vel
        return v_x, 0, v_z

    def GenerateRandomPos(self):
        "Generate a random position"
        x, y, z = tuple(
            np.random.uniform(
                -self.SpheresInitialRange, self.SpheresInitialRange, size=3
            )
        )
        # -self.BoxSize / 2 + self.SphereRadius # This is for the box
        return x, 0, z

    def ComputeForceOverSphere(self, IdSphere):
        SpherePos = np.array(getattr(self, str(IdSphere)).TuplePos)
        Force = np.array([0, 0, 0])
        for Id in range(self.TotalSpheres):
            if str(IdSphere) != str(Id):
                NeighborSpherePos = np.array(getattr(self, str(Id)).TuplePos)
                d = np.linalg.norm(NeighborSpherePos - SpherePos)
                # if d > 0:
                #    DirectionForce = 1000 * (SpherePos - NeighborSpherePos) / d
                #    Force2 = 100000000 * (NeighborSpherePos - SpherePos) / d**3
                #    Force = Force + Force2
                # else:
                #    return np.array([0, 0, 0])

                if d < 2 * self.SphereRadius:
                    DirectionForce = (SpherePos - NeighborSpherePos) / d
                    ModuleForce = self.k * (2 * self.SphereRadius - d) ** 3
                    Force = Force + ModuleForce * DirectionForce
        return tuple(Force)

    def ComputePotentialEnergyOverSphere(self, IdSphere):
        SpherePos = np.array(getattr(self, str(IdSphere)).TuplePos)
        PotentialEnergy = 0
        for Id in range(self.TotalSpheres):
            if str(IdSphere) != str(Id):
                NeighborSpherePos = np.array(getattr(self, str(Id)).TuplePos)
                d = np.linalg.norm(NeighborSpherePos - SpherePos)
                # if d > 0:
                #    DirectionForce = 1000 * (SpherePos - NeighborSpherePos) / d
                #    Force2 = 100000000 * (NeighborSpherePos - SpherePos) / d**3
                #    Force = Force + Force2
                # else:
                #    return np.array([0, 0, 0])

                if d < 2 * self.SphereRadius:
                    PotentialEnergy += (
                        self.k * (1 / 4) * (2 * self.SphereRadius - d) ** 4
                    )

        return (
            1 / 2
        ) * PotentialEnergy  # 1/2 because the potential for 2 particles are the same, view clasical mechanics of goldstein for understand

    def ComputeLinearMomentSystem(self):
        LinearMomentx, LinearMomenty, LinearMomentz = 0, 0, 0
        for Id in range(self.TotalSpheres):
            Sphere = getattr(self, str(Id))
            vx, vy, vz = Sphere.TupleVel
            LinearMomentx += self.m * vx
            LinearMomenty += self.m * vy
            LinearMomentz += self.m * vz
        self.LinearMomentxPlot.plot(self.t, LinearMomentx)
        self.LinearMomentyPlot.plot(self.t, LinearMomenty)
        self.LinearMomentzPlot.plot(self.t, LinearMomentz)

    def ComputeAngularMomentSystem(self):
        AngularMomenty, AngularMomentx, AngularMomentz = 0, 0, 0
        for Id in range(self.TotalSpheres):
            Sphere = getattr(self, str(Id))
            vx, vy, vz = Sphere.TupleVel
            x, y, z = Sphere.TuplePos
            LinearMomentx = self.m * vx
            LinearMomenty = self.m * vy
            LinearMomentz = self.m * vz
            AngularMomentz += 0
            AngularMomentx += 0
            AngularMomenty += LinearMomentz * x - LinearMomentx * z
        self.AngularMomentyPlot.plot(self.t, AngularMomenty)
        self.AngularMomentzPlot.plot(self.t, AngularMomentz)
        self.AngularMomentxPlot.plot(self.t, AngularMomentx)

    def ComputeEnergySystem(self):
        KinetEnergy, PotentialEnergy = 0, 0
        for Id in range(self.TotalSpheres):
            Sphere = getattr(self, str(Id))
            vx, vy, vz = Sphere.TupleVel
            PotentialEnergy += self.ComputePotentialEnergyOverSphere(Id)
            KinetEnergy += (1 / 2) * self.m * (vx**2 + vy**2 + vz**2)

        MechanicEnergy = KinetEnergy + PotentialEnergy
        self.KinetEnergyPlot.plot(self.t, KinetEnergy)
        self.PotentialEnergyPlot.plot(self.t, PotentialEnergy)
        self.MechanicEnergyPlot.plot(self.t, MechanicEnergy)

    def Actualize(self):
        ActualizeDict = dict()
        for Id in range(self.TotalSpheres):
            Sphere = getattr(self, str(Id))
            x, y, z = Sphere.TuplePos
            vx, vy, vz = Sphere.TupleVel
            Fx, Fy, Fz = self.ComputeForceOverSphere(Id)
            ax, ay, az = Fx / self.m, Fy / self.m, Fz / self.m
            NewPositions = (
                x + vx * self.dt + (1 / 2) * ax * (self.dt**2),
                y + vy * self.dt + (1 / 2) * ay * (self.dt**2),
                z + vz * self.dt + (1 / 2) * az * (self.dt**2),
            )
            NewVelocities = vx + ax * self.dt, vy + ay * self.dt, vz + az * self.dt
            ActualizeDict[str(Id)] = NewPositions, NewVelocities

        for Id in range(self.TotalSpheres):
            NewPositions, NewVelocities = ActualizeDict[str(Id)]
            newx, newy, newz = NewPositions
            newvx, newvy, newvz = NewVelocities
            getattr(self, str(Id)).TuplePos = newx, newy, newz
            getattr(self, str(Id)).TupleVel = newvx, newvy, newvz
            getattr(self, str(Id)).pos = vector(newx, newy, newz)


CollidingParticles()
