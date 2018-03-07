/*
 * rk4engine.h
 *
 */

#ifndef RK4ENGINE_H_
#define RK4ENGINE_H_

typedef struct Planet {
  double mass, density, radius;
  double pos_x, pos_y, vel_x, vel_y;
  int fixed;
  int mass_changed;
  int index;
} Planet;

typedef struct Acceleration {
  double ax;
  double ay;
} Acceleration;

typedef struct Rk4Engine {
  Planet* planets[1000];
} Rk4Engine;

Rk4Engine* create_rk4engine();

void free_rk4engine(Rk4Engine *rk4engine);

int create_planet(Rk4Engine *rk4engine, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density);

void delete_planet(Rk4Engine *rk4engine, int index);

double get_planet_mass(Rk4Engine *rk4engine, int index);
void set_planet_mass(Rk4Engine *rk4engine, int index, double mass);

double get_planet_density(Rk4Engine *rk4engine, int index);
void set_planet_density(Rk4Engine *rk4engine, int index, double density);

double get_planet_radius(Rk4Engine *rk4engine, int index);
void set_planet_radius(Rk4Engine *rk4engine, int index, double radius);

double get_planet_pos_x(Rk4Engine *rk4engine, int index);
double get_planet_pos_y(Rk4Engine *rk4engine, int index);

double get_planet_vel_x(Rk4Engine *rk4engine, int index);
double get_planet_vel_y(Rk4Engine *rk4engine, int index);

void fix_planet(Rk4Engine *rk4engine, int index);
void unfix_planet(Rk4Engine *rk4engine, int index);

void tick(Rk4Engine *rk4engine, double ratio);

int planet_exists(Rk4Engine *rk4engine, int index);

#endif /* RK4ENGINE_H_ */
