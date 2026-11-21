#!/usr/bin/env python3
"""Heuristic, read-only frontend style inventory. Python 3.9+, stdlib only.

This is not a CSS/JS parser and does not produce design-system tokens by itself.
It provides traceable candidates for subsequent human/agent verification.
"""

import argparse
import json
import os
from pathlib import Path
import re
import sys

SKIP_DIRS = {
    ".git", ".agents", ".next", ".nuxt", ".output", ".turbo", ".vercel",
    "node_modules", "bower_components", "dist", "build", "coverage", "vendor",
    "target", "out", "storybook-static", "__pycache__", "venv", ".venv",
}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
VIEW_EXT = {".tsx", ".jsx", ".vue", ".svelte", ".html"}
CONFIG_NAMES = {
    "tailwind.config.js", "tailwind.config.cjs", "tailwind.config.mjs",
    "tailwind.config.ts", "postcss.config.js", "postcss.config.cjs",
    "postcss.config.mjs", "postcss.config.ts", "theme.ts", "theme.js",
    "theme.tsx", "theme.jsx", "tokens.json", "tokens.ts", "tokens.js",
}
CSS_VAR = re.compile(r"(?m)(--[A-Za-z0-9_-]+)\s*:\s*([^;}\n]+)")
CSS_DECL = re.compile(
    r"(?m)(?<![\w-])(color|background(?:-color)?|border(?:-[\w-]+)?-color|"
    r"font-family|font-size|font-weight|line-height|letter-spacing|"
    r"padding(?:-[\w-]+)?|margin(?:-[\w-]+)?|gap|row-gap|column-gap|"
    r"border-radius|box-shadow|transition(?:-[\w-]+)?|animation(?:-[\w-]+)?|"
    r"z-index|max-width|min-width|width)\s*:\s*([^;}\n]+)",
    re.IGNORECASE,
)
COLOR = re.compile(r"(?<![\w-])(?:#[a-fA-F0-9]{3,8}\b|(?:rgb|rgba|hsl|hsla|oklch|oklab)\([^\n)]{1,100}\))")
MEDIA = re.compile(r"@media\s*([^\{\n]{3,180})\s*\{")
FONT_FACE = re.compile(r"@font-face\s*\{")
CLASS_ATTR = re.compile(r"\bclass(?:Name)?\s*=\s*([\"'`])([^\n\"'`]{1,180})\1")


def snippet(s, max_len=180):
    return re.sub(r"\s+", " ", s.strip())[:max_len]


def line_number(content, offset):
    return content.count("\n", 0, offset) + 1


def add_hit(items, label, path, content, offset, value, sample_limit=4):
    entry = items.setdefault(label, {"count": 0, "examples": []})
    entry["count"] += 1
    if len(entry["examples"]) < sample_limit:
        entry["examples"].append({
            "file": path,
            "line": line_number(content, offset),
            "value": snippet(value),
        })


def detect_stack(root):
    package_file = root / "package.json"
    result = {"frameworkHints": [], "stylingHints": [], "packageJsonReadable": False}
    if not package_file.is_file() or package_file.is_symlink():
        return result
    try:
        content = json.loads(package_file.read_text(encoding="utf-8"))
        deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
        result["packageJsonReadable"] = True
        for name in ("react", "next", "vue", "nuxt", "svelte", "@sveltejs/kit", "astro", "@angular/core"):
            if name in deps:
                result["frameworkHints"].append(name)
        for name in ("tailwindcss", "sass", "styled-components", "@emotion/react", "@mui/material", "antd", "bootstrap", "@chakra-ui/react", "@radix-ui/react-dialog"):
            if name in deps:
                result["stylingHints"].append(name)
    except (OSError, UnicodeError, ValueError, TypeError):
        pass
    return result


def scan(root, max_files=2500, max_bytes=1024 * 1024):
    root = root.resolve()
    result = {
        "tool": "style_inventory.py",
        "disclaimer": "Heuristic inventory only. Validate evidence in code and rendered UI before exporting design rules.",
        "root": str(root),
        "stack": detect_stack(root),
        "scan": {"files": 0, "styleFiles": 0, "viewFiles": 0, "skippedLargeFiles": 0,
                 "readErrors": 0, "truncatedByMaxFiles": False},
        "styleConfigFiles": [],
        "customProperties": {},
        "declarations": {},
        "colors": {},
        "mediaQueries": {},
        "classAttributes": {},
        "fontFaceCount": 0,
    }
    seen = 0
    for current_dir, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and not (Path(current_dir) / d).is_symlink())
        for filename in sorted(files):
            fpath = Path(current_dir) / filename
            if fpath.is_symlink():
                continue
            suffix = fpath.suffix.lower()
            if filename in CONFIG_NAMES:
                result["styleConfigFiles"].append(fpath.relative_to(root).as_posix())
            if suffix not in STYLE_EXT | VIEW_EXT:
                continue
            if filename.endswith(".min.css"):
                continue
            if seen >= max_files:
                result["scan"]["truncatedByMaxFiles"] = True
                break
            seen += 1
            try:
                if fpath.stat().st_size > max_bytes:
                    result["scan"]["skippedLargeFiles"] += 1
                    continue
                content = fpath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                result["scan"]["readErrors"] += 1
                continue
            rel = fpath.relative_to(root).as_posix()
            result["scan"]["files"] += 1
            if suffix in STYLE_EXT:
                result["scan"]["styleFiles"] += 1
                for m in CSS_VAR.finditer(content):
                    add_hit(result["customProperties"], m.group(1), rel, content, m.start(), m.group(2))
                for m in CSS_DECL.finditer(content):
                    add_hit(result["declarations"], m.group(1).lower(), rel, content, m.start(), m.group(2))
                for m in COLOR.finditer(content):
                    add_hit(result["colors"], m.group(0).lower(), rel, content, m.start(), m.group(0))
                for m in MEDIA.finditer(content):
                    add_hit(result["mediaQueries"], snippet(m.group(1)), rel, content, m.start(), m.group(1))
                result["fontFaceCount"] += len(FONT_FACE.findall(content))
            if suffix in VIEW_EXT:
                result["scan"]["viewFiles"] += 1
                for m in CLASS_ATTR.finditer(content):
                    add_hit(result["classAttributes"], snippet(m.group(2), 100), rel, content, m.start(), m.group(2), 2)
        if result["scan"]["truncatedByMaxFiles"]:
            break
    for key in ("customProperties", "declarations", "colors", "mediaQueries", "classAttributes"):
        result[key] = dict(sorted(result[key].items(), key=lambda item: (-item[1]["count"], item[0]))[:200])
    result["styleConfigFiles"] = sorted(set(result["styleConfigFiles"]))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Root directory of the frontend repository")
    parser.add_argument("--out", type=Path, help="Write JSON report to this file (default: stdout)")
    parser.add_argument("--max-files", type=int, default=2500)
    parser.add_argument("--max-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"not a directory: {args.root}")
    if args.max_files < 1 or args.max_bytes < 1:
        parser.error("--max-files and --max-bytes must be positive")
    result = scan(args.root, args.max_files, args.max_bytes)
    rendered = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
        print(f"Inventory: {args.out} | files={result['scan']['files']} styles={result['scan']['styleFiles']} views={result['scan']['viewFiles']}")
    else:
        sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
