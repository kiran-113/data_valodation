# src/etl.py
import pandas as pd
import numpy as np

def load_dirty_data():
    np.random.seed(42)
    n_rows = 100
    data = {
        "id": np.arange(1, n_rows + 1),
        "email": [f"user{i}@example.com" if i % 10 != 0 else None for i in range(1, n_rows + 1)],
        "age": [np.random.choice([25, 30, 45, 60, -5, 130, None]) for _ in range(n_rows)],
        "gender": [np.random.choice(["M", "F", "Other", "X", None]) for _ in range(n_rows)],
        "signup_date": pd.date_range(start="2022-01-01", periods=n_rows),
        "last_login": [
            pd.Timestamp("2022-01-01") + pd.to_timedelta(np.random.randint(-10, 300), unit="D")
            for _ in range(n_rows)
        ],
        "country": [np.random.choice(["US", "UK", "IN", "Unknown", ""]) for _ in range(n_rows)],
        "income": [np.random.choice([55000, 72000, 96000, None, -1000]) for _ in range(n_rows)],
    }

    df = pd.DataFrame(data)

    # Introduce some null IDs
    df.loc[np.random.choice(n_rows, 5, replace=False), "id"] = None

    # Add duplicates
    duplicates = df.sample(5, random_state=1)
    df = pd.concat([df, duplicates], ignore_index=True)

    return df
