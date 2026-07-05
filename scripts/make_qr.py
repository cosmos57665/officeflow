"""Create a high-error-correction QR code for the deployed OfficeFlow URL."""
import argparse
from pathlib import Path

import qrcode
from PIL import Image


DEFAULT_OUTPUT = Path("qr_officeflow.png")


def make_qr(url: str, output_path: Path = DEFAULT_OUTPUT, size_px: int = 800) -> Path:
    if not url.strip():
        raise ValueError("A deployed URL is required.")

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url.strip())
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    image = image.resize((size_px, size_px), Image.Resampling.NEAREST)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="PNG")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create qr_officeflow.png for slides.")
    parser.add_argument("url", help="Deployed Streamlit app URL")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="PNG output path (default: qr_officeflow.png)",
    )
    args = parser.parse_args()
    output = make_qr(args.url, args.output)
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
