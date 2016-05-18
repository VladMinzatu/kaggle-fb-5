class Box:

    def __init__(self, min_x, max_x, min_y, max_y):
        assert min_x < max_x, "min_x ({}) must be smaller than max_x ({})".format(min_x, max_x)
        assert min_y < max_y, "min_y ({}) must be smaller than max_y ({})".format(min_y, max_y)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def contains(self, x, y):
        return x >= self.min_x and x <= self.max_x and y >= self.min_y and y <= self.max_y

def split(b):
    half_x = b.min_x + (b.max_x - b.min_x) / 2.0
    half_y = b.min_y + (b.max_y - b.min_y) / 2.0
    return (Box(b.min_x, half_x, b.min_y, half_y),
            Box(half_x, b.max_x, b.min_y, half_y), 
            Box(half_x, b.max_x, half_y, b.max_y),
            Box(b.min_x, half_x, half_y, b.max_y))

class Node:

    def __init__(self, box, label):
        self.box = box
        self.label = label
        self.sub_a = None
        self.sub_b = None
        self.sub_c = None
        self.sub_d = None

    def get_sub(self, x, y):
        assert self.box.contains(x,y), "({},{}) coordinates are outside this node's box ({}, {}, {}, {})".format(x, y, self.box.min_x, self.box.max_x, self.box.min_y, self.box.max_y)
        (a,b,c,d) = split(self.box)
        if a.contains(x,y):
            return self.sub_a
        if b.contains(x,y):
            return self.sub_b
        if c.contains(x,y):
            return self.sub_c
        if d.contains(x,y):
            return self.sub_d
        assert False, "({},{}) pair could not be assigned to any subnode of current node with box ({}, {}, {}, {})".format(x, y, self.box.min_x, self.box.max_x, self.box.min_y, self.box.max_y)

def build_tree(depth, box, label):
    assert depth >= 0, "Tree depth must be >= 0"
    node = Node(box, label)
    if depth == 0:
        return node
    else:
        (a, b, c, d) = split(box)
        node.sub_a = build_tree(depth - 1, a, label + 'a')
        node.sub_b = build_tree(depth - 1, b, label + 'b')
        node.sub_c = build_tree(depth - 1, c, label + 'c')
        node.sub_d = build_tree(depth - 1, d, label + 'd')
        return node

class Labeler:

    def __init__(self, depth):
        assert depth > 0, "Tree depth must be > 0"
        self.tree = build_tree(depth, Box(0.0, 10.0, 0.0, 10.0), '')

    def get_label(self, x, y):
        label = self.tree.label
        node = self.tree
        while node != None:
            label = node.label
            node = node.get_sub(x,y)
        return label

