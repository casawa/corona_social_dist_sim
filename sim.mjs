/* A simple simulation to interactively show the importance of early social distancing. */

// TODO: Main flaws
// Considering state (i.e. order should not matter between operations)
// Parameter values
// Considering time duration?
// Stochastity?
export default class Simulation {
    // See step_day() for the model.
    constructor(population_size, r0, initial_outbreak_size) {
        this._population_size = population_size
        this._r0 = r0

        // TODO consider exposing these params in the API?
        // In a version that considers time better...
        // this._i_to_r = 0.25   # Idea being 1 - (1 - 0.25)^14 is approx 0.98
        // this._i_to_d = 0.003  # Idea being 1 - (1 - 0.003)^7 is approx 0.02

        // On a given day, how often do these transitions happen?
        this._i_to_r = 0.30
        this._i_to_d = 0.02
        this._i_to_i = 1 - this._i_to_r - this._i_to_d

        this._u_to_k = 0.5            // TODO find more accurate value
        this._incubation_period = 3   // TODO probably not the correct use of incubation period

        this._suspectible = new Set()
        for (let i = 0; i < population_size; i++) {
            this._suspectible.add(i)
        }

        this._unknown_infected = {}  // ID -> Days infected
        this._known_infected = {}    // ID -> Days infected
        this._move_s_to_u(initial_outbreak_size)

        this._recovered = new Set()
        this._deaths = new Set()
    }

    get num_suspectible() {
        return this._suspectible.size
    }

    get num_known_infected() {
        return Object.keys(this._known_infected).length
    }

    get num_unknown_infected() {
        return Object.keys(this._unknown_infected).length
    }

    get num_infected() {
        return this.num_known_infected + this.num_unknown_infected
    }

    get num_recovered() {
        return this._recovered.size
    }

    get num_deaths() {
        return this._deaths.size
    }

    _move_s_to_u(k) {
        // TODO consider random?
        // Moves k people from suspectible to unknown infected
        const susCopy = Array.from(this._suspectible)
        for (let elem of susCopy.slice(0, k)) {
            this._suspectible.delete(elem)
            this._unknown_infected[elem] = 0
        }
    }

    _suspectible_to_unknown(distance_likelihood) {
        // TODO I don't believe r0 is the right number here, but temporarily
        // Really should use beta for up to gamma days
        const num_will_get_infected = Math.floor(this._r0 * this.num_unknown_infected * ((1 - distance_likelihood) * this.num_suspectible) / this._population_size)
        this._move_s_to_u(num_will_get_infected)
    }

    _get_incubated_unknowns() {
        const incubated_unknowns = []
        Object.entries(this._unknown_infected).forEach(([id, days]) => {
            if (days >= this._incubation_period) {
                incubated_unknowns.push(id)
            }
        })
        return incubated_unknowns
    }

    _unknown_to_known_infected() {
        // TODO consider stochasticity
        const incubated_unknowns = this._get_incubated_unknowns()
        const num_to_known = Math.floor(this._u_to_k * incubated_unknowns.length)

        for (let p of incubated_unknowns.slice(0, num_to_known)) {
            this._known_infected[p] = this._unknown_infected[p]
            delete this._unknown_infected[p]
        }
    }

    _unknown_to_recovered() {
        // TODO consider stochasticity
        const incubated_unknowns = this._get_incubated_unknowns()
        const num_to_recovered = Math.floor(this._i_to_r * incubated_unknowns.length)

        for (let p of incubated_unknowns.slice(0, num_to_recovered)) {
            this._recovered.add(p)
            delete this._unknown_infected[p]
        }
    }

    _known_to_recovered() {
        // TODO make sure state-safe. Could probably share code with _known_to_death
        // TODO could depend on how long they've had it too.
        // TODO consider stochastic
        const num_to_recover = Math.floor(this.num_known_infected * this._i_to_r)

        for (let p of Object.keys(this._known_infected).slice(0, num_to_recover)) {
            this._recovered.add(p)
            delete this._known_infected[p]
        }
    }

    _known_to_death() {
        // TODO make sure state-safe. Could probably share code with _known_to_recovered
        // TODO could depend on how long they've had it too
        // TODO consider stochastic
        const num_to_die = Math.floor(this.num_known_infected * this._i_to_d)

        for (let p of Object.keys(this._known_infected).slice(0, num_to_die)) {
            delete this._known_infected[p]
            this._deaths.add(p)
        }
    }

    _update_day_counts() {
        Object.entries(this._known_infected).forEach(e => this._known_infected[e[0]] += 1)
        Object.entries(this._unknown_infected).forEach(e => this._unknown_infected[e[0]] += 1)
   }

    step_day(distance_likelihood) {
        /**
         * Simulates one day.
         *
         * The transition model is as follows:
         *   S --> U --> K --> D
         *         |     |
         *         v     v
         *         R     R
         * - Assumes takes at least one day to go between states.
         * - Assumes recovered can't get it again.
         * - Assumes only known cases are severe enough to lead to death.
         * - Assumes only unknown cases can infect because cases that are
         * known hopefully isolate (of course, this doesn't account for
         * hospitals, households, etc).
         **/
        this._suspectible_to_unknown(distance_likelihood)

        this._unknown_to_known_infected()
        this._unknown_to_recovered()
        this._known_to_death()
        this._known_to_recovered()

        this._update_day_counts()
    }
}
