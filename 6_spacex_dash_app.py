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
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    html.Br(),
    dcc.Dropdown(id='site-dropdown', options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
    ],
                 value='ALL',
                 placeholder="SELECT",
                 searchable=True,
                 clearable=True
                 ),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, marks={0: '0', 100: '100'},
                    value=[min_payload, max_payload]),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# Callback functions
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data_frame=filtered_df, values='class', names='Launch Site',title='Success/Failure per launch site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        grouped_df = filtered_df.groupby('class').size().reset_index(name = 'count')
        grouped_df['class'] = grouped_df['class'].astype(str)
        fig = px.pie(data_frame=grouped_df,
                     values='count', names='class',
                     title='Success/Failure per launch site')
    return fig


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter(entered_site, payload_range):
    filtered_df = spacex_df
    min_payload, max_payload = payload_range
    if entered_site == 'ALL':
        scatter_fig = px.scatter(filtered_df[(filtered_df['Payload Mass (kg)'] >= min_payload) & 
                                             (filtered_df['Payload Mass (kg)'] <= max_payload)], 
                                 x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category',
                                 title='Relationship Payload Mass and success rate')
    else:
        scatter_fig = px.scatter(filtered_df[(filtered_df['Launch Site'] == entered_site) &
                                             (filtered_df['Payload Mass (kg)'] >= min_payload) & 
                                             (filtered_df['Payload Mass (kg)'] <= max_payload)], 
                                 x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category',
                                 title='Relationship Payload Mass and success rate')
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
