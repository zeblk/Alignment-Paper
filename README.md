# Alignment Paper

## Layout

| Folder | Contents |
| --- | --- |
| `paper/` | Current version of the manuscript (`paper.tex`) — the live working draft. |
| `cover-letter/` | Submission cover letter (`cover_letter.tex`). |
| `pnas/` | PNAS materials: the accepted Perspective proposal, and the PNAS version of the manuscript (in preparation). |
| `assets/` | Shared across all documents: `proxyfailure.bib`, `signature.png`, `figures/`. |
| `archive/` | Superseded drafts and cut material — kept for reference, not compiled. |
| `tools/` | Bibliography helper scripts. |

## Building

Each document compiles from inside its own folder:

```sh
cd paper && latexmk -pdf paper.tex
```

Shared assets are referenced with relative paths (`../assets/...`), so the working
directory matters — run `latexmk` from the document's folder, not the repo root.

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored.
