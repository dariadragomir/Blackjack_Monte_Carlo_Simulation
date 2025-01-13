# Monte Carlo Blackjack Simulation

This project uses a **Monte Carlo simulation** to approximate the probabilities of winning a game of Blackjack. The simulation considers only two possible player actions: `hit` (draw a new card) and `stand` (do not draw a new card). By running a large number of simulated games (`N_SIMULATIONS`), the algorithm estimates the probability of winning for each initial game state (player's sum and dealer's upcard) and each possible action.

## Blackjack Rules

Each card has a value. Face cards are worth 10, and Aces can be worth 1 or 11.

The player's goal is to have a hand value closer to 21 than the dealer without exceeding 21 (busting).

The dealer must draw until their hand value is at least 17.

Possible outcomes for the player are Win (1), Lose (0).

- The probability of drawing a card tends to decrease as the player's hand total increases because higher totals are closer to 21, making the risk of going over (busting) higher.
- For smaller hands (e.g., 2–11), the probability of drawing a card is usually higher, as players aim to get closer to 21, while standing is riskier.
- The dealer's visible card has a significant impact on these probabilities: players are more likely to stand when the dealer has a weak card (such as 2–6) and more likely to draw a card when the dealer has a strong card (such as 10 or Ace).

## Data analysis:

- For smaller totals (e.g., 2, 3), the probabilities of drawing a card are higher, which is expected, as the player needs to draw cards to get closer to 21.
- For higher totals (e.g., 17–19), the probability of drawing a card is lower because the risk of going over outweighs the benefit of getting closer to 21.
- The dealer's visible card also influences probabilities, with weaker dealer cards (2–6) leading to a higher probability of standing.

# Monte Carlo Blackjack Simulation

### What is Monte Carlo Simulation?

Monte Carlo simulation is a computational algorithm that relies on repeated random sampling to approximate solutions to problems that are difficult to solve analytically. In this project, it is used to estimate the probability of winning in Blackjack by simulating thousands of games and analyzing the outcomes.

---

## Monte Carlo Blackjack Simulation Workflow

### 1. **Initialization**

- The following data structures are initialized:
  - `probabilites`: Stores the cumulative results of each simulated action (`hit` or `stand`).
  - `number_simulations`: Tracks the number of simulations for each action and game state.
  - `convergence_data`: Records the convergence of probabilities over multiple simulations.

### 2. **Simulation of a Single Blackjack Game**

The function `simulate_blackjack` runs a single game simulation:
1. **Card Dealing**:
   - Randomly select two cards for the player and two for the dealer.
   - Determine the player's initial score (`initial_player_score`) and the dealer's visible card (`initial_show_card`).

2. **Random Action**:
   - Decide randomly whether the player will `hit` or `stand` with a 50% chance for each.

3. **Game Rules**:
   - Implement Blackjack rules (e.g., checking for busts, 21, dealer hitting on soft 17, etc.).
   - Determine the outcome of the game:
     - `1`: Player wins.
     - `0`: Dealer wins.

### 3. **Simulation of Multiple Games**

The function `monte_carlo_blackjack` runs the `simulate_blackjack` function `N_SIMULATIONS` times:
1. **Data Collection**:
   - For each simulation, record:
     - The result (`1` for win, `0` for loss) in `probabilites`.
     - The number of times the action was taken in `number_simulations`.
2. **Probability Approximation**:
   - After all simulations, compute the probability of winning for each action:
     \[
     P(\text{win} | \text{action}) = \frac{\text{number of wins}}{\text{number of simulations}}
     \]
3. **Convergence Tracking**:
   - Append the current probability of winning to `convergence_data` to monitor how probabilities stabilize.

### 4. **Results**
After the simulations, the `probabilites` dictionary contains the estimated probability of winning for each combination of:
- Player's sum.
- Dealer's upcard.
- Player's action (`hit` or `stand`).

---

## How Monte Carlo Simulation Approximates the Probability of Winning

The Monte Carlo algorithm performs a **brute-force exploration** of all possible game states and actions:

1. **Large Number of Simulations**:
   - By simulating a large number of games (`N_SIMULATIONS`), the algorithm gathers a representative sample of possible outcomes for each game state.

2. **Randomness and Exploration**:
   - The random decision to `hit` or `stand` ensures that both strategies are explored under various conditions.

3. **Outcome Averaging**:
   - The fraction of games won for a particular action (`hit` or `stand`) under specific conditions converges to the true probability of winning:
     \[
     P(\text{win} | \text{action}) = \frac{\text{number of wins}}{\text{number of simulations}}
     \]

4. **Convergence**:
   - As the number of simulations increases, the estimated probabilities stabilize and reflect the true win probabilities.

---

## Example of Probability Approximation

Suppose the player starts with a sum of `13` and the dealer's upcard is `6`. The simulation randomly decides whether to `hit` or `stand` in each game, records the outcomes, and computes:

- \( P(\text{win} | \text{hit}) = \frac{\text{wins when hitting}}{\text{times hit}} \)
- \( P(\text{win} | \text{stand}) = \frac{\text{wins when standing}}{\text{times stood}} \)

For example, after 10,000 simulations:
- \( P(\text{win} | \text{hit}) = 0.44 \)
- \( P(\text{win} | \text{stand}) = 0.52 \)

This suggests that standing might be slightly better than hitting in this scenario.

---

## Why Monte Carlo Works for Blackjack

Blackjack is a stochastic (random) game with numerous possible states and outcomes. Monte Carlo simulation is well-suited because:

1. **Exploration of Game Space**:
   - The random sampling captures the variety of possible card draws and dealer/player outcomes.

2. **Approximation Without Full Enumeration**:
   - Exact probabilities would require analyzing every possible card combination and player action, which is computationally infeasible. Monte Carlo provides an efficient approximation.

3. **Convergence to True Probabilities**:
   - As the number of simulations increases, the estimated probabilities converge to the actual win probabilities.

---

## Conclusion

This Monte Carlo simulation allows you to approximate the probabilities of winning in Blackjack under different conditions. By analyzing the results, you can evaluate strategies (e.g., whether to `hit` or `stand`) based on empirical probabilities, offering insight into optimal decision-making for this stochastic game.

# Monte Carlo Tree Search (MCTS)

### Overview

This implementation uses Monte Carlo Tree Search (MCTS) to determine the optimal move in a simplified game of Blackjack. The algorithm explores the decision tree of possible moves (Hit or Stand) to maximize the expected reward while adhering to Blackjack rules.

![mcts_own](https://github.com/user-attachments/assets/6ac45e09-8568-453e-9afe-73e35bd12b42)

MCTS relies on a heuristic called Upper Confidence Bounds for Trees (UCT) to balance two critical aspects of decision-making:

- Exploitation: Favoring nodes with high average rewards.
- Exploration: Considering nodes with fewer visits to discover potentially better outcomes.

![CodeCogsEqn-8](https://github.com/user-attachments/assets/3265a7c9-e3df-4cb3-8eb9-f635d08cc32b)


Where:
```math
s_i = \text{value of node } i
```
```math
x_i = \text{empirical mean of a node } i
```
```math
c = \text{exploitation constant (usually, in practice, is used 2 or rad(2), or it is tested for best results)}
```
```math
t = \text{total number of simulations}
```


This algorithm is based on rollouts. For every rollout, the game continues until it reaches a final state (either player wins, dealer wins or draw). The result is then used to compute the value of the nodes (states) from the tree, so the nodes will be chosen based on that value in the future.
