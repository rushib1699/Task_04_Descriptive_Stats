#!/usr/bin/env python3
import csv, sys, math
from collections import Counter, defaultdict

def is_numeric_list(vals):
    return all(_is_num(v) for v in vals if v != "")

def _is_num(s):
    try:
        float(s)
        return True
    except:
        return False

def compute_numeric_stats(nums):
    n = len(nums)
    mean = sum(nums) / n if n else None
    mn, mx = (min(nums), max(nums)) if nums else (None, None)
    var = sum((x - mean)**2 for x in nums) / (n - 1) if n > 1 else 0.0
    std = math.sqrt(var)
    return {"count": n, "mean": mean, "min": mn, "max": mx, "std": std}

def compute_categorical_stats(vals):
    vals = [v for v in vals if v != ""]
    cnt = len(vals)
    uniq = len(set(vals))
    top = Counter(vals).most_common(5)
    return {"count": cnt, "unique": uniq, "top_5": top}

def analyze(rows, headers):
    cols = {h: [r[h] for r in rows] for h in headers}
    stats = {}
    for h, vals in cols.items():
        if is_numeric_list(vals):
            nums = [float(v) for v in vals if v != ""]
            stats[h] = compute_numeric_stats(nums)
        else:
            stats[h] = compute_categorical_stats(vals)
    return stats

def group_by(rows, group_cols):
    grouped = defaultdict(list)
    for r in rows:
        key = tuple(r[g] for g in group_cols)
        grouped[key].append(r)
    return grouped

def print_stats(title, stats):
    print(f"\n=== {title} ===")
    for col, s in stats.items():
        print(f"{col}: {s}")

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_pure.py <csv_file> [group_col1 [group_col2 ...]]")
        sys.exit(1)

    path = sys.argv[1]
    groups = sys.argv[2:]

    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames

    # Overall
    overall = analyze(rows, headers)
    print_stats("Overall statistics", overall)

    # Grouped
    if groups:
        gb = group_by(rows, groups)
        for key, subset in gb.items():
            title = f"Group {groups} = {key}"
            stats = analyze(subset, headers)
            print_stats(title, stats)

if __name__ == "__main__":
    main()
