import argparse
import pandas as pd
import os

def identify_trips(df):
    # Sort the dataframe by unit and timestamp
    df.sort_values(['unit', 'timestamp'], inplace=True)

    # Initialize variables
    trip_number = 0
    previous_time = None
    previous_unit = None

    for index, row in df.iterrows():
        current_time = pd.to_datetime(row['timestamp'])

        if (
            previous_unit is not None and
            row['unit'] == previous_unit and
            previous_time is not None and
            (current_time - previous_time) > pd.Timedelta(hours=7)
        ):
            # Start a new trip
            trip_number += 1

        # Update previous unit and timestamp
        previous_unit = row['unit']
        previous_time = current_time

        # Assign trip number to the row
        df.at[index, 'trip_number'] = trip_number

    return df

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process GPS data from a Parquet file and store results in CSV files.')
    parser.add_argument('--to_process', required=True, help='Path to the Parquet file to be processed.')
    parser.add_argument('--output_dir', required=True, help='Folder to store the resulting CSV files.')
    args = parser.parse_args()

    # Read the Parquet file into a pandas dataframe
    df = pd.read_parquet(args.to_process)

    # Identify trips
    df = identify_trips(df)

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Save individual trips to CSV files
    for unit, unit_df in df.groupby('unit'):
        for trip_number, trip_df in unit_df.groupby('trip_number'):
            csv_filename = os.path.join(args.output_dir, f'{unit}_{int(trip_number)}.csv')
            trip_df.to_csv(csv_filename, index=False)

if __name__ == "__main__":
    main()