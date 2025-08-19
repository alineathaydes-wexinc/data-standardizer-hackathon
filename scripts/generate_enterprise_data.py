# scripts/generate_enterprise_data.py
import pandas as pd
from faker import Faker
import random
import os
import uuid

# --- Configuration ---
NUM_EMPLOYEES_TO_GENERATE = 500
OUTPUT_DIR = "data"
fake = Faker()

# --- "Source of Truth": Our canonical list of companies ---
# Based on the real data provided. This is the master list we will standardize against.
CANONICAL_COMPANIES = [
    {'CompanyID': 42, 'CompanyName': 'TTG', 'City': 'Albuquerque', 'State': 'CA', 'Country': 'USA'},
    {'CompanyID': 15666, 'CompanyName': 'Rod Cute Cats', 'City': 'San Francisco', 'State': 'CA', 'Country': 'USA'},
    {'CompanyID': 2001, 'CompanyName': 'Innovate Solutions Inc.', 'City': 'Austin', 'State': 'TX', 'Country': 'USA'},
    {'CompanyID': 2002, 'CompanyName': 'Quantum Dynamics LLC', 'City': 'Boston', 'State': 'MA', 'Country': 'USA'},
    {'CompanyID': 2003, 'CompanyName': 'Apex Financial Group', 'City': 'New York', 'State': 'NY', 'Country': 'USA'},
    {'CompanyID': 2004, 'CompanyName': 'Starlight Media Ltd', 'City': 'Los Angeles', 'State': 'CA', 'Country': 'USA'}
]

def generate_dirty_company_name(canonical_name):
    """Creates realistic variations and typos of a given company name."""
    name = canonical_name
    rand = random.random()

    # We use if statements instead of elif to allow multiple "errors" to stack.
    if rand < 0.2:  # 20% chance of wrong case
        name = name.lower() if random.random() < 0.5 else name.upper()

    if rand > 0.3 and rand < 0.5: # 20% chance of removing suffix
        name = name.replace(" Inc.", "").replace(" LLC", "").replace(" Ltd", "")

    if rand > 0.5 and rand < 0.7: # 20% chance of a single character typo
        if len(name) > 4:
            pos = random.randint(1, len(name) - 2)
            char_to_replace = name[pos]
            # Replace with a nearby key on the keyboard or just a random letter
            name = name[:pos] + random.choice('abcdefghijklmnopqrstuvwxyz') + name[pos+1:]

    if rand > 0.7 and rand < 0.9: # 20% chance of abbreviation
         name = name.replace("Group", "Grp").replace("Solutions", "Sol.")

    # ~20% chance of being entered correctly
    return name

def generate_employees_data(companies_list):
    """Generates synthetic employee data with 'dirty' company name inputs."""
    employee_data = []
    for _ in range(NUM_EMPLOYEES_TO_GENERATE):
        # Pick a random company from our correct list
        correct_company = random.choice(companies_list)

        # Simulate a user typing the company name, possibly with errors
        submitted_name = generate_dirty_company_name(correct_company['CompanyName'])

        employee_data.append({
            "EmployeeID": str(uuid.uuid4()),
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Email": fake.email(),
            "Title": fake.job(),
            "CompanyID": correct_company['CompanyID'], # The correct foreign key
            "SubmittedCompanyName": submitted_name, # The text that needs standardization
        })

    print(f"Generated {len(employee_data)} employee records.")
    return pd.DataFrame(employee_data)

if __name__ == "__main__":
    print("Starting synthetic data generation based on enterprise schema...")

    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Create and save the canonical companies DataFrame
    companies_df = pd.DataFrame(CANONICAL_COMPANIES)
    companies_path = os.path.join(OUTPUT_DIR, "enterprise_companies.csv")
    companies_df.to_csv(companies_path, index=False)
    print(f"Canonical company list saved to '{companies_path}'")

    # 2. Generate and save the employees DataFrame with dirty data
    employees_df = generate_employees_data(CANONICAL_COMPANIES)
    employees_path = os.path.join(OUTPUT_DIR, "enterprise_employees.csv")
    employees_df.to_csv(employees_path, index=False)
    print(f"Synthetic employee data saved to '{employees_path}'")

    print("\nData generation complete.")