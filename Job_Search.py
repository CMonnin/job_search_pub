
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.io as pio

import pandas as pd

# set the theme to a simialar seaborn theme
pio.templates.default = "simple_white"

df_og = pd.read_csv("data/003.csv")

df_og.loc[df_og['Company']=='OrderEase','List']='Ghosted after interview' 
df = df_og
interview_count=df['List'].value_counts()['Rejected after interview']+df['List'].value_counts()['Ghosted after interview']
# clean up the sources 
source_list = ['indeed.com','linkedin.com',]
df['Source'] = df['Source'].apply(lambda x: x if x in source_list else 'other')

# remove jobs that I haven't applied to yet
df = df[df['List'].str.contains('apply to') == False]

# Creating category to simplify titles

df['Category'] = 'Other'
df.loc[df['Title'].str.contains('Data Scientist', case=False), 'Category'] = 'Data Scientist'
df.loc[df['Title'].str.contains('analyst', case=False), 'Category'] = 'Data Analyst'
df.loc[df['Title'].str.contains('Data engineer', case=False), 'Category'] = 'Data Engineer'
df.loc[df['Title'].str.contains('Python', case=False), 'Category'] = 'Python Dev'
df.loc[df['Title'].str.contains('Machine Learning', case=False), 'Category'] = 'ML Engineer'
#########################
# figures

# get the values for the categories and plot them

value_counts = df['Category'].value_counts()
role_fig = go.Figure(data=go.Bar(x=value_counts.index, y=value_counts.values))

# parcat fig
parcat_fig= px.parallel_categories(
        df,dimensions=['Source','List'],
    color_continuous_scale=px.colors.sequential.Inferno,
    labels={'Source':'Source','List':'Status'}
)


# tracking jobs applied in a scatter plot as number vs date
df_001 = pd.read_csv("data/001.csv")
df_002 = pd.read_csv("data/002.csv") 
df_003 = pd.read_csv("data/003.csv") 

dates = [pd.to_datetime("2023-05-20"),pd.to_datetime("2023-05-30"),pd.to_datetime("2023-06-06")]
number_applied_to = [len(df_001),len(df_002),len(df_003)]

history_plot = px.line(x=dates,
                       y=number_applied_to,
                       labels={'x':'Date','y':'Number of applicatations'},
                       )


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([
    # Title
    
    dbc.Row([
        dbc.Col(
            html.H1('Job_Search_2023', className='text-center mb-4'),
            width=12
        )
    ]),
    # Sub title
    
    dbc.Row([
        dbc.Col([
            html.H5('Cian Monnin', className='text-center mb-4'),
            html.Div([
                dcc.Link('Github', href='https://github.com/CMonnin/', target='_blank'),
            ], className='text-center'),
            html.Div([
                dcc.Link('LinkedIn', href='https://www.linkedin.com/in/cmonnin/', target='_blank'),
            ], className='text-center')
        ], width=12)
    ]),

    # Row 1
    ######
    dbc.Row([
        # Sankey fig
        dbc.Col([
            dcc.Graph(figure=parcat_fig)
        ],
        width={'size': 6, 'offset': 0, 'order': 'first'},
            xs={'size': 12, 'offset': 0, 'order': 'last'},
            sm={'size': 12, 'offset': 0, 'order': 'last'},
            md={'size': 12, 'offset': 0, 'order': 'first'},
            lg={'size': 6, 'offset': 0, 'order': 'first'},
            xl={'size': 6, 'offset': 0, 'order': 'first'}),
        # roles fig
        dbc.Col([
                dcc.Graph(figure=role_fig)
                ])

    ]),
    # Row 2
    #######
    dbc.Row([


        dbc.Col([
                    
                    dbc.Card(
                        dbc.CardBody([
                            html.H5('Number of Interviews'),
                            html.H2(interview_count, className='card-text')
                        ]),
                        className='text-center'
                    ),
                    dbc.Card(
                        dbc.CardBody([
                            html.H5('Total Applications'),
                            html.H2(len(df), className='card-text')
                        ]),
                        className='text-center'
                    ),
                     html.Div([
                        'Applications started mid-April 2023'
                    ]),
                    html.Div([
                        'Last updated 2023-06-06'
                    ]),
                    html.Div([
                        'Changelog: changed Sankey plot to a parcat plot'
                    ]),
                  
                ]),
        dbc.Col([
                    dcc.Graph(figure=history_plot), 
            ]),
    ],)
],)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
