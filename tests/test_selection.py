import itertools
import tempfile
import unittest
from pathlib import Path

from sigma_reveal import _Node, _subtree_knapsack, reveal


class SelectionTests(unittest.TestCase):
    def test_optimality_and_ancestor_closure(self):
        nodes = [_Node(i, str(i), 0, True, str(i), cost, score)
                 for i, (cost, score) in enumerate([(1, 1), (2, 3), (1, 5), (3, 4)])]
        nodes[0].children = [nodes[1], nodes[3]]
        nodes[1].children = [nodes[2]]
        for budget in range(9):
            selected = _subtree_knapsack(nodes[0], budget)
            feasible_scores = [0]
            for flags in itertools.product((False, True), repeat=4):
                subset = {i for i, flag in enumerate(flags) if flag}
                if subset and 0 not in subset:
                    continue
                if 2 in subset and 1 not in subset:
                    continue
                if sum(nodes[i].cost_b for i in subset) <= budget:
                    feasible_scores.append(sum(nodes[i].mu for i in subset))
            self.assertLessEqual(sum(nodes[i].cost_b for i in selected), budget)
            self.assertEqual(sum(nodes[i].mu for i in selected), max(feasible_scores))
            self.assertTrue(2 not in selected or 1 in selected)

    def test_rendered_budget_and_determinism(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'data').mkdir()
            (root / 'data/sales.csv').write_text('year,revenue\n2025,12\n')
            (root / 'run.py').write_text('print("hello")\n')
            for budget in (0, 15, 16, 32, 80, 2400):
                result = reveal(directory, 'Analyze sales.csv', budget)
                self.assertLessEqual(len(result), budget)
                self.assertEqual(result, reveal(directory, 'Analyze sales.csv', budget))
            self.assertIn('sales.csv', reveal(directory, 'Analyze sales.csv'))


if __name__ == '__main__':
    unittest.main()
