/*
 * planet.c
 *
 */

#include <stdlib.h>
#include "planet.h"
//#include <math.h>


PlanetKeeper* create_planetkeeper() {

  PlanetKeeper *planetkeeper = (PlanetKeeper *)malloc(sizeof(PlanetKeeper));

  int i;
  for(i = 0; i < 1000; i++) {
    planetkeeper->planets[i] = NULL;
  }

  planetkeeper->maxindex = -1;

  return planetkeeper;

}

void free_planetkeeper(PlanetKeeper *planetkeeper) {
  free(planetkeeper);
}

int create_planet(PlanetKeeper *planetkeeper, double pos_x, double pos_y, double vel_x, double vel_y, double mass, double density) {

  Planet *planet = (Planet *)malloc(sizeof(Planet));

  planet->pos_x = pos_x;
  planet->pos_y = pos_y;
  planet->vel_x = vel_x;
  planet->vel_y = vel_y;
  planet->mass = mass;
  planet->density = density;
  planet->fixed = 0;
  //planet->radius = radius;

  double radius_3 = ((3 * planet->mass) / (4 * 3.14 * planet->density));
  double radius = radius_3;

  int iterations2;
  for (iterations2 = 0; iterations2 < 10; iterations2++) {
    radius = ((2 * radius * radius * radius) + radius_3) / (3 * radius * radius);
  }

  planet->radius = radius;

  int i;
  int index;

  for(i = 0; i < 1000; i++) {
    if (planetkeeper->planets[i] == NULL) {
      planetkeeper->planets[i] = planet;
      planet->index = i;
      index = i;
      if (index > planetkeeper->maxindex) {
        planetkeeper->maxindex = index;
      }
      //break;
      return index;
    }
  }
  // free memory?
  return -1;

}

void delete_planet(PlanetKeeper *planetkeeper, int index) {

  int i;

  for(i = 0; i < 1000; i++) {
    if (i == index) {
      if (planetkeeper->planets[i] != NULL) {
        free(planetkeeper->planets[i]);
        planetkeeper->planets[i] = NULL;
      }
      break;
    }
  }

}

int planet_exists(PlanetKeeper *planetkeeper, int index) {

  if (planetkeeper->planets[index] == NULL) {
    return 0;
  } else {
    return 1;
  }

}


double get_planet_mass(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->mass;
}

void set_planet_mass(PlanetKeeper *planetkeeper, int index, double mass) {
  Planet *planet = planetkeeper->planets[index];
  planet->mass = mass;
}

double get_planet_density(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->density;
}

void set_planet_density(PlanetKeeper *planetkeeper, int index, double density) {
  Planet *planet = planetkeeper->planets[index];
  planet->density = density;
}

double get_planet_radius(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->radius;
}

void set_planet_radius(PlanetKeeper *planetkeeper, int index, double radius) {
  Planet *planet = planetkeeper->planets[index];
  planet->radius = radius;
}

double get_planet_pos_x(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->pos_x;
}

double get_planet_pos_y(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->pos_y;
}

double get_planet_vel_x(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->vel_x;
}

double get_planet_vel_y(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  return planet->vel_y;
}


void fix_planet(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  planet->fixed = 1;
}

void unfix_planet(PlanetKeeper *planetkeeper, int index) {
  Planet *planet = planetkeeper->planets[index];
  planet->fixed = 0;
}

void tick(PlanetKeeper *planetkeeper, double ratio) {

  int index_1;
  int index_2;

  for(index_1 = 0; index_1 < planetkeeper->maxindex + 1; index_1++) {

    // GRAVITY
    for(index_2 = index_1 + 1; index_2 < planetkeeper->maxindex + 1; index_2++) {

      Planet *planet1 = planetkeeper->planets[index_1];
      Planet *planet2 = planetkeeper->planets[index_2];

      if ((planet1 != NULL) && (planet2 != NULL)) {

        // CALCULATE DISTANCE

        double dist_x = planet1->pos_x - planet2->pos_x;
        double dist_y = planet1->pos_y - planet2->pos_y;

        double dist_sq = dist_x * dist_x + dist_y * dist_y;

        if (dist_sq == 0) {
          dist_sq = 0.00000001;
        }

        double dist = dist_sq / 2;

        int iterations;

        for (iterations = 0; iterations < 10; iterations++) {
          dist = (dist + dist_sq / dist) * 0.5;
        }

        // CHECK COLLISION
        if (dist < (planet1->radius + planet2->radius)) {

          double impulse_x = planet1->vel_x * planet1->mass + planet2->vel_x * planet2->mass;
          double impulse_y = planet1->vel_y * planet1->mass + planet2->vel_y * planet2->mass;

          if (planet1->mass <= planet2->mass) {
            planet2->mass += planet1->mass;
            planet2->vel_x = impulse_x / planet2->mass;
            planet2->vel_y = impulse_y / planet2->mass;
            double delete_index = planet1->index;
            delete_planet(planetkeeper, delete_index);
          } else {
            planet1->mass += planet2->mass;
            planet1->vel_x = impulse_x / planet1->mass;
            planet1->vel_y = impulse_y / planet1->mass;
            double delete_index = planet2->index;
            delete_planet(planetkeeper, delete_index);
          }

          continue;
        }

        // CALCULATE FORCE

        double force = (planet1->mass * planet2->mass) / (dist * dist);
        double force_x = force * (dist_x / dist);
        double force_y = force * (dist_y / dist);


        // CALCULATE VELOCITY

        planet1->vel_x -= force_x * ratio / planet1->mass;
        planet1->vel_y -= force_y * ratio / planet1->mass;

        planet2->vel_x += force_x * ratio / planet2->mass;
        planet2->vel_y += force_y * ratio / planet2->mass;

      }
    }
  }

  int index3;

  for(index3 = 0; index3 < planetkeeper->maxindex + 1; index3++) {
    // POSITION AND SIZE
    Planet *planet = planetkeeper->planets[index3];
    if (planet != NULL) {
      if (planet->fixed == 0) {
        planet->pos_x = planet->pos_x + planet->vel_x * ratio;
        planet->pos_y = planet->pos_y + planet->vel_y * ratio;
      }
      double radius_3 = ((3 * planet->mass) / (4 * 3.14 * planet->density));

      double radius = radius_3;

      int iterations2;
      for (iterations2 = 0; iterations2 < 10; iterations2++) {
        radius = ((2 * radius * radius * radius) + radius_3) / (3 * radius * radius);
      }

      planet->radius = radius;

    }
  }
}
