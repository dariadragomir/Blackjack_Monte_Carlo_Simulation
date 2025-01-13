import seaborn as sns
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

N_SIMULATIONS = 10**6

probabilities = {
    score: {
        upcard: {
            'hit': {'wins': 0, 'losses': 0, 'ties': 0, 'total': 0},
            'stand': {'wins': 0, 'losses': 0, 'ties': 0, 'total': 0}
        }
        for upcard in range(1, 11)
    }
    for score in range(2, 22)
}

def find_best_score(score):
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
    result = 0  # 1 = win, 0 = tie, -1 = loss

    if 1 in dealer_hand and find_best_score(dealer_score) == 21:
        result = -1
    elif 1 in player_hand and find_best_score(player_score) == 21:
        result = 1
    else:
        while np.random.random() < 0.5: 
            action = 'hit'
            chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
            player_hand = np.append(player_hand, cards[chosen_index])
            player_score += cards[chosen_index]
            cards = np.delete(cards, chosen_index, axis=0)
            
            if 1 in player_hand:
                player_score = find_best_score(player_score)

            if player_score > 21:
                result = -1
                break
            elif player_score == 21:
                result = 1
                break
        
        if result == 0:  
            while dealer_score < 17:
                chosen_index = np.random.choice(range(len(cards)), size=1, replace=False)
                dealer_hand = np.append(dealer_hand, cards[chosen_index])
                dealer_score += cards[chosen_index]
                cards = np.delete(cards, chosen_index, axis=0)
                
                if 1 in dealer_hand:
                    dealer_score = find_best_score(dealer_score)
            
            if dealer_score > 21:
                result = 1
            elif dealer_score == player_score:
                result = 0
            elif dealer_score > player_score:
                result = -1
            else:
                result = 1
    
    return result, initial_player_score, initial_show_card, action


def monte_carlo_blackjack(n_simulations):
    for _ in range(n_simulations):
        result, initial_score, dealer_upcard, action = simulate_blackjack()
        probabilities[initial_score][dealer_upcard][action]['total'] += 1
        if result == 1:
            probabilities[initial_score][dealer_upcard][action]['wins'] += 1
        elif result == -1:
            probabilities[initial_score][dealer_upcard][action]['losses'] += 1
        else:
            probabilities[initial_score][dealer_upcard][action]['ties'] += 1

    for score in probabilities:
        for upcard in probabilities[score]:
            for action in ['hit', 'stand']:
                data = probabilities[score][upcard][action]
                if data['total'] > 0:
                    data['win_prob'] = data['wins'] / data['total']
                    data['loss_prob'] = data['losses'] / data['total']
                    data['tie_prob'] = data['ties'] / data['total']
    return probabilities


def plot_probabilities(probabilities):
    scores = list(range(2, 22))
    upcards = range(1, 11)

    for upcard in upcards:
        hit_probs = [probabilities[score][upcard]['hit'].get('win_prob', 0) for score in scores]
        stand_probs = [probabilities[score][upcard]['stand'].get('win_prob', 0) for score in scores]

        plt.plot(scores, hit_probs, label=f"Hit (Upcard {upcard})")
        plt.plot(scores, stand_probs, label=f"Stand (Upcard {upcard})", linestyle='--')

    plt.xlabel("Player's Initial Score")
    plt.ylabel("Win Probability")
    plt.title("Win Probabilities for Hit vs Stand")
    plt.legend()
    plt.show()


def analyze_score_distribution():
    player_scores = []
    dealer_scores = []
    
    for _ in range(10000):  
        _, initial_player_score, initial_show_card, _ = simulate_blackjack()
        player_scores.append(initial_player_score)
    
    sns.histplot(player_scores, kde=True, bins=np.arange(2, 23) - 0.5, color='blue', label="Player Scores")
    
    mu, sigma = norm.fit(player_scores)
    x = np.linspace(min(player_scores), max(player_scores), 100)
    plt.plot(x, norm.pdf(x, mu, sigma), 'r-', label=f"Fit: μ={mu:.2f}, σ={sigma:.2f}")
    
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.title("Distribution of Player Scores")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    probabilities = monte_carlo_blackjack(N_SIMULATIONS)

    with open('results.txt', 'w') as file:
        for score in range(2, 22):
            file.write(f"Player's Score: {score}\n")
            for upcard in range(1, 11):
                hit_data = probabilities[score][upcard]['hit']
                stand_data = probabilities[score][upcard]['stand']
                file.write(f"  Dealer Upcard: {upcard} | "
                           f"Hit Win: {100*hit_data.get('win_prob', 0):.1f}% | "
                           f"Stand Win: {100*stand_data.get('win_prob', 0):.1f}%\n")
            file.write("\n\n")

    plot_probabilities(probabilities)
    analyze_score_distribution()

