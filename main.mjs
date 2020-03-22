import Simulation from './sim.mjs'

function print_stats(sim, reveal_unknown) {
    if (reveal_unknown) {
        console.log(`Number of infected: ${sim.num_infected}`)
        console.log(`- Number of known infected: ${sim.num_known_infected}`)
        console.log(`- Number of unknown infected: ${sim.num_unknown_infected}`)
    } else {
        console.log(`Number of known infected: ${sim.num_known_infected}`)
    }

    console.log(`Number of recovered: ${sim.num_recovered}`)
    console.log(`Number of deaths: ${sim.num_deaths}`)
    console.log()
}

function main() {
    const population_size = 10 * 1000
    const r0 = 2
    const num_days = 30
    const initial_outbreak_size = 3

    const sim = new Simulation(population_size, r0, initial_outbreak_size)

    console.log("Day 0")
    print_stats(sim, true)

    for (let i = 0; i < num_days; i++) {
        console.log(`Day ${i + 1}`)

        let distance_likelihood = 0.2 // TODO useful to prompt in here?
        sim.step_day(distance_likelihood)
        print_stats(sim, true)
    }
}

main()
