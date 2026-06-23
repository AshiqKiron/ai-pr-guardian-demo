import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.scan_pr import PolicyEngine, CodeScanner

class TestPolicyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PolicyEngine('.ai-guardrails/policies.yaml')
    
    def test_load_policies(self):
        policies = self.engine.get_active_policies()
        self.assertIsInstance(policies, list)
        self.assertGreater(len(policies), 0)

if __name__ == '__main__':
    unittest.main()
