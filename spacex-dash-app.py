# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                                        options=[{'label': 'All Sites', 'value': 'ALL'},
                                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                                        value = 'ALL',
                                                        placeholder = "Select a Launch Site here.",
                                                        searchable = True
                                                         )),


                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),


                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                    min = 0, # kg
                                                    max = 10000, # kg
                                                    step = 1000, # kg
                                                    marks={0: '0', 10000: '10000'},
                                                    value=[min_payload, max_payload]
                                                      )),
                               
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))


def get_pie_chart(entered_site):
    print(f"Dropdown selected: {entered_site}")
   
    if entered_site == 'ALL':
        filtered_df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(
            data_frame=filtered_df,
            values = 'class',
            names='Launch Site',
            title='Total Successes by Site')
        return fig
    else:
        specific_site = spacex_df[spacex_df['Launch Site']==entered_site]
        class_counts = specific_site['class'].value_counts().reset_index()
        class_counts.columns = ['class', 'Count']
        class_counts['class'] = class_counts['class'].map({1: 'Success', 0: 'Failure'})
        fig=px.pie(data_frame=class_counts,
            values = 'Count',
            names='class',
        title=f"Success for {entered_site} site")
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@ app.callback (Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])


def get_charts(entered_site, slide_value):
    print(f"Scatter chart callback triggered with site={entered_site} and payload_range={slide_value}")
    low = slide_value[0]
    high = slide_value[1]
    if entered_site=='ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color = "Booster Version Category")
        return fig
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        fig = px.scatter(data_frame=filtered_df, x='Payload Mass (kg)', y='class', color = "Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8080)







