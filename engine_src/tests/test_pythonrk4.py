import unittest
import sys
import time

from pyrk4engine import Engine


class CPlanetTests(unittest.TestCase):

    def setUp(self):
        self.keeper = Engine()

    def tearDown(self):
        del self.keeper

    def test_load(self):
        '''
        simple load test to measure engine improvements
        '''
        for _ in range(100):
            for index in range(1000):
                newindex = self.keeper.create_planet(
                    pos_x=index,
                    pos_y=index,
                    vel_x=index,
                    vel_y=index,
                    mass=index + 1,
                    density=index + 1
                )
            tick_start = time.time()
            self.keeper.tick(1)
            tick_took = time.time() - tick_start
            print('Tick %s/100 took %s seconds' % (_ + 1, round(tick_took, 3)))


if __name__ == '__main__':
    unittest.main()
