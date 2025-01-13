import numpy as np
import matplotlib.pyplot as plt

N_SIMULATIONS = 10**6

probabilites = {
    score: {upcard: {'hit': 0, 'stand': 0} 
            for upcard in range(1, 11)
        } for score in range(2, 22)
}

number_simulations = {
    score: {upcard: {'hit': 0, 'stand': 0} 
            for upcard in range(1, 11)
        } for score in range(2, 22)
}

def find_best_score(score):
    #in case we have an ace, we can use it as 1 or 11
    score_1 = score
    score_11 = score + 10
    if score_11 <= 21:
        return score_11
    return score_1


def simulate_blackjack():
    cards = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4)
    chosen_indexes = np.random.choice(range(len(cards)), size=4, replace=False)
    player_hand = cards[chosen_indexes[:2]]
    dealer_hand = cards[chosen_indexes[2:]]
    
    cards = np.delete(cards, chosen_indexes, axis=0)
    dealer_score = np.sum(dealer_hand)
    player_score = np.sum(player_hand)
    initial_player_score = player_score
    initial_show_card = dealer_hand[0]
    action = 'stand'
    is_a_win = -1   # -1 = not decided, 0 = dealer wins, 1 = player wins

    if 1 in dealer_hand and find_best_score(dealer_score) == 21:
        is_a_win = 0
    elif 1 in player_hand and  find_best_score(player_score) == 21:
        is_a_win = 1 
    else:
        #we will choose either to hit or to stand with a probability of 50%
        if np.random.random() < 0.5:
            action = 'hit'
            
            chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
            player_hand = np.append(player_hand, cards[chosen_index])
            player_score += cards[chosen_index]
            cards = np.delete(cards, chosen_index, axis=0)
            
            if 1 in player_hand:
                player_score = find_best_score(player_score)

            if player_score > 21:
                is_a_win = 0
            elif player_score == 21:
                is_a_win = 1
        
        while is_a_win == -1:

            if dealer_score < 17: 
                #dealer needs to hit
                chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
                dealer_hand = np.append(dealer_hand, cards[chosen_index])
                dealer_score += cards[chosen_index]
                cards = np.delete(cards, chosen_index, axis=0) 

                if 1 in dealer_hand:
                    dealer_score = find_best_score(dealer_score)
                
                if dealer_score > 21:
                    is_a_win = 0
                elif dealer_score == 21:
                    is_a_win = 1
            else:
                if dealer_score >= player_score:
                    is_a_win = 0
                else:
                    is_a_win = 1
                
    return is_a_win, initial_player_score, initial_show_card, action

def monte_carlo_blackjack(n_simulations):
    for i in range(n_simulations):
        print(i)
        result, initial_player_score, initial_show_card, action = simulate_blackjack()
        probabilites[initial_player_score][initial_show_card][action] += result
        number_simulations[initial_player_score][initial_show_card][action] += 1
    
    for score in probabilites.keys():
        for upcard in probabilites[score].keys():
            for act in ['hit', 'stand']:
                    if number_simulations[score][upcard][act] > 0:
                        prob = probabilites[score][upcard][act] / number_simulations[score][upcard][act]
                        probabilites[score][upcard][act] = prob

    return probabilites
    
if __name__ == "__main__":
    probabilities = monte_carlo_blackjack(N_SIMULATIONS)
    #print(probabilites)

    with open('results.txt', 'w') as file:
        for score in range(2, 21):
            file.write(f"Player's Score: {score}\n")
            for upcard in range(1, 11):
                hit_prob = probabilites[score][upcard]['hit']
                stand_prob = probabilites[score][upcard]['stand']
                file.write(f"  Dealer Upcard: {upcard} | Hit Probability: {100*hit_prob:.1f}% | Stand Probability: {100*stand_prob:.1f}% | Win Probability: {(100*hit_prob)+(100*stand_prob):.1f}%\n")
            file.write("\n\n")
    
