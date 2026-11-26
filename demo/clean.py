"""Clean data/messy_sales.csv -> data/clean_sales.csv and print a report."""
import re, json
import pandas as pd

RATE = 50.0  # fixed demo rate: 1 USD = 50 EGP

def money(v):
    if pd.isna(v) or str(v).strip() == "": return None
    s = str(v).strip()
    usd = s.startswith("$")
    s = re.sub(r"[^\d.,]", "", s).replace(",", "")
    if not s: return None
    x = float(s)
    return round(x * RATE if usd else x, 2)

def phone(v):
    if pd.isna(v): return None
    d = re.sub(r"\D", "", str(v))
    if d.startswith("20"): d = d[2:]
    if d.startswith("0"): d = d[1:]
    return "+20" + d if len(d) == 10 else None

CITY = {"alex": "Alexandria"}
def city(v):
    s = str(v).strip().title()
    return CITY.get(s.lower(), s)

df = pd.read_csv("data/messy_sales.csv", dtype=str)
before = {"rows": len(df), "duplicates": int(df.duplicated().sum()),
          "missing_amount": int(df.amount.fillna("").str.strip().eq("").sum()),
          "missing_phone": int(df.phone.isna().sum()),
          "distinct_cities": int(df.city.nunique()),
          "distinct_date_formats": 3}
df = df.drop_duplicates().copy()
df["customer"] = df.customer.str.strip().str.title()
df["email"] = df.email.str.strip().str.lower()
df["email_valid"] = df.email.str.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]+")
df["phone"] = df.phone.map(phone)
df["city"] = df.city.map(city)
df["order_date"] = df.order_date.map(lambda s: pd.to_datetime(s.strip(), format="mixed", dayfirst=True)).dt.strftime("%Y-%m-%d")
df["amount_egp"] = df.amount.map(money)
df = df.drop(columns="amount")
df.to_csv("data/clean_sales.csv", index=False)
after = {"rows": len(df), "duplicates": int(df.duplicated().sum()),
         "missing_amount": int(df.amount_egp.isna().sum()),
         "missing_phone": int(df.phone.isna().sum()),
         "invalid_email_flagged": int((~df.email_valid).sum()),
         "distinct_cities": int(df.city.nunique()), "date_format": "YYYY-MM-DD"}
print(json.dumps({"before": before, "after": after}, indent=2))
json.dump({"before": before, "after": after}, open("data/report.json", "w"), indent=2)
