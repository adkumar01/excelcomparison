# Registers the xlsx textconv driver for this clone (git config is not versioned).
git config diff.xlsx.textconv "python tools/xlsx2txt.py"
git config diff.xlsx.cachetextconv true
git config core.hooksPath tools/hooks   # pre-commit hook keeps .xlsx.txt sidecars in sync
Write-Host "Done. Try: git diff --no-index samples/budget.xlsx samples/budget_updated.xlsx"
