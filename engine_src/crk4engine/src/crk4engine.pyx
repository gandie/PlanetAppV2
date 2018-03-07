# distutils: language = c
# distutils: sources = rk4engine.c

cdef extern from "rk4engine.h":
    ctypedef struct Planet:
        double mass, density, radius
        double pos_x, pos_y, vel_x, vel_y
        int fixed
        int mass_changed
        int index

    ctypedef struct Acceleration:
        double ax
        double ay

    ctypedef struct Rk4Engine:
        Planet* planets[1000]

    Rk4Engine* create_rk4engine()
    void free_rk4engine(Rk4Engine *rk4engine)
    int create_planet(Rk4Engine *rk4engine, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density)
    void delete_planet(Rk4Engine *rk4engine, int index)

    double get_planet_mass(Rk4Engine *rk4engine, int index)
    void set_planet_mass(Rk4Engine *rk4engine, int index, double mass)

    double get_planet_density(Rk4Engine *rk4engine, int index)
    void set_planet_density(Rk4Engine *rk4engine, int index, double density)

    double get_planet_radius(Rk4Engine *rk4engine, int index)
    void set_planet_radius(Rk4Engine *rk4engine, int index, double radius)

    double get_planet_pos_x(Rk4Engine *rk4engine, int index)
    double get_planet_pos_y(Rk4Engine *rk4engine, int index)

    double get_planet_vel_x(Rk4Engine *rk4engine, int index)
    double get_planet_vel_y(Rk4Engine *rk4engine, int index)

    void fix_planet(Rk4Engine *rk4engine, int index)
    void unfix_planet(Rk4Engine *rk4engine, int index)

    void tick(Rk4Engine *rk4engine, double ratio)

    int planet_exists(Rk4Engine *rk4engine, int index)

cdef class CRk4Engine:

    cdef Rk4Engine *rk4engine

    def __cinit__(self):
        self.rk4engine = create_rk4engine()

    def __dealloc__(self):
        free_rk4engine(self.rk4engine)

    def create_planet(self, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density):
        return create_planet(self.rk4engine, pos_x, pos_y, vel_x, vel_y, mass, density)

    def delete_planet(self, int index):
        delete_planet(self.rk4engine, index)

    def get_planet_mass(self, int index):
        return get_planet_mass(self.rk4engine, index)

    def set_planet_mass(self, int index, double mass):
        set_planet_mass(self.rk4engine, index, mass)

    def get_planet_density(self, int index):
        return get_planet_density(self.rk4engine, index)

    def set_planet_density(self, int index, double density):
        set_planet_density(self.rk4engine, index, density)

    def get_planet_radius(self, int index):
        return get_planet_radius(self.rk4engine, index)

    def set_planet_radius(self, int index, double radius):
        set_planet_radius(self.rk4engine, index, radius)

    def get_planet_pos_x(self, int index):
        return get_planet_pos_x(self.rk4engine, index)

    def get_planet_pos_y(self, int index):
        return get_planet_pos_y(self.rk4engine, index)

    def get_planet_vel_x(self, int index):
        return get_planet_vel_x(self.rk4engine, index)

    def get_planet_vel_y(self, int index):
        return get_planet_vel_y(self.rk4engine, index)

    def fix_planet(self, int index):
        fix_planet(self.rk4engine, index)

    def unfix_planet(self, int index):
        unfix_planet(self.rk4engine, index)

    def tick(self, double ratio):
        tick(self.rk4engine, ratio)

    def planet_exists(self, int index):
        return planet_exists(self.rk4engine, index)
