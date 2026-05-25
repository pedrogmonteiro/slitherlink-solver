#!/usr/bin/env python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 70:
# 109293 Diogo Lobo
# 113818 Pedro Monteiro

import random, copy
from sys import stdin
from collections import defaultdict

import utils
from utils import *

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,  
    recursive_best_first_search,
)


class SlitherlinkState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = SlitherlinkState.state_id
        SlitherlinkState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id
    
    def __eq__(self, value):
        if not isinstance(value, SlitherlinkState):
            return False
        if self.board is None or value.board is None:
            return self.board == value.board
        return self.board == value.board
    
    def __hash__(self):
        if self.board is None:
            return hash(None)
        return hash(frozenset(self.board.edges_active_hash.items()))


class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, matrix: list, edges_hash=None, edges_active_hash=None):
        self.board = matrix
        self.N = len(matrix) 
        self.M = len(matrix[0]) if self.N > 0 else 0
        
        if edges_hash is None or edges_active_hash is None:
            self.edges_hash, self.edges_active_hash = self.initialize_edges_maps()
        else:
            self.edges_hash = edges_hash
            self.edges_active_hash = edges_active_hash

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return (self.N == other.N and 
                self.M == other.M and 
                self.edges_active_hash == other.edges_active_hash)

    def print(self) -> str:
        """Devolve a representação em string do estado das arestas do tabuleiro."""
        lines = []
        for i in range(self.N):
            row_str = []
            for j in range(self.M):
                edges_order = [
                    ('h', i, j),     # Top
                    ('v', i, j + 1), # Right
                    ('h', i + 1, j), # Bottom
                    ('v', i, j)      # Left
                ]
                cell_bits = ""
                for edge in edges_order:
                    cell_bits += "1" if self.edges_active_hash.get(edge, "0") == "1" else "0"
                row_str.append(cell_bits)
            lines.append("\t".join(row_str))
        return "\n".join(lines) + "\n"

    def initialize_edges_maps(self):
        edges_hash = {}
        edges_active_hash = {}
        
        # Inicializar todas as arestas horizontais possíveis: (N+1) linhas, M colunas
        for i in range(self.N + 1):
            for j in range(self.M):
                edges_active_hash[('h', i, j)] = "0"
                
        # Inicializar todas as arestas verticais possíveis: N linhas, (M+1) colunas
        for i in range(self.N):
            for j in range(self.M + 1):
                edges_active_hash[('v', i, j)] = "0"

        # Mapear quais as 4 arestas pertencem a cada célula (i, j)
        for i in range(self.N):
            for j in range(self.M):
                edges_hash[(i, j)] = [
                    ('h', i, j),      # Top
                    ('v', i, j + 1),  # Right
                    ('h', i + 1, j),  # Bottom
                    ('v', i, j)       # Left
                ]
                
        return edges_hash, edges_active_hash

    def adjacent_cell(self, cell: tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento."""
        r, c = cell
        adjacent = []
        # Direções: Cima, Baixo, Esquerda, Direita
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.N and 0 <= nc < self.M:
                adjacent.append((nr, nc))
        return adjacent

    def propagate_constraints(self) -> bool:
        """Propaga as restrições lógicas do Slitherlink pelas arestas."""
        changed = True
        while changed:
            changed = False
            
            # Propagação baseada nas pistas das células
            for r in range(self.N):
                for c in range(self.M):
                    hint = self.board[r][c]
                    if hint is not None:
                        active = self.get_active_edges(r, c)
                        free_edges = [e for e in self.get_cell_edges(r, c) if self.edges_active_hash[e] == "0"]
                        invalid_edges_count = sum(1 for e in self.get_cell_edges(r, c) if self.edges_active_hash[e] == "X")
                        
                        if active > hint or (4 - invalid_edges_count) < hint:
                            return False
                        
                        if active == hint and free_edges:
                            for e in free_edges:
                                self.edges_active_hash[e] = "X"
                            changed = True
                        elif active + len(free_edges) == hint and free_edges:
                            for e in free_edges:
                                self.edges_active_hash[e] = "1"
                            changed = True

            # Propagação baseada nos Vértices (Grau 0 ou 2)
            vertex_map = defaultdict(list)
            for edge, status in self.edges_active_hash.items():
                etype, r, c = edge
                v1, v2 = ((r, c), (r, c + 1)) if etype == 'h' else ((r, c), (r + 1, c))
                vertex_map[v1].append(edge)
                vertex_map[v2].append(edge)

            for vertex, edges in vertex_map.items():
                active = sum(1 for e in edges if self.edges_active_hash[e] == "1")
                free = [e for e in edges if self.edges_active_hash[e] == "0"]
                total_possible = active + len(free)

                if active > 2 or (active == 1 and total_possible < 2):
                    return False

                if active == 2 and free:
                    for e in free:
                        self.edges_active_hash[e] = "X"
                    changed = True
                elif active == 1 and len(free) == 1:
                    self.edges_active_hash[free[0]] = "1"
                    changed = True
                elif active == 0 and total_possible < 2 and free:
                    for e in free:
                        self.edges_active_hash[e] = "X"
                    changed = True

            # Poda Antecipada de Sub-loops Isolados
            if not self._check_subloops_validity():
                return False
                    
        return True

    def _check_subloops_validity(self) -> bool:
        """Verifica se existem ciclos fechados pequenos que violam a solução global."""
        graph = defaultdict(list)
        total_edges = 0
        for edge, status in self.edges_active_hash.items():
            if status == "1":
                total_edges += 1
                etype, r, c = edge
                v1, v2 = ((r, c), (r, c + 1)) if etype == 'h' else ((r, c), (r + 1, c))
                graph[v1].append(v2)
                graph[v2].append(v1)
        
        if not graph:
            return True

        visited = set()
        
        for start in graph:
            if start in visited:
                continue
            
            curr_component_vertices = set()
            queue = [start]
            is_closed_loop = True
            edges_count_in_component = 0
            
            while queue:
                curr = queue.pop(0)
                if curr in curr_component_vertices:
                    continue
                curr_component_vertices.add(curr)
                visited.add(curr)
                
                if len(graph[curr]) != 2:
                    is_closed_loop = False
                
                edges_count_in_component += len(graph[curr])
                
                for nxt in graph[curr]:
                    if nxt not in curr_component_vertices:
                        queue.append(nxt)
            
            edges_count_in_component //= 2
            
            if is_closed_loop and edges_count_in_component < total_edges:
                return False
                
        return True

    def get_cell_edges(self, row: int, column: int) -> list:
        """Devolve as arestas da célula enviada no argumento."""
        return self.edges_hash[(row, column)]

    def get_active_edges(self, row: int, column: int) -> int:
        """Devolve o número de arestas ativas."""
        return sum(1 for e in self.get_cell_edges(row, column) if self.edges_active_hash[e] == "1")

    def make_copy(self):
        return Board(self.board, self.edges_hash, self.edges_active_hash.copy())

    @staticmethod
    def parse_instance():
        board = []
        expected_cols = None
        while True:
            line = stdin.readline()
            if not line:
                break
            line = line.strip()
            if line == "":
                continue
            parts = line.split()
            row = [None if p == "." else int(p) for p in parts]
            if expected_cols is not None and len(row) != expected_cols:
                break
            if expected_cols is None:
                expected_cols = len(row)
                
            board.append(row)
        
        b = Board(board)
        
        # Tratar pistas de 0 (bloquear todas as suas arestas)
        for i in range(b.N):
            for j in range(b.M):
                if b.board[i][j] == 0:
                    for edge in b.get_cell_edges(i, j):
                        b.edges_active_hash[edge] = "X"

        for r in range(b.N):
            for c in range(b.M):
                if b.board[r][c] == 3:
                    for nr, nc in b.adjacent_cell((r, c)):
                        if b.board[nr][nc] == 3:
                            # Se são vizinhos na mesma linha (horizontal)
                            if r == nr:
                                shared_c = max(c, nc)
                                b.edges_active_hash[('v', r, shared_c)] = "1"      # Aresta comum central
                                b.edges_active_hash[('v', r, shared_c - 1)] = "1"  # Extremidade esquerda
                                b.edges_active_hash[('v', r, shared_c + 1)] = "1"  # Extremidade direita
                            # Se são vizinhos na mesma coluna (vertical)
                            elif c == nc:
                                shared_r = max(r, nr)
                                b.edges_active_hash[('h', shared_r, c)] = "1"      # Aresta comum central
                                b.edges_active_hash[('h', shared_r - 1, c)] = "1"  # Extremidade superior
                                b.edges_active_hash[('h', shared_r + 1, c)] = "1"  # Extremidade inferior

        b.propagate_constraints()
        return b


class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        super().__init__(SlitherlinkState(board))
        self.gui = gui

    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        if state.board is None:
            return []

        board = state.board
        best_edge = None
        min_free = 99
        
        for r in range(board.N):
            for c in range(board.M):
                hint = board.board[r][c]
                if hint is not None:
                    active = board.get_active_edges(r, c)
                    if active == hint:
                        continue
                    free_edges = [e for e in board.get_cell_edges(r, c) if board.edges_active_hash[e] == "0"]
                    if free_edges and len(free_edges) < min_free:
                        min_free = len(free_edges)
                        best_edge = free_edges[0]

        if best_edge:
            return [(best_edge, "1"), (best_edge, "X")]

        for edge, status in board.edges_active_hash.items():
            if status == "0":
                return [(edge, "1"), (edge, "X")]
                
        return []

    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        if state.board is None:
            return state
            
        edge, target_status = action
        new_board = state.board.make_copy()
        new_board.edges_active_hash[edge] = target_status
        
        if not new_board.propagate_constraints():
            return SlitherlinkState(None)
            
        return SlitherlinkState(new_board)

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        if state.board is None:
            return False
            
        board = state.board
        
        for r in range(board.N):
            for c in range(board.M):
                hint = board.board[r][c]
                if hint is not None and board.get_active_edges(r, c) != hint:
                    return False

        graph = defaultdict(list)
        for edge, status in board.edges_active_hash.items():
            if status == "1":
                etype, r, c = edge
                v1, v2 = ((r, c), (r, c + 1)) if etype == 'h' else ((r, c), (r + 1, c))
                graph[v1].append(v2)
                graph[v2].append(v1)
        
        if not graph:
            return False
            
        for vertex, neighbors in graph.items():
            if len(neighbors) != 2:
                return False 
                
        start_vertex = next(iter(graph))
        visited = set()
        current = start_vertex
        prev = graph[start_vertex][0] 
        
        while current not in visited:
            visited.add(current)
            neighbors = graph[current]
            next_vertex = neighbors[1] if neighbors[0] == prev else neighbors[0]
            prev = current
            current = next_vertex
            
        return len(visited) == len(graph)

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        if node.state.board is None:
            return float('inf')
        board = node.state.board
        h_val = 0
        for r in range(board.N):
            for c in range(board.M):
                hint = board.board[r][c]
                if hint is not None:
                    h_val += abs(hint - board.get_active_edges(r, c))
        return h_val


if __name__ == "__main__":
    board = Board.parse_instance()
    problem = Slitherlink(board)
    
    solution_node = depth_first_tree_search(problem)
    
    if solution_node is not None:
        print(solution_node.state.board.print(), end="")