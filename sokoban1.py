#!/usr/local/anaconda2.7/bin/python2.7
# -*- coding: utf-8 -*-

# By xuesj from 2016/4/26

import numpy as np
import pdb

(UP, DOWN, LEFT, RIGHT) = (0, 1, 2, 3)
DIR = ('^', 'V', '<', '>')

"""
Define a Exception of OutOfBoard, when we setup a game.
"""
class OutOfBoard(Exception):
    def __init__(self, *args):
        if args:
            self._msg = args[0]
        else:
            self._msg = None

    def __str__(self):
        if self._msg:
            return "Out of the board {0}".foramt(self._msg)
        else:
            return "Out og the board"


"""
Board is the Board of Game, a two dimentions array of boolean.
if the position e.g. (x, y) is on board, board(x, y) is True, or is by False.
"""
class Board(object):
    def __init__(self, alist):
        self._board = np.array(alist)
        self._x, self._y = self._board.shape

    """
    test if pos, a tuple, e.g. is on the board.
    """
    def is_on_board(self, pos):
        if pos[0] in range(self._x) and pos[1] in range(self._y):
            return self._board[pos]
        else:
            return 0

    def get_shape(self):
        return self._x, self._y

    """
    Test if pos,e.g. (x, y) is empty on board acording objs.
    usage:
	board.is_empty((1, 3), man, box1, box2)
    boxlist = [box1, box2]
    board.is_empty((1, 3), man, *boxlist)
    """
    def is_empty(self, pos, *objs):
        if not self.is_on_board(pos):
            return False
        if pos not in objs:
            return True


"""
The Game class have a board, man, boxes_state(set of pos) ,
and have a start_state(set of pos of boxes) and end_state(set of pos of boxes).
The Game manage a 3 list to record the network of game's state,
also node of network, a node record the state of game, when a move occur,
the state of game will change, we will record another node,
the connection of the two nodes is the move.
The algorithm is :
1. we initialize first node of the network,e.g.
the first state is game's start_state, the parent
state is None(or the same with the start_state), the first move is None.
2. we do a iteration from the network which is stored in the list:
    1)check the node, if it is the target node, or
    2)expend the network by next move and next node.
"""
class Game(object):
    """
    init the game with board, man's position, start_box_state, end_box_state.
    """
    def __init__(self, board, man_pos, start_box_pos, end_box_pos):
        self._board = board
        poses = {man_pos} | start_box_pos | end_box_pos
        if not self.is_on_board(*poses):
            raise OutOfBoard
        else:
            self._man_pos = man_pos
            self._start_box_pos = start_box_pos
            self._end_box_pos = end_box_pos
            self._box_pos = start_box_pos

            self._man_nodes = []    # _man_node[i] is man's a position of _nodes[i].
            self._nodes = []        # record the box's positions.
            self._index = []        # the _nodes[_index[i]] is parent node of the _node[i].
            self._moves = []        # moves[i] record the move from parent to the nodes[i],((x,y),d)).
            self._cur_index = 0     # current node index to be searched.

            self._man_nodes.append(man_pos)
            self._nodes.append(start_box_pos)
            self._index.append(0)
            self._moves.append(None)
            self._non_reachable = Game.is_not_reachable(board, end_box_pos)


    """
    Append a new node in the net, append a new node of the list.
    parameters: p_index is the index of parent, move is the move from parent node to the node
    through the move, man_pos is the position of the man dedrived from the move.
    return: n_index, the new node's index
    """
    def append_node(self, p_index, man_pos, new_node, move):
        self._index.append(p_index)
        self._man_nodes.append(man_pos)
        self._nodes.append(new_node)
        self._moves.append(move)
        n_index = len(self._nodes) - 1
        return n_index


    """
    Compute the next node.
    paramenters is cur_box_pos, move
    return is next_box_pos.
    """
    @staticmethod
    def compute_node(box_pos, move):
        man_pos = Game.get_man_pos(move)
        box, direct = move
        new_box_pos = box_pos - {box}
        if direct == UP:
           new_box = (box[0] - 1, box[1])
        if direct == DOWN:
           new_box = (box[0] + 1, box[1])
        if direct == LEFT:
           new_box = (box[0], box[1] - 1)
        if direct == RIGHT:
           new_box = (box[0], box[1] + 1)

        return new_box_pos | {new_box}


    """
    Handle a node.
    find all possible move, append new nodes into the net.
    Parameter i: the node[i] to handle.
    return:
    """
    def handle_node(self, i):
        parent_node = self._nodes[i]
        man_pos = self._man_nodes[i]
        moves = Game.get_all_moves(self._board, man_pos, parent_node)

        for move in moves:
            new_node = Game.compute_node(parent_node, move)
            man_pos = Game.get_man_pos(move)
            if new_node & self._non_reachable:               # if new node have a pos is nonreachable, continue.
                continue
            if new_node not in self._nodes:                  # new node for the exist net.
                self.append_node(i, man_pos, new_node, move)
            else:               # the node exist in the net, but we will test the man pos.
                j = self._nodes.index(new_node)
                man_pos_j = self._man_nodes[j]
                man_state = Game.get_man_state(self._board, man_pos, new_node)
                # man_state_j = Game.get_man_state(self._board, man_pos_j, new_node)
                #if man_state <> man_state_j:
                #    self.append_node(i, man_pos, new_node, move)
                if man_pos_j not in man_state:
                    self.append_node(i, man_pos, new_node, move)

    """
    Build and search the net.
    from node 0, repaet the cycle until find the target node.
    if reach the end of the net, return False.
    parameters: target_pos, the set of target boxes, i, the node index to be searched.
    return: i if find the target nodes[i], 0 if target not found.
    """
    def search_net(self, target_pos, i=0):
        while self._nodes[i] <> target_pos:
            self.handle_node(i)
            i += 1
            if i >= len(self._nodes):
                return 0
        if self._nodes[i] == target_pos:
            return i


    """
    Define get_all_moves, get all possible moves acording man_pos, box_pos.
    parameters: board, man_pos, box_pos
    return moves, list of (pos, direct), is is a form of (x, y).
    """
    @staticmethod
    def get_all_moves(board, man_pos, box_pos):
        moves = set()
        man_state = Game.get_man_state(board, man_pos, box_pos)
        for box in box_pos:
            if board.is_empty((box[0] + 1, box[1]), *box_pos) and \
               board.is_empty((box[0] - 1, box[1]), *box_pos):
                if (box[0] + 1, box[1]) in man_state:
                    moves.add((box, UP))
                if (box[0] - 1, box[1]) in man_state:
                    moves.add((box, DOWN))
            if board.is_empty((box[0], box[1] + 1), *box_pos) and \
               board.is_empty((box[0], box[1] - 1), *box_pos):
                if (box[0], box[1] + 1) in man_state:
                    moves.add((box, LEFT))
                if (box[0], box[1] - 1) in man_state:
                    moves.add((box, RIGHT))
        return moves


    """
    Define get man's position from the move of the board.
    parameters: move (box_pos, direct)
    return: man_pos
    """
    @staticmethod
    def get_man_pos(move):
        box_pos, direct = move
        if direct == UP:
            man_pos = (box_pos[0] + 1, box_pos[1])
        if direct == DOWN:
            man_pos = (box_pos[0] - 1, box_pos[1])
        if direct == LEFT:
            man_pos = (box_pos[0], box_pos[1] + 1)
        if direct == RIGHT:
            man_pos = (box_pos[0], box_pos[1] - 1)
        return man_pos


    """
    check if an set of pos in the board.
    the pos is a of tuple, e.g. (i,j) means the state of an obj.
    """
    def is_on_board(self, *poses):
        for pos in poses:
            if not self._board.is_on_board(pos):
                raise OutOfBoard
        return True


    """
    Get the set of (x, y) which is the man could reach at now.
    Game.get_man_state(board, (0, 0), start_box_pos)
    """
    @staticmethod
    def get_man_state(board, man_pos, box_pos):
        set_a = set()
        set_a.add(man_pos)
        #man_state = {man_pos}
        set_b = Game.get_neighbors(board, set_a, box_pos)
        while set_a <> set_a | set_b:
            set_a = set_a | set_b
            set_b = Game.get_neighbors(board, set_a, box_pos)
        return set_a


    """
    get the direct connected points of set of points, e.g. man_state, for example {(0, 0 )}.
    Usage: Game.get_neighbors(board, {(0, 3)}, start_box_pos)
    """
    @staticmethod
    def get_neighbors(board, man_state, box_pos):
        new_set = set()
        for (x, y) in man_state:
            if board.is_empty((x - 1, y), *box_pos):
                new_set.add((x-1, y))
            if board.is_empty((x + 1, y), *box_pos):
                new_set.add((x+1, y))
            if board.is_empty((x, y - 1), *box_pos):
                new_set.add((x, y-1))
            if board.is_empty((x, y + 1), *box_pos):
                new_set.add((x, y+1))
        return new_set


    """
    Get the direct reachable position of a box.
    parameters: board , box_set is set of pos, e.g. {(x, y), ...}
    return: set of positions {(x, y), ...}
    """
    @staticmethod
    def get_reachable(board, box_set):
        new_set = set()
        for (x, y) in box_set:
            # pdb.set_trace()
            if board.is_empty((x - 1, y)) and board.is_empty((x + 1, y)):
                new_set.add((x - 1, y))
                new_set.add((x + 1, y))
            if board.is_empty((x, y - 1)) and board.is_empty((x, y + 1)):
                new_set.add((x, y - 1))
                new_set.add((x, y + 1))
        return new_set


    """
    Get the set of (x, y) which is the box could reach.
    parameters:
    return:
    """
    @staticmethod
    def get_box_state(board, box_pos):
        set_a = box_pos
        set_b = Game.get_reachable(board, box_pos)
        while set_a <> set_a | set_b:
            set_a = set_a | set_b
            set_b = Game.get_reachable(board, set_a)
        return set_a


    """
    Get the distance of two box, e.g. get_box_dustance(board, box1, box2).
    parameters: board, box1, box2
    return: number of distance, range(1, n), 0 if not reachable.
    """
    @staticmethod
    def get_box_distance(board, box1, box2):
        i = 1
        set_a = {box1}
        #set_b = Game.get_reachable(board, box_pos)
        while set_a:
            if box2 in set_a:
                return i
            else:
                set_a = Game.get_reachable(board, set_a)
                i += 1
        return 0 


    """
    Get the set of (x, y) which is the box could reach.
    parameters: board, end_pos: set of end box positions.
    return: set of box position which could not reach the end box position.
    """
    @staticmethod
    def is_not_reachable(board, end_pos):
        new_set = set()
        x, y  = board.get_shape()
        for i in range(x):
            for j in range(y):
                if not board.is_on_board((i, j)):
                    continue
                box_set = Game.get_box_state(board, {(i, j)})
                if not box_set & end_pos:
                    new_set.add((i, j))

        return new_set


if __name__ == '__main__':

    thelist = [
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 1]
        ]

    board = Board(thelist)
    man_pos = (4, 4)
    start_box_pos = {(1, 4), (2, 4), (3, 4)}
    end_box_pos = {(0, 0), (0, 1), (0, 2)}
    game = Game(board, man_pos, start_box_pos, end_box_pos)

    i = game.search_net(end_box_pos)

    solution = []
    j = i
    while j <> 0:
        solution.append(game._moves[j])
        j = game._index[j]

    solution = solution[::-1]

    for move in solution:
        pos, direct = move
        print("({0},{1}):{2}".format(pos[0], pos[1], DIR[direct])),
