import requests
import pandas as pd
import os

url = "https://gbfs.velobixi.com/gbfs/en/station_information.json"

response = requests.get(url)
response.raise_for_status() 

data = response.json()

stations = data["data"]["stations"]

df = pd.DataFrame(stations)

output_path = "./data"
os.makedirs(output_path, exist_ok=True)

csv_file = os.path.join(output_path, "station_information.csv")
df.to_csv(csv_file, index=False)

print(f"Data saved to {csv_file}")
