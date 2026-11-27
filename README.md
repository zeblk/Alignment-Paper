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

Each of these folders has a `.latexmkrc` that turns on SyncTeX for every build. Without it, a terminal build deletes the `.synctex.gz` that LaTeX Workshop uses to jump between the PDF and the source, and the jump shortcuts stop working until the source next changes. Copy the file into any new document folder.

Shared assets are referenced with relative paths (`../assets/...` from a top-level folder, `../../assets/...` from a second-submission document folder or an archived document folder inside `Old/`), so the working
directory matters — run `latexmk` from the document's own folder, not the repo root.

LaTeX build artifacts (`.aux`, `.bbl`, `.log`, …) are gitignored.

## Line references and marked changes

Changes since the first submission are marked by hand in the paper's source, so there is only one copy of the paper:

- `\rev{key}{text}` marks added or rewritten text. It prints in blue.
- `\del{text}` marks removed text. It prints in red strikethrough. `\del[key]{text}` also records its line number.

The response letter cites a keyed passage's line numbers with `\paperlines{key}`. The numbers are read from the paper's `.aux` file, so build the paper before the response.

For a clean copy, change `\markchangestrue` to `\markchangesfalse` near the top of the paper. Removed text then disappears, which shifts line numbers, so rebuild the response afterwards.
