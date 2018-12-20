

class Simulation(object):
    def __init__(self, coils, z_min, z_max, z_points, rho_min, rho_max, rho_points):
        self.coils = coils
        self.z_min = z_min
        self.z_max = z_max
        self.z_points = z_points
        self.rho_min = rho_min
        self.rho_max = rho_max
        self.rho_points = rho_points
        