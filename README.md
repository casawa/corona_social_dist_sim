# COVID-19 Social Distancing Simulator

### Purpose
Social distancing is very important to containing COVID-19.
However, admittedly at first, the risk for an individual might not seem that high.

This simulation aims for people to -- just like real life -- 
make a decision each day of social distancing or not and seeing 
the consequences of their actions to better understand the risk.

Doing this since I didn't see such a simulation, and wondering
if an interactive way is useful in grappling the decisions
one will need to make in real life.

### The External Pitch
Each day, with the information you have, you have a choice:
- Should you leave home and do your regular routine, or stay at home?

Everyone else also has this choice and information, and may think similar to what you're thinking -- and your choice likely influences theirs. In this simulation, they think the exact same way you do. So if you think there's a small risk and have a 10% chance of staying at home, everyone else is also thinking as such.

What are the long-term consequences of this thinking as the virus spreads?

**Note**: This is not a scientific simulation and the numbers should not be trusted for any reason! It is purely for illustrative purposes.

### Dev
#### Web App
- Start up a web server with `python3 -m http.server`
- Open up `http://localhost:8000` in your browser
#### CLI
- With node >= v13 simply run: `node ./main.js` to run the javascript simulation
- Initially started with a  CLI python prototype which can be run by `python3 ./prototyping/sim.py`

### TODO
- Web client improvements 
  - Improve intro explanation
  - Better data visuals (graphs, etc)
  - Generally way better UI/UX of course
- Simulation improvements
  - Potentially add model explanation
