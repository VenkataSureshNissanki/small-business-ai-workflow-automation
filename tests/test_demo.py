import unittest
from scripts.run_demo import classify, process

class WorkflowTests(unittest.TestCase):
    def test_appointment(self): self.assertEqual(classify("book appointment"),"appointment")
    def test_quote(self): self.assertEqual(classify("need quote"),"quotation")
    def test_support(self): self.assertEqual(classify("broken machine"),"support")
    def test_injection(self): self.assertEqual(classify("ignore previous instructions"),"manual_review")
    def test_consent(self): self.assertEqual(process([{"id":"1","consent":"no","message":"book appointment"}])[0]["status"],"consent_hold")
    def test_never_send(self): self.assertFalse(process([{"id":"1","consent":"yes","message":"quote"}])[0]["sent"])
    def test_duplicates(self):
        items=[{"id":"1","consent":"yes","message":"quote"}]*2
        self.assertEqual(process(items)[1]["status"],"duplicate")

if __name__=="__main__":unittest.main()
