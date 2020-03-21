"""A simple simulation to interactively show the importance of early social distancing."""
class Simulation(object):
    def __init__(self, population_size, r0):
        self._population_size = population_size
        self._r0 = r0

        self._num_infected = 0
        self._num_recovered = 0
        self._num_deaths = 0

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

    # Run repl simulation
    for i in range(num_days):
        print("Day {}".format(i))

        # TODO prompt for distance_likelihood
        distance_likelihood = 0
        sim.step_day(distance_likelihood)

if __name__ == '__main__':
    main()
