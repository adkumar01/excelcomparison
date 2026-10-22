"""Generate two sample workbooks that differ in a few known ways."""
import os

from openpyxl import Workbook

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "samples")
os.makedirs(OUT, exist_ok=True)


def build(version):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget"
    ws.append(["Item", "Q1", "Q2", "Total"])
    rows = [("Hardware", 1000, 1200), ("Software", 800, 900), ("Travel", 300, 250)]
    if version == 2:
        rows[0] = ("Hardware", 1100, 1200)  # changed value
        rows.append(("Training", 150, 200))  # added row
    for i, (name, q1, q2) in enumerate(rows, start=2):
        ws.append([name, q1, q2, f"=B{i}+C{i}"])
    if version == 2:
        notes = wb.create_sheet("Notes")  # added sheet
        notes.append(["Revised after Q2 review"])
    return wb


build(1).save(os.path.join(OUT, "budget.xlsx"))
build(2).save(os.path.join(OUT, "budget_updated.xlsx"))
print("samples written to", os.path.normpath(OUT))
