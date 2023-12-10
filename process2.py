import os
import requests
from pathlib import Path
import argparse
import concurrent.futures


# TollGuru API configuration
API_KEY = 'r6N7Q8NF8JBRBbrBHmpbbN7RnDRMMLJq'
HEADERS = {'x-api-key': API_KEY, 'Content-Type': 'text/csv'}

def process_csv(csv_path, output_dir):
    # Prepare the API URL
    api_url = 'https://apis.tollguru.com/toll/v2/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'

    # Prepare file names for JSON output
    file_name = Path(csv_path).stem
    json_output_path = os.path.join(output_dir, f'{file_name}.json')

    # Open the CSV file and send the request to TollGuru API
    with open(csv_path, 'rb') as file:
        response = requests.post(api_url, data=file, headers=HEADERS)

    # Save the JSON response to the output directory
    with open(json_output_path, 'w') as json_file:
        json_file.write(response.text)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process CSV files and interact with TollGuru API.')
    parser.add_argument('--to_process', required=True, help='Path to the CSV folder.')
    parser.add_argument('--output_dir', required=True, help='The folder where resulting JSON files will be stored.')
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Process CSV files concurrently using ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        csv_files = Path(args.to_process).glob('*.csv')
        executor.map(lambda csv_file: process_csv(str(csv_file), args.output_dir), csv_files)

if __name__ == "__main__":
    main()
