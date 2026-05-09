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

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""

    def __init__(self, matrix: list):
        self.board = matrix
        self.N = len(matrix) # numero de linhas [i,0]
        self.M = len(matrix[0]) if self.N > 0 else 0 # numero de colunas [0,j]
        self.edges_hash, self.edges_active_hash = self.initialize_edges_maps()

    def initialize_edges_maps(self):
        edges_hash = {}
        edges_active_hash = {}
        for i in range(self.N):
            for j in range(self.M):
                edges_hash[(i, j)] = [('h',i,j), ('h',i+1,j), ('v',i,j), ('v',i,j+1)]
                edges_active_hash[('h',i,j)] = "0"
                edges_active_hash[('h',i+1,j)] = "0"
                edges_active_hash[('v',i,j)] = "0"
                edges_active_hash[('v',i,j+1)] = "0"
        return edges_hash, edges_active_hash

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
    
    def invalidate_edges_that_border_zero_edge_cells(self, row:int, column:int):
        """Invalida as arestas que fazem fronteira com células que têm valor 0"""
        for edge in self.get_cell_edges(row, column):
            if self.edges_active_hash[edge] == "1":
                self.invalidate_edge(edge)

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
    
    def make_copy_with_edge_activation(self, edge:tuple):
        """Devolve uma cópia do tabuleiro, ou seja, uma nova instância da classe Board
        com o mesmo estado do tabuleiro atual, mas com a aresta enviada no argumento ativada."""
        new_board = self.make_copy()
        new_board.activate_edge(edge)
        return new_board
    
    def make_move(self, edge:tuple):
        """Devolve uma cópia do tabuleiro, ou seja, uma nova instância da classe Board
        com o mesmo estado do tabuleiro atual, mas com a aresta enviada no argumento ativada
        e as arestas que fazem fronteira com células que têm valor 0 invalidadas."""
        new_board = self.make_copy_with_edge_activation(edge)
        for cell in self.get_cells_bordering_edge(edge):
            if self.board[cell[0]][cell[1]] == 0:
                new_board.invalidate_edges_that_border_zero_edge_cells(cell[0], cell[1])
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
        # TODO
        pass


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass


    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    # TODO:
    board = Board.parse_instance()
    print(board.adjacent_cell((3,1)))
    print(board.get_cell_edges(3,1))
    print(board.get_cell_edges(4,4))
    board.activate_edge(('h',3,1))
    board.invalidate_edge(('h',4,1))
    print(board.get_active_edges(3,1))
    problem = Slitherlink(board)
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass







