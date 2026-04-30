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
        self.arestas_hash = {}
        for i in range(self.N):
            for j in range(self.M):
                self.arestas_hash[(i, j)] = [('h',i,j), ('h',i+1,j), ('v',i,j), ('v',i,j+1)]



    def adjacent_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        # as celulas irao aparecer no formato WASD
        # ATENCAO: celulas nas extremidades nem sempre teem WASD completo
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
        #TODO
        #pass

    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve as arestas da célula enviada no argumento"""
        #TODO
        return self.arestas_hash[(row, column)]
        pass

    def get_active_edges(self, row:int, column:int) -> list:
        """Devolve o número de arestas ativas"""
        #TODO
        pass


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
    print(board.adjacent_cell((0,0)))
    problem = Slitherlink(board)
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass







