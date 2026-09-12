import os
import pandas as pd


DATASET_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "dataset"
)


files = [
    "requests.csv",
    "sample_requests.csv",
    "financial_profiles.csv",
    "financial_events.csv",
    "request_payment_options.csv",
    "messages.csv",
    "images.csv",
    "exchange_rates.csv",
    "output.csv"
]


for filename in files:

    file_path = os.path.join(DATASET_DIR, filename)

    print("\n" + "=" * 80)
    print(f"FILE: {filename}")
    print("=" * 80)

    try:
        df = pd.read_csv(file_path)

        print("\nROWS:", len(df))

        print("\nCOLUMNS:")
        for column in df.columns:
            print(f"  - {column}")

        print("\nFIRST 3 ROWS:")
        print(df.head(3).to_string())

    except Exception as error:
        print(f"\nERROR: {error}")