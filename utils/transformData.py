import json
import csv
from datetime import datetime
from collections import defaultdict


# Got help from AI in this function but adapted it by myself to add the update date as a newer column
def json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'prices' not in data:
        print("Error: 'prices' key not found in the JSON file.")
        return

    prices = data['prices']

    updateDate = datetime(2025,10,22)
    daily_data = defaultdict(lambda: {'prices': [], 'volumes': [],'afterUpdate':0})

    # Process and group the rows
    for row in prices:
        raw_date_str = row[0]
        price = float(row[1])
        volume = int(row[2])
        
        date_part = raw_date_str[:11]
        date_obj = datetime.strptime(date_part, "%b %d %Y")

        afterUpdate = int(date_obj >= updateDate)
        formatted_date = date_obj.strftime("%Y-%m-%d")

        daily_data[formatted_date]['prices'].append(price)
        daily_data[formatted_date]['volumes'].append(volume)
        daily_data[formatted_date]['afterUpdate'] = afterUpdate
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'price', 'volume','afterUpdate'])
        
        # Calculate daily averages/totals and write the rows
        for date, stats in daily_data.items():
            # Calculate the average price for the day
            avg_price = sum(stats['prices']) / len(stats['prices'])
            
            # Calculate total volume for the day
            total_volume = sum(stats['volumes'])
            
            # Write to CSV, rounding the price to 3 decimal places to keep it clean
            writer.writerow([date, round(avg_price, 3), total_volume,stats['afterUpdate']])

    print(f"Successfully processed records to {output_file}")

