import unittest
from main import CSP

class CSPTest(unittest.TestCase):
    def consistent(self, coloring, constrains, colorable):
        if colorable:
            for i in constrains:
                if i[0] not in coloring or i[1] not in coloring:
                    return False
                if coloring[i[0]] == coloring[i[1]]:
                    return False
            return True
        else:
            if len(coloring) > 0:
                return False
            else:
                return True

    def test_gc_78317094521100(self):
        csp = CSP("coloring/gc_78317094521100.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, True))

    def test_gc_78317097930400(self):
        csp = CSP("coloring/gc_78317097930400.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, False))

    def test_gc_78317097930401(self):
        csp = CSP("coloring/gc_78317097930401.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, False))

    def test_gc_78317100510400(self):
        csp = CSP("coloring/gc_78317100510400.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, True))

    def test_gc_78317103208800(self):
        csp = CSP("coloring/gc_78317103208800.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, True))


    def test_gc_1378296846561000(self):
        csp = CSP("coloring/gc_1378296846561000.txt")
        coloring = csp.solve()
        self.assertTrue(self.consistent(coloring, csp.constrains, True))


if __name__ == '__main__':
    unittest.main()