# Blackjack_Monte_Carlo_Simulation

## Blackjack Rules

Each card has a value. Face cards are worth 10, and Aces can be worth 1 or 11.

The player's goal is to have a hand value closer to 21 than the dealer without exceeding 21 (busting).

The dealer must draw until their hand value is at least 17.

Possible outcomes for the player are Win (+1), Lose (-1), or Draw (0).

- The probability of drawing a card tends to decrease as the player's hand total increases because higher totals are closer to 21, making the risk of going over (busting) higher.
- For smaller hands (e.g., 2–11), the probability of drawing a card is usually higher, as players aim to get closer to 21, while standing is riskier.
- The dealer's visible card has a significant impact on these probabilities: players are more likely to stand when the dealer has a weak card (such as 2–6) and more likely to draw a card when the dealer has a strong card (such as 10 or Ace).

## Data analysis:

- For smaller totals (e.g., 2, 3), the probabilities of drawing a card are higher, which is expected, as the player needs to draw cards to get closer to 21.
- For higher totals (e.g., 17–19), the probability of drawing a card is lower because the risk of going over outweighs the benefit of getting closer to 21.
- The dealer's visible card also influences probabilities, with weaker dealer cards (2–6) leading to a higher probability of standing.


## Monte Carlo Tree Search (MCTS)

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

