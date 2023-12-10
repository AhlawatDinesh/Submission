import os
import json
import csv
import argparse
from pathlib import Path

def process_json(json_path, output_csv):
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

        # Check if there are tolls in the route
        if 'route' in data and 'tolls' in data['route']:
            tolls = data['route']['tolls']

            for toll in tolls:
                # Extract relevant data
                unit = Path(json_path).stem.split('_')[0]
                trip_id = Path(json_path).stem
                toll_loc_id_start = toll.get('start', {}).get('id', {})
                toll_loc_id_end = toll.get('end', {}).get('id', '')
                toll_loc_name_start = toll.get('start', {}).get('name', '')
                toll_loc_name_end = toll.get('end', {}).get('name', '')
                toll_system_type = toll.get('type', '')
                entry_time = toll.get('start', {}).get('arrival', {}).get('time', '')
                exit_time = toll.get('end', {}).get('arrival', {}).get('time', '')
                tag_cost = toll.get('tagCost', '')
                cash_cost = toll.get('cashCost', '')
                license_plate_cost = toll.get('licensePlateCost', '')

                # Write data to CSV
                with open(output_csv, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([unit, trip_id, toll_loc_id_start, toll_loc_id_end, toll_loc_name_start,
                                         toll_loc_name_end, toll_system_type, entry_time, exit_time, tag_cost,
                                         cash_cost, license_plate_cost])

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process toll information stored in JSON files.')
    parser.add_argument('--to_process', required=True, help='Path to the JSON responses folder.')
    parser.add_argument('--output_dir', required=True, help='The folder where the final transformed_data.csv will be stored.')
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Define the CSV output file
    output_csv = os.path.join(args.output_dir, 'transformed_data.csv')

    # Write CSV header
    with open(output_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['unit', 'trip_id', 'toll_loc_id_start', 'toll_loc_id_end',
                             'toll_loc_name_start', 'toll_loc_name_end', 'toll_system_type',
                             'entry_time', 'exit_time', 'tag_cost', 'cash_cost', 'license_plate_cost'])

    # Process JSON files
    for json_file in Path(args.to_process).glob('*.json'):
        process_json(str(json_file), output_csv)

if __name__ == "__main__":
    main()
