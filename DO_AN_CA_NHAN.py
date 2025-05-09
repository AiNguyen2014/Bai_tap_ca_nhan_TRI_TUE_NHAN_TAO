import sys
import time
import copy
import heapq
import random
import math
import ast
from collections import deque
import sys
sys.setrecursionlimit(2000)

# PyQt5 imports
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLabel, QGridLayout, 
                          QWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QFrame, 
                          QTabWidget, QSpinBox, QComboBox, QTextEdit)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

# Định nghĩa trạng thái đích
goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]  # 0 đại diện cho ô trống
]

class Node:
    def __init__(self, state, parent=None, move=None, depth=0, action_cost=1, cost=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.action_cost = action_cost  # Đặt chi phí hành động (mặc định là 1)
        self.cost = cost 
        self.depth = parent.depth + 1 if parent else 0  # Độ sâu của node
    
    def __lt__(self, other):
        # So sánh dựa trên chi phí
        return self.cost < other.cost

    def __repr__(self):
        return f"Node(state={self.state}, cost={self.cost})"
    
    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
        return -1, -1

    def generate_children(self):
        children = []
        i, j = self.find_blank()
        
        # Các hướng di chuyển: lên, xuống, trái, phải
        moves = [('Lên', -1, 0), ('Xuống', 1, 0), ('Trái', 0, -1), ('Phải', 0, 1)]
        
        for move_name, di, dj in moves:
            ni, nj = i + di, j + dj
            
            # Kiểm tra xem vị trí mới có hợp lệ không
            if 0 <= ni < 3 and 0 <= nj < 3:
                # Tạo trạng thái mới bằng cách hoán đổi ô trống với ô kế
                new_state = copy.deepcopy(self.state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                
                # Tính chi phí cho hành động này (mỗi hành động có thể có chi phí là 1)
                new_cost = self.cost + 1  # Nếu mỗi bước di chuyển có chi phí bằng 1

                # Tạo node con mới
                child = Node(new_state, self, move_name, self.depth + 1, new_cost)
                children.append(child)
        
        return children

    def __eq__(self, other):
        return self.state == other.state

def solve_puzzle_dfs(initial_state, max_depth=50):
    # Tạo node gốc
    initial_node = Node(initial_state)
    
    # Nếu trạng thái ban đầu đã là đích
    if initial_node.state == goal_state:
        return [initial_node], 0
    
    # Stack để DFS
    stack = [initial_node]
    
    # Tập hợp các trạng thái đã thăm
    visited = set()
    
    # Chuyển trạng thái ban đầu thành chuỗi để lưu vào tập visited
    visited.add(str(initial_node.state))
    
    # Số bước đã duyệt
    steps_explored = 0
    
    # Bắt đầu thuật toán DFS
    while stack:
        # Lấy node từ đỉnh của stack
        current_node = stack.pop()
        steps_explored += 1
        
        # Bỏ qua các node có độ sâu vượt quá giới hạn
        if current_node.depth >= max_depth:
            continue
        
        # Sinh ra các node con
        for child in current_node.generate_children():
            # Chuyển trạng thái child thành chuỗi
            child_state_str = str(child.state)
            
            # Nếu trạng thái này chưa được thăm
            if child_state_str not in visited:
                # Nếu đây là trạng thái đích, trả về đường đi
                if child.state == goal_state:
                    # Tạo đường đi từ gốc đến đích
                    path = []
                    current = child
                    while current:
                        path.append(current)
                        current = current.parent
                    return path[::-1], steps_explored  # Đảo ngược đường đi
                
                # Thêm trạng thái vào tập visited
                visited.add(child_state_str)
                
                # Thêm node vào đầu stack
                stack.append(child)
    
    # Nếu không tìm thấy đường đi
    return None, steps_explored

def solve_puzzle_bfs(initial_state):
    # Tạo node gốc
    initial_node = Node(initial_state)
    
    # Nếu trạng thái ban đầu đã là đích
    if initial_node.state == goal_state:
        return [initial_node], 0
    
    # Queue để BFS
    queue = deque([initial_node])
    
    # Tập hợp các trạng thái đã thăm
    visited = set()
    
    # Chuyển trạng thái ban đầu thành chuỗi để lưu vào tập visited
    visited.add(str(initial_node.state))
    
    # Số bước đã duyệt
    steps_explored = 0
    
    # Bắt đầu thuật toán BFS
    while queue:
        # Lấy node từ đầu queue
        current_node = queue.popleft()
        steps_explored += 1
        
        # Sinh ra các node con
        for child in current_node.generate_children():
            # Chuyển trạng thái child thành chuỗi
            child_state_str = str(child.state)
            
            # Nếu trạng thái này chưa được thăm
            if child_state_str not in visited:
                # Nếu đây là trạng thái đích, trả về đường đi
                if child.state == goal_state:
                    # Tạo đường đi từ gốc đến đích
                    path = []
                    current = child
                    while current:
                        path.append(current)
                        current = current.parent
                    return path[::-1], steps_explored  # Đảo ngược đường đi
                
                # Thêm trạng thái vào tập visited
                visited.add(child_state_str)
                
                # Thêm node vào cuối queue
                queue.append(child)
    
    # Nếu không tìm thấy đường đi
    return None, steps_explored

def heuristic(state):
    """Hàm đánh giá heuristic - số ô sai vị trí"""
    cost = 0 
    for i in range(3):
        for j in range(3):
            #Duyệt toàn bộ bảng, nếu vị trí trạng thái không phải trạng thái đích thì tăng cost lên 1
            if state[i][j] != 0 and state[i][j] != goal_state[i][j]:
                cost += 1
    return cost

def greedy_search(initial_state):
    """Thuật toán Greedy Best-First Search"""
    initial_node = Node(initial_state)
    counter = 0
    visited = set()
    heap = [(heuristic(initial_node.state), counter, initial_node)]
    
    while heap:
        _, _, current_node = heapq.heappop(heap)
        
        if current_node.state == goal_state:
            path = []
            node = current_node
            while node:
                path.append(node)
                node = node.parent
            return path[::-1], len(visited)
        
        visited.add(str(current_node.state))
        
        for child in current_node.generate_children():
            if str(child.state) not in visited:
                counter += 1
                heapq.heappush(heap, (heuristic(child.state), counter, child))
    
    return None, len(visited)

def uniform_cost_search(initial_state):
    # Khởi tạo frontier và visited
    frontier = []
    visited = set()

    # Khởi tạo node ban đầu
    initial_node = Node(initial_state, cost=0)  # Đảm bảo rằng node ban đầu có chi phí là 0
    heapq.heappush(frontier, (initial_node.cost, id(initial_node), initial_node))  # frontier chứa tuple (cost, id(node),node)

    steps = 0 #Đếm số bước đã duyệt

    while frontier:
        #Lấy node có chi phí thấp nhất từ frontier
        cost, _,  current_node = heapq.heappop(frontier)
        steps += 1

        # Nếu đã đạt được trạng thái đích, tiến hành truy vết đường đi
        if current_node.state == goal_state:
            path = []
            node = current_node
            while node: #Truy vết đường đi từ đích về gốc
                path.append(node)
                node = node.parent
            return path[::-1], steps  # Trả lại đường đi và số bước

        # Thêm trạng thái của node hiện tại vào visited (chuyển list thành tuple để có thể thêm vào set)
        visited.add(tuple(map(tuple, current_node.state)))  # Chuyển state từ list thành tuple

        # Mở rộng node và kiểm tra các node con
        for child in current_node.generate_children():

            # Kiểm tra xem trạng thái của child đã được thăm chưa
            if tuple(map(tuple, child.state)) not in visited:
                # Tính chi phí cho child (có thể là cost của cha + chi phí cố định 1 cho mỗi bước di chuyển)
                child_cost = current_node.cost + 1  # Mỗi hành động có chi phí cố định là 1
                child.cost = child_cost  # Cập nhật chi phí cho node co
                
                #Thêm node con vào frontier với chi phí làm ưu tiên s
                heapq.heappush(frontier, (child.cost, id(child), child))  # Thêm node con vào frontier

    return None, steps  # Không tìm thấy đường đi

def solve_puzzle_ids(initial_state, max_depth_limit=50):
    """Thuật toán Iterative Deepening Search"""
    total_steps_explored = 0
    for depth in range(max_depth_limit + 1):  # Tăng độ sâu từ 0 đến max_depth_limit
        path, steps = solve_puzzle_dfs(initial_state, depth)
        total_steps_explored += steps
        if path is not None:  # Nếu tìm thấy đường đi, trả về
            return path, total_steps_explored
    return None, total_steps_explored  # Không tìm thấy trong giới hạn

def solve_puzzle_astar(initial_state):
    initial_node = Node(initial_state, cost=0)
    frontier = [(heuristic(initial_node.state), id(initial_node), initial_node)]  # f(n) = g(n) + h(n)
    visited = set()
    steps_explored = 0
    
    while frontier:
        f_cost, _, current_node = heapq.heappop(frontier)
        steps_explored += 1
        state_str = str(current_node.state)
        
        if current_node.state == goal_state:
            path = []
            node = current_node
            while node:
                path.append(node)
                node = node.parent
            return path[::-1], steps_explored
        
        if state_str not in visited:
            visited.add(state_str)
            for child in current_node.generate_children():
                if str(child.state) not in visited:
                    f_child = child.cost + heuristic(child.state)  # f(n) = g(n) + h(n)
                    heapq.heappush(frontier, (f_child, id(child), child))
    
    return None, steps_explored

def solve_puzzle_idastar(initial_state, max_cost_limit=50):
    def dfs_with_cost_limit(node, cost_limit, visited, steps_explored_ref):
        f_cost = node.cost + heuristic(node.state)
        if f_cost > cost_limit:
            return None, f_cost

        state_key = tuple(map(tuple, node.state))
        if state_key in visited:
            return None, float('inf')
        visited.add(state_key)

        steps_explored_ref[0] += 1

        if node.state == goal_state:
            path = []
            while node:
                path.append(node)
                node = node.parent
            return path[::-1], f_cost

        min_over_limit = float('inf')
        for child in node.generate_children():
            child.cost = node.cost + 1  # g(n) tăng thêm mỗi bước
            result, temp_limit = dfs_with_cost_limit(child, cost_limit, visited.copy(), steps_explored_ref)
            if result:
                return result, temp_limit
            min_over_limit = min(min_over_limit, temp_limit)

        return None, min_over_limit

    cost_limit = heuristic(initial_state)
    steps_explored_ref = [0]  # dùng list để truyền tham chiếu
    root = Node(initial_state, cost=0)

    while cost_limit <= max_cost_limit:
        visited = set()
        result, new_limit = dfs_with_cost_limit(root, cost_limit, visited, steps_explored_ref)
        if result:
            return result, steps_explored_ref[0]
        cost_limit = new_limit

    return None, steps_explored_ref[0]


def solve_simple_hill_climbing(initial_state):
    current_node = Node(initial_state)
    steps_explored = 0
    path = [current_node]
    
    while True:
        current_h = heuristic(current_node.state)
        if current_h == 0:  # Đạt trạng thái đích
            return path, steps_explored
        
        children = current_node.generate_children()
        steps_explored += len(children)
        improved = False
        
        for child in children:
            child_h = heuristic(child.state)
            if child_h < current_h:  # Chọn neighbor đầu tiên tốt hơn
                current_node = child
                path.append(child)
                improved = True
                break
        
        if not improved:  # Không còn cải thiện
            return None, steps_explored

def solve_steepest_ascent_hill_climbing(initial_state):
    current_node = Node(initial_state)
    steps_explored = 0
    path = [current_node]
    
    while True:
        current_h = heuristic(current_node.state)
        if current_h == 0:  # Đạt trạng thái đích
            return path, steps_explored
        
        children = current_node.generate_children()
        steps_explored += len(children)
        
        best_child = None
        best_h = current_h
        
        for child in children:  # Tìm neighbor tốt nhất
            child_h = heuristic(child.state)
            if child_h < best_h:
                best_h = child_h
                best_child = child
        
        if best_child is None:  # Không còn cải thiện
            return None, steps_explored 
        
        current_node = best_child
        path.append(best_child)

def solve_stochastic_hill_climbing(initial_state):
    current_node = Node(initial_state)
    steps_explored = 0
    path = [current_node]
    
    while True:
        current_h = heuristic(current_node.state)
        if current_h == 0:  # Đạt trạng thái đích
            return path, steps_explored
        
        children = current_node.generate_children()
        steps_explored += len(children)
        
        better_children = [child for child in children if heuristic(child.state) < current_h]
        
        if not better_children:  # Không còn cải thiện
            return None, steps_explored
        
        # Chọn ngẫu nhiên một neighbor tốt hơn
        current_node = random.choice(better_children)
        path.append(current_node)

def solve_beam_search(initial_state, beam_width=2):
    initial_node = Node(initial_state)
    if initial_node.state == goal_state:
        return [initial_node], 0
    
    beam = [(heuristic(initial_node.state), initial_node)]
    visited = set()
    steps_explored = 0
    
    while beam:
        new_beam = []
        for _, current_node in beam:
            if current_node.state == goal_state:
                path = []
                node = current_node
                while node:
                    path.append(node)
                    node = node.parent
                return path[::-1], steps_explored
            
            children = current_node.generate_children()
            steps_explored += len(children)
            for child in children:
                if str(child.state) not in visited:
                    visited.add(str(child.state))
                    new_beam.append((heuristic(child.state), child))
        
        # Sắp xếp và giữ lại beam_width trạng thái tốt nhất
        new_beam.sort(key=lambda x: x[0])
        beam = new_beam[:beam_width]
        
        if not beam:
            return None, steps_explored
    
    return None, steps_explored

def solve_genetic_algorithm(initial_state, population_size=20, max_generations=100, mutation_rate=0.1):
    def generate_random_state():
        state = copy.deepcopy(initial_state)
        for _ in range(5):  # Tạo trạng thái ngẫu nhiên bằng 5 bước di chuyển
            node = Node(state)
            children = node.generate_children()
            state = random.choice(children).state
        return state
    
    def crossover(parent1, parent2):
        # Lai ghép theo thứ tự (Order Crossover - OX) cho bài toán 8-puzzle
        flat1 = sum(parent1.state, [])
        flat2 = sum(parent2.state, [])
        size = 9
        a, b = sorted(random.sample(range(size), 2))
        child_flat = [None]*size
        child_flat[a:b] = flat1[a:b]
        fill = [x for x in flat2 if x not in child_flat[a:b]]
        idx = 0
        for i in range(size):
            if child_flat[i] is None:
                child_flat[i] = fill[idx]
                idx += 1
        # Chuyển về ma trận 3x3
        child = [child_flat[i*3:(i+1)*3] for i in range(3)]
        return Node(child)
    
    def mutate(node):
        if random.random() < mutation_rate:
            children = node.generate_children()
            if children:
                return random.choice(children)
        return node
    
    # Khởi tạo quần thể
    population = [Node(generate_random_state()) for _ in range(population_size - 1)]
    population.append(Node(initial_state))
    steps_explored = population_size
    
    for generation in range(max_generations):
        # Đánh giá quần thể
        population.sort(key=lambda x: heuristic(x.state))
        if heuristic(population[0].state) == 0:  # Tìm thấy đích
            best = population[0]
            path = [best]
            while best.parent:
                path.append(best.parent)
                best = best.parent
            return path[::-1], steps_explored
        
        # Chọn lọc (giữ 50% tốt nhất)
        half_size = population_size // 2
        new_population = population[:half_size]
        
        # Lai ghép và đột biến
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(new_population[:half_size], 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
            steps_explored += 1
        
        population = new_population
    
    return None, steps_explored

def solve_simulated_annealing(initial_state, initial_temp=1000, cooling_rate=0.95, max_steps=1000):
    current_node = Node(initial_state)
    steps_explored = 0
    path = [current_node]
    temperature = initial_temp
    
    while steps_explored < max_steps and temperature > 1:
        current_h = heuristic(current_node.state)
        if current_h == 0:
            return path, steps_explored
        
        children = current_node.generate_children()
        steps_explored += len(children)
        next_node = random.choice(children)
        next_h = heuristic(next_node.state)
        
        delta_h = next_h - current_h
        
        # Chấp nhận bước đi nếu tốt hơn hoặc theo xác suất Boltzmann nếu xấu hơn
        if delta_h < 0 or random.random() < math.exp(-delta_h / temperature):
            current_node = next_node
            path.append(next_node)
        
        temperature *= cooling_rate  # Giảm nhiệt độ
    
    if heuristic(current_node.state) == 0:
        return path, steps_explored
    return None, steps_explored

def solve_andor_graph_search(initial_state, max_depth=20):
    """Thuật toán AND-OR Graph Search cho bài toán 8-puzzle."""
    
    def or_search(state, problem, path, depth):
        """Tìm kiếm OR cho đỉnh OR trong đồ thị AND-OR."""
        if depth > max_depth:
            return None, 1
        
        # Kiểm tra trạng thái đích
        if state == goal_state:
            return {}, 1  # Trả về plan rỗng và số bước là 1
        
        # Kiểm tra chu trình
        if any(state == s for s in path):
            return None, 1
        
        # Mở rộng path
        path = path + [state]
        
        # Thử các hành động và trạng thái kế tiếp
        for action, next_states in generate_next_states(state):
            # Gọi AND-search cho các trạng thái kết quả của hành động
            plan, steps = and_search(next_states, problem, path, depth + 1)
            
            if plan is not None:
                return {action: plan}, steps + 1
        
        return None, len(path)
    
    def and_search(states, problem, path, depth):
        """Tìm kiếm AND cho đỉnh AND trong đồ thị AND-OR."""
        plan = {}
        total_steps = 0
        
        for state in states:
            subplan, steps = or_search(state, problem, path, depth)
            if subplan is None:
                return None, total_steps + steps
            plan[state] = subplan
            total_steps += steps
            
        return plan, total_steps
    
    def generate_next_states(state):
        """Tạo ra các cặp (hành động, tập trạng thái kế tiếp) từ một trạng thái."""
        # Tìm vị trí ô trống
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    blank_i, blank_j = i, j
                    break
        
        # Các hướng di chuyển: lên, xuống, trái, phải
        moves = [('Lên', -1, 0), ('Xuống', 1, 0), ('Trái', 0, -1), ('Phải', 0, 1)]
        action_states = []
        
        for move_name, di, dj in moves:
            ni, nj = blank_i + di, blank_j + dj
            
            # Kiểm tra vị trí mới có hợp lệ không
            if 0 <= ni < 3 and 0 <= nj < 3:
                # Tạo trạng thái mới
                new_state = [row[:] for row in state]
                new_state[blank_i][blank_j], new_state[ni][nj] = new_state[ni][nj], new_state[blank_i][blank_j]
                
                # Vì 8-puzzle là môi trường xác định, mỗi hành động dẫn đến đúng một trạng thái
                action_states.append((move_name, [new_state]))
        
        return action_states
    
    # Chuyển đổi initial_state thành tuple để dễ dàng so sánh
    initial_node = Node(initial_state)
    path = []
    
    # Tìm kiếm OR bắt đầu từ trạng thái ban đầu
    plan, steps_explored = or_search(initial_state, None, path, 0)
    
    if plan is None:
        return None, steps_explored
    
    # Tạo đường đi từ plan
    current_state = initial_state
    solution_path = [initial_node]
    
    while plan and current_state != goal_state:
        for action in plan:
            # Tìm trạng thái kế tiếp dựa trên hành động
            for move_name, di, dj in [('Lên', -1, 0), ('Xuống', 1, 0), ('Trái', 0, -1), ('Phải', 0, 1)]:
                if action == move_name:
                    # Tìm vị trí ô trống
                    for i in range(3):
                        for j in range(3):
                            if current_state[i][j] == 0:
                                blank_i, blank_j = i, j
                                break
                    
                    ni, nj = blank_i + di, blank_j + dj
                    if 0 <= ni < 3 and 0 <= nj < 3:
                        new_state = [row[:] for row in current_state]
                        new_state[blank_i][blank_j], new_state[ni][nj] = new_state[ni][nj], new_state[blank_i][blank_j]
                        
                        new_node = Node(new_state, solution_path[-1], action)
                        solution_path.append(new_node)
                        current_state = new_state
                        
                        # Cập nhật plan cho trạng thái tiếp theo
                        plan = plan.get(action, {})
                        break
    
    return solution_path, steps_explored

import random
import copy

def solve_belief_state_search(initial_belief_states, goal_states=None, max_steps=100):
    if goal_states is None:
        goal_states = [[[1,2,3],[4,5,6],[7,8,0]]]

    def update_belief_state(belief_states, action):
        new_belief_states = []
        for state in belief_states:
            node = Node(state)
            i, j = node.find_blank()
            di, dj = 0, 0
            if action == 'Lên':
                di, dj = -1, 0
            elif action == 'Xuống':
                di, dj = 1, 0
            elif action == 'Trái':
                di, dj = 0, -1
            elif action == 'Phải':
                di, dj = 0, 1
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = copy.deepcopy(state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                new_belief_states.append(new_state)
            else:
                new_belief_states.append(state)  # Không di chuyển được thì giữ nguyên
        return new_belief_states

    def check_goal_in_belief(belief_states, goal_states):
        for state in belief_states:
            for goal in goal_states:
                if state == goal:
                    return True, state
        return False, None

    belief_states = initial_belief_states
    path = [Node(belief_states[0])]
    steps_explored = 0
    actions_taken = []

    while steps_explored < max_steps:
        steps_explored += 1
        reached, goal_state = check_goal_in_belief(belief_states, goal_states)
        if reached:
            last_node = Node(goal_state, parent=path[-1], move=actions_taken[-1] if actions_taken else None)
            path.append(last_node)
            return path, steps_explored, actions_taken

        action_choices = ['Lên', 'Xuống', 'Trái', 'Phải']
        random.shuffle(action_choices)
        chosen_action = action_choices[0]
        actions_taken.append(chosen_action)

        belief_states = update_belief_state(belief_states, chosen_action)
        new_node = Node(belief_states[0], parent=path[-1], move=chosen_action)
        path.append(new_node)

    return None, steps_explored, actions_taken


def solve_partial_observable_search(initial_state, observable_cells=None, max_steps=100):
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    if observable_cells is None:
        observable_cells = [(0, 0), (1, 1), (2, 2)]

    def get_observation(state):
        observation = [[-1 for _ in range(3)] for _ in range(3)]
        for i, j in observable_cells:
            if 0 <= i < 3 and 0 <= j < 3:
                observation[i][j] = state[i][j]
        return observation

    def is_consistent(state, observation):
        for i in range(3):
            for j in range(3):
                if (i, j) in observable_cells and observation[i][j] != -1:
                    if state[i][j] != observation[i][j]:
                        return False
        return True

    def move(state, action):
        node = Node(state)
        i, j = node.find_blank()
        di, dj = 0, 0
        if action == 'Lên':
            di, dj = -1, 0
        elif action == 'Xuống':
            di, dj = 1, 0
        elif action == 'Trái':
            di, dj = 0, -1
        elif action == 'Phải':
            di, dj = 0, 1
        ni, nj = i + di, j + dj
        if 0 <= ni < 3 and 0 <= nj < 3:
            new_state = copy.deepcopy(state)
            new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
            return new_state
        else:
            return state

    current_state = initial_state
    belief_states = [initial_state]
    path = [Node(initial_state)]
    steps_explored = 0
    actions_taken = []

    while steps_explored < max_steps:
        steps_explored += 1
        observation = get_observation(current_state)
        
        belief_states = [state for state in belief_states if is_consistent(state, observation)]
        if not belief_states:
            belief_states = [current_state]

        if any(state == goal_state for state in belief_states):
            return path, steps_explored, actions_taken

        actions = ['Lên', 'Xuống', 'Trái', 'Phải']
        random.shuffle(actions)
        chosen_action = actions[0]
        actions_taken.append(chosen_action)

        current_state = move(current_state, chosen_action)
        belief_states = [move(state, chosen_action) for state in belief_states]

        new_node = Node(current_state, parent=path[-1], move=chosen_action)
        path.append(new_node)

    return None, steps_explored, actions_taken

def solve_puzzle_backtracking(initial_state, max_depth=50):
    # Tạo node gốc
    initial_node = Node(initial_state)
    
    # Nếu trạng thái ban đầu đã là đích
    if initial_node.state == goal_state:
        return [initial_node], 0
    
    # Tập hợp các trạng thái đã thăm
    visited = set()
    visited.add(str(initial_node.state))
    
    # Số bước đã duyệt
    steps_explored = [0]  # Dùng list để có thể thay đổi trong đệ quy
    
    # Hàm đệ quy backtracking
    def backtrack(current_node, depth):
        if depth >= max_depth:
            return None
        
        steps_explored[0] += 1
        
        for child in current_node.generate_children():
            child_state_str = str(child.state)
            if child_state_str not in visited:
                if child.state == goal_state:
                    path = []
                    current = child
                    while current:
                        path.append(current)
                        current = current.parent
                    return path[::-1]
                
                visited.add(child_state_str)
                result = backtrack(child, depth + 1)
                if result:
                    return result
                visited.remove(child_state_str)
        
        return None

    result = backtrack(initial_node, 0)
    return result, steps_explored[0]
    
def get_valid_actions(node):
    i, j = node.find_blank()
    actions = []
    if i > 0: actions.append('Lên')
    if i < 2: actions.append('Xuống')
    if j > 0: actions.append('Trái')
    if j < 2: actions.append('Phải')
    return actions

def apply_action(node, action):
    for child in node.generate_children():
        if child.move == action:
            return child
    return None  # Không tìm được

def get_state_key(node):
    return tuple(tuple(row) for row in node.state)

#Hàm Q_learning
def train_q_learning(initial_state, goal_state):
    Q = {}
    EPSILON = 0.2
    ALPHA = 0.1
    GAMMA = 0.9
    EPISODES = 5000000

    steps_explored = 0  # Đếm số bước tìm kiếm
    final_node = None

    for ep in range(EPISODES):
        current = Node(state=initial_state)
        visited = set()
        for step in range(100):
            state_key = get_state_key(current)
            if state_key not in Q:
                Q[state_key] = {a: 0 for a in get_valid_actions(current)}

            # Epsilon-greedy
            if random.random() < EPSILON:
                action = random.choice(get_valid_actions(current))
            else:
                action = max(Q[state_key], key=Q[state_key].get)

            next_node = apply_action(current, action)
            if next_node is None:
                continue
            next_key = get_state_key(next_node)

            if next_key not in Q:
                Q[next_key] = {a: 0 for a in get_valid_actions(next_node)}

            reward = 100 if next_node.state == goal_state else -1
            Q[state_key][action] += ALPHA * (
                reward + GAMMA * max(Q[next_key].values()) - Q[state_key][action]
            )

            next_node.parent = current  # Lưu liên kết ngược để truy vết
            next_node.move = action     # Lưu hành động
            next_node.depth = current.depth + 1  # Đồng bộ depth
            current = next_node

            steps_explored += 1

            if current.state == goal_state:
                final_node = current
                break

        if final_node:
            break

    # Truy vết đường đi từ đích về gốc
    path = []
    while final_node:
        path.append(final_node)
        final_node = final_node.parent
    path = path[::-1]

    return path, steps_explored, Q

class PuzzleCell(QFrame):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value
        self.initUI()
        
    def initUI(self):
        self.setMinimumSize(80, 80)
        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)
        
        # Thiết lập màu nền
        pal = self.palette()
        if self.value != 0:
            pal.setColor(QPalette.Background, QColor(65, 105, 225))  # Xanh dương cho các ô có số
        else:
            pal.setColor(QPalette.Background, QColor(255, 255, 255))  # Trắng cho ô trống
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
        # Thiết lập label hiển thị số
        layout = QVBoxLayout(self)
        if self.value != 0:
            label = QLabel(str(self.value))
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 24, QFont.Bold))
            label.setStyleSheet("color: white;")
            layout.addWidget(label)

class PuzzleSolverApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giải bài toán 8-puzzle")
        self.resize(1100,900)
        
        # Khởi tạo trạng thái ban đầu
        self.initial_state = [
            [2, 6, 5],
            [0, 8, 7],
            [4, 3, 1]
        ]
        
        # Khởi tạo trạng thái mục tiêu (goal_state)
        self.goal_state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

        # Khởi tạo các biến
        self.path = None
        self.steps_explored = 0
        self.current_step = 0
        self.selected_algorithm = "DFS"  # Thuật toán mặc định
        self.initial_belief_states = [self.initial_state]  # Danh sách trạng thái niềm tin

        # Tạo widget chính
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout chính
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Tạo panel chọn thuật toán
        self.create_algorithm_panel()

        # Tạo panel nhập trạng thái niềm tin
        self.create_belief_input_panel()
        
        # Tạo layout hiển thị trạng thái
        self.create_states_panel()
        
        # Tạo panel điều khiển
        self.create_control_panel()
        
        # Tạo panel hiển thị giải pháp
        self.create_solution_panel()
        
        # Thiết lập timer cho chế độ tự động chạy
        self.auto_timer = QTimer()
        self.auto_timer.timeout.connect(self.next_step)
        self.auto_playing = False
        
        # Hiển thị trạng thái ban đầu và đích
        self.display_initial_state()
        self.display_goal_state()

    def create_algorithm_panel(self):
        # Panel chọn thuật toán
        self.algo_frame = QFrame()
        self.algo_frame.setFrameShape(QFrame.Box)
        self.algo_frame.setLineWidth(2)
        self.algo_layout = QHBoxLayout(self.algo_frame)
        
        self.algo_label = QLabel("Chọn thuật toán:")
        self.algo_label.setFont(QFont("Arial", 12))
        self.algo_layout.addWidget(self.algo_label)
        
        self.algo_combo = QComboBox()
        self.algo_combo.addItem("DFS - Tìm kiếm theo chiều sâu")
        self.algo_combo.addItem("BFS - Tìm kiếm theo chiều rộng")
        self.algo_combo.addItem("Greedy - Tìm kiếm tham lam")
        self.algo_combo.addItem("UCS - Tìm kiếm chi phí đồng nhất")
        self.algo_combo.addItem("IDS - Tìm kiếm sâu dần")
        self.algo_combo.addItem("A* - Tìm kiếm A*")
        self.algo_combo.addItem("IDA* - Tìm kiếm IDA*")
        self.algo_combo.addItem("Simple HC - Leo đồi đơn giản") 
        self.algo_combo.addItem("Steepest HC - Leo đồi dốc nhất") 
        self.algo_combo.addItem("Stochastic HC - Leo đồi ngẫu nhiên")
        self.algo_combo.addItem("Beam - Tìm kiếm chùm") 
        self.algo_combo.addItem("GA - Thuật toán di truyền")  
        self.algo_combo.addItem("SA - Simulated Annealing")
        self.algo_combo.addItem("AND-OR - Tìm kiếm đồ thị AND-OR")
        self.algo_combo.addItem("Belief - Tìm kiếm với trạng thái niềm tin")
        self.algo_combo.addItem("Partial - Tìm kiếm môi trường quan sát được một phần")
        self.algo_combo.addItem("Backtracking - Thuật toán quay lui")
        self.algo_combo.addItem("Q-Learning - Học tăng cường Q")
                                
        self.algo_combo.currentIndexChanged.connect(self.algorithm_changed)
        self.algo_layout.addWidget(self.algo_combo)
        
        self.main_layout.addWidget(self.algo_frame)
    
    def create_belief_input_panel(self):
        self.belief_input_frame = QFrame()
        self.belief_input_layout = QVBoxLayout(self.belief_input_frame)
        
        self.belief_label = QLabel("Nhập trạng thái niềm tin ban đầu (cho Belief Search):")
        self.belief_label.setFont(QFont("Arial", 12))
        self.belief_input_layout.addWidget(self.belief_label)
        
        self.belief_input = QTextEdit()
        self.belief_input.setPlaceholderText("Ví dụ: [[[1,2,3],[4,5,6],[7,8,0]],[[1,2,3],[4,5,0],[7,8,6]]]")
        self.belief_input_layout.addWidget(self.belief_input)
        
        self.main_layout.addWidget(self.belief_input_frame)
    
    def get_belief_input(self):
        # Lấy dữ liệu từ belief_input
        belief_input = self.belief_input.toPlainText().replace('\n', '').replace(' ', '')

        try:
            # Sử dụng ast.literal_eval để an toàn hơn trong việc chuyển chuỗi thành cấu trúc dữ liệu
            belief_states = ast.literal_eval(belief_input)

            # Kiểm tra định dạng dữ liệu
            if not isinstance(belief_states, list) or not all(
                isinstance(state, list) and len(state) == 3 and all(len(row) == 3 for row in state)
                for state in belief_states
            ):
                raise ValueError("Định dạng trạng thái niềm tin không hợp lệ! Mỗi trạng thái phải là ma trận 3x3.")

            return belief_states

        except (ValueError, SyntaxError) as e:
            self.solution_info.setText(f"Lỗi: {str(e)}")
            return None

    def create_states_panel(self):
        # Panel hiển thị trạng thái
        self.states_panel = QFrame()
        self.states_layout = QHBoxLayout(self.states_panel)
        
        # Tạo khung hiển thị trạng thái ban đầu
        self.initial_frame = QFrame()
        self.initial_frame.setFrameShape(QFrame.Box)
        self.initial_frame.setLineWidth(3)
        self.initial_layout = QVBoxLayout(self.initial_frame)
        
        self.initial_title = QLabel("Trạng thái xuất phát")
        self.initial_title.setAlignment(Qt.AlignCenter)
        self.initial_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.initial_layout.addWidget(self.initial_title)
        
        self.initial_grid = QGridLayout()
        self.initial_layout.addLayout(self.initial_grid)
        
        # Tạo khung hiển thị trạng thái đích
        self.goal_frame = QFrame()
        self.goal_frame.setFrameShape(QFrame.Box)
        self.goal_frame.setLineWidth(3)
        self.goal_layout = QVBoxLayout(self.goal_frame)
        
        self.goal_title = QLabel("Trạng thái đích")
        self.goal_title.setAlignment(Qt.AlignCenter)
        self.goal_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.goal_layout.addWidget(self.goal_title)
        
        self.goal_grid = QGridLayout()
        self.goal_layout.addLayout(self.goal_grid)
        
        # Thêm vào layout chính
        self.states_layout.addWidget(self.initial_frame)
        self.states_layout.addWidget(self.goal_frame)
        self.main_layout.addWidget(self.states_panel)
    
    def create_control_panel(self):
        # Panel điều khiển
        self.control_panel = QFrame()
        self.control_layout = QVBoxLayout(self.control_panel)
        
        # Layout cho các điều khiển đầu vào
        self.input_layout = QHBoxLayout()
        
        # Thêm điều khiển độ sâu cho DFS
        self.depth_layout = QHBoxLayout()
        self.depth_label = QLabel("Độ sâu tối đa:")
        self.depth_input = QSpinBox()
        self.depth_input.setMinimum(10)
        self.depth_input.setMaximum(100)
        self.depth_input.setValue(50)
        self.depth_layout.addWidget(self.depth_label)
        self.depth_layout.addWidget(self.depth_input)
        self.input_layout.addLayout(self.depth_layout)
        
        # Nút giải bài toán
        self.solve_button = QPushButton("Giải bài toán")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.input_layout.addWidget(self.solve_button)
        
        self.control_layout.addLayout(self.input_layout)
        
        # Layout cho các nút điều khiển hiển thị
        self.buttons_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Bước trước")
        self.prev_button.clicked.connect(self.previous_step)
        self.prev_button.setEnabled(False)
        self.buttons_layout.addWidget(self.prev_button)
        
        self.next_button = QPushButton("Bước tiếp")
        self.next_button.clicked.connect(self.next_step)
        self.next_button.setEnabled(False)
        self.buttons_layout.addWidget(self.next_button)
        
        self.auto_button = QPushButton("Tự động chạy")
        self.auto_button.clicked.connect(self.toggle_auto_play)
        self.auto_button.setEnabled(False)
        self.buttons_layout.addWidget(self.auto_button)
        
        self.control_layout.addLayout(self.buttons_layout)
        
        self.main_layout.addWidget(self.control_panel)
    
    def create_solution_panel(self):
        # Panel hiển thị kết quả
        self.solution_panel = QFrame()
        self.solution_layout = QVBoxLayout(self.solution_panel)
        
        # Hiển thị thông tin thời gian và số bước
        self.stats_frame = QFrame()
        self.stats_frame.setFrameShape(QFrame.Box)
        self.stats_frame.setLineWidth(2)
        self.stats_layout = QVBoxLayout(self.stats_frame)
        
        # Thông tin thuật toán và kết quả
        self.algorithm_info = QLabel()
        self.algorithm_info.setAlignment(Qt.AlignCenter)
        self.algorithm_info.setFont(QFont("Arial", 12, QFont.Bold))
        self.stats_layout.addWidget(self.algorithm_info)
        
        self.solution_info = QLabel()
        self.solution_info.setAlignment(Qt.AlignCenter)
        self.solution_info.setFont(QFont("Arial", 12))
        self.stats_layout.addWidget(self.solution_info)
        
        self.solution_layout.addWidget(self.stats_frame)
        
        # Khung hiển thị quá trình giải
        self.solution_frame = QFrame()
        self.solution_frame.setFrameShape(QFrame.Box)
        self.solution_frame.setLineWidth(3)
        self.current_layout = QVBoxLayout(self.solution_frame)
        
        self.solution_title = QLabel("Quá trình giải")
        self.solution_title.setAlignment(Qt.AlignCenter)
        self.solution_title.setFont(QFont("Arial", 16, QFont.Bold))
        self.current_layout.addWidget(self.solution_title)
        
        self.step_info = QLabel()
        self.step_info.setAlignment(Qt.AlignCenter)
        self.step_info.setFont(QFont("Arial", 12))
        self.current_layout.addWidget(self.step_info)
        
        self.current_grid = QGridLayout()
        self.current_layout.addLayout(self.current_grid)
        
        self.solution_layout.addWidget(self.solution_frame)
        
        self.main_layout.addWidget(self.solution_panel)
    
    def display_initial_state(self):
        for i in range(3):
            for j in range(3):
                label = QLabel(str(self.initial_state[i][j]))
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont("Arial", 20))
                label.setStyleSheet("border: 1px solid black; padding: 10px;")
                self.initial_grid.addWidget(label, i, j)
    
    def display_goal_state(self):
        for i in range(3):
            for j in range(3):
                label = QLabel(str(self.goal_state[i][j]))
                label.setAlignment(Qt.AlignCenter)
                label.setFont(QFont("Arial", 20))
                label.setStyleSheet("border: 1px solid black; padding: 10px;")
                self.goal_grid.addWidget(label, i, j)

    def display_current_state(self):
        for i in range(self.current_grid.count()):
            self.current_grid.itemAt(i).widget().deleteLater()
        
        if self.path and 0 <= self.current_step < len(self.path):
            state = self.path[self.current_step].state
            for i in range(3):
                for j in range(3):
                    label = QLabel(str(state[i][j]))
                    label.setAlignment(Qt.AlignCenter)
                    label.setFont(QFont("Arial", 20))
                    label.setStyleSheet("border: 1px solid black; padding: 10px;")
                    self.current_grid.addWidget(label, i, j)
            self.step_info.setText(f"Bước {self.current_step}: {self.path[self.current_step].action or 'Khởi tạo'}")
        else:
            self.step_info.setText("Không có trạng thái để hiển thị")

    def algorithm_changed(self, index):
        algorithm_map = {
            0: "DFS", 
            1: "BFS", 
            2: "Greedy",
            3: "UCS",
            4: "IDS", 
            5: "A*",
            6: "IDA*",
            7: "Simple HC",
            8: "Steepest HC",
            9: "Stochastic HC",
            10: "Beam",
            11: "GA",
            12: "SA",
            13: "AND-OR",
            14: "Belief",
            15: "Partial",
            16: "Backtracking",
            17: "Q-Learning"
            }
        self.selected_algorithm = algorithm_map.get(index, "DFS")
        self.display_initial_state()
        self.display_goal_state()

        # Hiển thị/ẩn các điều khiển riêng cho từng thuật toán
        if self.selected_algorithm in ["DFS", "IDS", "IDA*"]:
            self.depth_label.setVisible(True)
            self.depth_input.setVisible(True)
        else:
            self.depth_label.setVisible(False)
            self.depth_input.setVisible(False)
        
        # Cập nhật thông tin thuật toán
        algorithm_descriptions = {
            "DFS": "Thuật toán tìm kiếm theo chiều sâu (DFS): Quét sâu vào một nhánh trước khi quay lui.",
            "BFS": "Thuật toán tìm kiếm theo chiều rộng (BFS): Quét tất cả các trạng thái ở cùng độ sâu trước khi đi sâu hơn.",
            "Greedy": "Thuật toán tìm kiếm tham lam (Greedy): Chọn bước đi tốt nhất tại mỗi bước mà không quan tâm đến kết quả cuối cùng.",
            "UCS": "Thuật toán tìm kiếm theo chi phí đồng nhất (UCS): Tìm đường đi ngắn nhất bằng cách mở rộng các trạng thái theo chi phí từ thấp đến cao.",
            "IDS": "Thuật toán tìm kiếm sâu dần (IDS): Kết hợp DFS và BFS, tăng dần độ sâu để tìm đường đi ngắn nhất.",
            "A*": "Thuật toán A* (A*): Tìm kiếm tối ưu bằng cách kết hợp chi phí đường đi và heuristic.",
            "IDA*": "Thuật toán IDA* (IDA*): Tìm kiếm sâu dần với heuristic, tối ưu như A* nhưng tiết kiệm bộ nhớ.",
            "Simple HC": "Thuật toán Leo đồi đơn giản: Chọn neighbor đầu tiên tốt hơn trạng thái hiện tại.",
            "Steepest HC": "Thuật toán Leo đồi dốc nhất: Chọn neighbor tốt nhất trong tất cả các neighbor.",
            "Stochastic HC": "Thuật toán Leo đồi ngẫu nhiên: Chọn ngẫu nhiên một neighbor tốt hơn trạng thái hiện tại.",
            "Beam": "Thuật toán Beam Search: Giữ một số trạng thái tốt nhất ở mỗi mức độ sâu.",
            "GA": "Thuật toán di truyền (GA): Mô phỏng tiến hóa để tìm lời giải.",
            "SA": "Thuật toán Simulated Annealing: Chấp nhận bước đi xấu với xác suất giảm dần theo nhiệt độ.",
            "AND-OR": "Thuật toán tìm kiếm đồ thị AND-OR: Tìm kiếm trong môi trường không xác định bằng cách phân tích các nút AND và OR.",
            "Belief": "Thuật toán tìm kiếm không quan sát với trạng thái niềm tin: Duy trì tập hợp các trạng thái có thể và cập nhật theo hành động.",            
            "Partial": "Thuật toán tìm kiếm trong môi trường quan sát được một phần: Chỉ quan sát được một số ô trên bảng, các ô khác bị ẩn.",
            "Backtracking": "Tìm kiếm giải pháp bằng cách thử từng khả năng và quay lại khi gặp phải ngõ cụt.",
            "Q-Learning": "Học tăng cường Q: Học từ kinh nghiệm để tối ưu hóa hành động trong môi trường không xác định."
        }
        self.algorithm_info.setText(algorithm_descriptions.get(self.selected_algorithm, ""))
    
    def display_initial_state(self):
        self.clear_layout(self.initial_grid)
        for i in range(3):
            for j in range(3):
                cell = PuzzleCell(self.initial_state[i][j])
                self.initial_grid.addWidget(cell, i, j)
    
    def display_goal_state(self):
        self.clear_layout(self.goal_grid)
        for i in range(3):
            for j in range(3):
                cell = PuzzleCell(goal_state[i][j])
                self.goal_grid.addWidget(cell, i, j)
    
    def display_current_state(self):
        if not self.path:
            return
            
        self.clear_layout(self.current_grid)
        current_state = self.path[self.current_step].state
        for i in range(3):
            for j in range(3):
                cell = PuzzleCell(current_state[i][j])
                self.current_grid.addWidget(cell, i, j)
                
        # Cập nhật thông tin bước
        if self.current_step == 0:
            self.step_info.setText("Trạng thái ban đầu")
        else:
            self.step_info.setText(f"Bước {self.current_step}: {self.path[self.current_step].move}")
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())
    
    def solve_puzzle(self):
        start_time = time.time()
        
        if self.selected_algorithm == "DFS":
            max_depth = self.depth_input.value()
            self.path, self.steps_explored = solve_puzzle_dfs(self.initial_state, max_depth)
        elif self.selected_algorithm == "BFS":
            self.path, self.steps_explored = solve_puzzle_bfs(self.initial_state)
        elif self.selected_algorithm == "Greedy":
            self.path, self.steps_explored = greedy_search(self.initial_state)
        elif self.selected_algorithm == "UCS":
             self.path, self.steps_explored = uniform_cost_search(self.initial_state)
        elif self.selected_algorithm == "IDS":
            max_depth = self.depth_input.value()
            self.path, self.steps_explored = solve_puzzle_ids(self.initial_state, max_depth)
        elif self.selected_algorithm == "A*":
            self.path, self.steps_explored = solve_puzzle_astar(self.initial_state)
        elif self.selected_algorithm == "IDA*":
            max_depth = self.depth_input.value()  # Dùng max_depth như max_cost_limit
            self.path, self.steps_explored = solve_puzzle_idastar(self.initial_state, max_depth)
        elif self.selected_algorithm == "Simple HC":
            self.path, self.steps_explored = solve_simple_hill_climbing(self.initial_state)
        elif self.selected_algorithm == "Steepest HC":
            self.path, self.steps_explored = solve_steepest_ascent_hill_climbing(self.initial_state)
        elif self.selected_algorithm == "Stochastic HC":
            self.path, self.steps_explored = solve_stochastic_hill_climbing(self.initial_state)
        elif self.selected_algorithm == "Beam":
            self.path, self.steps_explored = solve_beam_search(self.initial_state, beam_width=2)
        elif self.selected_algorithm == "GA":
            self.path, self.steps_explored = solve_genetic_algorithm(self.initial_state)
        elif self.selected_algorithm == "SA":
            self.path, self.steps_explored = solve_simulated_annealing(self.initial_state)
        elif self.selected_algorithm == "AND-OR":
            self.path, self.steps_explored = solve_andor_graph_search(self.initial_state)
        elif self.selected_algorithm == "Backtracking":
            self.path, self.steps_explored = solve_puzzle_backtracking(self.initial_state)
        elif self.selected_algorithm == "Q-Learning":
            self.path, self.steps_explored, self.q_table = train_q_learning(self.initial_state, self.goal_state)
        elif self.selected_algorithm == "Belief":
            # Phân tích trạng thái niềm tin từ ô nhập
            try:
                belief_input = self.belief_input.toPlainText().replace('\n', '').replace(' ', '')
                if belief_input:
                    # Thay thế eval() bằng ast.literal_eval() để an toàn hơn
                    self.initial_belief_states = ast.literal_eval(belief_input)
        
                    # Kiểm tra định dạng của belief_states
                    if not isinstance(self.initial_belief_states, list) or not all(
                        isinstance(state, list) and len(state) == 3 and all(len(row) == 3 for row in state)
                        for state in self.initial_belief_states
                    ):
                        raise ValueError("Định dạng trạng thái niềm tin không hợp lệ!")
                else:
                    self.initial_belief_states = [self.initial_state]  # Nếu không nhập, sử dụng initial_state mặc định
            except Exception as e:
                self.solution_info.setText(f"Lỗi: {str(e)}")
                return

            # Kiểm tra trạng thái niềm tin sau khi xử lý
            if self.initial_belief_states:
                max_steps = self.depth_input.value()
                self.path, self.steps_explored, self.actions = solve_belief_state_search(
                    self.initial_belief_states, [self.goal_state], max_steps
                )
    
                if self.path:
                    self.algorithm_info.setText("Tìm kiếm với trạng thái niềm tin")
                    self.solution_info.setText(f"Đã tìm thấy giải pháp sau {self.steps_explored} bước! Hành động: {self.actions}")
                    self.current_step = 0
                    self.display_current_state()
                    self.next_button.setEnabled(True)
                    self.auto_button.setEnabled(True)
                else:
                    self.solution_info.setText(f"Không tìm thấy giải pháp sau {self.steps_explored} bước.")
            else:
                    self.solution_info.setText("Thuật toán chưa được triển khai!")
                    self.path, self.steps_explored = solve_belief_state_search(self.initial_state)

        end_time = time.time()
        execution_time = end_time - start_time
        
        if not self.path:
            if self.selected_algorithm in ["DFS", "IDS", "IDA*"]:
                QMessageBox.critical(self, "Lỗi", f"Không tìm thấy đường đi trong giới hạn độ sâu {self.depth_input.value()}!")
            else:
                QMessageBox.critical(self, "Lỗi", "Không tìm thấy đường đi!")
            return
        
        # Hiển thị thông tin giải pháp
        solution_info = f"Thời gian chạy: {execution_time:.4f} giây | "
        solution_info += f"Số bước giải pháp: {len(self.path) - 1} | "
        solution_info += f"Số trạng thái đã duyệt: {self.steps_explored} | "
        solution_info += f"Độ sâu: {self.path[-1].depth}"
        self.solution_info.setText(solution_info)
        
        # Hiển thị trạng thái ban đầu
        self.current_step = 0
        self.display_current_state()
        
        # Kích hoạt các nút điều khiển
        self.next_button.setEnabled(True)
        self.auto_button.setEnabled(True)
        self.prev_button.setEnabled(False)  # Tắt nút trước vì đang ở bước đầu tiên
        
        QMessageBox.information(self, "Thông tin", f"Đã tìm thấy đường đi bằng thuật toán {self.selected_algorithm}!\nSử dụng các nút để xem từng bước giải.")
    
    def next_step(self):
        if not self.path or self.current_step >= len(self.path) - 1:
            if self.auto_playing:
                self.toggle_auto_play()  # Dừng tự động nếu đã đến bước cuối
            return
            
        self.current_step += 1
        self.display_current_state()
        
        self.prev_button.setEnabled(True)
        if self.current_step >= len(self.path) - 1:
            self.next_button.setEnabled(False)
            if self.auto_playing:
                self.toggle_auto_play()  # Dừng tự động nếu đã đến bước cuối
    
    def previous_step(self):
        if not self.path or self.current_step <= 0:
            return
            
        self.current_step -= 1
        self.display_current_state()
        
        self.next_button.setEnabled(True)
        if self.current_step <= 0:
            self.prev_button.setEnabled(False)
    
    def toggle_auto_play(self):
        if not self.path:
            return
            
        if not self.auto_playing:
            self.auto_playing = True
            self.auto_button.setText("Dừng tự động")
            self.auto_timer.start(1000)  # 1 giây cho mỗi bước
        else:
            self.auto_playing = False
            self.auto_button.setText("Tự động chạy")
            self.auto_timer.stop()

def main():
    app = QApplication(sys.argv)
    window = PuzzleSolverApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()