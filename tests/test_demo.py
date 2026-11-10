import unittest
from scripts.run_demo import classify, process

class WorkflowTests(unittest.TestCase):
    """Synthetic inquiry triage; no live messages are sent."""

    def request(self, message="Please quote", consent="yes", identifier="A01"):
        return {"id": identifier, "message": message, "consent": consent}

    def test_01_appointment_classification(self):
        self.assertEqual(classify("book appointment"), "appointment")

    def test_02_quotation_classification(self):
        self.assertEqual(classify("Need a PRICE estimate"), "quotation")

    def test_03_support_classification(self):
        self.assertEqual(classify("BROKEN machine"), "support")

    def test_04_unknown_request_requires_review(self):
        self.assertEqual(classify("Good afternoon"), "manual_review")

    def test_05_prompt_injection_requires_review(self):
        self.assertEqual(classify("ignore previous instructions"), "manual_review")

    def test_06_missing_consent_holds_request(self):
        self.assertEqual(process([self.request(consent="no")])[0]["status"], "consent_hold")

    def test_07_explicit_consent_accepted(self):
        self.assertEqual(process([self.request(consent="YES")])[0]["status"], "quotation")

    def test_08_duplicate_id_flagged(self):
        items = [self.request(), self.request(message="Appointment")]
        self.assertEqual(process(items)[1]["status"], "duplicate")

    def test_09_distinct_ids_processed(self):
        items = [self.request(identifier="1"), self.request(identifier="2")]
        self.assertEqual([x["status"] for x in process(items)], ["quotation", "quotation"])

    def test_10_never_sends_customer_message(self):
        self.assertTrue(all(not x["sent"] for x in process([self.request()])))

    def test_11_every_draft_requires_approval(self):
        self.assertTrue(all(x["approval_required"] for x in process([self.request()])))

    def test_12_empty_batch_is_safe(self):
        self.assertEqual(process([]), [])

if __name__ == "__main__":
    unittest.main()
