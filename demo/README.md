# Messy Sales Data Cleaner

A small Python project that turns a messy sales export into a clean, analysis-ready CSV, with a report of what changed.

All data is synthetic. No real customers.

## The problem

The input file (`data/messy_sales.csv`, 203 rows) looks like a typical real export:

- exact duplicate rows
- names in mixed case, extra spaces
- emails with capital letters, trailing spaces, or missing domains
- phone numbers in four formats, some empty
- city spelled many ways (`Cairo`, `cairo `, `CAIRO`, `alex`)
- dates in three formats
- amounts like `2,474`, `113 EGP`, `$25`, or blank

## What the script does

| Step | Result |
|---|---|
| Remove exact duplicates | 203 to 200 rows |
| Standardize names and cities | 9 city spellings to 5 real cities |
| Normalize phones to `+20XXXXXXXXXX` | blanks stay blank, nothing invented |
| Parse all dates | `YYYY-MM-DD` |
| Convert amounts to numeric EGP | `$` converted at a fixed demo rate of 50 |
| Flag bad emails | new `email_valid` column, rows are kept |

Missing values are never guessed. They stay empty so you can decide what to do.

![Before and after](docs/before_after.png)

## Run it

```bash
pip install -r requirements.txt
python make_sample.py   # regenerate the messy sample (optional)
python clean.py         # writes data/clean_sales.csv and data/report.json
python chart.py         # writes docs/before_after.png
```

## Use it on your own data

Change the input path and column names in `clean.py`. Need this done on your file? Contact details go here.
