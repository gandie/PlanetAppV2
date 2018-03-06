/*
 * planet.c
 *
 */

#include <stdlib.h>
#include "planet.h"

Rk4Engine* create_rk4engine() {

  Rk4Engine *rk4engine = (Rk4Engine *)malloc(sizeof(Rk4Engine));

  int i;
  for(i = 0; i < 1000; i++) {
    rk4engine->planets[i] = NULL;
  }

  return rk4engine;

}

void free_rk4engine(Rk4Engine *rk4engine) {
  free(rk4engine);
}

int create_planet(Rk4Engine *rk4engine, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density) {

  int i;
  int index;
  index = -1;

  for(i = 0; i < 1000; i++) {
    if (rk4engine->planets[i] == NULL) {
      index = i;
      break;
    }
  }

  if (index == -1) {
    return -1;
  }

  Planet *planet = (Planet *)malloc(sizeof(Planet));
  planet->pos_x = pos_x;
  planet->pos_y = pos_y;
  planet->vel_x = vel_x;
  planet->vel_y = vel_y;
  planet->mass = mass;
  planet->density = density;
  planet->fixed = 0;
  planet->mass_changed = 0;

  // calculate radius from mass and density
  double radius_3 = ((3 * planet->mass) / (4 * 3.14 * planet->density));
  double radius = calc_third_root(radius_3);

  planet->radius = radius;
  planet->index = index;
  rk4engine->planets[index] = planet;
  return index;
}

void delete_planet(Rk4Engine *rk4engine, int index) {

  if (rk4engine->planets[index] != NULL) {
    free(rk4engine->planets[index]);
    rk4engine->planets[index] = NULL;
  }

}

int planet_exists(Rk4Engine *rk4engine, int index) {

  if (rk4engine->planets[index] == NULL) {
    return 0;
  } else {
    return 1;
  }

}

/************************/
/*PLANET GETTER / SETTER*/
/************************/

double get_planet_mass(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->mass;
}

void set_planet_mass(Rk4Engine *rk4engine, int index, double mass) {
  Planet *planet = rk4engine->planets[index];
  planet->mass = mass;
  planet->mass_changed = 1;
}

double get_planet_density(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->density;
}

void set_planet_density(Rk4Engine *rk4engine, int index, double density) {
  Planet *planet = rk4engine->planets[index];
  planet->density = density;
}

double get_planet_radius(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->radius;
}

void set_planet_radius(Rk4Engine *rk4engine, int index, double radius) {
  Planet *planet = rk4engine->planets[index];
  planet->radius = radius;
}

double get_planet_pos_x(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->pos_x;
}

double get_planet_pos_y(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->pos_y;
}

double get_planet_vel_x(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->vel_x;
}

double get_planet_vel_y(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  return planet->vel_y;
}

void fix_planet(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  planet->fixed = 1;
}

void unfix_planet(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  planet->fixed = 0;
}

/**************/
/*MATH HELPERS*/
/**************/

double calc_third_root(double value) {
  double start_value = value / 4;

  int iterations2;
  for (iterations2 = 0; iterations2 < 10; iterations2++) {
    start_value = ((2 * start_value * start_value * start_value) + value) / (3 * start_value * start_value);
  }
  return start_value;
}

double calc_root(double value) {

  double start_value = value / 2;

  int iterations;

  for (iterations = 0; iterations < 8; iterations++) {
    start_value = (start_value + value / start_value) * 0.5;
  }
  return start_value;

}
