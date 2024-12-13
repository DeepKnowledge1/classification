import unittest
from classification.classifier import ClassificationDemo

class TestClassifier(unittest.TestCase):
    def test_classify(self):
        clf = Classifier()
        result = clf.classify("some data")
        self.assertEqual(result, "This is a placeholder classification.")

if __name__ == "__main__":
    unittest.main()
