# excelcomparison

Why GitHub can't diff Excel files, and how to get readable diffs anyway.

`.xlsx` is a zipped bundle of XML, which git treats as an opaque binary. GitHub's web UI shows "Binary file not shown" and can't render a diff. These options fix that.

## 1. Local `git diff` (textconv)

`.gitattributes` maps `*.xlsx` to a `diff=xlsx` driver, and `tools/xlsx2txt.py` converts a workbook to one line per cell.

```powershell
pip install openpyxl
.\setup.ps1            # registers the driver in your local git config (once per clone)
git diff --no-index samples/budget.xlsx samples/budget_updated.xlsx
git diff               # also works for committed history, `git log -p`, `git show`
```

`git config` isn't versioned, so each clone needs `setup.ps1`. This only affects the command line and desktop tools that honor textconv. The GitHub website ignores it.

## 2. On GitHub: PR comment from CI

`.github/workflows/xlsx-diff.yml` runs on pull requests that touch `.xlsx`/`.xlsm` files. It converts the base and head versions to text and posts the diff as a PR comment and in the job summary.

Try it: on a branch, replace `samples/budget.xlsx` with `samples/budget_updated.xlsx`, open a PR against `main`, and read the bot comment.

## 3. Other options

- **Sidecar text file**: commit a generated `book.xlsx.txt` next to each workbook, so the normal Files changed tab shows a diff.
- **Rich visual diffs**: Microsoft Spreadsheet Compare (Windows), xlCompare, or Beyond Compare.
- **Better source format**: where you can, keep data as CSV or Flat OPC XML, which diff natively.

## Limits

The converter compares values and formulas only. Formatting, charts, macros, and pivot tables are not compared. Formula cached values appear only for files last saved by Excel.
