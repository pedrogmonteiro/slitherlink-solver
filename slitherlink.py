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
        return self.board == value.board
    
    def __hash__(self):
        return hash(frozenset(self.board.edges_active_hash.items()))

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, matrix: list):
        self.board = matrix
        self.N = len(matrix) # numero de linhas [i,0]
        self.M = len(matrix[0]) if self.N > 0 else 0 # numero de colunas [0,j]
        self.edges_hash, self.edges_active_hash = self.initialize_edges_maps()
        self.activate_edges_that_reach_cell_limit()

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        return (self.N == other.N and 
                self.M == other.M and 
                self.edges_active_hash == other.edges_active_hash)

    
    def print(self) -> str:
        """Devolve a representação em string do estado das arestas do tabuleiro,
        seguindo a ordem estrita do enunciado/GUI: Top, Right, Bottom, Left."""
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
                    cell_bits += "1" if self.edges_active_hash[edge] == "1" else "0"
                row_str.append(cell_bits)
            lines.append(" ".join(row_str))
        return "\n".join(lines) + "\n"
    
    

    def initialize_edges_maps(self):
        edges_hash = {}
        edges_active_hash = {}
        activated_value = "0"
        for i in range(self.N):
            for j in range(self.M):
                if self.board[i][j] is not None and self.board[i][j] == 0:
                    activated_value = "X"
                edges_hash[(i, j)] = [('h',i,j), ('h',i+1,j), ('v',i,j), ('v',i,j+1)]
                edges_active_hash[('h',i,j)] = activated_value
                edges_active_hash[('h',i+1,j)] = activated_value
                edges_active_hash[('v',i,j)] = activated_value
                edges_active_hash[('v',i,j+1)] = activated_value
        return edges_hash, edges_active_hash
    

    def activate_edges_that_reach_cell_limit(self):
        for i in range(self.N):
            for j in range(self.M):
                if self.board[i][j] is not None:
                    inactive_edges = self.get_inactive_edges(i, j)
                    if inactive_edges == self.board[i][j]:
                        for edge in self.get_cell_edges(i, j):
                            if self.edges_active_hash[edge] == "0":
                                self.activate_edge(edge)

    def adjacent_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        # Formato WASD
        n = self.N
        m = self.M
        adjacent = []

        i,j = cell[0], cell[1]
        if i - 1 >= 0: # caso exista celula em cima (W)
            adjacent.append((i - 1, j))
        if j - 1 >= 0: # caso exista celula a esquerda (A)
            adjacent.append((i, j - 1))
        if i + 1 < n: # caso exista celula em baixo (S)
            adjacent.append((i + 1, j))
        if j + 1 < m: # caso exista celula a direita (D)
            adjacent.append((i, j + 1))
        return adjacent

    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve as arestas da célula enviada no argumento"""
        return self.edges_hash[(row, column)]

    def get_active_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas ativas"""
        count = 0
        for edge in self.get_cell_edges(row, column):
            if self.edges_active_hash[edge] == "1":
                count += 1
        return count
    
    def get_inactive_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas inativas"""
        count = 0
        for edge in self.get_cell_edges(row, column):
            if self.edges_active_hash[edge] == "0":
                count += 1
        return count

    def disactivate_edge(self, edge:tuple):
        """Desativa a aresta enviada no argumento"""
        self.edges_active_hash[edge] = "0"

    def activate_edge(self, edge:tuple):
        """Ativa a aresta enviada no argumento"""
        self.edges_active_hash[edge] = "1"

    def invalidate_edge(self, edge:tuple):
        """Invalida a aresta enviada no argumento, ou seja, não pode ser ativada"""
        self.edges_active_hash[edge] = "X"

    def make_copy(self):
        """Devolve uma cópia do tabuleiro, ou seja, uma nova instância da classe Board
        com o mesmo estado do tabuleiro atual."""
        new_board = Board(copy.deepcopy(self.board))
        new_board.edges_hash = copy.deepcopy(self.edges_hash)
        new_board.edges_active_hash = copy.deepcopy(self.edges_active_hash)
        return new_board
    
    def make_move(self, edge:tuple):
        """Devolve uma nova instância da classe Board com o estado do 
        tabuleiro resultante de ativar a aresta enviada no argumento."""
        new_board = self.make_copy()
        new_board.activate_edge(edge)
        return new_board

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board = []
        line = stdin.readline().strip().split("   ")
        while line != [""]:
            for i, l in enumerate(line):
                if l == ".":
                    line[i] = None
                else:
                    line[i] = int(l)
            board.append(line)
            line = stdin.readline().strip().split("   ")
        return Board(board)

    # TODO: outros metodos da classe

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        super().__init__(SlitherlinkState(board))


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.board
        valid_actions = []
        
        # Gather all edges currently marked as "0" (undecided)
        for edge, status in board.edges_active_hash.items():
            if status == "0":
                valid_actions.append(edge)
                
        return valid_actions


    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = state.board.make_move(action)
        return SlitherlinkState(new_board)
    
    def _verify_single_closed_loop(self, board) -> bool:
        """
        Verifica se as arestas ativas ("1") formam exatamente um único
        ciclo contínuo fechado, sem linhas soltas, bifurcações ou mini-loops.
        """
        graph = defaultdict(list)
        
        for edge, status in board.edges_active_hash.items():
            if status == "1":
                edge_type, r, c = edge
                if edge_type == 'h':
                    # Aresta horizontal liga o ponto (r, c) ao ponto (r, c+1)
                    v1 = (r, c)
                    v2 = (r, c + 1)
                else:
                    # Aresta vertical liga o ponto (r, c) ao ponto (r+1, c)
                    v1 = (r, c)
                    v2 = (r + 1, c)
                
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


    def goal_test(self, state: SlitherlinkState):
        board = state.board
        
        for r in range(board.N):
            for c in range(board.M):
                hint = board.board[r][c]
                if hint is not None:
                    if board.get_active_edges(r, c) != hint:
                        return False

        return self._verify_single_closed_loop(board)
    

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    board = Board.parse_instance()
    
    problem = Slitherlink(board)
    
    print("Searching for solution...")
    solution_node = depth_first_tree_search(problem)
    
    if solution_node is not None:
        print("Solution found!")
        print(solution_node.state.board.print())
    else:
        print("No solution could be found.")







