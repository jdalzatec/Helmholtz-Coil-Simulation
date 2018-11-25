import numpy
from functions import  *

class Coil(object):
    def __init__(self, num_turns, I, pos_z, color="black"):
        self.num_turns = num_turns
        self.I = I
        self.pos_z = pos_z
        self.color = color
        

class CircularCoil(Coil):
    def __init__(self, radius, num_turns, I, pos_z, color="black"):
        Coil.__init__(self, num_turns, I, pos_z, color)
        self.radius = radius


    def Brho(self, rho, z):
        kto2 = 4.0 * self.radius * rho / (
            (self.radius + rho)**2 + (z - self.pos_z)**2)
        return (self.num_turns * self.I * (z - self.pos_z) / (2.0 * numpy.pi * rho * numpy.sqrt((
            rho + self.radius)**2 + (z - self.pos_z)**2))) * \
            ((self.radius**2 + rho**2 + (z - self.pos_z)**2) * E(kto2) / (
                (self.radius - rho)**2 + (z - self.pos_z)**2) - K(kto2) )


    def Bz(self, rho, z):
        kto2 = 4.0 * self.radius * rho / (
            (self.radius + rho)**2 + (z - self.pos_z)**2)
        return (self.num_turns * self.I / (2.0 * numpy.pi * numpy.sqrt((
            rho + self.radius)**2 + (z - self.pos_z)**2))) * \
            ((self.radius**2 - rho**2 - (z - self.pos_z)**2) * E(kto2) / (
                (self.radius - rho)**2 + (z - self.pos_z)**2) + K(kto2) )