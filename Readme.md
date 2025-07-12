````markdown
# Descriptive Analysis Scripts

This repository provides three standalone scripts to perform basic descriptive statistics on CSV datasets using:

1. **Pure Python** (stdlib only)  
2. **Pandas**  
3. **Polars**

You can run each script on any CSV file and optionally group by one or more columns.

---

## Datasets

Below are two example public datasets you can download and analyze. **Do not** commit the raw CSVs—just record the URLs so others can fetch them.

1. **Titanic Passenger Manifest**  
   - URL:  
     ```
     https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
     ```  
   - Download:  
     ```bash
     wget https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv \
          -O data/titanic.csv
     ```

---

## Prerequisites

- **Python 3.8+**
- For the Pandas script:  
  ```bash
  pip install pandas
````

* For the Polars script:

  ```bash
  pip install polars
  ```

---

## Usage

Place your CSV files under a `data/` directory (or anywhere you like) and run:

```bash
# Pure Python version
python pure_python_stats.py <csv_file> [group_col1 [group_col2 …]]

# Pandas version
python pandas_stats.py <csv_file> [group_col1 [group_col2 …]]

# Polars version
python polars_stats.py <csv_file> [group_col1 [group_col2 …]]
```

If you supply grouping columns, each script will compute the same statistics within each group.

---

## Script Details

### 1. `analyze_pure.py` (Pure Python)

* **Reads** a CSV via the `csv` module.
* **Overall stats** for each column:

  * **Numeric:** count, mean, min, max, standard deviation.
  * **Categorical:** count, number of unique values, top-5 most frequent.
* **Grouped stats** using one or more columns: same set of metrics on each subset.

---

### 2. `pandas_stats.py` (Pandas)

* **Reads** a CSV into `pd.DataFrame`.
* **Overall**:

  * `df.describe(include="all")`
  * `df.nunique()`
  * `df[col].value_counts().head(5)` for each categorical (`object`) column.
* **Grouped** (`df.groupby(...)`):

  * `grouped.describe()`
  * `grouped[col].value_counts().unstack(fill_value=0).head()` for each categorical.

> **Note:** We removed the deprecated `datetime_is_numeric=True` argument to maintain compatibility with older pandas versions.

---

### 3. `polars_stats.py` (Polars)

* **Reads** a CSV via `pl.read_csv()`.
* **Overall**:

  * `df.describe()`
  * `df.n_unique()`
  * Identify string columns with

    ```python
    utf8_cols = df.select(pl.col(pl.Utf8)).columns
    ```
  * For each string column:

    ```python
    df[col].value_counts().head(5)
    ```
* **Grouped** (`df.groupby(...)`):

  * `df.groupby(...).agg(pl.all().describe())`
  * For each string column:

    ```python
    df.groupby(groups)
      .agg(pl.col(col).value_counts().alias("counts"))
      .explode("counts")
    ```
