# chopsticks

# what it does
Using reinforcement learning I made a perfect chopsticks player

# code
  * utilityFunctions.py: contains useful functions for interactions between representations of chopsticks hands
  * learn.py: the reinforcement learning. Uses Bellman's equation to compute the value function and stores this is results.json
  * play.py: use the value function to play chopsticks from the terminal
  * resultsToStrategy.py: compute the optimal move from each state using the value function to make a simpler strategy csv
# how to test it
Either download the code and play from the terminal, or go to the website: <a href="https://chopsticks.surge.sh">https://chopsticks.surge.sh</a>
