#!/usr/local/anaconda2.7/bin/python2.7
# -*- coding: utf-8 -*-

# xuesj at 2016/4/26

import pytest
import pdb
from sokoban1 import Board, OutOfBoard, Game
from sokoban1 import UP, DOWN, LEFT, RIGHT

# from sukoban import UP, DOWN, LEFT, RIGHT

def test_board():
    thelist = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 0],
    ]

    board = Board(thelist)

    x, y = board.get_shape()
    for i in range(x):
	for j in range(y):
            assert board.is_on_board((i, j)) == thelist[i][j]

    assert not board.is_on_board((3, 0))
    assert not board.is_on_board((0, 4))
    assert not board.is_on_board((2, 2))
    assert not board.is_on_board((2, 3))
    assert not board.is_on_board((2, 4))
    assert board.is_on_board((1, 3))
    assert board.is_on_board((2, 1))
    assert board.is_on_board((1, 2))

    # test a empty position
    man = (0, 0)
    box1 = (0, 1)
    box2 = (0, 2)
    boxlist1 = [box1, box2]
    boxlist2 = (box1, box2)
    boxlist3 = {box1, box2}
    assert board.is_empty((1, 3), man, box1, box2)
    assert board.is_empty((1, 3), man, *boxlist1)
    assert not board.is_empty((0, 2), man, *boxlist1)
    assert not board.is_empty((2, 3), man, *boxlist2)
    assert not board.is_empty((0, 4), man, *boxlist3)
    assert board.is_empty((0, 0), *boxlist3)


"""
def test_obj():
    obj11 = Obj((1, 1))
    obj01 = Obj((0, 1))
    obj21 = Obj((2, 1))
    obj10 = Obj((1, 0))
    obj12 = Obj((1, 2))
    obj11.move(UP)
    assert obj11 == obj01
    obj11.move(DOWN)
    assert obj11.get_pos() == (1, 1)
    obj11.move(LEFT)
    assert obj11 == obj10
    obj = obj11.move(RIGHT)
    assert obj11.get_pos() == (1, 1)
"""


"""
def test_box():
    thelist = [
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 0, 0],
    ]
    board = Board(thelist)
    pos = (2, 1)
    box1 = Box(pos, board)
    assert pos == box1.get_pos()

    pos = (2, 3)
    with pytest.raises(OutOfBoard):
        box1 = Box(pos, board)

    box2 = Box((2, 0), board)
    assert box2 <> box1

    boxes = set()
    for box in (box1, box2):
        boxes.add(box.get_pos())

    box3 = Box((2, 1), board)
    box4 = Box((1, 3), board)
    assert box3.get_pos() in boxes
    assert box4.get_pos() not in boxes

    box11 = Box((1, 1), board)
    assert box11.move(UP).get_pos() == (0, 1)
    assert box11.move(DOWN).get_pos() == (1, 1)
    assert box11.move(LEFT).get_pos() == (1, 0)
    assert box11.move(RIGHT).get_pos() == (1, 1)

    # test get_movables method of Box
    box00 = Box((0, 0), board)
    box02 = Box((0, 2), board)
    box10 = Box((1, 0), board)
    box11 = Box((1, 1), board)
    box20 = Box((2, 0), board)

    boxlist = [box00, box02, box10, box11, box20]
    boxes = set()
    for box in boxlist:
        boxes.add(box.get_pos())

    assert not box00.get_movables(*boxes)
    assert box02.get_movables(*boxes) == {((0, 2), LEFT), ((0, 2), RIGHT)}
    assert not box10.get_movables(*boxes)
    assert box11._board.is_empty((0, 1), *boxes)
    assert not box20.get_movables(*boxes)
    assert box11.get_movables(*boxes) == {((1, 1), UP), ((1, 1), DOWN)}
"""

# test man's init
#def test_man():
#    thelist = [
#    [1, 1, 1, 1],
#    [1, 1, 1, 1],
#    [1, 1, 0, 0],
#    ]
#    board = Board(thelist)

#    man = Man((0, 0), board)
#    assert man.get_pos() == (0, 0)
#    with pytest.raises(OutOfBoard):
#        man1 = Man((-1, 0), board)

def test_game():
    thelist = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 0],
    ]

    board = Board(thelist)
    man_pos1 = (0, 0)
    man_pos2 = (0, 3)
    start_box_pos = {(0, 2), (1, 1)}
    end_box_pos = {(2, 0), (2, 1)}

    game1 = Game(board, man_pos1, start_box_pos, end_box_pos)
    game2 = Game(board, man_pos2, start_box_pos, end_box_pos)
    assert game1

    with pytest.raises(OutOfBoard):
        game_err = Game(board, man_pos1, {(-1, 0)}, end_box_pos)
        game_err = Game(board, (-1, 0), start_box_pos, end_box_pos)
        game_err = Game(board, man_pos1, start_box_pos,{(-1, 0)})

    # test get_neighbors()
    assert Game.get_neighbors(board, {(0, 0)}, start_box_pos) == {(0, 1), (1, 0)}
    assert Game.get_neighbors(board, {(0, 3)}, start_box_pos) == {(1, 3)}

    # test Game.get_man_state()
    man_state1 = Game.get_man_state(board, man_pos1, start_box_pos)
    assert man_state1 == {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)}

    man_state2 = Game.get_man_state(board, man_pos2, start_box_pos)
    assert man_state2 == {(0, 3), (1, 2), (1, 3)}

    # test get_man_pos()
    assert Game.get_man_pos(((1, 1), UP)) == (2, 1)
    assert Game.get_man_pos(((1, 1), DOWN)) == (0, 1)
    assert Game.get_man_pos(((1, 1), LEFT)) == (1, 2)
    assert Game.get_man_pos(((1, 1), RIGHT)) == (1, 0)

    # test get_all_moves(board, man_pos, box_pos)
    moves = Game.get_all_moves(board, man_pos1, start_box_pos)
    assert moves == {((0, 2), RIGHT), ((1, 1), UP), ((1, 1), DOWN), ((1, 1), RIGHT)}
    moves = Game.get_all_moves(board, man_pos2, start_box_pos)
    assert moves == {((0, 2), LEFT), ((1, 1), LEFT)}

    # test get_man_pos(def get_man_pos(move)
    assert Game.get_man_pos(((0, 2), LEFT)) == (0, 3)
    assert Game.get_man_pos(((1, 1), UP)) == (2, 1)
    assert Game.get_man_pos(((1, 1), DOWN)) == (0, 1)
    assert Game.get_man_pos(((1, 1), RIGHT)) == (1, 0)

    # test compute_node(box_pos, move)
    box_pos = start_box_pos
    move = ((0, 2), RIGHT)
    assert Game.compute_node(box_pos, move) == {(0, 3), (1, 1)}
    move = ((1, 1), RIGHT)
    assert Game.compute_node(box_pos, move) == {(0, 2), (1, 2)}
    move = ((1, 1), UP)
    assert Game.compute_node(box_pos, move) == {(0, 2), (0, 1)}
    move = ((1, 1), DOWN)
    assert Game.compute_node(box_pos, move) == {(0, 2), (2, 1)}
    move = ((1, 1), LEFT)
    assert Game.compute_node(box_pos, move) == {(0, 2), (1, 0)}

    # test __init__(self, board, man_pos, start_box_pos, end_box_pos)
    man_pos = (0, 0)
    game = Game(board, man_pos, start_box_pos, end_box_pos)
    assert game._board == board
    assert game._man_pos == man_pos
    assert game._start_box_pos == start_box_pos
    assert game._end_box_pos == end_box_pos
    assert game._box_pos == start_box_pos

    assert game._man_nodes[0] == man_pos
    assert game._nodes[0] == start_box_pos
    assert game._index[0] == 0
    assert game._moves[0] == None
    assert game._cur_index == 0
    assert len(game._nodes) == 1
    assert len(game._man_nodes) == 1
    assert len(game._index) == 1

    # test append_node(self, p_index, man_pos, new_node, move)
    p_index = 0
    move = ((1, 1), UP)
    man_pos = Game.get_man_pos(move)
    new_node = Game.compute_node(game._nodes[p_index], move)
    game.append_node(p_index, man_pos, new_node, move)
    assert len(game._nodes) == 2
    assert len(game._man_nodes) == 2
    assert len(game._index) == 2
    assert len(game._moves) == 2

    assert game._nodes[1] == {(0, 2), (0, 1)}
    assert game._index[1] == 0

    # test handle_node(self, i)
    thelist = [
    [1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 0, 0],
    ]

    board = Board(thelist)
    man_pos = (0, 0)
    start_box_pos = {(0, 2), (1, 1)}
    end_box_pos = {(2, 0), (2, 1)}

    game = Game(board, man_pos, start_box_pos, end_box_pos)
    moves = Game.get_all_moves(game._board, man_pos, start_box_pos)
    assert moves == {((0, 2), RIGHT), ((1, 1), UP), ((1, 1), DOWN), ((1, 1), RIGHT)}
    assert game._non_reachable == {(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)}

    game.handle_node(0)
    #assert len(game._nodes) == 5
    #assert len(game._man_nodes) == 5
    #assert len(game._index) == 5
    #assert len(game._moves) == 5

    #assert game._index[1:5] == [0, 0, 0, 0]
    #assert {x for x in game._moves[1:5]} == moves
    #for x in game._nodes[1:5]:
    #    assert x in [{(0, 3), (1, 1)}, {(0, 2), (0, 1)},
    #                 {(0, 2), (2, 1)}, {(0, 2), (1, 2)}]

    # test search_net(self, target_pos, i=0)
    i = game.search_net(end_box_pos)
    assert i == 0

    board = Board(thelist)
    man_pos = (0, 3)
    start_box_pos = {(1, 1), (1, 2)}
    end_box_pos = {(2, 0), (2, 1)}

    game = Game(board, man_pos, start_box_pos, end_box_pos)
    i = game.search_net(end_box_pos)
    # pdb.set_trace()
    assert i

    # test get_reachable(board, box_set)
    box_set = {(0, 0)}
    assert  not Game.get_reachable(board, box_set)
    box_set = {(0, 1)}
    assert  Game.get_reachable(board, box_set) == {(0, 0), (0, 2)}
    box_set = {(1, 0)}
    assert  Game.get_reachable(board, box_set) == {(0, 0), (2, 0)}
    box_set = {(1, 1)}
    assert  Game.get_reachable(board, box_set) == {(0, 1), (2, 1), (1, 0), (1, 2)}

    # test get_box_state(board, box_pos)
    box_set = {(0, 0)}
    assert  Game.get_box_state(board, box_set) == {(0, 0)}
    box_set = {(2, 1)}
    assert  Game.get_box_state(board, box_set) == {(2, 1)}
    box_set = {(0, 1)}
    assert  Game.get_box_state(board, box_set) == {(0, 0), (0, 1), (0, 2), (0, 3)}
    box_set = {(1, 0)}
    assert  Game.get_box_state(board, box_set) == {(0, 0), (1, 0), (2, 0)}
    box_set = {(1, 1)}
    assert  Game.get_box_state(board, box_set) == {(0, 0), (0, 1), (0, 2), (0, 3),
                                                   (1, 0), (1, 1), (1, 2), (1, 3),
                                                   (2, 0), (2, 1)}

    # test is_not_reachable(board, end_pos)
    non_reachable = Game.is_not_reachable(board, end_box_pos)
    assert (0, 0) in non_reachable
    assert (0, 1) in non_reachable
    assert (0, 2) in non_reachable
    assert (0, 3) in non_reachable
    assert (1, 3) in non_reachable
    assert not (1, 0) in non_reachable


    # test get_box_dsitance(board, box1, box2)
    thelist = [
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 1]
        ]

    board = Board(thelist)
    man_pos = (5, 4)
    start_box_pos = {(1, 4), (2, 4), (3, 4)}
    end_box_pos = {(0, 0), (0, 1), (0, 2)}
    game = Game(board, man_pos, start_box_pos, end_box_pos)

    assert Game.get_box_distance(board, (0, 0), (0, 0)) == 1
    assert Game.get_box_distance(board, (0, 1), (0, 2)) == 2
    assert Game.get_box_distance(board, (0, 2), (0, 1)) == 0
    assert Game.get_box_distance(board, (1, 1), (0, 4)) == 7
    assert Game.get_box_distance(board, (0, 1), (0, 0)) == 2
    assert Game.get_box_distance(board, (5, 4), (4, 4)) == 0
    assert Game.get_box_distance(board, (4, 4), (5, 4)) == 2


    # test search_net(self, target_pos, i=0) for a real game of sokoban.
    """
    thelist = [
        [1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 1, 1]
        ]

    board = Board(thelist)
    man_pos = (5, 4)
    start_box_pos = {(1, 4), (2, 4), (3, 4)}
    end_box_pos = {(1, 5), (2, 5), (3, 5)}
    game = Game(board, man_pos1, start_box_pos, end_box_pos)
    """
