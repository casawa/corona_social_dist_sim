"""A simple simulation to interactively show the importance of early social distancing."""

import random

class Simulation(object):
    def __init__(self, population_size, r0, initial_outbreak_size):
        self._r0 = r0

        # TODO better models? (e.g. consider time better)
        # TODO consider exposing these params in the API?
        self._i_to_r = 0.25  # Idea being 1 - (1 - 0.25)^14 is approx 0.98
        self._i_to_d = 0.003  # Idea being 1 - (1 - 0.003)^7 is approx 0.02
        self._i_to_i = 1 - self._i_to_r - self._i_to_d

        self._suspectible = set(range(population_size))
        self._infected = set()
        Simulation._random_split_set(self._suspectible, self._infected, k=initial_outbreak_size)

        self._recovered = set()
        self._deaths = set()

    @staticmethod
    def _random_split_set(source_set, dest_set, k):
        """Randomly moves k elements from the source_set to dest_set"""
        rand_elems = random.sample(source_set, k)
        for elem in rand_elems:
            dest_set.add(elem)
            source_set.remove(elem)

    @property
    def num_infected(self):
        return len(self._infected)

    @property
    def num_recovered(self):
        return len(self._recovered)

    @property
    def num_deaths(self):
        return len(self._deaths)

    def step_day(self, distance_likelihood):
        # ASSUMPTION: recovered don't get it again
        pass

def main():
    # Parse arguments
    # TODO replace with args parsed
    population_size = 10 * 1000
    r0 = 2
    num_days = 3
    initial_outbreak_size = 3

    sim = Simulation(population_size, r0, initial_outbreak_size)

    # Run simulation over days
    for i in range(num_days):
        print("Day {}".format(i))

        # TODO prompt for distance_likelihood
        distance_likelihood = 0
        sim.step_day(distance_likelihood)
        print("Number of infected: {}".format(sim.num_infected))
        print("Number of recovered: {}".format(sim.num_recovered))
        print("Number of deaths: {}".format(sim.num_deaths))

if __name__ == '__main__':
    main()
