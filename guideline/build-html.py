#!/usr/bin/env python3
"""Regenerate the HTML equivalent of every markdown file in guideline/.

Run this after editing any .md source. Requires pandoc on PATH.
Diagrams (assets/*.svg) are spliced in as inline SVG (not <img src=...>)
so they inherit the page's CSS variables and work in light/dark mode.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

WORKFLOW_SVG = (ASSETS / "workflow-diagram.svg").read_text(encoding="utf-8")
COMMIT_SVG = (ASSETS / "commit-graph.svg").read_text(encoding="utf-8")


def diagram_block(svg: str, caption: str) -> str:
    return f'\n\n<div class="diagram">\n{svg}\n<p class="step" style="text-align:center;opacity:.7;font-size:.85rem;margin-top:.5rem">{caption}</p>\n</div>\n\n'


def splice(text: str, anchor: str, block: str, after: bool = True) -> str:
    idx = text.index(anchor)  # raises if not found -- fail loudly, don't silently skip
    pos = idx + len(anchor) if after else idx
    return text[:pos] + block + text[pos:]


# HTML is generated only for documentation/instructional files (the manual,
# READMEs, CLAUDE.md instructions) -- NOT for the files a live topic
# repository actually maintains as working data (TODO.md, sources.md,
# paper.md, ai-requests/*/question.md|answer.md). Those change every AI
# cycle; an HTML mirror of them would go stale immediately and isn't
# documentation, so it's intentionally out of scope here.
#
# (markdown path, html path, title, relative path to assets/, toc?, crumb html or None)
FILES = [
    ("README.md", "README.html", "Working with AI in Theological Research and Paper Writing", "assets", True, None),
    ("access-control-for-it.md", "access-control-for-it.html", "Access control for research git repositories -- IT guidance", "assets", True,
     '<a href="README.html">&larr; back to the department manual</a>'),
    ("tutorial-git-markdown-pdf.md", "tutorial-git-markdown-pdf.html", "Tutorial: Git, Markdown, and Producing a Properly-Cited PDF", "assets", True,
     '<a href="README.html">&larr; back to the department manual</a>'),
    ("templates/new-topic-repo/README.md", "templates/new-topic-repo/README.html", "Template: new topic repository", "../../assets", False,
     '<a href="../../README.html">&larr; back to the department manual</a>'),
    ("templates/new-topic-repo/CLAUDE.md", "templates/new-topic-repo/CLAUDE.html", "Template: CLAUDE.md maintenance instructions", "../../assets", False,
     '<a href="../../README.html">&larr; back to the department manual</a>'),
    ("templates/new-topic-repo/DEPARTMENT-RULES.md", "templates/new-topic-repo/DEPARTMENT-RULES.html", "Template: DEPARTMENT-RULES.md", "../../assets", False,
     '<a href="../../README.html">&larr; back to the department manual</a>'),
    ("example/README.md", "example/README.html", "Worked example: revelation-dating", "../assets", False,
     '<a href="../README.html">&larr; back to the department manual</a>'),
    ("example/CLAUDE.md", "example/CLAUDE.html", "Worked example: CLAUDE.md", "../assets", False,
     '<a href="../README.html">&larr; back to the department manual</a> &middot; <a href="README.html">example overview</a>'),
]


def build_one(md_rel, html_rel, title, cssrelpath, toc, crumb):
    md_path = ROOT / md_rel
    html_path = ROOT / html_rel
    text = md_path.read_text(encoding="utf-8")

    if md_rel == "README.md":
        text = splice(
            text,
            "doing, and what's still genuinely yours to decide.",
            diagram_block(WORKFLOW_SVG, "The propose → apply → fact-check cycle (Section 13)."),
        )
    if md_rel == "example/README.md":
        text = splice(
            text,
            "fact-checking catches an AI hallucination (a fabricated journal article), not\na complete treatment of the dating question.",
            diagram_block(COMMIT_SVG, "The actual commit history of this example repository."),
        )

    cmd = [
        "pandoc", "-f", "gfm", "-t", "html5", "--standalone",
        "--template", str(ASSETS / "pandoc-template.html"),
        "--metadata", f"title={title}",
        "--metadata", f"cssrelpath={cssrelpath}",
    ]
    if crumb:
        cmd += ["--variable", f"crumb={crumb}"]
    if toc:
        cmd += ["--toc", "--toc-depth=2"]
    html_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(cmd, input=text, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(f"FAILED: {md_rel}\n{result.stderr}", file=sys.stderr)
        return False
    html_path.write_text(result.stdout, encoding="utf-8")
    print(f"built {html_rel}")
    return True


def main():
    ok = True
    for row in FILES:
        ok = build_one(*row) and ok
    if not ok:
        sys.exit(1)
    print(f"\n{len(FILES)} files built.")


if __name__ == "__main__":
    main()
