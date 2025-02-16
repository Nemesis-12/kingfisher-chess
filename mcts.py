import random
import math
import time

class MCTSNode(object):
    def __init__(self, board, parent=None, move=None):
        self.board = board.copy()
        self.parent = parent
        self.move = move
        self.wins = 0
        self.visits = 0
        self.children = []
        self.unvisited_moves = list(board.legal_moves)

    def is_expanded_node(self):
        return len(self.unvisited_moves) == 0
    
    def uct(self, child, c=1.5):
        if child.visits == 0:
            return float('inf')
        return (child.wins / child.visits) + (c * math.sqrt(math.log(self.visits) / child.visits))
    
    def best_child(self):
        best_score = float('-inf')
        best_child_node = None

        for child in self.children:
            score = self.uct(child)

            if score > best_score:
                best_score = score
                best_child_node = child
        
        return best_child_node
    
    def expand(self):
        move = self.unvisited_moves.pop(random.randrange(len(self.unvisited_moves)))
        self.board.push(move)
        child_node = MCTSNode(self.board, parent=self, move=move)
        self.board.pop()
        self.children.append(child_node)
        return child_node

class MCTS(object):
    def __init__(self, max_time=1.0, c=1.5):
        self.max_time = max_time
        self.c = c
    
    def policy(self, node):
        while not node.board.is_game_over():
            if not node.is_expanded_node():
                return node.expand()
            else:
                node = node.best_child()
        
        return node
    
    def rollout(self, board):
        sim_board = board.copy()

        while not sim_board.is_game_over():
            moves = list(sim_board.legal_moves)
            move = random.choice(moves)
            sim_board.push(move)

        result = sim_board.result()
        if result == "1-0":
            return 1
        elif result == "0-1":
            return -1
        else:
            return 0
        
    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result

            result = -result
            node = node.parent

    def search(self, board):
        start_time = time.time()
        root = MCTSNode(board)

        for _ in range(1000):
            node = self.policy(root)
            reward = self.rollout(node.board)
            self.backpropagate(node, reward)

        most_visits = float('-inf')
        best_child = None
        for child in root.children:
            if child.visits > most_visits:
                most_visits = child.visits
                best_child = child
        
        return best_child.move
        