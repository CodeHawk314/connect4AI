class TreeNode:

    def __init__(self):
        self.isleaf  # at the bottom of the mcts search tree?
        self.W  # store the children's Weight
        self.N  # ... Count

        self.A   # UCI move to get here
        self.P   # ... Policy

        self.parent  # store pointer to parent
        self.children  # store pointer to each child node

    def children_stats(self):
        return [(W, N, P) for W, N, P in zip(self.W, self.N, self.P)]
