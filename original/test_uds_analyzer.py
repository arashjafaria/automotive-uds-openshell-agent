import unittest
import contextlib
from io import StringIO
from uds_analyzer import analyze_uds


class TestUDSAnalyzer(unittest.TestCase):

    SAMPLES_FULL = [
        (bytes.fromhex("10 03"), bytes.fromhex("50 03")),
        (bytes.fromhex("22 F1 90"), bytes.fromhex("62 F1 90 12 34")),
        (bytes.fromhex("22 F1 90"), bytes.fromhex("7F 22 31")),
        (bytes.fromhex("3E 00"), bytes.fromhex("7E 00")),
        (bytes.fromhex("27 01"), bytes.fromhex("7F 27 33")),
    ]

    def _capture_output(self, samples):
        captured = StringIO()
        with contextlib.redirect_stdout(captured):
            analyze_uds(samples)
        return captured.getvalue()

    def test_nrc_31_reported_as_request_out_of_range(self):
        """NRC 0x31 is reported as 'Request out of range'."""
        samples = [
            (bytes.fromhex("10 03"), bytes.fromhex("50 03")),
            (bytes.fromhex("22 F1 90"), bytes.fromhex("7F 22 31")),
        ]
        output = self._capture_output(samples)
        self.assertIn("0x31 (Request out of range): 1", output)

    def test_nrc_33_reported_as_security_access_denied(self):
        """NRC 0x33 is reported as 'Security Access Denied'."""
        samples = [
            (bytes.fromhex("10 03"), bytes.fromhex("50 03")),
            (bytes.fromhex("27 01"), bytes.fromhex("7F 27 33")),
        ]
        output = self._capture_output(samples)
        self.assertIn("0x33 (Security Access Denied): 1", output)

    def test_service_22_positive_response_detected(self):
        """Service 0x22 positive response is correctly detected."""
        samples = [
            (bytes.fromhex("22 F1 90"), bytes.fromhex("62 F1 90 12 34")),
        ]
        output = self._capture_output(samples)
        self.assertIn("Positive responses: 1", output)
        self.assertIn("Negative responses: 0", output)

    def test_five_samples_produce_three_positive_two_negative(self):
        """The five existing samples produce 3 positive and 2 negative responses."""
        output = self._capture_output(self.SAMPLES_FULL)
        self.assertIn("Positive responses: 3", output)
        self.assertIn("Negative responses: 2", output)


if __name__ == "__main__":
    unittest.main()