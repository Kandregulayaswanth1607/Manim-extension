"""Finding (and optionally downloading) picture files."""
from __future__ import annotations

import urllib.request
from pathlib import Path
from urllib.parse import urlparse

EXTS = (".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif")

# Folders searched in order. Default: ./assets next to wherever you run manim.
_dirs: list[Path] = [Path.cwd() / "assets"]


def add_asset_dir(path) -> None:
    """Add a folder to search first (it also becomes the download target)."""
    p = Path(path).expanduser().resolve()
    if p in _dirs:
        _dirs.remove(p)
    _dirs.insert(0, p)


def asset_dirs() -> list[Path]:
    return list(_dirs)


def resolve(name) -> Path | None:
    """'cat' -> assets/cat.png (or .jpg/.svg/...). A real path also works."""
    p = Path(str(name)).expanduser()
    if p.is_file():
        return p
    for d in _dirs:
        for ext in ("",) + EXTS:
            c = d / f"{name}{ext}"
            if c.is_file():
                return c
    return None


def fetch(url: str, name: str, subdir: str = "") -> Path:
    """Download and cache an HTTP(S) asset (maximum 25 MiB)."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Asset URL must use HTTP or HTTPS.")
    if not name or Path(name).name != name or "/" in name or "\\" in name or name in {".", ".."}:
        raise ValueError("name must be a plain filename without path components.")
    relative_dir = Path(subdir) if subdir else Path()
    if relative_dir.is_absolute() or ".." in relative_dir.parts or "\\" in subdir:
        raise ValueError("subdir must stay inside the asset directory.")
    dest_dir = (_dirs[0] / relative_dir).resolve()
    root = _dirs[0].resolve()
    if dest_dir != root and root not in dest_dir.parents:
        raise ValueError("subdir must stay inside the asset directory.")
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = Path(parsed.path).suffix.lower() or ".png"
    if ext not in EXTS:
        raise ValueError(f"Unsupported remote asset extension: {ext}")
    dest = dest_dir / f"{name}{ext}"
    if dest.exists():
        return dest
    req = urllib.request.Request(url, headers={"User-Agent": "manim-pics/0.2"})
    temporary = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            length = response.headers.get("Content-Length")
            if length and int(length) > 25 * 1024 * 1024:
                raise ValueError("Remote asset exceeds the 25 MiB download limit.")
            data = response.read(25 * 1024 * 1024 + 1)
            if len(data) > 25 * 1024 * 1024:
                raise ValueError("Remote asset exceeds the 25 MiB download limit.")
        temporary.write_bytes(data)
        temporary.replace(dest)
    finally:
        if temporary.exists():
            temporary.unlink()
    return dest
