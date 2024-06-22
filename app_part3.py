import dash_bootstrap_components as dbc
from dash import Dash, Input, callback, Output, dcc, html
import pandas as pd
import plotly.express as px
import json

df = pd.read_csv('https://raw.githubusercontent.com/Kal1n1na/Regeons-of-Russia/main/regions.csv', sep=';')
all_cont = df['Okrug'].unique()
all_reg = df['Region'].unique()
all_year = df['Year'].unique()

with open('russia copy.geojson','r',encoding='UTF-8') as response:
        counties = json.loads(response.read())

external_stylesheets = [dbc.themes.LITERA]  
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#F2F8FD",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([
         html.H3("Анализ региональной экономики России", className="display-14"),
        html.Hr(),
        html.P(
            "Калинина Ю.А.", className="display-18"
        ),
        html.P(
            "Макарова А.В. ", className="display-18"
        ),
        html.Hr(style={'color': 'black'}),
        dbc.Nav(
            [
                dbc.NavLink("Статистика", href="/", active="exact"),
                dbc.NavLink("Регионы", href="/page-1", active="exact"),
                dbc.NavLink("Карта регионов", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],style=SIDEBAR_STYLE,),  
    html.Div(id="page-content", children=[], style=CONTENT_STYLE)
     
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/":
        return [
            html.Div([
                html.H4("Анализ экономики России с 2005 по 2023 годы"),
                html.Hr(style={'color': 'black'}),
                ], 
                style={'textAlign': 'center'}
                ),
            html.Div([

            html.Div([
                html.H6('Основные показатели'),
                            dcc.RadioItems(
                            options = [
                                {'label':'ВВП', 'value': 'VVP'},
                                {'label':'Доля инновационно активных организаций', 'value': 'Dolya_innovatsionno_aktivnykh_organizatsiy'},
                                {'label':'Доля инновационных продуктов', 'value': 'Dolya_innovatsionnykh_produktov'},
                                {'label':'Инвестиции в основной капитал на душу населения', 'value': 'Investitsii_v_osnovnoy_kapital'},
                            ],
                            id = 'crossfilter-ind0',
                            value = 'VVP',
                            labelStyle={'display': 'inline-block', 'width': '19%', 'float': 'left'}
                            )
                        ],
                        style = {'width': '120%',  'float': 'center', 'display': 'inline-block'}),
                    ], style = {
                        'borderBottom': 'thin lightgrey solid',
                        'backgroundColor': 'rgb(250, 250, 250)',
                        'padding': '5px 10px'}
            ),
                dbc.Col([
                    dbc.Col([
                        html.P("Выберите год:")
                    ],width=2),
                    dbc.Col([
                    dcc.Dropdown(
                            id = 'crossfilter-year0',
                            options = [{'label': i, 'value': i} for i in all_year],
                            value = all_year[0],
                            # возможность множественного выбора
                            multi = False
                        )
                    ],width=4),
                ]),
                    html.Br(),
            dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.Row([
                                dbc.CardHeader("Общие доходы рег. бюджета, млн руб.")
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.CardBody(
                                            html.P(
                                                id='card_1',
                                                className="card-value"),
                                            ),
                                            # html.P("%", className="card-text"),
                                            ],style = {'width': '340px','float': 'center', 'display': 'inline-block'}, width= 10),
                                        ])
                                    ], color = "success", outline=True, style={'textAlign': 'center'}),
                                ],width=4),
                    dbc.Col([
                        dbc.Card([
                            dbc.Row([
                                dbc.CardHeader("Общие расходы рег. бюджета, млн руб.")
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.CardBody([
                                            html.P(
                                                id='card_2',
                                                className="card-value",),
                                            # html.P("чел.", className="card-text"),
                                            ]
                                            )],style = {'width': '340px','float': 'center', 'display': 'inline-block'}, width=8),
                                        ])
                                    ], color = "info", outline=True, style={'textAlign': 'center'}),
                                ],width=4),

                        dbc.Col([
                            dbc.Card([
                                dbc.Row([
                                    dbc.CardHeader("Сальдо рег. бюджета, млн руб.")
                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.CardBody(
                                                html.P(
                                                    id='card_3',
                                                    className="card-value"),
                                                )],style = {'width': '340px','float': 'center', 'display': 'inline-block'}, width= 8),
                                        ])
                                    ], color = "primary", outline=True, style={'textAlign': 'center'}),
                                ],width=4),
                ]),
                html.Br(),   
                    html.Div(
                        dcc.Graph(id = 'line'),
                        style = {'width': '100%','height': '100%', 'display': 'inline-block'}
                    ),
                html.Br(), html.Br(),
                html.Div(
                        dbc.Col([
                            dbc.Row([
                            html.H5("ТОП-10 регионов"),
                            html.Div(id="tabletop"),
                        ])

                ], width=10, style={'textAlign':'center'}),
                        style = {'width': '120%','float': 'center', 'display': 'inline-block'}
                    ),
                
            ]

    elif pathname == "/page-1":
        return [
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H3("Подробная информация об экономике выбранного региона"),
                        html.Hr(style={'color': 'black'}),
                    ], style={'textAlign': 'center'})
                )
            ]),
            dbc.Row ([
                dbc.Col([
                    html.P("Выберите регион:")
                ],width=2),
                dbc.Col([
                    dcc.Dropdown(
                        id = 'crossfilter-reg',
                        options = [{'label': i, 'value': i} for i in all_reg],
                        value = all_reg[0],
                        # возможность множественного выбора
                        multi = False
                    )
                ],width=4),
                dbc.Col([
                    html.P("Выберите год:")
                ],width=2),
                dbc.Col([
                dcc.Dropdown(
                        id = 'crossfilter-year1',
                        options = [{'label': i, 'value': i} for i in all_year],
                        value = all_year[0],
                        # возможность множественного выбора
                        multi = False
                    )
                ],width=3),
            ]),

            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.CardHeader("Доходы регион. бюджета, млн руб.")
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody(
                                        html.P(
                                            id='card_text1',
                                            className="card-value"),
                                        ),
                                        ],style = {'width': '170px','float': 'center', 'display': 'inline-block'}, width= 8),
                                    ])
                                ], color = "success", outline=True, style={'textAlign': 'center'}),
                            ],style = {'width': '15%','float': 'center', 'display': 'inline-block'},width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.CardHeader("Расходы регион. бюджета, млн руб.")
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody([
                                        html.P(
                                            id='card_text2',
                                            className="card-value",)
                                        ]
                                        )],style = {'width': '170px','float': 'center', 'display': 'inline-block'}, width=8),
                                    ])
                                ], color = "info", outline=True, style={'textAlign': 'center'}),
                            ],style = {'width': '15%','float': 'center', 'display': 'inline-block'},width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.CardHeader("Сальдо регион. бюджета, млн руб.")
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody(
                                        html.P(
                                            id='card_text3',
                                            className="card-value"),
                                        ),
                                        ],style = {'width': '170px','float': 'center', 'display': 'inline-block'}, width= 8),
                                ])
                            ], color = "success", outline=True, style={'textAlign': 'center'}),
                        ],style = {'width': '16%','float': 'center', 'display': 'inline-block'},width=2),
                        dbc.Col([
                dbc.Card([
                    dbc.Row([
                        dbc.CardHeader("Доля инновационных продуктов, %")
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.CardBody(
                                    html.P(
                                        id='card_text4',
                                        className="card-value"),
                                    ),
                                    ],style = {'width': '170px','float': 'center', 'display': 'inline-block'}, width= 8),
                                ])
                            ], color = "info", outline=True, style={'textAlign': 'center'}),
                        ],style = {'width': '16%','float': 'center', 'display': 'inline-block'},width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.CardHeader("Доля иннв.-активных орг-ий,%")
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody([
                                        html.P(
                                            id='card_text5',
                                            className="card-value",),
                                        ]
                                        )],style = {'width': '170px','float': 'center', 'display': 'inline-block'}, width=8),
                                    ])
                                ], color = "success", outline=True, style={'textAlign': 'center'}),
                            ],style = {'width': '16%','float': 'center', 'display': 'inline-block'},width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.Row([
                            dbc.CardHeader("Инвестиции в осн. капитал, руб.")
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.CardBody(
                                        html.P(
                                            id='card_text6',
                                            className="card-value"),
                                        ),
                                        ],style = {'width': '160px','float': 'center', 'display': 'inline-block'}, width= 10),
                                ])
                            ], color = "primary", outline=True, style={'textAlign': 'center'}),
                        ],style = {'width': '15%','float': 'center', 'display': 'inline-block'},width=2),
            ]),
            html.Br(),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("ВВП на душу населения"),
                    ], style={'textAlign': 'center'})
                )
            ]),
            html.Div(
                    dcc.Graph(id = 'vvp'),
                    style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Сальдо региональнного бюджета"),
                    ], style={'textAlign': 'center'})
                )
            ]), 
            html.Div(
                    dcc.Graph(id = 'sald'),
                    style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Доходы региональнного бюджета"),
                    ], style={'textAlign': 'center'})
                ), 
                html.Div(
                    dcc.Graph(id = 'dox'),
                    style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            ]),    
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Расходы региональнного бюджета"),
                    ], style={'textAlign': 'center'})
                ),
                html.Div(
                    dcc.Graph(id = 'ras'),
                    style = {'width': '100%', 'display': 'inline-block'}
                ),
            ]), 
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Инвестиции в основной капитал на душу населения"),
                    ], style={'textAlign': 'center'})
                )
            ]), 
            html.Div(
                    dcc.Graph(id = 'inv'),
                    style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Глубина 'воронки отсталости'"),
                    ], style={'textAlign': 'center'})
                ),html.Div(
                    dcc.Graph(id = 'vor'),
                    style = {'width': '100%', 'display': 'inline-block'}
                ),
            ]), 
        ]
    
    elif pathname == "/page-2":
        return [
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H3("Тепловая карта показателей за 2023"),
                        html.Hr(style={'color': 'black'}),
                    ], style={'textAlign': 'center'})
                )
            ]),
            html.Br(),
            dbc.Row ([
                dbc.Col([
                    dbc.Label("Выберите показатель:"),
                    dbc.RadioItems(
                        options=[
                            {'label':'ВВП', 'value': 'VVP'},
                            {'label':'Доля инновационно активных организаций', 'value': 'Dolya_innovatsionno_aktivnykh_organizatsiy'},
                            {'label':'Доля инновационных продуктов', 'value': 'Dolya_innovatsionnykh_produktov'},
                            {'label':'Инвестиции в основной капитал на душу населения', 'value': 'Investitsii_v_osnovnoy_kapital'},
                        ],
                        value='VVP',
                        id='crossfilter-ind2',
                    ),
                ],width=3),
            
                dbc.Col([
                    dcc.Graph(id = 'rusmap', config={'displayModeBar': False}),
                ], width=7)
            ],style = {
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(242,248,253)',
                    'padding': '5px 5px'}) 
        ]
    
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

@callback(
    Output('line', 'figure'),
    [Input('crossfilter-ind0', 'value'),
    Input('crossfilter-year0', 'value')]
)
def update_stacked_area(indication, year):
    filtered_data = df[(df['Year'] == year)]
    figure = px.bar(
        filtered_data,
        x = indication,
        y = 'Region',
        labels={'Region':'Регион', 'Year':'Год',
                'Dolya_innovatsionnykh_produktov':'Доля инновационных продуктов', 'VVP':'ВВП',
                'Dolya_innovatsionno_aktivnykh_organizatsiy':'Доля инновационно-активных организаций',
                'Investitsii_v_osnovnoy_kapital':'Инвестиции в основной капитал на душу населения'},
                )
    figure.update_layout(mapbox_style="carto-positron",
                        margin={"r":0,"t":0,"l":0,"b":0},
                        mapbox_zoom=2, mapbox_center = {"lat": 66, "lon": 94}, height=800, width=1000,
                        showlegend=False)
    return figure


@callback(
    Output('tabletop', 'children'),
    [Input('crossfilter-ind0', 'value'),
    Input('crossfilter-year0', 'value')]
)
def update_table(indication, year):
    vvp_count = df[(df['Year'] == year)].sort_values(by=indication, ascending=False)
    vvp_table = vvp_count.iloc[0:10][['Region', indication]]
    table = dbc.Table.from_dataframe(
        vvp_table, striped=True, bordered=True, hover=True, index=False)
    return table

@callback(
    Output('card_1', 'children'),
    Output('card_2', 'children'),
    Output('card_3', 'children'),
    [Input('crossfilter-year0', 'value')]
)
def update_card1(year):
    df_count=df[(df['Year'] <= year) ]

    c1=df_count['Dokhody_regionalnogo_byudzheta'].sum()
    c2=df_count['Raskhody_regionalnogo_byudzheta'].sum()
    c3=df_count['Saldo_regionalnogo_byudzheta'].sum()
    
    return c1,c2,c3

@callback(
    Output('vvp', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_vvp(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.line(
        filtered_data,
        x='Year',
        y='VVP',
        markers = False,
        labels={ 'Year':'Год',
                'VVP':'ВВП на душу населения'},
    )
    return figure

@callback(
    Output('sald', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_sald(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.line(
        filtered_data,
        x='Year',
        y='Saldo_regionalnogo_byudzheta',
        markers = False,
        labels={ 'Year':'Год',
                'Saldo_regionalnogo_byudzheta':'Сальдо региональнного бюджета'},
    )
    return figure

@callback(
    Output('dox', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_dox(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.line(
        filtered_data,
        x='Year',
        y='Dokhody_regionalnogo_byudzheta',
        markers = False,
        labels={ 'Year':'Год',
                'Dokhody_regionalnogo_byudzheta':'Доходы региональнного бюджета'},
    )
    return figure

@callback(
    Output('ras', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_ras(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.line(
        filtered_data,
        x='Year',
        y='Raskhody_regionalnogo_byudzheta',
        markers = False,
        labels={ 'Year':'Год',
                'Raskhody_regionalnogo_byudzheta':'Расходы региональнного бюджета'},
    )
    return figure

@callback(
    Output('inv', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_inv(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.line(
        filtered_data,
        x='Year',
        y='Investitsii_v_osnovnoy_kapital',
        markers = False,
        labels={ 'Year':'Год',
                'Investitsii_v_osnovnoy_kapital':'Инвестиции в основной капитал на душу населения'},
    )
    return figure

@callback(
    Output('vor', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_vor(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    figure = px.bar(
        filtered_data,
        x='Year',
        y='Glubina_voronki',
        labels={ 'Year':'Год',
                'Glubina_voronki':'Глубина воронки отсталости'},
    )

    return figure

@callback(
    Output('card_text1', 'children'),
    Output('card_text2', 'children'),
    Output('card_text3', 'children'),
    Output('card_text4', 'children'),
    Output('card_text5', 'children'),
    Output('card_text6', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card2(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]

    ct1=df_count.iloc[0]['Dokhody_regionalnogo_byudzheta']
    ct2=df_count.iloc[0]['Raskhody_regionalnogo_byudzheta']
    ct3=df_count.iloc[0]['Saldo_regionalnogo_byudzheta']
    ct4=df_count.iloc[0]['Dolya_innovatsionnykh_produktov']
    ct5=df_count.iloc[0]['Dolya_innovatsionno_aktivnykh_organizatsiy']
    ct6=df_count.iloc[0]['Investitsii_v_osnovnoy_kapital']
    
    return ct1,ct2,ct3,ct4,ct5,ct6,

@callback(
    Output('rusmap', 'figure'),
    [Input('crossfilter-ind2', 'value'),
    ])

def update_rusmap(indication):
    figure = px.choropleth_mapbox(
        df,
        geojson=counties,
        featureidkey='properties.cartodb_id',
        color=indication,
        locations='cartodb_id',
        color_continuous_scale=px.colors.sequential.Blues,
        mapbox_style="carto-positron",
        zoom=10,
        center = {'lat':55.755773, 'lon':37.617761},
        opacity=0.5,
        hover_name='Region',
        hover_data = {'Region':True,'Year':True,'cartodb_id':False,
                    'VVP':True,'Dolya_innovatsionno_aktivnykh_organizatsiy':True,
                    'Dolya_innovatsionnykh_produktov':True,'Investitsii_v_osnovnoy_kapital':True,
                    'Okrug':False},
        labels={'Region':'Регион', 'Year':'Год',
                'Dolya_innovatsionnykh_produktov':'Доля иннв. продуктов', 'VVP':'ВВП',
                'Dolya_innovatsionno_aktivnykh_organizatsiy':'Доля иннв-актив. организаций',
                'Investitsii_v_osnovnoy_kapital':'Инвестиции в капитал '},
                #animation_frame='Year',

        )
   
    figure.update_layout(mapbox_style="carto-positron",
                        margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='world',
                        mapbox_zoom=2, mapbox_center = {"lat": 66, "lon": 94}, height=500, width=800,
                        showlegend=False)
    return figure


if __name__ == '__main__':
        app.run_server(debug=True)
