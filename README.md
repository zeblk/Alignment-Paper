# Alignment Paper

## Layout

| Folder | Contents |
| --- | --- |
| `PNAS second submission/` | **Live working draft.** The revise-and-resubmit manuscript and cover letter (seeded from the first submission), the response to reviewers, and `revision notes.md`. |
| `PNAS first submission/` | The manuscript as first submitted to PNAS (`PNAS first submission.tex`) and its cover letter. Frozen — do not edit. |
| `assets/` | Shared across all documents: `proxyfailure.bib`, `signature.png`, `figures/`. |
| `tools/` | Bibliography helper scripts. |
| `Old/` | Superseded material, kept for reference: `Long Paper/`, `Outline/`, `eLife Cover Letter/`, `PNAS Proposal/`, `PNAS Paper/` (earlier PNAS drafts and pre-submission reviews), and loose archived drafts and cut material. |

## Building

Each document compiles from inside its own folder:

```sh
cd "PNAS second submission" && latexmk -pdf "PNAS second submission.tex"
```

Shared assets are referenced with relative paths (`../assets/...` from a top-level folder, `../../assets/...` from inside `Old/`), so the working
directory matters — run `latexmk` from the document's own folder, not the repo root.

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored.
