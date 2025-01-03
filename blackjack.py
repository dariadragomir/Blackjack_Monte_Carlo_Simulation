import numpy as np
import matplotlib.pyplot as plt
N_SIMULATIONS = 1000000
initial_show_card = None
initial_player_score = None
action = None
probabilites = {sum:{upcard: {'hit':0, 'stand':0} for upcard in range(1, 11)} for sum in range(2, 22)}
number_simulations = {sum:{upcard: {'hit':0, 'stand':0} for upcard in range(1, 11)} for sum in range(2, 22)}
def simulate_blackjack():
    cards = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])
    chosen_indexes = np.random.choice(range(len(cards)), size=4, replace=False)
    player_hand = cards[chosen_indexes[:2]]
    dealer_hand = cards[chosen_indexes[2:]]
    
    cards = np.delete(cards, chosen_indexes, axis=0) # scoatem cartile alese din pachet
    initial_player_score = np.sum(player_hand)
    initial_show_card = dealer_hand[0]
    hit = np.random.random() < 0.5 # luam o carte de jos
    if hit:
        action = 'hit'
    else:
        action = 'stand' 
    if initial_player_score == 11 and 1 in player_hand:
        return 1, initial_player_score, initial_show_card, action
    if hit:
        chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
        player_hand = np.append(player_hand, cards[chosen_index])
        cards = np.delete(cards, chosen_index, axis=0)
        new_player_score = np.sum(player_hand)
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
            if number_simulations[sum][upcard]['hit'] > 0:
                probabilites[sum][upcard]['hit'] /= number_simulations[sum][upcard]['hit']
            if number_simulations[sum][upcard]['stand'] > 0:
                probabilites[sum][upcard]['stand'] /= number_simulations[sum][upcard]['stand']

    return probabilites

probabilities = monte_carlo_blackjack(N_SIMULATIONS)
print(probabilites)
