import numpy as np
import matplotlib.pyplot as plt
N_SIMULATIONS = 100000
probabilites = {
    sum_: {upcard: {'hit': 0, 'stand': 0} for upcard in range(1, 11)} for sum_ in range(2, 22)
}
number_simulations = {
    sum_: {upcard: {'hit': 0, 'stand': 0} for upcard in range(1, 11)} for sum_ in range(2, 22)
}
convergence_data = {
    sum_: {upcard: {'hit': [], 'stand': []} for upcard in range(1, 11)} for sum_ in range(2, 22)
}
def simulate_blackjack():
    cards = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4)
    chosen_indexes = np.random.choice(range(len(cards)), size=4, replace=False)
    player_hand = cards[chosen_indexes[:2]]
    dealer_hand = cards[chosen_indexes[2:]]
    
    cards = np.delete(cards, chosen_indexes, axis=0) # scoatem cartile alese din pachet
    initial_player_score = np.sum(player_hand)
    initial_show_card = dealer_hand[0]
    hit = np.random.random() < 0.5 # luam o carte de jos
    action = 'hit' if hit else 'stand'

    if initial_player_score == 11 and 1 in player_hand:
        return 1, initial_player_score, initial_show_card, action
    if hit:
        chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
        player_hand = np.append(player_hand, cards[chosen_index])
        new_player_score = cards[chosen_index] + initial_player_score
        cards = np.delete(cards, chosen_index, axis=0)
        if new_player_score > 21:
            return 0, initial_player_score, initial_show_card, action
        elif new_player_score == 21:
            return 1, initial_player_score, initial_show_card, action
        elif 1 in player_hand and new_player_score + 10 == 21:
            return 1, initial_player_score, initial_show_card, action 
    if np.sum(dealer_hand) == 11 and 1 in dealer_hand:
        return 0, initial_player_score, initial_show_card, action
    while True:
        if 1 in dealer_hand and 17 <= np.sum(dealer_hand) + 10 <= 21:
            if np.sum(dealer_hand) + 10 >= np.sum(player_hand):
                return 0, initial_player_score, initial_show_card, action # castiga dealer
            return 1, initial_player_score, initial_show_card, action
        elif np.sum(dealer_hand) < 17: # dealer mai trage o carte
            chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
            dealer_hand = np.append(dealer_hand, cards[chosen_index])
            cards = np.delete(cards, chosen_index, axis=0)
        elif np.sum(dealer_hand) > 21:
            return 1, initial_player_score, initial_show_card, action
        else:
            if np.sum(dealer_hand) >= np.sum(player_hand):
                return 0, initial_player_score, initial_show_card, action
            return 1, initial_player_score, initial_show_card, action

def monte_carlo_blackjack(n_simulations):
    for _ in range(n_simulations):
        results, initial_player_score, initial_show_card, action = simulate_blackjack()
        probabilites[initial_player_score][initial_show_card][action] += results 
        number_simulations[initial_player_score][initial_show_card][action] += 1
    for sum in probabilites.keys():
        for upcard in probabilites[sum].keys():
            for act in ['hit', 'stand']:
                    if number_simulations[sum][upcard][act] > 0:
                        prob = probabilites[sum][upcard][act] / number_simulations[sum][upcard][act]
                        probabilites[sum][upcard][act] = prob
                        convergence_data[sum][upcard][act].append(prob)

    return probabilites
    
if __name__ == "__main__":
    probabilities = monte_carlo_blackjack(N_SIMULATIONS)
    print(probabilites)


for sum in range(2, 21):
    print(f"Player's Sum: {sum}")
    for upcard in range(1, 11):
        hit_prob = probabilites[sum][upcard]['hit']
        stand_prob = probabilites[sum][upcard]['stand']
        print(f"  Dealer Upcard: {upcard} | Hit Probability: {hit_prob:.4f} | Stand Probability: {stand_prob:.4f}")
    print("\n")
    
