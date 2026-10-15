import contextlib
import importlib.util
import io
import pathlib
import unittest
from unittest.mock import patch

root = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cupp_choice_test", root / "cupp.py")
cupp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cupp)


class DownloadChoiceTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch.dict(cupp.CONFIG, {"global": {"dicturl": "https://example.invalid/"}}))

    def test_invalid_input_is_revalidated_after_invalid_range(self):
        with patch("builtins.input", side_effect=["39", "not a number", "1"]), patch.object(cupp, "download_wordlist_http") as download, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cupp.download_wordlist(), "1")
        download.assert_called_once_with("1")

    def test_nondecimal_digit_and_zero_are_rejected(self):
        with patch("builtins.input", side_effect=["²", "0", "1"]), patch.object(cupp, "download_wordlist_http") as download, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cupp.download_wordlist(), "1")
        download.assert_called_once_with("1")

    def test_exit_and_surrounding_whitespace(self):
        with patch("builtins.input", return_value=" 38 "), patch.object(cupp, "download_wordlist_http") as download, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cupp.download_wordlist(), "38")
        download.assert_called_once_with("38")


if __name__ == "__main__":
    unittest.main()
