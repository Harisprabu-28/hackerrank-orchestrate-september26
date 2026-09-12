import os
import pandas as pd


DATASET_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "dataset"
)


def load_csv(filename):
    path = os.path.join(DATASET_DIR, filename)
    return pd.read_csv(path)


events = load_csv("financial_events.csv")
profiles = load_csv("financial_profiles.csv")
payment_options = load_csv("request_payment_options.csv")
messages = load_csv("messages.csv")
sample_requests = load_csv("sample_requests.csv")


print("\n" + "=" * 90)
print("FINANCIAL EVENTS ANALYSIS")
print("=" * 90)


columns_to_analyze = [
    "event_type",
    "category",
    "direction",
    "status",
    "flexibility",
    "currency"
]


for column in columns_to_analyze:

    print("\n" + "-" * 90)
    print(f"COLUMN: {column}")
    print("-" * 90)

    counts = events[column].fillna("MISSING").value_counts()

    print(counts.to_string())


print("\n" + "=" * 90)
print("MISSING AMOUNTS")
print("=" * 90)

missing_amounts = events[events["amount"].isna()]

print(f"\nNumber of events with missing amounts: {len(missing_amounts)}")

if len(missing_amounts) > 0:
    print("\nEvents with missing amounts:")
    print(
        missing_amounts[
            [
                "event_id",
                "user_id",
                "event_type",
                "description",
                "category",
                "currency",
                "event_date",
                "status"
            ]
        ].to_string(index=False)
    )


print("\n" + "=" * 90)
print("LINKED EVENTS")
print("=" * 90)

linked_events = events[events["linked_event_id"].notna()]

print(f"\nNumber of events with linked_event_id: {len(linked_events)}")

print("\nFirst 20 linked events:")

print(
    linked_events[
        [
            "event_id",
            "user_id",
            "event_type",
            "description",
            "amount",
            "status",
            "linked_event_id"
        ]
    ].head(20).to_string(index=False)
)


print("\n" + "=" * 90)
print("PAYMENT METHODS")
print("=" * 90)

print(
    payment_options["payment_method"]
    .value_counts()
    .to_string()
)


print("\n" + "=" * 90)
print("PAYMENT OPTION EXAMPLES")
print("=" * 90)

print(
    payment_options.head(20).to_string(index=False)
)


print("\n" + "=" * 90)
print("MESSAGE SOURCE TYPES")
print("=" * 90)

print(
    messages["source_type"]
    .value_counts()
    .to_string()
)


print("\n" + "=" * 90)
print("ALL SAMPLE REQUEST OUTPUTS")
print("=" * 90)


sample_columns = [
    "request_id",
    "user_id",
    "requested_amount",
    "amount_safe_to_pay",
    "affordability_status",
    "recommended_payment_method",
    "payment_plan",
    "earliest_date_for_full_payment",
    "spending_changes_needed"
]


print(
    sample_requests[
        sample_columns
    ].to_string(index=False)
)


print("\n" + "=" * 90)
print("SAMPLE DECISION EXPLANATIONS")
print("=" * 90)


for _, row in sample_requests.iterrows():

    print(f"\nREQUEST: {row['request_id']}")
    print(f"STATUS: {row['affordability_status']}")
    print(f"METHOD: {row['recommended_payment_method']}")
    print(f"EXPLANATION: {row['decision_explanation']}")


print("\n" + "=" * 90)
print("ANALYSIS COMPLETE")
print("=" * 90)