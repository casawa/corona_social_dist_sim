"""A simple simulation to interactively show the importance of early social distancing."""

import random

# TODO: Main flaws
# Considering state
# Considering time?
# Stochastity?
class Simulation(object):
    """See step_day() for the model."""
    def __init__(self, population_size, r0, initial_outbreak_size):
        self._population_size = population_size
        self._r0 = r0

        # TODO consider exposing these params in the API?
        self._i_to_r = 0.25   # Idea being 1 - (1 - 0.25)^14 is approx 0.98
        self._i_to_d = 0.003  # Idea being 1 - (1 - 0.003)^7 is approx 0.02
        self._u_to_k = 0.5    # No idea if this is right
        self._incubation_period = 1   # TODO probably not the correct use of incubation period
        self._i_to_i = 1 - self._i_to_r - self._i_to_d

        self._suspectible = set(range(population_size))
        self._unknown_infected = dict()  # ID -> Days infected
        self._known_infected = dict()    # ID -> Days infected
        self._move_rand_s_to_u(k=initial_outbreak_size)

        self._recovered = set()
        self._deaths = set()

    @staticmethod
    def _rand_split_set(source_set, dest_set, k):
        """Randomly moves k elements from the source_set to dest_set"""
        rand_elems = random.sample(source_set, k)
        for elem in rand_elems:
            dest_set.add(elem)
            source_set.remove(elem)

    @property
    def num_suspectible(self):
        return len(self._suspectible)

    @property
    def num_infected(self):
        return len(self._unknown_infected) + len(self._known_infected)

    @property
    def num_known_infected(self):
        return len(self._known_infected)

    @property
    def num_unknown_infected(self):
        return len(self._unknown_infected)

    @property
    def num_recovered(self):
        return len(self._recovered)

    @property
    def num_deaths(self):
        return len(self._deaths)

    def _move_rand_s_to_u(self, k):
        """Randomly moves k people from suspectible to unknown infected"""
        rand_elems = random.sample(self._suspectible, k)
        for elem in rand_elems:
            self._unknown_infected[elem] = 0
            self._suspectible.remove(elem)

    def _suspectible_to_unknown(self, distance_likelihood):
        # TODO I don't believe r0 is the right number here, but temporarily
        # Really should use beta for up to gamma days
        num_will_get_infected = int(self._r0 * self.num_unknown_infected * ((1 - distance_likelihood) * self.num_suspectible) / self._population_size)
        self._move_rand_s_to_u(k=num_will_get_infected)

    def _get_incubated_unknowns(self):
        incubated_unknowns = set()
        for u in self._unknown_infected:
            if self._unknown_infected[u] >= self._incubation_period:
                incubated_unknowns.add(u)

        return incubated_unknowns

    def _unknown_to_known_infected(self):
        # TODO make sure state safe, consider stochasticity
        incubated_unknowns = self._get_incubated_unknowns()
        num_to_known = int(self._u_to_k * len(incubated_unknowns))
        rand_persons = random.sample(incubated_unknowns, num_to_known)
        for person in rand_persons:
            self._known_infected[person] = self._unknown_infected[person]
            del self._unknown_infected[person]

    def _unknown_to_recovered(self):
        # TODO make sure state safe, consider stochasticity
        incubated_unknowns = self._get_incubated_unknowns()
        num_to_recovered = int(self._i_to_r * len(incubated_unknowns))
        rand_persons = random.sample(incubated_unknowns, num_to_recovered)
        for person in rand_persons:
            del self._unknown_infected[person]
            self._recovered.add(person)

    def _known_to_recovered(self):
        # TODO make sure state-safe. Could probably share code with _known_to_death
        # TODO could depend on how long they've had it too
        num_to_recover = int(self.num_known_infected * self._i_to_r)
        rand_persons = random.sample(self._known_infected.keys(), num_to_recover)
        for person in rand_persons:
            del self._known_infected[person]
            self._recovered.add(person)

    def _known_to_death(self):
        # TODO make sure state-safe. Could probably share code with _known_to_recovered
        # TODO could depend on how long they've had it too
        num_to_die = int(self.num_known_infected * self._i_to_d)
        rand_persons = random.sample(self._known_infected.keys(), num_to_die)
        for person in rand_persons:
            del self._known_infected[person]
            self._deaths.add(person)

    def _update_day_counts(self):
        for person in self._known_infected:
            self._known_infected[person] += 1

        for person in self._unknown_infected:
            self._unknown_infected[person] += 1

    def step_day(self, distance_likelihood):
        """Simulates one day.

        The transition model is as follows:
          S --> U --> K --> D
                |     |
                v     v
                R     R
        - Assumes takes at least one day to go between states.
        - Assumes recovered can't get it again.
        - Assumes only known cases are severe enough to lead to death.
        - Assumes only unknown cases can infect because cases that are
        known hopefully self-isolate (of course, this doesn't account for
        hospitals, households, etc).
        """
        self._suspectible_to_unknown(distance_likelihood)

        self._unknown_to_known_infected()
        self._unknown_to_recovered()
        self._known_to_death()
        self._known_to_recovered()

        self._update_day_counts()

def prompt_social_distance_likelihood():
    while True:
        try:
            user_response = input("How likely are you to social distance today? Enter between 0 to 1: ")
            if user_response.lower().startswith('q'):
                return None

            distance_likelihood = float(user_response)
            if 0 <= distance_likelihood <= 1:
                return distance_likelihood
        except:
            pass

def main():
    # TODO replace with args parsed
    population_size = 10 * 1000
    r0 = 2
    num_days = 3
    initial_outbreak_size = 3

    sim = Simulation(population_size, r0, initial_outbreak_size)

    # Run simulation over days
    for i in range(num_days):
        print("Day {}".format(i))

        distance_likelihood = 0.
        # distance_likelihood = prompt_social_distance_likelihood()
        # if distance_likelihood is None:
        #     return
        sim.step_day(distance_likelihood)
        print("Number of infected: {}".format(sim.num_infected))
        print("- Number of known infected: {}".format(sim.num_known_infected))
        print("- Number of unknown infected: {}".format(sim.num_unknown_infected))
        print("Number of recovered: {}".format(sim.num_recovered))
        print("Number of deaths: {}".format(sim.num_deaths))

if __name__ == '__main__':
    main()
