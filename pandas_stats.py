#!/usr/bin/env python3
import sys
import pandas as pd

def main():
    if len(sys.argv) < 2:
        print("Usage: pandas_stats.py <csv_file> [group_col1 [group_col2 ...]]")
        sys.exit(1)

    path = sys.argv[1]
    groups = sys.argv[2:]
    df = pd.read_csv(path)

    # Overall
    print("\n=== Overall statistics (describe) ===")
    print(df.describe(include="all"))

    # unique & freq for categoricals
    print("\n=== Unique counts ===")
    print(df.nunique())
    for col in df.select_dtypes(include="object").columns:
        print(f"\n--- Top values for {col} ---")
        print(df[col].value_counts().head(5))

    # Grouped
    if groups:
        grouped = df.groupby(groups)
        print(f"\n=== Grouped by {groups}: describe() ===")
        print(grouped.describe())

        for col in df.select_dtypes(include="object").columns:
            print(f"\n=== Grouped value_counts for {col} ===")
            # unstack to turn counts into a table
            print(grouped[col].value_counts().unstack(fill_value=0).head())

if __name__ == "__main__":
    main()
