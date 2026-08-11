# Alignment Paper

## Layout

| Folder | Contents |
| --- | --- |
| `Long Paper/` | Current version of the full-length manuscript (`paper.tex`) — the live working draft. |
| `eLife Cover Letter/` | Cover letter for the eLife submission (`cover_letter.tex`). |
| `PNAS Proposal/` | The PNAS Perspective proposal. |
| `PNAS Paper/` | The PNAS version of the manuscript — not yet started. |
| `assets/` | Shared across all documents: `proxyfailure.bib`, `signature.png`, `figures/`. |
| `archive/` | Superseded drafts and cut material — kept for reference, not compiled. |
| `tools/` | Bibliography helper scripts. |

## Building

Each document compiles from inside its own folder:

```sh
cd "Long Paper" && latexmk -pdf paper.tex
```

Shared assets are referenced with relative paths (`../assets/...`), so the working
directory matters — run `latexmk` from the document's own folder, not the repo root.

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored.
