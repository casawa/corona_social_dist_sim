"""A simple simulation to interactively show the importance of early social distancing."""
class Simulation(object):
    def __init__(self, population_size, r0):
        self._population_size = population_size
        self._r0 = r0

        self._num_infected = 0
        self._num_recovered = 0
        self._num_deaths = 0

    @property
    def num_infected(self):
        return self._num_infected

    @property
    def num_recovered(self):
        return self._num_recovered

    @property
    def num_deaths(self):
        return self._num_deaths

    def step_day(self, distance_likelihood):
        # ASSUMPTION: recovered don't get it again
        pass

def main():
    # Parse arguments
    # TODO replace with args parsed
    population_size = 10 * 1000
    r0 = 2
    num_days = 3

    sim = Simulation(population_size, r0)

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
