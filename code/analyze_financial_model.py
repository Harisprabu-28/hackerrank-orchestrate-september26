import os
import pandas as pd


BASE_DIR = os.path.join(
    os.path.dirname(__file__),
    ".."
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)


def load(filename):
    path = os.path.join(DATASET_DIR, filename)
    return pd.read_csv(path)


requests = load("requests.csv")
sample_requests = load("sample_requests.csv")
profiles = load("financial_profiles.csv")
events = load("financial_events.csv")
messages = load("messages.csv")
images = load("images.csv")
rates = load("exchange_rates.csv")


def section(title):
    print("\n")
    print("=" * 100)
    print(title)
    print("=" * 100)


# ============================================================
# 1. REQUEST STRUCTURE
# ============================================================

section("1. REQUESTS.CSV STRUCTURE")

print("\nColumns:")
for column in requests.columns:
    print(f" - {column}")

print("\nFirst 10 requests:")
print(requests.head(10).to_string(index=False))


# ============================================================
# 2. SAMPLE REQUEST STRUCTURE
# ============================================================

section("2. SAMPLE_REQUESTS.CSV STRUCTURE")

print("\nColumns:")
for column in sample_requests.columns:
    print(f" - {column}")

print("\nFirst 10 rows:")
print(sample_requests.head(10).to_string(index=False))


# ============================================================
# 3. FINANCIAL PROFILE STRUCTURE
# ============================================================

section("3. FINANCIAL_PROFILES.CSV")

print("\nColumns:")
for column in profiles.columns:
    print(f" - {column}")

print("\nAll profiles:")
print(profiles.head(10).to_string(index=False))


# ============================================================
# 4. FINANCIAL EVENT COLUMNS
# ============================================================

section("4. FINANCIAL_EVENTS.CSV COLUMNS")

for column in events.columns:
    print(f" - {column}")


# ============================================================
# 5. DATE ANALYSIS
# ============================================================

section("5. EVENT DATE ANALYSIS")

date_columns = [
    column
    for column in events.columns
    if "date" in column.lower()
]

print("\nDate columns:")
for column in date_columns:
    print(f" - {column}")


for column in date_columns:

    print("\n" + "-" * 80)
    print(f"DATE COLUMN: {column}")
    print("-" * 80)

    converted = pd.to_datetime(
        events[column],
        errors="coerce"
    )

    print("Earliest:", converted.min())
    print("Latest:  ", converted.max())
    print("Missing: ", converted.isna().sum())


# ============================================================
# 6. FUTURE / NON-SETTLED EVENTS
# ============================================================

section("6. NON-SETTLED EVENTS")

non_settled = events[
    events["status"].isin(
        ["pending", "scheduled"]
    )
]

print("\nNumber of pending/scheduled events:")
print(len(non_settled))

print("\nFirst 30:")
print(
    non_settled.head(30).to_string(
        index=False
    )
)


# ============================================================
# 7. EVENT TYPE EXAMPLES
# ============================================================

section("7. EVENT TYPE EXAMPLES")

event_types = events["event_type"].dropna().unique()

for event_type in sorted(event_types):

    print("\n" + "-" * 80)
    print(f"EVENT TYPE: {event_type}")
    print("-" * 80)

    subset = events[
        events["event_type"] == event_type
    ]

    print(
        subset.head(8).to_string(
            index=False
        )
    )


# ============================================================
# 8. FLEXIBLE EVENT EXAMPLES
# ============================================================

section("8. FLEXIBLE EXPENSE EXAMPLES")

flexible_events = events[
    events["flexibility"].isin(
        [
            "reducible",
            "stoppable",
            "reducible_or_stoppable"
        ]
    )
]

print(
    flexible_events.head(30).to_string(
        index=False
    )
)


# ============================================================
# 9. MESSAGES
# ============================================================

section("9. MESSAGES.CSV STRUCTURE")

print("\nColumns:")
for column in messages.columns:
    print(f" - {column}")

print("\nAll messages:")
print(messages.to_string(index=False))


# ============================================================
# 10. IMAGES
# ============================================================

section("10. IMAGES.CSV STRUCTURE")

print("\nColumns:")
for column in images.columns:
    print(f" - {column}")

print("\nImage records:")
print(images.to_string(index=False))


# ============================================================
# 11. EXCHANGE RATES
# ============================================================

section("11. EXCHANGE_RATES.CSV")

print(rates.to_string(index=False))


# ============================================================
# 12. SAMPLE USERS - COMPLETE FINANCIAL HISTORY
# ============================================================

section("12. SAMPLE USER FINANCIAL EXAMPLES")


sample_user_ids = (
    sample_requests["user_id"]
    .dropna()
    .head(5)
    .tolist()
)


for user_id in sample_user_ids:

    print("\n" + "#" * 100)
    print(f"USER: {user_id}")
    print("#" * 100)

    print("\nPROFILE:")

    user_profile = profiles[
        profiles["user_id"] == user_id
    ]

    print(
        user_profile.to_string(
            index=False
        )
    )


    print("\nEVENTS:")

    user_events = events[
        events["user_id"] == user_id
    ]

    print(
        user_events.to_string(
            index=False
        )
    )


    print("\nMESSAGES:")

    user_messages = messages[
        messages["user_id"] == user_id
    ]

    if len(user_messages) == 0:
        print("No messages")
    else:
        print(
            user_messages.to_string(
                index=False
            )
        )


print("\n")
section("ANALYSIS COMPLETE")