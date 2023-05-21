
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

df_og = pd.read_csv("data/jobs.csv")

# adding a column to ID companies that ghosted after interview
df_og['Ghosted after interview'] = 0
# find the index of the Company that ghosted me after an interview
ghosters = df_og.loc[df_og['Company']=='OrderEase'].index[0]
df_og.at[ghosters, 'Ghosted after interview'] = 1

df = df_og

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


#######################
# Variables for the Sankey plot

linkedin_count = df['Source'].value_counts()['linkedin.com']
indeed_count = df['Source'].value_counts()['indeed.com']
# otta_count = df['Source'].value_counts()['otta.com']
other_count = df['Source'].value_counts()['other']
rejected_interview_count = df['List'].value_counts()['Rejected after interview'] - df['Ghosted after interview'].sum()
rejected_count =  df['List'].value_counts()['TRASH']
interview_count = df['List'].value_counts()['Rejected after interview']
ghosted_count = df['Ghosted after interview'].sum()
no_response_count = len(df)  - rejected_count - rejected_interview_count - ghosted_count

nodes = [
    {'label': 'Linkedin'},      # 0
    {'label': 'Indeed'},        # 1
    {'label': 'Placeholder'},   # 2 
    {'label': 'Other'},         # 3
    {'label': 'Applied'},       # 4
    {'label': 'No Response'},   # 5
    {'label': 'Rejected'},      # 6
    {'label': 'Ghosted'},       # 7
    {'label': 'Interview'},     # 8
]
#########################
# figures

# get the values for the categories and plot them
value_counts = df['Category'].value_counts()
role_fig = go.Figure(data=go.Bar(x=value_counts.index, y=value_counts.values))
# creating the Sankey figure
sankey_fig = go.Figure(data=[go.Sankey(
    node=dict(
        label=[node['label'] for node in nodes],
    ),
    link=dict(
        source=[0, 1, 2, 3, 4, 4, 4, 8, 8],
        target=[4, 4, 4, 4, 5, 6, 8, 7, 6],
        value=[linkedin_count,
               indeed_count,
                0,
               other_count,
               no_response_count,
               rejected_count,
               interview_count,
               ghosted_count,
               rejected_interview_count
               ]
    )
)])


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1('Job_Search_2023', className='text-center mb-4'),
            width=12
        )
    ]),
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

    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=sankey_fig)
        ],
        width={'size': 6, 'offset': 0, 'order': 'first'},
            sm={'size': 12, 'offset': 0, 'order': 'last'},
            md={'size': 12, 'offset': 0, 'order': 'first'},
            lg={'size': 6, 'offset': 0, 'order': 'first'},
            xl={'size': 6, 'offset': 0, 'order': 'first'}),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(figure=role_fig)
                ])
            ]),
            
            dbc.Row([
                dbc.Col([
                    
                    html.Div([
                        'Applications started mid-April 2023'
                    ]),
                    html.Div([
                        'Last updated 2023-05-20'
                    ]),
                ]),
            ]),

        ],width={'size': 6, 'offset': 0, 'order': 'first'},
            sm={'size': 12, 'offset': 0, 'order': 'last'},
            md={'size': 12, 'offset': 0, 'order': 'first'},
            lg={'size': 6, 'offset': 0, 'order': 'first'},
            xl={'size': 6, 'offset': 0, 'order': 'first'})
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5('Total Applications'),
                    html.H2(len(df), className='card-text')
                ]),
                className='text-center'
            ),
            width={'size': 6, 'offset': 0, 'order': 'first'},
            sm={'size': 12, 'offset': 0, 'order': 'last'},
            md={'size': 6, 'offset': 0, 'order': 'first'},
            lg={'size': 6, 'offset': 0, 'order': 'first'},
            xl={'size': 6, 'offset': 0, 'order': 'first'}
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5('Number of Interviews'),
                    html.H2(interview_count, className='card-text')
                ]),
                className='text-center'
            ),
            width={'size': 6, 'offset': 0, 'order': 'last'},
            sm={'size': 12, 'offset': 0, 'order': 'first'},
            md={'size': 6, 'offset': 0, 'order': 'last'},
            lg={'size': 6, 'offset': 0, 'order': 'last'},
            xl={'size': 6, 'offset': 0, 'order': 'last'}
        )
    ], className='mt-4')
], className='p-5')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)