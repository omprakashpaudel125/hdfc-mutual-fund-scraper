from bs4 import BeautifulSoup
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

print("Current time is", datetime.now().strftime('%d-%m-%Y_%H:%M:%S'))

years = ["2020", "2021", "2022", "2023", "2024"]
months = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]



 # change the variables here
url_every_month = []
url_first_part = "https://www.hdfcfund.com/digitalfactsheets/"
# url_second_part = "/innerpages/Balanced-Advantage-Fund.html"
url_second_part = "/innerpages/Hybrid-Equity-Fund.html"

plot_x = []
for year in years:
    for month in months:
        temp = url_first_part + year + "-" + month + url_second_part
        url_every_month.append(temp)
        plot_x.append(year + " " + month)

print("---------------")

final_value = []
for url in url_every_month:
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Error fetching {url}")
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        target_value = soup.select_one("#collapseaum .card-body table.key-fact tr:nth-of-type(2) td:nth-of-type(2) div")
        if target_value:
            value = target_value.text.strip()
            value = value.replace(",", "").replace("Cr.", "").strip()
            final_value.append(float(value))
        else:
            print(f"not found {url}")
    except Exception as e:
        print(f"error while checking for {url}: {e}")

# with open("permonth.txt", "a") as g:
#     for value in final_value:
#         g.write(str(value) + "\n")

plot_x = plot_x[:len(final_value)]

print("-----------------------")
plt.figure(figsize=(14, 7))  
plt.plot(plot_x, final_value, marker="o", label="Fund Data")
plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
plt.xlabel("Months")
plt.ylabel("Crores (in Cr.)")
plt.title("Mutual Fund Research "+url_second_part)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

print("--------------")

aum_series = np.array(final_value)
model = ARIMA(aum_series, order=(5, 1, 0))
model_fit = model.fit()
forecast_steps = 12 
forecast = model_fit.forecast(steps=forecast_steps)
future_x = ["Future " + str(i+1) for i in range(forecast_steps)]
plt.figure(figsize=(20,16));
plt.plot(plot_x + future_x, list(aum_series) + list(forecast), linestyle="--", marker="o", label="Future Prediction", color="red")
plt.title("FUTURE AUM PREDICTION, DIRECTLY PROPORTIONAL TO NAV size")
plt.xlabel("Months")
plt.ylabel("Crores (in Cr.)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
