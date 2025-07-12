#!/usr/bin/env python3
import sys
import polars as pl

def main():
    if len(sys.argv) < 2:
        print("Usage: polars_stats.py <csv_file> [group_col1 [group_col2 ...]]")
        sys.exit(1)

    path = sys.argv[1]
    groups = sys.argv[2:]
    df = pl.read_csv(path)

    # Overall
    print("\n=== Overall statistics (describe) ===")
    print(df.describe())

    # unique & freq for categoricals
    print("\n=== Unique counts ===")
    print(df.n_unique())

    # Identify string columns by selecting all Utf8-typed columns
    utf8_cols = df.select(pl.col(pl.Utf8)).columns
    for col in utf8_cols:
        print(f"\n--- Top values for {col} ---")
        vc = df[col].value_counts()
        print(vc.head(5))

    # Grouped
    if groups:
        print(f"\n=== Grouped by {groups}: describe() ===")
        print(df.groupby(groups).agg(pl.all().describe()))

        for col in utf8_cols:
            print(f"\n=== Grouped value_counts for {col} ===")
            grouped_vc = (
                df.groupby(groups)
                  .agg(pl.col(col).value_counts().alias("counts"))
                  .explode("counts")
            )
            print(grouped_vc)

if __name__ == "__main__":
    main()
