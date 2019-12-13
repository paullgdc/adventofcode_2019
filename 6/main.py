from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

class Node:
    name: str
    children: List[Node]
    parent: Optional[Node]

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None

def get_node_or(nodes, name):
    node = nodes.get(name)
    if node is None:
        node = Node(name)
        nodes[name] = node
    return node

def build_tree(input_list):
    nodes = dict()
    for parent_name, child_name in input_list:
        parent = get_node_or(nodes, parent_name)
        child = get_node_or(nodes, child_name)
        parent.children.append(child)
        child.parent = parent
    return nodes

def sum_depth(root_node):
    to_see = [(root_node, 0)]
    total = 0
    while len(to_see) > 0:
        node, depth = to_see.pop()
        total += depth
        for child in node.children:
            to_see.append((child, depth + 1))
    return total

def parents_depth(start_node):
    current = start_node
    depth = 0
    parents = [(current, depth)]
    while current.parent is not None:
        current = current.parent
        depth += 1
        parents.append((current, depth))
    return parents

def find_depth_to_lca(nodes):
    you_parents = parents_depth(nodes["YOU"])
    san_parents = parents_depth(nodes["SAN"])
    for node1, node2 in zip(reversed(you_parents), reversed(san_parents)):
        if node1[0].name != node2[0].name:
            break
    return node1[1] + node2[1]

with open("input.txt") as f:
    parent_children_list = [tuple(line.strip().split(")")) for line in f]

nodes = build_tree(parent_children_list)
print(sum_depth(nodes["COM"]))
print(find_depth_to_lca(nodes))