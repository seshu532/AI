"""
Authors: Krikor Herlopian & Seshaiah Erugu , small implementation to Monte Carlo tree search
"""

import math
from collections import defaultdict
# abc. This module provides the infrastructure for defining abstract base classes (ABCs)  in Python
from abc import abstractmethod, ABC




class MonteCarloTreeSearch:
    "The Monte Carlo tree search algorithm. We First rollout the tree , then we choose a move. It follows 4 steps. Select, Expand, simulate,backpropagate."

    def __init__(self, weight=1):
        self.weight = weight
        self.totalVisit = defaultdict(int)
        self.totalReward = defaultdict(int)
        self.children = dict()  # children of each node

    def choose(self, child):
        if child.isLeaf():
            raise RuntimeError("choose called on leaf node {node}")

        if child not in self.children:
            return child.findRandomChild()

        def score(s):
            if self.totalVisit[s] == 0:
                return float("-inf")  # avoid unseen moves
            return self.totalReward[s] / self.totalVisit[s]  # average reward
        return max(self.children[child], key=score)

    def  makeRollout(self, node):
        path = self.select(node)
        leaf = path[-1]
        self.expand(leaf)
        reward = self.simulate(leaf)
        self.backPropagate(path, reward)
       

    def select(self, node):
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                return path
            notExplored = self.children[node] - self.children.keys()
            if notExplored:
                n = notExplored.pop()
                path.append(n)
                return path
            node = self.uctSelect(node)

    def expand(self, node):
        if node in self.children:
            return
        self.children[node] = node.findChildren()

    def simulate(self, node):
        invertReward = True
        while True:
            if node.isLeaf():
                reward = node.reward()
                if invertReward:
                    return 1 - reward
                else:
                    return reward
            node = node.findRandomChild()
            invertReward = not invertReward

    def backPropagate(self, path, reward):
        for node in reversed(path):
            self.totalVisit[node] = self.totalVisit[node] + 1
            self.totalReward[node] = self.totalReward[node] + reward
            reward = 1 - reward  # one for me is, zero for my enemy.

    def uctSelect(self, node):
        assert all(child in self.children for child in self.children[node])

        logN = math.log(self.totalVisit[node])

        def uct(n):
            return self.totalReward[n] / self.totalVisit[n] + self.weight * math.sqrt(
                logN / self.totalVisit[n]
            )

        return max(self.children[node], key=uct)


class Node(ABC):
    @abstractmethod
    def __eq__(node1, node2):
        return True
        
    @abstractmethod
    def reward(self):
        "0=loss, 1=win, 0.5=tie"
        return 0
    
    @abstractmethod
    def findRandomChild(self):
        return None
    
    @abstractmethod
    def findChildren(self):
        return set()

    @abstractmethod
    def __hash__(self):
        return 123456789

    @abstractmethod
    def isLeaf(self):
        "It will return if the node has no children, thus meaning the leaf."
        return True


