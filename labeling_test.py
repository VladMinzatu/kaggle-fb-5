import unittest
from labeling import Box
from labeling import split
from labeling import Node
from labeling import build_tree
from labeling import Labeler

class TestBox(unittest.TestCase):

    def test_assertions(self):
        self.assertRaises(AssertionError, Box, 1.0, 0.0, 1.0, 2.0)
        self.assertRaises(AssertionError, Box, 1.0, 2.0, 3.0, 2.0)

    def test_corners(self):
        b = Box(1.0, 2.0, 1.0, 2.0)
        self.assertTrue(b.contains(1.0, 1.0))
        self.assertTrue(b.contains(1.0, 2.0))
        self.assertTrue(b.contains(2.0, 1.0))
        self.assertTrue(b.contains(2.0, 2.0))

    def test_edges(self):
        b = Box(1.0, 2.0, 1.0, 2.0)
        self.assertTrue(b.contains(1.0, 1.5))
        self.assertTrue(b.contains(2.0, 1.5))
        self.assertTrue(b.contains(1.5, 1.0))
        self.assertTrue(b.contains(1.5, 2.0))

    def test_interior(self):
        b = Box(1.0, 2.0, 1.0, 2.0)
        self.assertTrue(b.contains(1.5, 1.5))
        self.assertTrue(b.contains(1.0 + 1e-9, 1.5))
        self.assertTrue(b.contains(1.5, 2.0 - 1e-9))

    def test_interior(self):
        b = Box(1.0, 2.0, 1.0, 2.0)
        self.assertFalse(b.contains(1.5, 2.5))
        self.assertFalse(b.contains(1.5, 2.0 + 1e-9))
        self.assertFalse(b.contains(1.0 - 1e-9, 1.5))

class TestSplit(unittest.TestCase):

    def test_split(self):
        (a,b,c,d) = split(Box(1.0, 2.0, 1.0, 2.0))

        self.assertAlmostEqual(a.min_x, 1.0)
        self.assertAlmostEqual(a.max_x, 1.5)
        self.assertAlmostEqual(a.min_y, 1.0)
        self.assertAlmostEqual(a.max_y, 1.5)

        self.assertAlmostEqual(b.min_x, 1.5)
        self.assertAlmostEqual(b.max_x, 2.0)
        self.assertAlmostEqual(b.min_y, 1.0)
        self.assertAlmostEqual(b.max_y, 1.5)

        self.assertAlmostEqual(c.min_x, 1.5)
        self.assertAlmostEqual(c.max_x, 2.0)
        self.assertAlmostEqual(c.min_y, 1.5)
        self.assertAlmostEqual(c.max_y, 2.0)

        self.assertAlmostEqual(d.min_x, 1.0)
        self.assertAlmostEqual(d.max_x, 1.5)
        self.assertAlmostEqual(d.min_y, 1.5)
        self.assertAlmostEqual(d.max_y, 2.0)

class TestNode(unittest.TestCase):

    def test_sub(self):
        n = Node(Box(1.0, 2.0, 1.0, 2.0), 'label')
        n.sub_a = 'A'
        n.sub_b = 'B'
        n.sub_c = 'C'
        n.sub_d = 'D'

        self.assertEqual(n.get_sub(1.2, 1.1), 'A')
        self.assertEqual(n.get_sub(1.5, 1.1), 'A')
        self.assertEqual(n.get_sub(1.5, 1.5), 'A')
        self.assertEqual(n.get_sub(1.6, 1.1), 'B')
        self.assertEqual(n.get_sub(1.6, 1.5), 'B')
        self.assertEqual(n.get_sub(1.6, 1.9), 'C')
        self.assertEqual(n.get_sub(2.0, 2.0), 'C')
        self.assertEqual(n.get_sub(1.5, 1.9), 'C')
        self.assertEqual(n.get_sub(1.4, 1.9), 'D')
        self.assertEqual(n.get_sub(1.0, 1.9), 'D')

class TestTreeBuilding(unittest.TestCase):

    def test_empty_tree(self):
        tree = build_tree(0, Box(1.0, 2.0, 1.0, 2.0), 'L')

        self.assertAlmostEqual(tree.box.min_x, 1.0)
        self.assertAlmostEqual(tree.box.max_x, 2.0)
        self.assertAlmostEqual(tree.box.min_y, 1.0)
        self.assertAlmostEqual(tree.box.max_y, 2.0)
        self.assertEqual(tree.label, 'L')
        self.assertEqual(tree.sub_a, None)
        self.assertEqual(tree.sub_b, None)
        self.assertEqual(tree.sub_c, None)
        self.assertEqual(tree.sub_d, None)

    def test_depth_one(self):
        tree = build_tree(1, Box(1.0, 2.0, 1.0, 2.0), 'L')

        self.assertEqual(tree.sub_a.label, 'La')
        self.assertAlmostEqual(tree.sub_a.box.min_x, 1.0)
        self.assertAlmostEqual(tree.sub_a.box.max_x, 1.5)
        self.assertAlmostEqual(tree.sub_a.box.min_y, 1.0)
        self.assertAlmostEqual(tree.sub_a.box.max_y, 1.5)

        self.assertEqual(tree.sub_b.label, 'Lb')
        self.assertAlmostEqual(tree.sub_b.box.min_x, 1.5)
        self.assertAlmostEqual(tree.sub_b.box.max_x, 2.0)
        self.assertAlmostEqual(tree.sub_b.box.min_y, 1.0)
        self.assertAlmostEqual(tree.sub_b.box.max_y, 1.5)

        self.assertEqual(tree.sub_c.label, 'Lc')
        self.assertAlmostEqual(tree.sub_c.box.min_x, 1.5)
        self.assertAlmostEqual(tree.sub_c.box.max_x, 2.0)
        self.assertAlmostEqual(tree.sub_c.box.min_y, 1.5)
        self.assertAlmostEqual(tree.sub_c.box.max_y, 2.0)

        self.assertEqual(tree.sub_d.label, 'Ld')
        self.assertAlmostEqual(tree.sub_d.box.min_x, 1.0)
        self.assertAlmostEqual(tree.sub_d.box.max_x, 1.5)
        self.assertAlmostEqual(tree.sub_d.box.min_y, 1.5)
        self.assertAlmostEqual(tree.sub_d.box.max_y, 2.0)

class TestLabeler(unittest.TestCase):

    def test_labeling(self):
        l = Labeler(1)

        self.assertEqual(l.get_label(2.0, 5.0), 'a')
        self.assertEqual(l.get_label(5.0, 2.0), 'a')
        self.assertEqual(l.get_label(6.0, 5.0), 'b')
        self.assertEqual(l.get_label(6.0, 7.0), 'c')
        self.assertEqual(l.get_label(4.0, 7.0), 'd')

        l = Labeler(3)
        self.assertEqual(l.get_label(1.1, 2.0), 'aad')
        self.assertEqual(l.get_label(2.0, 2.0), 'aac')
        self.assertEqual(l.get_label(2.6, 2.6), 'aca')

if __name__ == '__main__':
    unittest.main()
