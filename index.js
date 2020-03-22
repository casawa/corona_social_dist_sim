import Simulation from './sim.js'

// Setup simulation
const population_size = 10 * 1000
const r0 = 2
const num_days = 30
const initial_outbreak_size = 3

const sim = new Simulation(population_size, r0, initial_outbreak_size)
let day = 0

const statsTextElem = document.getElementById("stats")

function display_stats() {
    // Admittedly just slightly jank, could instead append child nodes/etc
    let stats_text = `<p>Day ${day}</p>`
    stats_text = stats_text.concat(`<p>Number infected: ${sim.num_infected}</p>`)
    stats_text = stats_text.concat(`<p>Number known infected: ${sim.num_known_infected}</p>`)
    stats_text = stats_text.concat(`<p>Number unknown infected: ${sim.num_unknown_infected}</p>`)
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
    display_stats()
}

const button = document.getElementById("runButton")
button.onclick = run_step

display_stats()
