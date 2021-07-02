import numpy as np
from tree import TreeNode


def simulate(root, s, nsims):
    for _ in range(nsims):
        mcts(s, root)  # deep copy bc making moves modifies board (s)


def mcts(game, node):
    if game.is_draw():
        backpropagate(0.0, node)
    elif game.is_win():
        backpropagate(1.0, node)
    elif node.isleaf:
        node.isleaf = False
        r = expand(node, game)
        backpropagate(r, node)
    else:
        W, N, P = children_stats(node)
        child = node.children[argmaxUCT(W, N, P)]
        game.play_move(child.A)
        mcts(game, child)


def expand(node, s):
    x = alphazero_rep(s)  # convert board to features

    p, v = nnet()
    a, vp = valid_policy(s, p)

    node.children = [TreeNode(a, vp, node) for (a, vp) in zip(a, vp)]
    return v


def backpropagate(r, node):
    while node != None:
        node.W += r
        node.N += 1.0
        node = node.parent
        r = -r


def argmaxUCT(W, N, P, c=2.0):
    Q = [0.0 if N == 0.0 else W/N for (W, N) in zip(W, N)]
    U = c * P / (1 + N) * np.sqrt(np.sum(N))
    UCT = Q + U
    return np.argmax(UCT)
