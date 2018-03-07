/*
 * planet.c
 *
 */

#include <stdlib.h>
#include "rk4engine.h"


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

  for (iterations = 0; iterations < 15; iterations++) {
    start_value = (start_value + value / start_value) * 0.5;
  }
  return start_value;

}

/**************/
/*ENGINE START*/
/**************/

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

/******************/
/*ENGINE MAIN PART*/
/******************/

void update_radius(Rk4Engine *rk4engine, int index) {
  Planet *planet = rk4engine->planets[index];
  if (planet->mass_changed == 1) {
    double radius_3 = ((3 * planet->mass) / (4 * 3.14 * planet->density));
    double radius = calc_third_root(radius_3);
    planet->radius = radius;
    planet->mass_changed = 0;
  }
}

struct Acceleration calc_acceleration(Rk4Engine *rk4engine, int myindex, double mypos_x, double mypos_y, double mymass) {
  double ax = 0.0;
  double ay = 0.0;

  int index;
  for(index = 0; index < 1000; index++) {
    if (index == myindex) {
      continue;
    }
    Planet *planet2 = rk4engine->planets[index];
    if (planet2 == NULL) {
      continue;
    }

    double dist_x = planet2->pos_x - mypos_x;
    double dist_y = planet2->pos_y - mypos_y;
    double dist_sq = dist_x * dist_x + dist_y * dist_y;

    if (dist_sq == 0) {
      dist_sq = 0.00001;
    }

    double dist = calc_root(dist_sq);

    double force = 0.1 * (mymass * planet2->mass) / (dist * dist);
    double force_x = force * (dist_x / dist);
    double force_y = force * (dist_y / dist);

    ax = ax + (force_x / mymass);
    ay = ay + (force_y / mymass);
  }

  Acceleration a = { ax, ay };
  return a;
}

void update_planet(Rk4Engine *rk4engine, int index, double dt) {
  Planet *planet = rk4engine->planets[index];

  double initial_state_pos_x = planet->pos_x;
  double initial_state_pos_y = planet->pos_y;

  //Rk4Engine *rk4engine, int myindex, double mypos_x, double mypos_y, double mymass
  struct Acceleration initial_A = calc_acceleration(rk4engine, index, planet->pos_x, planet->pos_y, planet->mass);

  // INITIAL DERIVATIVE
  double initial_ax = initial_A.ax;
  double initial_ay = initial_A.ay;
  double initial_vx = planet->vel_x;
  double initial_vy = planet->vel_y;

  // CALCULATE SECOND DERIVATIVE
  double second_state_pos_x = initial_state_pos_x + initial_vx * (dt * 0.5);
  double second_state_pos_y = initial_state_pos_y + initial_vy * (dt * 0.5);

  struct Acceleration second_A = calc_acceleration(rk4engine, index, second_state_pos_x, second_state_pos_y, planet->mass);

  // SECOND DERIVATIVE
  double second_ax = second_A.ax;
  double second_ay = second_A.ay;
  double second_vx = initial_vx + initial_ax * (dt * 0.5);
  double second_vy = initial_vy + initial_ay * (dt * 0.5);

  // CALCULATE THIRD DERIVATIVE
  double third_state_pos_x = initial_state_pos_x + second_vx * (dt * 0.5);
  double third_state_pos_y = initial_state_pos_y + second_vy * (dt * 0.5);

  struct Acceleration third_A = calc_acceleration(rk4engine, index, third_state_pos_x, third_state_pos_y, planet->mass);

  // THIRD DERIVATIVE
  double third_ax = third_A.ax;
  double third_ay = third_A.ay;
  double third_vx = initial_vx + second_ax * (dt * 0.5);
  double third_vy = initial_vy + second_ay * (dt * 0.5);

  // CALCULATE FOURTH DERIVATIVE
  double fourth_state_pos_x = initial_state_pos_x + third_vx * dt;
  double fourth_state_pos_y = initial_state_pos_y + third_vy * dt;

  struct Acceleration fourth_A = calc_acceleration(rk4engine, index, fourth_state_pos_x, fourth_state_pos_y, planet->mass);

  // FOURTH DERIVATIVE
  double fourth_ax = fourth_A.ax;
  double fourth_ay = fourth_A.ay;
  double fourth_vx = initial_vx + third_ax * dt;
  double fourth_vy = initial_vy + third_ay * dt;

  // NOW CALCULATE THE ACTUAL CHANGE USING RK4 MAGIC
  double actual_vx = (1.0 / 6.0) * (initial_vx + 2 * (second_vx + third_vx) + fourth_vx);
  double actual_vy = (1.0 / 6.0) * (initial_vy + 2 * (second_vy + third_vy) + fourth_vy);
  double actual_ax = (1.0 / 6.0) * (initial_ax + 2 * (second_ax + third_ax) + fourth_ax);
  double actual_ay = (1.0 / 6.0) * (initial_ay + 2 * (second_ay + third_ay) + fourth_ay);

  // UPDATE PLANET
  planet->pos_x = planet->pos_x + actual_vx * dt;
  planet->pos_y = planet->pos_y + actual_vy * dt;
  planet->vel_x = planet->vel_x + actual_ax * dt;
  planet->vel_y = planet->vel_y + actual_ay * dt;

}


void tick (Rk4Engine *rk4engine, double dt) {
  int index;

  /*
  UPDATE LOOP
  update planets position and velocity based on rk4-smoothed gravity calculation
  also update radius if mass has changed
  */
  for(index = 0; index < 1000; index++) {
    Planet *planet = rk4engine->planets[index];
    if (planet == NULL) {
      continue;
    }
    if (planet->fixed == 0) {
      update_planet(rk4engine, index, dt);
    }
    update_radius(rk4engine, index);
  }


  /*
  COLLISION LOOP
  check if two plantes collide, use elastic collision if so
  */
  int index_1;
  int index_2;
  for(index_1 = 0; index_1 < 1000; index_1++) {

    Planet *planet1 = rk4engine->planets[index_1];

    if (planet1 == NULL) {
      continue;
    }


    for(index_2 = index_1 + 1; index_2 < 1000; index_2++) {

      Planet *planet2 = rk4engine->planets[index_2];

      if (planet2 == NULL) {
        continue;
      }

      double dist_x = planet1->pos_x - planet2->pos_x;
      double dist_y = planet1->pos_y - planet2->pos_y;
      double dist_sq = dist_x * dist_x + dist_y * dist_y;

      if (dist_sq == 0) {
        dist_sq = 0.00001;
      }

      double dist = calc_root(dist_sq);

      // CHECK COLLISION
      if (dist < (planet1->radius + planet2->radius)) {

        double impulse_x = planet1->vel_x * planet1->mass + planet2->vel_x * planet2->mass;
        double impulse_y = planet1->vel_y * planet1->mass + planet2->vel_y * planet2->mass;

        if (planet1->mass <= planet2->mass) {
          planet2->mass += planet1->mass;
          planet2->vel_x = impulse_x / planet2->mass;
          planet2->vel_y = impulse_y / planet2->mass;
          planet2->mass_changed = 1;
          double delete_index = planet1->index;
          delete_planet(rk4engine, delete_index);
        } else {
          planet1->mass += planet2->mass;
          planet1->vel_x = impulse_x / planet1->mass;
          planet1->vel_y = impulse_y / planet1->mass;
          planet1->mass_changed = 1;
          double delete_index = planet2->index;
          delete_planet(rk4engine, delete_index);
        }
      }
    }
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
