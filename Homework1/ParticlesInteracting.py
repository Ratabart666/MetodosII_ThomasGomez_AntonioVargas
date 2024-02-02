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
        # Title,caption, dimentions of the box , initial range of the spheres , numbers of spheres , spheres radius
        scene.title = "\n Particulas en colisión \n \n \n"
        scene.caption = "\n Elija los parámetros : \n \n \n"
        self.BoxSize = 40
        self.SpheresInitialRange = (
            10  # maximu range to left or right of the origin of the box
        )
        self.SphereRadius = 10
        self.TotalSpheres = 10

        # Create the box if the users wants, the default is True
        self.ExistsBox = True
        if self.ExistsBox == True:
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

        # Create the spheres
        self.GenerateRandomSpheres()
        t = 0
        dt = 0.001

        while True:
            speed = 10
            self.FramesPerSecond = rate(speed * (1 / 0.001))
            t += dt
            if t == 10:
                pass
            LinealMomentx, LinealMomenty, LinealMomentz = 0, 0, 0
            for Id in range(1, self.TotalSpheres + 1):
                Sphere = getattr(self, str(Id))
                vx, vy, vz = Sphere.TupleVel
                x, y, z = Sphere.TuplePos
                ax, ay, az = tuple(self.ComputeForce(str(Id)))
                LinealMomentx += vx
                LinealMomenty += vy
                LinealMomentz += vz
                newx, newy, newz = (
                    x + vx * dt + (1 / 2) * ax * (dt**2),
                    y + vy * dt + (1 / 2) * ay * (dt**2),
                    z + vz * dt + (1 / 2) * az * (dt**2),
                )
                getattr(self, str(Id)).pos = vector(newx, newy, newz)
                getattr(self, str(Id)).TuplePos = (newx, newy, newz)
                self.ComputeForce(str(Id))

    def GenerateRandomPos(self):
        "Generate a random position"
        x, y, z = tuple(
            np.random.uniform(
                -self.SpheresInitialRange, self.SpheresInitialRange, size=3
            )
        )

        return x, y, z

    def GenerateRandomVel(self):
        x, y, z = tuple(np.random.uniform(-1, 1, size=3))  # Vector of direction
        vel = np.random.uniform(0, 0)
        v_x, v_y, v_z = x * vel, y * vel, z * vel
        return v_x, v_y, v_z

    def GenerateRandomSpheres(self):
        "Generates randoms spheres"
        self.SpheresDict = dict()
        Id = 0
        for Id in range(1, self.TotalSpheres + 1):
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
                ),
            )

    def ComputeForce(self, IdSphere):
        SpherePos = np.array(getattr(self, str(IdSphere)).TuplePos)
        Force = np.array([0, 0, 0])
        for Id in range(1, self.TotalSpheres + 1):
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
                    ModuleForce = (2 * self.SphereRadius - d) ** 3
                    Force = Force + ModuleForce * DirectionForce
        return Force


CollidingParticles()
