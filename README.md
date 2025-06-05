# housing-prices-dash-app
Contains code to render plotly dash app of Iowa homes data

### About the Dash App

This plotly dash application is designed to give the viewer insight on home sale price data in Ames, Iowa between the years of 2006 and 2010. This tool can be used for home buyers, sellers, or real estate agents in the area to understand sale price data orgranized by neighborhood, year, and various features of the homes (ie. total square footage, whether or not the home has AC or no centrail air, etc.). While the data is confined to Ames county Iowa between the years of 2006 and 2010, this app serves as an example of a tool that can be used by those interested in home sale price in different regions and over different years.

I did some data cleaning and feature engineering that can be seen (easier in the notebook because it is segemented well), in order to better visualize the data and understand home sale price in this data set.

### About the Data

The Ames Iowa Housing Dataset was compiled by Dean De Cock in 2011 to serve as an alternative to the very well-known Boston Housing Dataset that many data scientists are familiar with. I collected the data from https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/data and was split into test.csv and train.csv, I merged the data from these files (using R) into a single csv file (iowa_homes_full.csv) that is used to populate the dash app plots.

### Running the Plotly Dash Dpp

In order to run this application, there are two options:

1) You can run the app through a jupyter notebook using the app.ipynb file, and you can see the dash application within the notebook or can visit http://localhost:8050 to open the application.

2) You can run the app from the command line by running python app.py and then you can see the dash app by visiting http://localhost:8050

### Some Navigation Instructions

Hopefully the app is somewhat intuitive and the navigation is smooth, however here are some guidelines for visualizing data within the app.

* First the user can select the neighborhood that they would like to view sale price data for by using the 'Neighborhood' dropdown menu. By default, all neighborhoods are selected.
* Following this, the user can then select the year sold that they would like to view sale price data for using the "Year Sold" slider. By default, the year is set to 'All Years' and data for all years will be displayed in the plots.
* The first row of plots contain (from left to right) a horizontal bar chart which shows the sale price by neighborhood, and a frequency distribution of sale price where the bars are colored by neighborhood.
* Following the first row of plots, the user will notice there are 2 more menu items where they can select more options.
* First there is a "Numeric Feature" drop down where the user can select the feature that they would like to be compared with sale price in the plot below the drop down.
* Second, there is a "Categorical Feature" radio item list where the user can select a categorical feature that is listed to view a box plot with points of the sale price by the categorical feature selected.
