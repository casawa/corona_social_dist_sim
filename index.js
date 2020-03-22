import Simulation from './sim.js'

// Setup simulation
const population_size = 10 * 1000
const r0 = 2
const initial_outbreak_size = 3
const conditionsElem = document.getElementById("initConditions")
conditionsElem.innerHTML = `Population Size: ${population_size}, Initial Outbreak Size: ${initial_outbreak_size}`

let sim = new Simulation(population_size, r0, initial_outbreak_size)
let day = 0

const statsTextElem = document.getElementById("stats")

function display_stats(display_unknown) {
    // Admittedly slightly jank, could instead append child nodes/etc
    let stats_text = `<p>Day ${day}</p>`
    if (display_unknown) {
        stats_text = stats_text.concat(`<p>Number infected: ${sim.num_infected}</p>`)
        stats_text = stats_text.concat(`<p>-- Number known infected: ${sim.num_known_infected}</p>`)
        stats_text = stats_text.concat(`<p>-- Number unknown infected: ${sim.num_unknown_infected}</p>`)
    } else {
        stats_text = stats_text.concat(`<p>Number known infected: ${sim.num_known_infected}</p>`)
    }
    stats_text = stats_text.concat(`<p>Number recovered: ${sim.num_recovered}</p>`)
    stats_text = stats_text.concat(`<p>Number of deaths: ${sim.num_deaths}</p>`)
    statsTextElem.innerHTML = stats_text
}

const slider = document.getElementById("distLikelihoodSlider")
const sliderValue = document.getElementById("sliderVal")
sliderValue.innerHTML = slider.value;
slider.oninput = function() {
  sliderValue.innerHTML = this.value;
}

function run_step() {
    sim.step_day(slider.value / 100.);
    day += 1
    display_stats(false)
}

const runButton = document.getElementById("runButton")
runButton.onclick = run_step

function reset() {
    day = 0
    sim = new Simulation(population_size, r0, initial_outbreak_size)
    display_stats(false)
}

const resetButton = document.getElementById("resetButton")
resetButton.onclick = reset

display_stats(false)
