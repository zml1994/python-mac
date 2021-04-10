from datetime import datetime, timedelta
# import pandas as pd


data = [(datetime.strptime('2020-12-01', "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(62)]
print(data)

# date = pd.date_range(start,end)