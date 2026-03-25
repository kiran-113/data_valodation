# tests/test_data_quality.py
import pytest
from src.etl import load_dirty_data
@pytest.fixture(scope='module')
def df():
    return load_dirty_data()
def test_no_missing_ids(df):
    assert df['id'].notnull().all(), "Missing 'id' values found"
def test_no_missing_emails(df):
    assert df['email'].notnull().all(), "Missing 'email' values found"
def test_valid_ages(df):
    valid = df['age'].between(0, 120).fillna(False)
    assert valid.all(), f"Invalid ages at rows: {df[~valid].index.tolist()}"
def test_valid_genders(df):
    valid = df['gender'].isin({'M', 'F', 'Other'}).fillna(False)
    assert valid.all(), f"Unexpected genders at: {df[~valid].index.tolist()}"
def test_login_after_signup(df):
    valid = df['last_login'] >= df['signup_date']
    assert valid.all(), f"Signup/login mismatch rows: {df[~valid].index.tolist()}"
def test_known_countries(df):
    valid = df['country'].isin({'US', 'UK', 'IN'}).fillna(False)
    assert valid.all(), f"Unknown countries: {df[~valid].index.tolist()}"
def test_non_negative_income(df):
    valid = df['income'].apply(lambda x: x is None or x >= 0)
    assert valid.all(), "Negative income values found"
def test_no_duplicates(df):
    dupes = df[df.duplicated()]
    assert len(dupes) == 0, f"Found {len(dupes)} duplicate rows"