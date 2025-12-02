from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import numpy as np


#df = pd.read_csv('../project1/iowa_homes.csv')
df = pd.read_csv('iowa_homes_full.csv')

'''remove features where there are many na values''' 

#create series with index = column name, value = percentage (decimal) of rows with 'NA' for each column
na_percentages = df.isnull().sum() / len(df)

# create a list of the column names that have more than 20% of rows with 'NA'
cols_to_drop = na_percentages[na_percentages > .2].index

additional_cols_to_drop = ['BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond'] 

print(cols_to_drop)

#remove columns with more than 20% NA
df = df.drop(columns = cols_to_drop)
df = df.drop(columns= additional_cols_to_drop)



''' get numerical columns '''

# #create list of numeric columns in dataframe
numeric_cols = df.select_dtypes(include=np.number).columns


# ''' replace na in numerical column with 0 for that column ''' 
df[numeric_cols] = df[numeric_cols].fillna(0)

# create new columns for features to be used in dash
df['HasBsmt'] = df['TotalBsmtSF'] > 0 
df['HasGarage'] = df['GarageArea'] > 0
df['HasFinishedBsmt'] = df['BsmtFinSF1'] > 0
df['Has2ndStory'] = df['X2ndFlrSF'] > 0


# drop the remainder of rows with NA. These will all be categorical columns as none of the numerical columns contain NA at this point

df = df.dropna()

# create total square footage feature
df['TotalSF'] = df['X1stFlrSF'] + df['X2ndFlrSF'] + df['TotalBsmtSF']

# reinstantiate numeric cols list and remove SalePrice and Id for visualization in dash later
numeric_cols = df.select_dtypes(include=np.number).columns
numeric_cols = numeric_cols.drop('Id')
numeric_cols = numeric_cols.drop('SalePrice')

#create list of neighborhoods for visualizatin later
list_of_neighborhoods = df['Neighborhood'].unique()
list_of_neighborhoods = np.append(list_of_neighborhoods, 'ALL')
list_of_neighborhoods.sort()


app = Dash()

#dash background, widget background, primary text, secondary text, chart line 
colors=['#191D24', '#232935', '#EFF7FF', '#DADFE9', '#f25876','#1dc690', '#F5DC71']

app.layout = html.Div([
    html.Br(),

    #Header Div
    html.Div([
        html.H2(children='Ames, Iowa House Price Data'),
    ], style={'textAlign': 'center'}),


    #Options Div1
    html.Div([
        html.Div([
            html.H3('Neighborhood', style={'color':colors[2]}),
            dcc.Dropdown(
               list_of_neighborhoods,
                value = 'ALL',
                id = 'neighborhood_dropdown'
            )
        ], style={'color':'#5566FC', 'width': '28%', 'textAlign': 'center', 'display': 'inline-block', 'margin-left': '4%', 'margin-right': '6%'}),


        html.Div([
            html.H3('Year Sold'),
            dcc.Slider(
                min=int(min(df['YrSold'])),
                max=2011,
                step=2,
                marks = {
                  2006 :'2006',
                  2007:'2007',
                  2008:'2008',
                  2009:'2009',
                  2010:'2010',
                  2011:'All years'
                },
                value = 2011,
                id = 'yr_slider'
            )
        ], style={'width': '48%', 'textAlign': 'center', 'display': 'inline-block', 'margin-left': '6%', 'margin-right': '4%'})
    ]),

    html.Br(),

    #First row of graphs
    html.Div([
        html.Div([
            dcc.Graph(id='neighborhood_comparison')
        ], style={'width':'50%', 'margin-left':'2%', 'margin-right':'2%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(id='saleprice_histogram')
        ], style ={'width':'44%', 'maring-left':'2%', 'display':'inline-block'})
    ]),

   html.Br(),

    #Options Div 2
    html.Div([
         html.Div([
            html.H3('Numeric Feature Dropdown', style={'color':colors[2], 'display':'inline-block'}),
            dcc.Dropdown(
                numeric_cols.sort_values(),
                value = 'TotalSF',
                id = 'numeric_dropdown'
            )
        ], style={'color':'#5566FC', 'width': '28%', 'textAlign': 'center', 'display': 'inline-block', 'margin-left': '10%', 'margin-right': '6%'}),           
            
        html.Div([
            html.H3('Categorical Feature Comparison', style={'color':colors[2], 'display':'inline-block'}),
            dcc.RadioItems(['Finished Basement', '2nd Story', 'Central Air'], 
                          value = 'Finished Basement', 
                          id='features_radio')
        ], style={'width': '20%', 'textAlign': 'center', 'display': 'inline-block', 'margin-left': '22%', 'margin-right': '0%'})
 ]),

    html.Br(),

    #2nd row of graphs
    html.Div([
        html.Div([
            dcc.Graph(id='SF_SalePrice_Graph')
        ], style={'width':'44%','backgroundColor':colors[1], 'display': 'inline-block', 'margin-left':'2%', 'margin-right': '4%'}),

        html.Div([
            dcc.Graph(id='SalePrice_Hist')
        ], style={'width':'44%','backgroundColor':colors[1], 'display': 'inline-block', 'margin-left': '4%'})
    ],style={'margin-bottom':'8%'}),

    html.Br()

],style={'backgroundSize':'cover','backgroundColor':colors[0], 'color':colors[2], 'font':'arial'})

# callback decorator number 1 to update the second row of graphs
@callback(
    [Output('SF_SalePrice_Graph', 'figure'),
     Output('SalePrice_Hist', 'figure')],
    [Input('neighborhood_dropdown', 'value'),
     Input('yr_slider', 'value'),
     Input('features_radio', 'value'),
     Input('numeric_dropdown', 'value')]
)

#callback function to update 2nd row of graphs
def update_graphs_1(neighborhood_dropdown, yr_slider, features_radio, numeric_dropdown):

    filtered_df = df

    # set year to 'All Years' as 2011 is a place holder for 'All Years'
    if yr_slider == 2011:
        yr_slider = 'All Years'
    
    else:
        filtered_df = filtered_df[filtered_df['YrSold'] == yr_slider]  

    # filter dataframe based on neighborhood selected
    if neighborhood_dropdown == 'ALL':
        filtered_df = filtered_df
        neighborhood_dropdown_new = "All Neighborhoods"
    
    else:
        filtered_df = filtered_df[filtered_df['Neighborhood'] == neighborhood_dropdown]
        neighborhood_dropdown_new = neighborhood_dropdown

    # Get the column value that corresponds to the radio item selected
    if features_radio == 'Finished Basement':
        selected_item = 'HasFinishedBsmt'
    
    elif features_radio == '2nd Story':
        selected_item = 'Has2ndStory'
    
    else:
        selected_item = 'CentralAir'  

    # sort data by sale price for scatter plot with OLS
    filtered_df = filtered_df.sort_values(by='SalePrice')   

    # create scatter plot of sale price by selected numeric feature 
    fig1 = px.scatter(filtered_df, x=numeric_dropdown, y="SalePrice", 
                trendline="ols",
                hover_name="SalePrice", 
                color_discrete_sequence=[colors[4]],
                labels={
                    'SalePrice':'Sale Price'
                    },
                title = f'Sale Price by {numeric_dropdown} ({yr_slider}, {neighborhood_dropdown_new})')
    
    fig1.update_layout(
        showlegend=True,
        title_font_family='Arial',
        title_font_color=colors[2])
    
    fig1.data[1].update(line_color='#92B0FF')

    fig1.layout.plot_bgcolor = colors[1]
    fig1.layout.paper_bgcolor = colors[1]

    fig1.update_xaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
    fig1.update_yaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))

    # create box plot of selected categorical feature vs. sale price
    fig2 = px.box(filtered_df, x=selected_item, y='SalePrice', 
                points="all",
                color=selected_item,
                color_discrete_sequence=[colors[4], '#92B0FF'],
                labels={
                    'SalePrice':'Sale Price'
                    },
                title = f'Sale Price by {selected_item} ({yr_slider}, {neighborhood_dropdown_new})')

    fig2.update_layout(
        title_font_family='Arial',
        title_font_color=colors[2],
        legend_font_color = colors[2])

    fig2.layout.plot_bgcolor = colors[1]
    fig2.layout.paper_bgcolor = colors[1]

    fig2.update_xaxes(tickfont_color=colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
    fig2.update_yaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))

    return fig1, fig2

#callback decorator number 2 to update the 1st row of graphs
@callback(
    [Output('neighborhood_comparison', 'figure'),
     Output('saleprice_histogram', 'figure')],
    [Input('neighborhood_dropdown', 'value'),
     Input('yr_slider', 'value')]
)

#callback function to update 2nd row of graphs
def update_graphs_2(neighborhood_dropdown, yr_slider):

    # set 2011 to "All Years" if selected
    if yr_slider == 2011:
        filtered_df = df
        yr_slider = 'All Years'
    
    else:
        filtered_df = df[df['YrSold'] == yr_slider]

    # create series with mean sale price grouped by neighborhood
    mean_by_nbhd = filtered_df.groupby('Neighborhood')['SalePrice'].mean()

    #flattne series and convert to dataframe
    mean_by_nbhd = mean_by_nbhd.reset_index(name='Values')
    mean_by_nbhd = pd.DataFrame(mean_by_nbhd)

    # create plots that don't highlight a singular neighborhood if ALL is selected in neighborhood dropdown
    if neighborhood_dropdown =='ALL':

        # create horizontal bar chart of sale price by neighborhood
        fig1 = px.bar(mean_by_nbhd, x='Values', y='Neighborhood', 
                    color = 'Neighborhood',
                    color_discrete_sequence=['#92B0FF'],
                    labels={
                        'Values':'Mean Sale Price'
                    },
                    title = f'Mean Sale Price by Neighborhood ({yr_slider})',
                    range_x=[50000,max(mean_by_nbhd['Values']+5000)]
                    )
        
        fig1.update_layout(
            showlegend=False,
            title_font_family='Arial',
            title_font_color=colors[2])
        
        fig1.layout.plot_bgcolor = colors[1]
        fig1.layout.paper_bgcolor = colors[1]

        fig1.update_xaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
                        
        fig1.update_yaxes(tickfont_color=colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))

        # Create frequency distribution of sale price
        fig2 = px.histogram(filtered_df, x = 'SalePrice', 
                    color = 'Neighborhood',
                    color_discrete_map={neighborhood_dropdown:colors[4]},
                    title = f'Sale Price Distribution ({yr_slider})')
        
        fig2.update_layout(
            title_font_family='Arial',
            title_font_color=colors[2],
            legend_font_color = colors[2]
            )
    
    
        fig2.layout.plot_bgcolor = colors[1]
        fig2.layout.paper_bgcolor = colors[1]

        fig2.update_xaxes(tickfont_color=colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
                        
        fig2.update_yaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))



    #This indicates that a neighborhood was selected from the dropdown that we need to highlight in our plots
    else:
        
        #create a horizontal bar chart that displays the sale price by neighborhood with the selected neighborhood offset by a different color from the others
        fig1 = px.bar(mean_by_nbhd, x='Values', y='Neighborhood', 
                    color = 'Neighborhood',
                    color_discrete_sequence=['#92B0FF'],
                    color_discrete_map={neighborhood_dropdown:colors[4]},
                    labels={
                        'Values':'Mean Sale Price'
                    },
                    title = f'Mean Sale Price by Neighborhood ({yr_slider})',
                    range_x=[50000,max(mean_by_nbhd['Values']+5000)]
                    )
        
        fig1.update_layout(
            showlegend=False,
            title_font_family='Arial',
            title_font_color=colors[2])
        
        fig1.layout.plot_bgcolor = colors[1]
        fig1.layout.paper_bgcolor = colors[1]

        fig1.update_xaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
                        
        fig1.update_yaxes(tickfont_color=colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))

        # create frequency distribution of sale price where the selected neighborhood is highlighted
        fig2 = px.histogram(filtered_df, x = 'SalePrice', 
                    color = 'Neighborhood',
                    color_discrete_map={neighborhood_dropdown:colors[4]},
                    title = f'Sale Price Distribution ({yr_slider})')
        
        fig2.update_layout(
            title_font_family='Arial',
            title_font_color=colors[2],
            legend_font_color = colors[2])

    
    
        fig2.layout.plot_bgcolor = colors[1]
        fig2.layout.paper_bgcolor = colors[1]

        fig2.update_xaxes(tickfont_color=colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))
                        
        fig2.update_yaxes(tickfont_color=colors[6], gridcolor = colors[6], title_font=dict(size=18, family='Arial', color=colors[2]))

        # remaining lines of code (including for loop) make sure that we highlight the selected neighborhood
        fig2.update_traces(visible='legendonly')
        
        for x in fig2.data:
            if x.name == neighborhood_dropdown:
                x.visible=True

    return fig1, fig2

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)