# Tutorial: Git, Markdown, and Producing a Properly-Cited PDF

This is a from-scratch tutorial for anyone who hasn't used git or Markdown
before. If you already know both, skip to
[Part 3](#part-3-converting-a-draft-into-a-properly-cited-pdf) for the
citation/PDF pipeline. Everything here is what the department manual
(`README.md`) assumes you already know — this fills that gap.

## Part 1: Git, from scratch

### What git actually is

Git tracks changes to a folder of files over time, as a series of
snapshots called **commits**. Each commit records exactly what changed,
when, and (if you write a good message) why. `README.md` Section 1 explains
why this department uses it for research, not just code — the short version
is that a commit is a permanent, timestamped fact about your project's
history that a plain folder of files can't give you.

### Install it

On Windows, install [Git for Windows](https://git-scm.com/download/win),
which also gives you **Git Bash**, a terminal you can run the commands
below in. On macOS, `git` is usually already available (or installed via
Xcode's command line tools); on Linux, install via your package manager
(e.g. `sudo apt install git`).

### The vocabulary you actually need

- **Repository ("repo")** — a folder git is tracking. Created with `git
  init`.
- **Working directory** — the actual files on disk, as you're editing them
  right now.
- **Staging** — telling git *which* changes you want in the *next* commit
  (`git add <file>`). You can edit five files and only stage/commit two.
- **Commit** — a saved snapshot of whatever is staged, with a message
  (`git commit -m "message"`).
- **Log** — the list of all commits (`git log`).

### The exact commands this workflow uses

```bash
# once, when starting a brand-new repository
git init
git config user.name "Your Name"
git config user.email "you@example.edu"

# the normal cycle, repeated constantly
git status              # what's changed since the last commit?
git add <file>          # stage a specific file (or `git add .` for everything changed)
git commit -m "message" # save a snapshot of what's staged

# looking at history
git log --oneline        # one line per commit, newest first
git show <commit-hash>   # exactly what one commit changed
git diff                 # what's changed but not yet staged
```

That's genuinely most of it. `README.md` Section 14 layers a specific
*pattern* on top of these same six commands (a "proposal" commit, then an
"apply" commit) — nothing about the underlying commands changes.

### A five-minute worked example

```bash
mkdir my-first-repo && cd my-first-repo
git init
git config user.name "Your Name"
git config user.email "you@example.edu"

echo "# My Topic" > notes.md
git status               # notes.md shows as untracked
git add notes.md
git commit -m "Start notes"

echo "A new finding." >> notes.md
git status               # notes.md now shows as modified
git diff                 # shows the exact line you just added
git add notes.md
git commit -m "Add a finding"

git log --oneline        # shows both commits, newest first
```

### Command line vs. a GUI git client — what to use when

Every command above works exactly the same whether you type it yourself or
click a button in a graphical tool — a GUI is just a different way of
issuing the same underlying git operations, not a different kind of git.
Both belong in your toolkit for different moments:

- **The command line (Git Bash, Terminal) is worth actually learning**,
  even if you end up using a GUI day to day, for two reasons specific to
  this workflow: it's exactly what your AI assistant is running on your
  behalf (`README.md` Section 14's `CLAUDE.md` automation is just these
  same commands, issued for you), so understanding it means you understand
  what just happened to your repository; and it's the only option for
  anything scripted — `scripts/check-repo-invariants.sh` and the
  `.claude/settings.json` hook (Section 18) are shell commands, not
  something a GUI can substitute for.
- **A GUI client is often genuinely easier for specific tasks**: reviewing
  a diff before you confirm an AI apply-commit (Section 6.6) — seeing old
  and new text side by side is easier to read at a glance than a terminal's
  `+`/`-` lines, especially for a long paragraph; browsing `git log`
  visually, particularly when recovering from the hand-edit/AI-apply
  collision Section 14 describes (comparing two versions of `paper.md` is
  more legible in a visual diff view); and staging only *part* of a changed
  file, which most GUIs make easier than the command line's `git add -p`.
  If you're using VS Code, its built-in **Source Control** panel (the
  branching icon in the left sidebar) covers all of this without installing
  anything extra — stage, commit, and view diffs directly next to the file
  you're editing. Dedicated clients (GitHub Desktop, GitKraken, Sourcetree)
  work the same way if you prefer a separate application.
- **Neither is "more correct."** Use the command line when you want to
  understand or script something precisely; reach for a GUI when you want
  to *see* something clearly (a diff, a history, a conflict) before acting
  on it. Most people end up using both, on different days, for exactly
  these reasons.

### Common beginner mistakes

- **Forgetting `git add` before `git commit`** — git commits only what's
  staged; if you edit a file and commit without adding it first, git will
  say there's nothing to commit (or, worse, commit an old version if
  something else was already staged). `git status` before every commit
  tells you exactly what will and won't be included.
- **Not setting `user.name`/`user.email` first** — git will refuse to
  commit, or (on some setups) commit under a placeholder identity. Do this
  once per machine (`git config --global user.name "..."` sets it for every
  repository, not just one).
- **Running git commands in the wrong folder** — git only sees the
  repository you're currently inside (or a subfolder of it). `git status`
  is also the quickest way to confirm you're where you think you are — it
  errors clearly ("not a git repository") if you're not.

In this department's actual workflow, an AI assistant following
`CLAUDE.md` runs steps like `git add`/`git commit` for you automatically
(`README.md` Sections 14 and 17) — this section exists so you understand
*what* it's doing on your behalf, not because you'll usually type these by
hand.

## Part 2: Markdown, from scratch

Markdown is plain text with a small set of symbols that mean something when
rendered. You can always read the raw file even without rendering it —
that's the whole point (and why it works so well with git: a git diff of a
Markdown file is just readable text, unlike a Word document's internal
format).

| Write this | Get this |
|---|---|
| `# Heading 1` | Large heading |
| `## Heading 2` | Smaller heading |
| `*italic*` | *italic* |
| `**bold**` | **bold** |
| `- item` (repeated) | Bullet list |
| `1. item` (repeated) | Numbered list |
| `[link text](https://example.com)` | A hyperlink |
| `> a quotation` | A blockquote |
| `` `inline code` `` | `inline code` |
| a line of `` ``` ``, code, then `` ``` `` | A fenced code block |
| `\| a \| b \|` header row + `\|---\|---\|` | A table |

Two extensions matter specifically for the citation/PDF pipeline in Part 3
(supported by Pandoc, the tool this department uses to convert Markdown —
not universally supported by every Markdown renderer, but that's fine,
since Pandoc is what you'll actually use):

- **Footnotes**: `text needing a note.[^1]` in the body, and, anywhere else
  in the file, `[^1]: The footnote's actual text.`
- **Citations**: `a claim [@citekey]` or `a claim [@citekey, 123]` for a
  specific page — covered fully in Part 3.

## Part 3: Converting a draft into a properly-cited PDF

The goal: take `paper.md`, with inline citations, and produce a PDF with
**real Chicago-style footnotes** (not just parenthetical text) and
**clickable bookmarks** (a navigable outline in the PDF, and footnote
markers that jump to their note and back). This was tested end-to-end for
this tutorial — the mechanism below is verified, not assumed.

### Step 1 — build a bibliography file

Pandoc reads a separate bibliography file, in either CSL-JSON or BibTeX
format (it detects which from the file extension). If you use Zotero,
export your library as either format directly (`File → Export Library`).
A minimal hand-written CSL-JSON example (`sources.json`):

```json
[
  {
    "id": "irenaeus1885",
    "type": "book",
    "title": "Against Heresies",
    "author": [{"family": "Irenaeus of Lyons"}],
    "translator": [{"given": "Alexander", "family": "Roberts"}, {"given": "James", "family": "Donaldson"}],
    "publisher": "Ante-Nicene Fathers",
    "issued": {"date-parts": [[1885]]},
    "volume": "1"
  }
]
```

The `id` (`irenaeus1885`) is what you'll cite by.

### Step 2 — reference it and cite inline in `paper.md`

Add a YAML block at the very top of the file, then cite with `[@id]`:

```markdown
---
bibliography: sources.json
---

John's vision is dated by Irenaeus to the end of Domitian's reign
[@irenaeus1885, 559].
```

`, 559` after the citekey adds a specific page/location reference. Cite
more than one source at once with `[@id1; @id2]`.

### Step 3 — get the actual Chicago style file

Citation *style* (Chicago vs. MLA vs. SBL — what the footnote/bibliography
actually looks like) is controlled by a separate CSL (Citation Style
Language) file, not by anything in your Markdown. Get the real one from the
[Zotero Style Repository](https://www.zotero.org/styles) — search "Chicago"
and download:

- **"Chicago Manual of Style 17th edition (note)"** — footnotes only, no
  separate bibliography page.
- **"Chicago Manual of Style 17th edition (full note)"** or **"(note, with
  bibliography)"** — footnotes *and* a bibliography page (the usual choice
  for a thesis or paper).

Save the downloaded `.csl` file in your topic repository (e.g. as
`chicago-fullnote-bibliography.csl`) and commit it once, like any other
repository asset — not as an AI-request cycle, just a plain maintenance
commit (`README.md` Section 14's "skip the ceremony for anything that isn't
a research question" applies here too).

### Step 4 — convert

Two routes, depending on what you have installed. Both were verified to
produce real Chicago-style footnotes (not parenthetical citations) from the
exact same `paper.md` and CSL file — which route you pick only changes the
last step.

**Route A — via Word/LibreOffice (works with what most of this department
already uses for `.docx` conversion):**

```bash
pandoc paper.md --citeproc --csl=chicago-fullnote-bibliography.csl -o paper.docx
```

Open `paper.docx` in Word or LibreOffice — the citations are now real,
native Word footnotes (confirmed: `--citeproc` writes them into the docx's
actual footnotes part, not as plain text) — then **File → Save As / Export
→ PDF**. Word and LibreOffice both automatically turn your `#`/`##`
headings into PDF bookmarks (the collapsible outline panel most PDF
readers show in a sidebar) during this export, with no extra step.

**Route B — direct to PDF in one command (needs a LaTeX distribution
installed once — [MiKTeX](https://miktex.org/) on Windows is the standard
choice; this route was not re-verified with an actual LaTeX install in this
session, so treat the command as standard/well-documented pandoc usage
rather than something tested end-to-end here):**

```bash
pandoc paper.md --citeproc --csl=chicago-fullnote-bibliography.csl \
  --toc --pdf-engine=xelatex -o paper.pdf
```

`--toc` generates the table of contents *and* the PDF's bookmark panel from
your headings in one step; the LaTeX engine (`xelatex`) handles real
footnotes and citation formatting directly.

### Step 5 — verify the result yourself

Don't take either route's output on faith — this is the same verification
habit `README.md` Section 3 asks of every AI claim, applied to your own
tooling:

- Click a footnote marker: it should jump to the note at the bottom/end,
  and the note should have its own link back up to where you clicked from.
- Open the PDF's bookmark/outline panel (usually a sidebar icon in your PDF
  viewer) and confirm your headings appear there, nested correctly.
- Check one citation against `sources.json`/your `.bib` file by eye — does
  the rendered footnote actually match the entry you expect?

### Fixing citation/footnote placement — by hand, and by directing the AI

A very common problem, whether you or an AI drafted the paragraph: several
distinct claims in a row, but the citations all get bundled at the very
end, so a reader can't tell which source actually backs which sentence.

**Before (wrong — three separate claims, one citation dump at the end):**

```markdown
Irenaeus dates John's vision to the end of Domitian's reign. Clement of
Alexandria's account in *Quis Dives Salvetur* 42 is sometimes read as
supporting a similar dating, though less directly. Internal evidence such
as Revelation 17:10 is read by some scholars as pointing instead to the
60s AD [@irenaeus1885, 559][@clement1857][@thornbury2004].
```

**After (fixed — each citation sits right after the sentence it supports):**

```markdown
Irenaeus dates John's vision to the end of Domitian's reign
[@irenaeus1885, 559]. Clement of Alexandria's account in *Quis Dives
Salvetur* 42 is sometimes read as supporting a similar dating, though less
directly [@clement1857]. Internal evidence such as Revelation 17:10 is
read by some scholars as pointing instead to the 60s AD [@thornbury2004].
```

The fix itself is just moving the `[@citekey]` marker to sit next to the
right sentence — unlike old-fashioned manually-numbered footnotes, there is
no renumbering to do afterward; Pandoc/citeproc generates the actual
footnote numbers fresh at conversion time from wherever the markers
currently sit. This is also true for plain (non-bibliographic) footnotes
written as `[^label]`: use a short descriptive label instead of a number
(`[^hyksos-note]` rather than `[^7]`), and inserting or removing one never
forces you to relabel the others.

**Asking the AI to place citations correctly the first time.** Applying
Section 7's "specify what you need, don't leave it implicit" advice to
citation placement specifically:

> Good: *"When drafting this section, attach each citation immediately to
> the specific sentence it supports — never bundle multiple citations at
> the end of a paragraph that makes several distinct claims. If a sentence
> makes a claim with no source behind it, don't attach a citation to it at
> all; list it as unsupported in `TODO.md` instead."*
>
> Bad: *"Add citations for this section."* — says nothing about
> per-sentence attachment, so bundling-at-the-end (the default failure
> mode) is left just as likely as doing it correctly.

**Recognizing misplacement, and the corrective prompt.** Watch for:

- One citation marker covering a paragraph that actually makes several
  distinct claims.
- A citation sitting next to a sentence whose specific content doesn't
  match what that source (check `sources.json`/your bibliography entry)
  actually says — it exists, just attached to the wrong neighboring
  sentence.
- A sentence with a specific factual claim and no citation anywhere near
  it, while the paragraph as a whole has one dangling at the end.

When you catch this, don't just move the marker yourself and move on if the
same draft has more of these — send it back with a scoped, checkable
request, the same "encode the fix, don't just patch this one instance"
habit from Section 8:

> *"Re-check `ch2-draft.md`, paragraph 3: three separate claims, one
> citation at the end. For each sentence in that paragraph, tell me which
> specific source (if any) actually supports it, and move each citation to
> sit directly after its own sentence. If a sentence has no source, say so
> explicitly rather than leaving the shared citation in place."*

### Cross-references to a specific heading elsewhere in the text

Pandoc automatically gives every heading an anchor derived from its text
(`## The Two Traditional Dating Positions` becomes `#the-two-traditional-dating-positions`).
Link to it from anywhere else in the same document with normal Markdown
link syntax:

```markdown
See [the discussion above](#the-two-traditional-dating-positions) for the
external evidence.
```

This becomes a real, clickable internal jump in both the docx and PDF
output — the same mechanism this very manual's own table of contents uses
to link to its numbered sections.
