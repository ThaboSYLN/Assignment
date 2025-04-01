from typing import List, Tuple
from collections import deque
import heapq

# Constants
ODD_POSITIONS = ['A', 'C']
EVEN_POSITIONS = ['B', 'D']
ALL_POSITIONS = ['A', 'B', 'C', 'D', 'E']

class CoinState:
    def __init__(self, num_coins: int):
        self.stacks = {pos: [] for pos in ALL_POSITIONS}
        self.stacks['E'] = list(range(num_coins, 0, -1))  # Coins in descending order
    
    def __str__(self):
        return ' | '.join(f"{pos}: {stack}" for pos, stack in self.stacks.items())
    
    def __lt__(self, other):
        return False

    def is_valid_move(self, from_pos: str, to_pos: str) -> bool:
        if not self.stacks[from_pos]:
            return False
        if to_pos == from_pos: 
            return False

        moving_coin = self.stacks[from_pos][-1] 
        if moving_coin % 2 != 0 and to_pos not in ODD_POSITIONS + ['E']:
            return False
        if moving_coin % 2 == 0 and to_pos not in EVEN_POSITIONS + ['E']:
            return False
        if self.stacks[to_pos]:
            top_coin = self.stacks[to_pos][-1]
            if moving_coin > top_coin:
                return False
            if (moving_coin % 2 != top_coin % 2) and to_pos != 'E':
                return False

        return True

    def move(self, from_pos: str, to_pos: str) -> 'CoinState':
        new_state = CoinState(0)  # Create a new state
        new_state.stacks = {pos: stack.copy() for pos, stack in self.stacks.items()}
        coin = new_state.stacks[from_pos].pop()
        new_state.stacks[to_pos].append(coin)
        return new_state

    def is_goal(self) -> bool:
        for pos in ODD_POSITIONS + EVEN_POSITIONS:
            if not self.stacks[pos]:
                continue
            if pos in ODD_POSITIONS and any(coin % 2 == 0 for coin in self.stacks[pos]):
                return False
            if pos in EVEN_POSITIONS and any(coin % 2 != 0 for coin in self.stacks[pos]):
                return False
        return len(self.stacks['E']) == 0

def get_valid_moves(state: CoinState) -> List[Tuple[str, str]]:
    moves = []
    for from_pos in ALL_POSITIONS:
        for to_pos in ALL_POSITIONS:
            if state.is_valid_move(from_pos, to_pos):
                moves.append((from_pos, to_pos))
    return moves

def heuristic(state: CoinState) -> int:
    # Heuristics determination such that we count misplaced coins 
    misplaced = 0
    for pos, stack in state.stacks.items():
        if pos in ODD_POSITIONS:
            misplaced += sum(1 for coin in stack if coin % 2 == 0)
        elif pos in EVEN_POSITIONS:
            misplaced += sum(1 for coin in stack if coin % 2 != 0)
        elif pos == 'E':
            misplaced += len(stack)
    return misplaced

def dfs(initial_state: CoinState) -> List[Tuple[str, str]]:
    stack = [(initial_state, [])]
    visited = set()

    while stack:
        state, path = stack.pop()
        if state.is_goal():
            return path
        
        state_str = str(state)
        if state_str in visited:
            continue
        visited.add(state_str)

        for move in get_valid_moves(state):
            new_state = state.move(*move)
            stack.append((new_state, path + [move]))

    return None

def bfs(initial_state: CoinState) -> List[Tuple[str, str]]:
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        state, path = queue.popleft()
        if state.is_goal():
            return path
        
        state_str = str(state)
        if state_str in visited:
            continue
        visited.add(state_str)

        for move in get_valid_moves(state):
            new_state = state.move(*move)
            queue.append((new_state, path + [move]))

    return None

def greedy_best_first(initial_state: CoinState) -> List[Tuple[str, str]]:
    heap = [(heuristic(initial_state), initial_state, [])]
    visited = set()

    while heap:
        _, state, path = heapq.heappop(heap)
        if state.is_goal():
            return path
        
        state_str = str(state)
        if state_str in visited:
            continue
        visited.add(state_str)

        for move in get_valid_moves(state):
            new_state = state.move(*move)
            heapq.heappush(heap, (heuristic(new_state), new_state, path + [move]))

    return None

def astar(initial_state: CoinState) -> List[Tuple[str, str]]:
    heap = [(0 + heuristic(initial_state), 0, initial_state, [])]
    visited = set()

    while heap:
        _, g, state, path = heapq.heappop(heap)
        if state.is_goal():
            return path
        
        state_str = str(state)
        if state_str in visited:
            continue
        visited.add(state_str)

        for move in get_valid_moves(state):
            new_state = state.move(*move)
            new_g = g + 1
            heapq.heappush(heap, (new_g + heuristic(new_state), new_g, new_state, path + [move]))

    return None


def main():
    #(4(Coins(4,3,2,1)), 6(Coins(6,5,4,3,2,1)), 8(Coins(8,7,6,5,4,3,2,1)), or 10(Coins(10,9,8,7,6,54,3,2,1))):
    num_coins = int(input("Enter number of coins (4(Coins(4,3,2,1)), 6(Coins(6,5,4,3,2,1)), 8(Coins(8,7,6,5,4,3,2,1)), or 10(Coins(10,9,8,7,6,54,3,2,1))): "))
    if num_coins not in [4, 6, 8, 10]:
        print("Invalid number of coins. Please choose 4, 6, 8, or 10.")
        return

    initial_state = CoinState(num_coins)
    
    print("\nChoose an algorithm:")
    print("1. Depth-first search")
    print("2. Breadth-first search")
    print("3. Greedy best-first search")
    print("4. A* search")
    choice = int(input("Enter your choice (1-4): "))
    
    algorithms = {
        1: ("Depth-first search", dfs),
        2: ("Breadth-first search", bfs),
        3: ("Greedy best-first search", greedy_best_first),
        4: ("A* search", astar)
    }
    
    if choice not in algorithms:
        print("Invalid choice")
        return
    
    algo_name, algo_func = algorithms[choice]
    print(f"\nSolving with {algo_name}...")
    solution = algo_func(initial_state)
    
    if solution:
        print(f"\nSolution found in {len(solution)} moves:")
        current_state = initial_state
        print(f"Initial state: {current_state}")
        for i, (from_pos, to_pos) in enumerate(solution, 1):
            current_state = current_state.move(from_pos, to_pos)
            print(f"Move {i}: {from_pos} -> {to_pos}")
            print(f"State: {current_state}")
    else: 
        print("No solution found")

if __name__ == "__main__":
    main()
