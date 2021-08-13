from datetime import date
import calendar
import os
import requests

API_KEY = 'e1f10a1e78da46f5b10a1e78da96f525'
LOCATION_CODE = 'VOGO:9:IN'

base_url = f'https://api.weather.com/v1/location/{LOCATION_CODE}/observations/historical.json?apiKey={API_KEY}&units=e&startDate={{0}}&endDate={{1}}'

def main():
  today = date.today()
  year = today.year
  month = today.month
  while True:
    month = ((month - 1) % 12)
    if (month == 0):
      month = 12
      year = year - 1

    lastday = calendar.monthrange(year, month)[1]
    start_date = f'{year}{month:02}01'
    end_date = f'{year}{month:02}{lastday:02}'
    url = base_url.format(start_date, end_date)
    try:
      download_data(url, month, year, LOCATION_CODE)
    except Exception as e:
      print(e)
      break

def download_data(url, month, year, location):
  os.makedirs(location, exist_ok=True)
  response = requests.get(url)
  if(response.status_code != 200):
    raise Exception(f'No data found for {year:02}-{month:02}')
  with open(f'{location}/{year}-{month}.json', 'wb') as f:
    f.write(response.content)

  print(f'Data downloaded for {year:02}-{month:02}. Size: {(len(response.content)/1024):.2f}kB')

main()
