/*
 * planet.h
 *
 */

#ifndef PLANET_H_
#define PLANET_H_

typedef struct Planet {
  double pos_x, pos_y, vel_x, vel_y, mass, density, radius;
  int fixed;
  int mass_changed;
  int index;
} Planet;

typedef struct PlanetKeeper {
  //int *planets[1000];
  Planet* planets[1000];
  int maxindex;
} PlanetKeeper;

// Create the mighty planetkeeper
PlanetKeeper* create_planetkeeper();

void free_planetkeeper(PlanetKeeper *planetkeeper);

// Creates a new planet-object
int create_planet(PlanetKeeper *planetkeeper, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density);

void delete_planet(PlanetKeeper *planetkeeper, int index);

double get_planet_mass(PlanetKeeper *planetkeeper, int index);
void set_planet_mass(PlanetKeeper *planetkeeper, int index, double mass);

double get_planet_density(PlanetKeeper *planetkeeper, int index);
void set_planet_density(PlanetKeeper *planetkeeper, int index, double density);

double get_planet_radius(PlanetKeeper *planetkeeper, int index);
void set_planet_radius(PlanetKeeper *planetkeeper, int index, double radius);

double get_planet_pos_x(PlanetKeeper *planetkeeper, int index);
double get_planet_pos_y(PlanetKeeper *planetkeeper, int index);

double get_planet_vel_x(PlanetKeeper *planetkeeper, int index);
double get_planet_vel_y(PlanetKeeper *planetkeeper, int index);

void fix_planet(PlanetKeeper *planetkeeper, int index);
void unfix_planet(PlanetKeeper *planetkeeper, int index);

void tick(PlanetKeeper *planetkeeper, double ratio);

int planet_exists(PlanetKeeper *planetkeeper, int index);

#endif /* PLANET_H_ */
