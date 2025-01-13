import random
import math
from graphviz import Digraph

## DEBUGGING PURPOSES
## import os
## os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz-12.2.1-win64/bin/'

CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  

def hand_value(hand):
    value = sum(CARD_VALUES[card] for card in hand)
    if 1 in hand and value + 10 <= 21: 
        value += 10
    return value

def is_bust(hand):
    return hand_value(hand) > 21

def blackjack_result(player_hand, dealer_hand):
    player_value = hand_value(player_hand)
    dealer_value = hand_value(dealer_hand)
    if is_bust(player_hand):
        return -1  
    if is_bust(dealer_hand):
        return 1
    if player_value > dealer_value:
        return 1 
    if player_value < dealer_value:
        return -1  
    return 0  

def dealer_play(dealer_hand):
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(random.randint(0, 12))
    return dealer_hand

class MCTSNode:
    def __init__(self, player_hand, dealer_hand, parent=None, move_from_parent=None, player_stands=False):
        self.player_hand = player_hand[:]
        self.dealer_hand = dealer_hand[:]
        self.parent = parent
        self.move_from_parent = move_from_parent
        self.player_stands = player_stands
        self.children = []
        self.untried_moves = [0, 1] 
        self.visits = 0
        self.total_value = 0.0

    def is_terminal(self):
        return is_bust(self.player_hand) or self.player_stands

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c=1.41):
        best_node = None
        best_ucb = float('-inf')
        for child in self.children:
            if child.visits == 0:
                ucb = float('inf')
            else:
                avg = child.total_value / child.visits
                explore = c * math.sqrt(2.0 * math.log(self.visits) / child.visits)
                ucb = avg + explore

            if ucb > best_ucb:
                best_ucb = ucb
                best_node = child
        return best_node

    def add_child(self, move_id, player_hand_after_move, player_stands):
        child = MCTSNode(
            player_hand_after_move, 
            self.dealer_hand, 
            parent=self, 
            move_from_parent=move_id, 
            player_stands=player_stands
        )
        self.children.append(child)
        self.untried_moves.remove(move_id)
        return child

    def update(self, value):
        self.visits += 1
        self.total_value += value

def tree_policy(node, c=1.41):
    while not node.is_terminal():
        if not node.is_fully_expanded():
            return expand(node)
        node = node.best_child(c)
    return node

def expand(node):
    move_id = random.choice(node.untried_moves)
    if move_id == 0:  
        new_hand = node.player_hand[:]
        new_hand.append(random.randint(0, 12))
        return node.add_child(move_id, new_hand, player_stands=False)
    elif move_id == 1:  
        return node.add_child(move_id, node.player_hand, player_stands=True)

def default_policy(player_hand, dealer_hand, player_stands):
    if player_stands:
        dealer_hand = dealer_play(dealer_hand)
    return blackjack_result(player_hand, dealer_hand)

def backup(node, value):
    while node is not None:
        node.update(value)
        node = node.parent

def mcts_blackjack(player_hand, dealer_hand, iterations=1000, c=1.41):
    root = MCTSNode(player_hand, dealer_hand)
    for _ in range(iterations):
        leaf = tree_policy(root, c)
        value = default_policy(leaf.player_hand, leaf.dealer_hand, leaf.player_stands)
        backup(leaf, value)

    best_child_node = root.best_child(c=0) 
    tree_visualization = visualize_tree(root)
    tree_visualization.render("proiect-ps/mcts_tree.png", format="png", cleanup=True)  # Saves as 'mcts_tree.png'
    tree_visualization                
    return best_child_node.move_from_parent if best_child_node else None

def draw_card():
    card = random.randint(1, 10)
    return card

def visualize_tree(root, max_nodes=4000):
    dot = Digraph(comment="MCTS Tree")
    def make_label(node):
        label = f"Visits: {node.visits}\nValue: {node.total_value:.2f}"
        if node.move_from_parent is not None:
            label += f"\nMove: {node.move_from_parent}"
        return label

    node_id_map = {}
    node_id_map[root] = 0
    dot.node("0", label=make_label(root))

    current_layer = [root]
    layer = 0

    while current_layer and len(node_id_map) < max_nodes:
        next_layer_candidates = []
        for node in current_layer:
            for child in node.children:
                if len(node_id_map) >= max_nodes:
                    break
                if child not in node_id_map:
                    if child.visits > 0:
                        metric = child.total_value / child.visits
                    else:
                        metric = 0.0  

                    parent_id = node_id_map[node]
                    next_layer_candidates.append((child, parent_id, metric))
        
        if not next_layer_candidates:
            break

        next_layer_candidates.sort(key=lambda x: x[2], reverse=True)
        next_layer_candidates = next_layer_candidates[:16]

        next_layer = []
        for child, parent_id, metric in next_layer_candidates:
            if child not in node_id_map:
                new_id = len(node_id_map)
                node_id_map[child] = new_id
                dot.node(str(new_id), label=make_label(child))
                dot.edge(str(parent_id), str(new_id))
                next_layer.append(child)
            else:
                child_id = node_id_map[child]
                dot.edge(str(parent_id), str(child_id))
        
        current_layer = next_layer
        layer += 1

    return dot

if __name__ == "__main__":
    random.seed() 
    
    player_hand = [draw_card(), draw_card()]
    dealer_hand = [draw_card()]
    
    print("Player Hand:", player_hand)
    print("Dealer Hand:", dealer_hand)
    
    best_move = mcts_blackjack(player_hand, dealer_hand, iterations=2000)
    moves = {0: "HIT", 1: "STAND"}
    print("Recommended Move:", moves.get(best_move, "NONE"))
