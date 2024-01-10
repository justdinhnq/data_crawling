import pandas as pd
import urllib.request
import json
from datetime import datetime, timedelta

def func():
    """ 
        Hourly net generation by balancing authority and energy source. 
        Source: Form EIA-930 
        Product: Hourly Electric Grid Monitor
    """
    data_for_dataframe = []

    try:
        # API Key
        api_key = "bFgu973Wcapd06xDDWIxvhkkx4xBhIenennc6mnb"

        # Specify the base URL without dates
        base_url = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/?api_key={}&frequency=hourly&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000".format(api_key)

        # Get the current month and year
        today = datetime.today()
        current_month = today.month
        current_year = today.year

        # Loop through each day of the month
        for day in range(1, today.day + 1):
            # Format the start and end dates for the current day
            start_date = "{:04d}-{:02d}-{:02d}T00".format(current_year, current_month, day)
            end_date = "{:04d}-{:02d}-{:02d}T23".format(current_year, current_month, day)

            # Construct the complete URL for the current day
            url = "{}&start={}&end={}".format(base_url, start_date, end_date)

            # Create the request
            hdr ={
                'Cache-Control': 'no-cache',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/58.0.3029.110Safari/537.3'
            }
            req = urllib.request.Request(url, headers=hdr)
            req.get_method = lambda: 'GET'

            print(f'Request Data for {start_date} to {end_date}...')

            # Get the response
            response = urllib.request.urlopen(req)

            # Read and decode JSON content
            json_data = response.read().decode('utf-8')

            # Parse JSON data
            json_response = json.loads(json_data)

            # Extract data from the "value" field
            data_array = json_response["response"]["data"]

            total_value = json_response["response"]["total"]
            print("Total:", total_value)
            print(f'Respond Data for {start_date} to {end_date}.')

            # Append data to the list (if needed)
            data_for_dataframe.extend(data_array)

    except Exception as e:
        print(f'Exception: {e}')

    # Create DataFrame
    df = pd.DataFrame(data_for_dataframe)
    
    if not df.empty:
        # Set the index to "period"
        df = df.set_index("period")

        # Save DataFrame to CSV
        df.to_csv("./data/by_energy_source.csv")
        print("DataFrame saved to CSV.")
    else:
        print("DataFrame is empty.")

if __name__ == "__main__":
    func()
