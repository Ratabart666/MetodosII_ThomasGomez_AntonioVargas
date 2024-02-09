from vpython import *
import numpy as np


class ProjectilSimulation:
    #################################################################################################################################################
    # Init scene
    def __init__(self):
        ##################################################################################
        # Title,caption and color
        scene.title = "\n  Projectil simulation.\n \n \n"  # Title above the simulation
        scene.caption = (
            "\n  Choose the parameters : \n \n \n"  # Caption below the simulation
        )

        ##################################################################################
        # Initial Parameters and objects
        self.Range = 40  # Inmutable parameter
        self.radius = 2.5  # Inmutable parameter
        self.MinGravity = 5  # Inmutable parameter
        self.MaxGravity = 20  # Inmutable parameter
        self.MaxSpeed = 20  # Inmutable parameter

        self.Gravity = 9.8  # Mutable parameter
        self.InitialAngle = 0  # Mutable parameter
        self.InitialSpeed = 2  # Mutable parameter
        self.y_0 = 10  # Inmutable parameter
        self.x_0 = -15  # Inmutable parameter
        self.Projectil = sphere(
            pos=vector(self.x_0, self.y_0, 0),
            radius=self.radius,
            make_trail=True,
            trail_type="points",
            texture=textures.wood_old,
            trail_color=color.gray(0.6),
        )  # Inmutable object
        self.Floor = box(
            pos=vector(0, -0.5, 0),
            size=vector(40, 1, 40),
            color=color.red,
            texture=textures.wood_old,
        )  # Inmutable object
        self.Right = box(
            pos=vector(20, 20, 0),
            size=vector(1, 40, 40),
            color=color.red,
            texture=textures.wood_old,
        )
        ##################################################################################
        # Run/Stop button
        self.Running = False
        self.RunningButton = button(text="Run", pos=scene.title_anchor, bind=self.Run)

        ##################################################################################
        # Re-start button
        self.RestartButton = button(
            text="Clean", pos=scene.title_anchor, bind=self.Restart
        )

        ##################################################################################
        # Gravity button
        scene.append_to_caption("  Gravity : ")
        self.GravitySlider = slider(
            min=self.MinGravity,
            max=self.MaxGravity,
            step=0.1,
            value=self.Gravity,
            bind=self.ShowGravity,
            length=250,
        )
        self.GravityText = wtext(text=self.GravitySlider.value)
        scene.append_to_caption(" m/s^2")
        scene.append_to_caption(3 * "\n")

        ##################################################################################
        # Initial angle button
        scene.append_to_caption("  Initial Angle : ")
        self.InitialAngleSlider = slider(
            min=0,
            max=90,
            step=1,
            value=self.InitialAngle,
            bind=self.ShowInitialAngle,
            length=250,
        )
        self.InitialAngleText = wtext(text=self.InitialAngleSlider.value)
        scene.append_to_caption("°")
        scene.append_to_caption(3 * "\n")

        ##################################################################################
        # Initial speed button
        scene.append_to_caption("  Initial Speed : ")
        self.InitialSpeedSlider = slider(
            min=self.MaxSpeed / 2,
            max=self.MaxSpeed,
            step=0.1,
            value=self.InitialSpeed,
            bind=self.ShowInitialSpeed,
            length=250,
        )
        self.InitialSpeedText = wtext(text=self.InitialSpeedSlider.value)
        scene.append_to_caption(" m/s")

        scene.append_to_caption(3 * "\n")

        ##################################################################################
        # Put of the information (parameters)

        self.PutParametersInformation()

        ##################################################################################
        # Initial interactive objects (This initial interactive objects depends of the parameters information)
        # We define 2 points for build a tangent line, that represents the aproximate initial trajectory of the particle
        Point1 = vector(self.x_0, self.y_0, 0)  # Starting position of the tangent line
        self.time = 0.1
        self.x_position()
        self.y_position()
        Point2 = vector(self.x, self.y, 0)  # Final position of the tangent line
        self.TangentLine = curve(pos=[Point1, Point2])  # Tangent line
        self.time = 0  # We don't associate the value of time = 0.1 to the projectile, the the projectil is still in x_0.y_0,0
        # We restart the time because we have already defined the tangent line and for start the animation
        self.x = self.x_0
        self.y = self.y_0
        self.TangentLine = curve(pos=[Point1, Point2])

        ##################################################################################

        # Start the program
        self.time = 0
        while True:
            self.FramesPerSecond = rate(60)
            if (
                self.Running == True
            ):  # When the time is less or equal than the total time and the animation is running
                self.time += 1 / 60
                self.x_position()  # compute the x position according to the time (self.time)
                self.y_position()  # compute the y position according to the time (self.time)
                self.Projectil.pos = vector(
                    self.x, self.y, 0
                )  # We put the position in the projectile

    ##########################################################################################################################################################
    # Buttons functions

    def Run(self, button):
        self.Running = (
            not self.Running
        )  # When you press the button the animation put change the self.Running to not self.Running
        if self.Running:
            button.text = "Pause"
        else:
            button.text = "Run"

    def Restart(self):  # Restarts the projectil to the default initial position
        self.Projectil.pos = vector(self.x_0, self.y_0, 0)
        self.Projectil.clear_trail()  # Clean the trajectory
        self.time = 0  # Restart the time
        if self.Running == True:  # If the animation is running, then stop the animation
            self.Run(self.RunningButton)
            self.PutParametersInformation()  # Reboot the parameters information to the default
            self.PutInteractiveObjects()  # Reboot the interactive objects to the default

    def ShowGravity(self, slider):
        self.Gravity = float(slider.value)
        self.GravityText.text = str(self.Gravity)
        self.PutParametersInformation()
        self.PutInteractiveObjects()

    def ShowInitialAngle(self, slider):
        self.InitialAngle = float(slider.value)
        self.InitialAngleText.text = str(self.InitialAngle)
        self.PutParametersInformation()
        self.PutInteractiveObjects()

    def ShowInitialSpeed(self, slider):
        self.InitialSpeed = float(slider.value)
        self.InitialSpeedText.text = self.InitialSpeed
        self.PutParametersInformation()
        self.PutInteractiveObjects()

    #################################################################################################################################################
    # Parameters

    def PutParametersInformation(self):
        ##################################################################################
        # Put parameters of the simulation only if the simulation is not running
        # Because the tangent line is draw only if the simulation is not running, we add the tangent line in this function
        if self.Running == False:
            self.v0_x = 2
            self.v0_y = 0
            self.TotalTime = (
                2
                * self.InitialSpeed
                * np.sin(np.radians(self.InitialAngle))
                * (1 / self.Gravity)
            )

    #################################################################################################################################################
    # Interactives objectcs

    def PutInteractiveObjects(self):
        if (
            self.Running == False and self.time == 0
        ):  # The simulation is not running and the time is in 0
            self.time = 0.1 * self.TotalTime
            Point1 = vector(self.x_0, self.y_0, 0)
            self.x_position()
            self.y_position()
            Point2 = vector(self.x, self.y, 0)
            self.time = 0
            self.TangentLine.clear()
            self.TangentLine = curve(pos=[Point1, Point2])

    #################################################################################################################################################
    # Formulas

    def x_position(self):  # Put the atribute x position
        self.x = self.x_0 + self.v0_x * self.time
        if round(self.x) == 20:
            print("se cumple")
            self.v0_x = -0.9 * self.v0_x
            print(self.v0_x)

    def y_position(self):  # Put the atribute y position
        self.y = (
            self.y_0 + self.v0_y * self.time - (1 / 2) * self.Gravity * (self.time**2)
        )

        if self.y < 1e-6:
            self.x_0 = self.x
            self.v0_y = 0.9 * np.sqrt(self.v0_y**2 + 2 * self.Gravity * self.y_0)
            self.y_0 = 0
            self.time = 0


ProjectilSimulation()
