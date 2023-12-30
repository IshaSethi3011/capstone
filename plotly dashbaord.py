# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='site-dropdown',  
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                            value = 'ALL',
                                            placeholder = 'Select a launch site',
                                            searchable = True)),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                # TASK 3: Add a slider to select payload range
                                html.P("Payload range (Kg):"),
                                html.Div(dcc.RangeSlider(min = 0, max = 10000, step = 1000, value = [min_payload, max_payload], id='payload-slider')),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id = 'success-pie-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value')
)
def get_pie(selected_site):
    if (selected_site == 'ALL'):
        df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(df, values = df['class'] ,names = df['Launch Site'], title = 'Total Success Launches by All Sites')
    else :
        df = spacex_df[(spacex_df['Launch Site'] == selected_site)] 
        zd = 0
        od = 0
        for i in df['class']:
            if (i == 0) :
                zd = zd + 1
            else :
                od = od + 1
        lab = ['Success', 'Failure']
        val = [od, zd]
        fig = px.pie(df, values = val, names = lab, title = 'Success vs Failure Counts')
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
    Input(component_id = 'site-dropdown', component_property = 'value'),
    Input(component_id = 'payload-slider', component_property = 'value')
)
def get_chart(selected_site, selected_value):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_value[0]) & (spacex_df['Payload Mass (kg)'] <= selected_value[1])]
    if (selected_site == 'ALL'):
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
    else :
        df = filtered_df[(filtered_df['Launch Site'] == selected_site)]
        fig = px.scatter(df, x = 'Payload Mass (kg)', y = 'class', color = 'Booster Version Category')
    return fig    

# Run the app
if __name__ == '__main__':
    app.run_server()