
# Descriptive Analysis Scripts

A set of three standalone Python scripts to compute basic descriptive statistics on CSV datasets using:

- **Pure Python** (standard library only)  
- **Pandas**  
- **Polars**

Each script can be run on any CSV file and optionally grouped by one or more columns.

---

## Table of Contents

- [Datasets](#datasets)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Scripts](#scripts)  
  - [analyze_pure.py (Pure Python)](#analyze_purepy-pure-python)  
  - [pandas_stats.py (Pandas)](#pandas_statspy-pandas)  
  - [polars_stats.py (Polars)](#polars_statspy-polars)  
- [License](#license)  

---

## Datasets

These are example public datasets. **Do not** commit the raw CSVs—record only the URLs so others can download them.

1. **Titanic Passenger Manifest**  
   - **URL:**  

     https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
  
   - **Download example:**  
bash
     wget https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv \
          -O data/titanic.csv


2. **Iris Flower Measurements**  
   - **URL:**  

     https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv

   - **Download example:**  

     wget https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv \
          -O data/iris.csv
 

---

## Prerequisites

- **Python 3.8+**

---

## Installation

Install the required libraries for the Pandas and Polars scripts:


pip install pandas
pip install polars


---

## Usage

Run any script with a CSV filepath and optional grouping columns:

```bash
# Pure Python version
python analyze_pure.py <csv_file> [group_col1 [group_col2 ...]]

# Pandas version
python pandas_stats.py <csv_file> [group_col1 [group_col2 ...]]

# Polars version
python polars_stats.py <csv_file> [group_col1 [group_col2 ...]]
```

If you supply grouping columns, each script will compute the same metrics within each group.

---

## Scripts

### `analyze_pure.py` (Pure Python)

* **Reads** a CSV using the `csv` module.
* **Overall statistics** for each column:

  * Numeric: count, mean, min, max, standard deviation
  * Categorical: count, unique values count, top-5 most frequent
* **Grouped statistics**: same metrics computed for each subset defined by one or more grouping columns.

### `pandas_stats.py` (Pandas)

* **Reads** a CSV into a `pd.DataFrame`.
* **Overall**:

  * `df.describe(include="all")`
  * `df.nunique()`
  * `df[col].value_counts().head(5)` for each categorical (`object`) column
* **Grouped** (`df.groupby(...)`):

  * `grouped.describe()`
  * `grouped[col].value_counts().unstack(fill_value=0).head()` for each categorical column
* **Compatibility note**: does **not** use the deprecated `datetime_is_numeric` argument.

### `polars_stats.py` (Polars)

* **Reads** a CSV via `pl.read_csv()`.
* **Overall**:

  * `df.describe()`
  * `df.n_unique()`
  * Identify string columns:

    ```python
    utf8_cols = df.select(pl.col(pl.Utf8)).columns
    ```
  * Top-5 value counts for each string column:

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

