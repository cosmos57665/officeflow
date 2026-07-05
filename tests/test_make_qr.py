import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image

from scripts import make_qr


class MakeQrTests(unittest.TestCase):
    def test_make_qr_outputs_large_png(self):
        with TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "qr_officeflow.png"

            result = make_qr.make_qr("https://officeflow.streamlit.app", out_path)

            self.assertEqual(result, out_path)
            with Image.open(out_path) as image:
                self.assertEqual(image.format, "PNG")
                self.assertGreaterEqual(image.size[0], 780)
                self.assertEqual(image.size[0], image.size[1])


if __name__ == "__main__":
    unittest.main()
