# requires cplanet build in this directory
from cplanet import CPlanetKeeper
import unittest


class CPlanetTests(unittest.TestCase):

    def setUp(self):
        self.keeper = CPlanetKeeper()

    def tearDown(self):
        del self.keeper

    def test_basic(self):
        '''
        very simple test to see if index is returned
        '''
        pos = (0, 0)
        vel = (0, 0)
        mass = 1
        density = 1
        newindex = self.keeper.create_planet(
            pos_x=pos[0],
            pos_y=pos[1],
            vel_x=vel[0],
            vel_y=vel[1],
            mass=mass,
            density=density
        )
        self.assertEqual(newindex, 0)

    def test_multi(self):
        '''
        check for body limit of 1000
        '''
        for index in xrange(1000):
            pos = (index, index)
            vel = (index, index)
            mass = index
            density = index
            newindex = self.keeper.create_planet(
                pos_x=pos[0],
                pos_y=pos[1],
                vel_x=vel[0],
                vel_y=vel[1],
                mass=mass,
                density=density
            )
        self.assertEqual(newindex, 999)
        newindex = self.keeper.create_planet(
            pos_x=pos[0],
            pos_y=pos[1],
            vel_x=vel[0],
            vel_y=vel[1],
            mass=mass,
            density=density
        )
        self.assertEqual(newindex, -1)

    def test_load(self):
        '''
        simple load test to measure engine improvements
        '''
        for _ in xrange(100):
            for index in xrange(1000):
                pos = (index, index)
                vel = (index, index)
                mass = index
                density = index
                newindex = self.keeper.create_planet(
                    pos_x=pos[0],
                    pos_y=pos[1],
                    vel_x=vel[0],
                    vel_y=vel[1],
                    mass=mass,
                    density=density
                )
            self.keeper.tick(1)

    def test_calc_third_root(self):
        number = 8
        result = self.keeper.calc_third_root(number)
        print 'HOLY THIRD GRAIL of', number, result
        number = 125
        result = self.keeper.calc_third_root(number)
        print 'HOLY THIRD GRAIL of', number, result
        number = 1000
        result = self.keeper.calc_third_root(number)
        print 'HOLY THIRD GRAIL of', number, result
        number = 8000
        result = self.keeper.calc_third_root(number)
        print 'HOLY THIRD GRAIL of', number, result

    def test_calc_root(self):
        number = 4
        result = self.keeper.calc_root(number)
        print 'HOLY SECOND GRAIL of', number, result
        number = 100
        result = self.keeper.calc_root(number)
        print 'HOLY SECOND GRAIL of', number, result
        number = 10000
        result = self.keeper.calc_root(number)
        print 'HOLY SECOND GRAIL of', number, result

    def test_force_calculation(self):
        dist = 600
        index1 = self.keeper.create_planet(
            pos_x=0,
            pos_y=0,
            vel_x=0,
            vel_y=0,
            mass=270000.0,
            density=1
        )
        index2 = self.keeper.create_planet(
            pos_x=dist,
            pos_y=0,
            vel_x=0,
            vel_y=0,
            mass=27.5,
            density=1
        )
        force = self.keeper.calc_force(index1, index2, dist)
        print 'Force between', index1, index2, force

        dist = 600
        index1 = self.keeper.create_planet(
            pos_x=0,
            pos_y=0,
            vel_x=0,
            vel_y=0,
            mass=36500.0,
            density=1
        )
        index2 = self.keeper.create_planet(
            pos_x=dist,
            pos_y=0,
            vel_x=0,
            vel_y=0,
            mass=27.5,
            density=1
        )
        force = self.keeper.calc_force(index1, index2, dist)
        print 'Force between', index1, index2, force




if __name__ == '__main__':
    unittest.main()
