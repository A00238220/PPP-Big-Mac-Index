#importing libraries
import nasdaqdatalink
import pandas as pd
import json
import urllib.request
import pygal

from flask import Flask, render_template
# from ppp import get_data 

app = Flask('app')

@app.route('/')
def hello_world():
  #setting api key
  nasdaqdatalink.ApiConfig.api_key = 'T_HsELBky_xHxzCEXCYi'

  #creating list of countries to loop through
  countries = ["UKR","EGY","CHN","AUS"]

  #creating empty list to append extracted data
  data_list = []
  data_list2 = []
  

  #looping through the countries list
  for country in countries:
    data = nasdaqdatalink.get(f'ECONOMIST/BIGMAC_{country}', start_date='2021-01-31', end_date='2022-01-31')
        
    url = f'https://restcountries.com/v3.1/alpha/{country}'
    request = urllib.request.urlopen(url)
    result = json.loads(request.read())

    # print(result)
    #calculating mac index based on ppp
    number = float(round(data.iloc[0,3],2))
    burger = "🍔" * (int(number))

    #creating dictionary to store data
    country = {
    "country": country,
    "local_price": round(data.iloc[0,0],6),
    "dollar_ex": round(data.iloc[0,1],6),
    "dollar_price": round(data.iloc[0,2],6),
    "dollar_ppp": round(data.iloc[0,3],6),
    "dollar_valuation": data.iloc[0,4],
    "dollar_adj_valuation": data.iloc[0,5],
    "flag": result[0]["flags"]["png"],
    "country_name": result[0]["name"]["common"],
    "currencies": result[0]["currencies"],
    "burger": burger,
    }
    
    #creating a sub dictionary
    sub_dict = {"Country Name" : country['country_name'],
                "Country Code" : country['country'],
                "Dollar Exchange": country['dollar_ex'],
                "Dollar Price" : country['dollar_price'],
                "Dollar PPP" : country['dollar_ppp'],       
    }    
    #appending stored data to a list
    data_list.append(country)
    data_list2.append(sub_dict)
    

  #converting sublist to a data frame
  df = pd.DataFrame(data_list2)
  print(df)

  #creating bar chart visual
  bar_chart = pygal.Bar()         
  bar_chart.title = "Purchasing Power Parity (PPP)"
  bar_chart.x_labels = map(str, df['Country Name'])
  bar_chart.add('Countries', df['Dollar PPP'])  # Add some values
  bar_chart.render_to_file('static/images/bg4.svg')

  
  return render_template("index.html", data_list=data_list)

app.run(host='0.0.0.0', port=8080, debug=True)
