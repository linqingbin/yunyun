import unittest
from yunyun import route

class Test(unittest.TestCase):

    def test1(self):
        feature_weights,scores = [['f1', 1], ['f2', 2]],[['f1', 't1', 2], ['f1', 't2', 1], ['f2', 't1', 0], ['f2', 't2', 1]]
        df = route.parse(feature_weights,scores)
        print(df)

if __name__ == '__main__':
    unittest.main()

