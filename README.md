# Alignment Paper

## Layout

| Folder | Contents |
| --- | --- |
| `PNAS second submission/` | **Live working draft.** Documents are grouped into `Paper/`, `Response to reviewers/` (including `reviews.txt`), and `Cover letter/`, each containing its LaTeX source, PDF, and local build artifacts. General revision notes remain in `revision notes.md`. |
| `PNAS first submission/` | The manuscript as first submitted to PNAS (`PNAS first submission.tex`) and its cover letter. Frozen — do not edit. |
| `assets/` | Shared across all documents: `proxyfailure.bib`, `signature.png`, `figures/`. |
| `tools/` | Bibliography helper scripts. |
| `Old/` | Superseded material, kept for reference: `Long Paper/`, `Outline/`, `eLife Cover Letter/`, `PNAS Proposal/`, `PNAS Paper/` (earlier PNAS drafts and pre-submission reviews), and loose archived drafts and cut material. |

## Building

Each document compiles from inside its own folder:

```sh
cd "PNAS second submission/Paper"
latexmk -pdf "PNAS second submission.tex"
```

Build the response and cover letter from their respective subfolders in the same way.

Shared assets are referenced with relative paths (`../assets/...` from a top-level folder, `../../assets/...` from a second-submission document folder or an archived document folder inside `Old/`), so the working
directory matters — run `latexmk` from the document's own folder, not the repo root.

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored.
