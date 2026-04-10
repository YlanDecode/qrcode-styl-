from pathlib import Path
from urllib.parse import urlparse

import qrcode

try:
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.colormasks import RadialGradiantColorMask
    from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
except ImportError:
    StyledPilImage = None
    RoundedModuleDrawer = None
    RadialGradiantColorMask = None


URLS_FILE = Path("urls.txt")


def slug_from_url(url: str) -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/").replace("/", "-")
    return f"{domain}-{path}".strip("-") or "qrcode"


def make_qr(url: str, output_dir: Path) -> Path:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=14,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    if StyledPilImage and RoundedModuleDrawer and RadialGradiantColorMask:
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            color_mask=RadialGradiantColorMask(
                center_color=(20, 25, 35),
                edge_color=(25, 135, 210),
            ),
        )
    else:
        img = qr.make_image(fill_color="black", back_color="white")

    output_path = output_dir / f"{slug_from_url(url)}.png"
    img.save(output_path)
    return output_path


def load_urls(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Le fichier '{file_path}' est introuvable. Cree-le avec 1 URL par ligne."
        )

    lines = file_path.read_text(encoding="utf-8").splitlines()
    urls = [
        line.strip()
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]

    if not urls:
        raise ValueError(f"Le fichier '{file_path}' est vide. Ajoute au moins une URL.")

    return urls


def main() -> None:
    output_dir = Path("qrcode_image_list")
    output_dir.mkdir(exist_ok=True)
    urls = load_urls(URLS_FILE)

    for url in urls:
        path = make_qr(url, output_dir)
        print(f"OK: {url} -> {path}")


if __name__ == "__main__":
    main()
