# Data Analytics: Flight Traffic Patterns

Data Analytics & Visualizations Course Project: Impact of COVID-19 Pandemic on US Flight Traffic

In this project, we examine the impact of the Covid-19 pandemic on domestic flight traffic in the United States. The Covid-19 pandemic has brought unprecedented negative impact on the aviation industry, leading to a sharp decline in the number of flights and passengers. To assess the extent and duration of the pandemic's impact on US flight traffic, We analyze the data from [Transtats](https://www.transtats.bts.gov/) library. In addition to highlighting annual trends in flight traffic, our findings provide insights into the effects of the pandemic on the aviation industry and can inform policy decisions aimed at mitigating the impact of future pandemics on air travel. We opted to use Tableau for visualizations, Colab as our IDE, pandas and pytorch for pre-processing the data.

The dataset is available [here](https://www.kaggle.com/datasets/robikscube/flight-delay-dataset-20182022?select=Combined_Flights_2020.csv).

Colab notebook with preprocessing code:

Colab notebook with predictive analysis code: ForecastNumFlights.ipynb
 - 'combinedFlightsperDay.snappy.parquet' contains the dataset of flight records combined per day, download it and run the ForecastNumFlights notebook.

Tableau dashboard file is available [here](https://yuoffice-my.sharepoint.com/:f:/r/personal/msivakum_yorku_ca/Documents/Data%20Analytics%20-Tableau?csf=1&web=1&e=Inhtzv).

Project report:

## Summary
Through our data analysis, we were able to identify trends in flight patterns across airlines and years. With our Tableau dashboard, we compared number of flights, percentage delays and cancellations across years to identify  peak travel months and the best year for airlines in terms of number of flights. We explored flight patterns before, during and after the peak of the COVID-19 pandemic. A key finding was some airlines went out of business during the pandemic period despite having less delays, and this highlights the importance of analysing several flight attributes before drawing conclusions.

Here are a few examples of the charts we created in Tableau:

<b>100 percent stacked bar chart showing status of flight over pre-pandemic, pandemic and post pandemic:</b>

<img width="546" alt="3 periods" src="https://user-images.githubusercontent.com/127549357/230979687-a5c5c183-1218-43f1-af07-17caa7942813.png">

<b>Map chart showing arrivals in 2018:</b>

![AirportArrivals2018_1cropped(1)](https://user-images.githubusercontent.com/127549357/230979870-3e76bd34-f391-4de9-94be-ef16eb620373.png)

<b>Chart showing cancellations per 1000 flights for selected airlines:</b>

<img width="535" alt="Cancellations per 1000 flights" src="https://user-images.githubusercontent.com/127549357/230979896-d223a937-ffa5-439c-8ceb-62d9c1f1eb50.png">

<b>Bar chart showing Top 10 airlines with most number of flights:</b>

<img width="546" alt="Top 10 with flights" src="https://user-images.githubusercontent.com/127549357/230979921-813dc5ce-d56e-4a88-b193-02b23afffaf9.png">
