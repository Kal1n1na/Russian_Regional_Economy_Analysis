import dash_bootstrap_components as dbc
from dash import Dash, Input, callback, Output, dcc, html
import pandas as pd
import plotly.express as px
import json
import plotly.graph_objects as go

df = pd.read_csv('https://raw.githubusercontent.com/Anastas1aMakarova/Russian_Regional_Economy_Analysis/main/regions.csv', sep=';')
all_cont = df['Okrug'].unique()
all_reg = df['Region'].unique()
all_year = df['Year'].unique()

with open('russia_copy.geojson','r',encoding='UTF-8') as response:
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
        html.P("Калинина Ю.А.", className="display-18"),
        html.P(
            "Макарова А.В. ", className="display-18"
        ),
        html.Hr(style={'color': 'black'}),
        dbc.Nav(
            [
                dbc.NavLink("Статистика", href="/", active="exact"),
                dbc.NavLink("Регионы", href="/page-1", active="exact"),
                dbc.NavLink("Карта регионов", href="/page-2", active="exact"),
                dbc.NavLink("О проекте", href="/page-3", active="exact"),
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
                                {'label':'ВВП', 'value': 'ВВП'},
                                {'label':'Доля инновационно активных организаций', 'value': 'Доля инновационно активных организации'},
                                {'label':'Доля инновационных продуктов', 'value': 'Доля инновационных продуктов'},
                                {'label':'Инвестиции в основной капитал на душу населения', 'value': 'Инвестиции в основной капитал на душу населения'},
                            ],
                            id = 'crossfilter-ind0',
                            value = 'ВВП',
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
                        value = all_year[1],
                        # возможность множественного выбора
                        multi = False
                    )
                ],width=3),
            ]),

            html.Br(),
            dbc.Row([  
            dbc.Col([
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_1"),
                ]),],style = {'font-size': '1em','width': '33%','float': 'center', 'display': 'inline-block'},width=2),
                
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_2"),
                ]),],style = {'font-size': '1em','width': '33%','float': 'center', 'display': 'inline-block'},width=2),
                
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_3"),
                ]),],style = {'font-size': '1em','width': '33%','float': 'center', 'display': 'inline-block'},width=2),
                ],style = {'font-size': '0.8em','width':'100%','float': 'center', 'display': 'inline-block'},width=2),

        dbc.Col([        
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_4"),
                ])],style = {'font-size': '1em','width': '33%','float': 'center', 'display': 'inline-block'},width=2),
                
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_5"),
                ]),],style = {'font-size': '1em','width': '33%','float': 'center', 'display': 'inline-block'},width=2),    
            dbc.Col([
                dbc.Row([
                    html.Div(id="cards_6"),
                ]),],style = {'font-size': '1.25em','width': '33%','float': 'center', 'display': 'inline-block'},width=1),
                
            ],style = {'font-size': '0.8em','height':'100%','width':'100%','float': 'center', 'display': 'inline-block'},width=2),

            html.Br(),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("ВВП на душу населения"),
                        dbc.Badge(id="region-badge1", color="primary", className="mr-1"),
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
                        dbc.Badge(id="region-badge2", color="primary", className="mr-1"),
                    ], style={'textAlign': 'center'})
                )
            ]), 
            html.Div(
                    dcc.Graph(id = 'sald'),
                    style = {'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Доходы и расходы регионального бюджета"),
                        dbc.Badge(id="region-badge3", color="primary", className="mr-1"),
                    ], style={'textAlign': 'center'})
                ),
                html.Div(
                    dcc.Graph(id='dox'),
                    style={'width': '100%', 'float': 'right', 'display': 'inline-block'}
                ),
            ]),
            
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.Hr(style={'color': 'black'}),
                        html.H5("Инвестиции в основной капитал на душу населения"),
                        dbc.Badge(id="region-badge4", color="primary", className="mr-1"),
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
                        dbc.Badge(id="region-badge5", color="primary", className="mr-1"),
                    ], style={'textAlign': 'center'})
                ),html.Div(
                    dcc.Graph(id = 'vor'),
                    style = {'width': '100%', 'display': 'inline-block'}
                ),
            ]),]) 
        ]
    
    elif pathname == "/page-2":
        return [
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H3("Тепловая карта показателей"),
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
                            {'label':'ВВП', 'value': 'ВВП'},
                            {'label':'Доля инновационно активных организаций', 'value': 'Доля инновационно активных организации'},
                            {'label':'Доля инновационных продуктов', 'value': 'Доля инновационных продуктов'},
                            {'label':'Инвестиции в основной капитал на душу населения', 'value': 'Инвестиции в основной капитал на душу населения'},
                        ],
                        value='ВВП',
                        id='crossfilter-ind2',
                    ),
                ],width=3),
            
                dbc.Col([
                    dcc.Graph(id = 'rusmap', config={'displayModeBar': False}),
                ], width=9)
            ],style = {'font-size': '0.8em',
                    'borderBottom': 'thin lightgrey solid',
                    'backgroundColor': 'rgb(242,248,253)',
                    'padding': '5px 10px'}) 
        ]
    elif pathname == "/page-3":
        return [
           dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H3("Анализ региональной экономики России"),
                        html.P("Подготовили Калинина Ю. А. и Макарова А. В. – группа БСБО-14-21", className="display-18"),
                        html.Hr(style={'color': 'black'}),
                    ], style={'textAlign': 'center'})
                )
            ]), 

            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H4("Анализ региональной экономики России"),
                    ], style={'textAlign': 'left'})
                )
            ]), 
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.P("Высокая степень регионализации является характерной для России чертой. Хотя с одной стороны это поддерживает многообразие общества, с другой — вызывает диспропорции в экономике и неустойчивость.", className="display-20"),
                        html.P("В свою очередь это сказывается и на стратегии развития экономики. На данный момент перед Россией стоит цель перехода в категорию развитых стран, для этого необходимо обеспечить сбалансированность региональной экономики (Стратегия пространственного развития России), в том числе сгладить различия в уровне и темпе развития регионов. ", className="display-20"),
                        html.P("Для составления экономической стратегии важно провести качественный анализ региональной экономики, однако этому препятствует дефицит и бессистемность статистики. Анализ региональной экономики на основе комплексного подхода с использованием современных методов исследования должен решить данную проблему и помочь эффективно и качественно анализировать и выстраивать экономическую политику.", className="display-20"),
                    ], style={'textAlign': 'left'})
                )
            ]), 
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H2(""),
                        html.H4("Актуальные вопросы, решаемые дашбордом"),
                    ], style={'textAlign': 'left'})
                )
            ]),
             dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H6("1. Неравномерность развития:"),
                        html.P("Регионы России отличаются по уровню развития, доходам, инвестиционной привлекательности и т.д. Анализ региональной экономики помогает выявить эту неравномерность и разработать меры для ее устранения.", className="display-20"),
                        html.H6("2.Влияние внутренних и внешних факторов:"),
                        html.P("Экономика каждого региона в разной степени испытывает на себе влияние внутренних и внешних проблем страны. Анализ экономической ситуации в определенном временном периоде позволяет оценить это влияние и разработать стратегии адаптации.", className="display-20"),
                        html.H6("3.Повышение конкурентоспособности:"),
                        html.P("Регионы конкурируют между собой за инвестиции и квалифицированные кадры. Анализ региональной экономики позволяет оценить конкурентоспособность региона, а также разработать меры по ее повышению.", className="display-20"),
                        html.H6("4.Обеспечение устойчивого развития:"),
                        html.P("Региональная экономика должна обеспечить не только экономический рост, но и социальное благополучие населения. Анализ экономики региона позволяет оценить уровень его устойчивости и разработать меры повышения.", className="display-20"),
                        html.H6("5.Выравнивание бюджетной обеспеченности: "),
                        html.P("Обеспечение равного доступа к бюджетным ресурсам для всех регионов, невозможно без тщательного анализа их финансового положения и потребности в средствах.", className="display-20"),
                        html.H6("6.Оценка эффективности региональной политики:"),
                        html.P("Анализ региональной экономики позволяет оценить эффективность реализуемой региональной политики, выявить ее сильные и слабые стороны, скорректировать курс развития при необходимости.", className="display-20"),
                        html.H6("7.Реализация национальных проектов: "),
                        html.P("Эффективная реализация национальных проектов в регионах требует оценки их влияния на экономику конкретных регионов.", className="display-20"),
                        html.H6("8.Распределение полномочий: "),
                        html.P("Разграничение полномочий между федеральным центром и регионами требует тщательного анализа экономического потенциала и возможностей каждого региона.", className="display-20"),
                    ], style={'textAlign': 'left'})
                )
            ]),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H2(""),
                        html.H4("Как собирались данные"),
                    ], style={'textAlign': 'left'})
                )
            ]),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.P("Сайт https://datasets-isc.ru/ предоставляет ценный набор данных, который может быть использован для создания информативного и актуального дашборда. Нами был взят датасет «Интерактивная статистика и интеллектуальная аналитика сбалансированности региональной экономики России на основе Больших данных и блокчейн – 2024» (https://datasets-isc.ru/data-2/747-data-set-interaktivnaya-statistika-i-intellektualnaya-analitika-sbalansirovannosti-regionalnoj-ekonomiki-rossii-na-osnove-bolshikh-dannykh-i-blokchejn-2021). В датасете объединена статистика по теме сбалансированности региональной экономики России за 2005-2023 гг., отражающая уровень и потенциал социально-экономического развития российских регионов. ", className="display-18"),                    
                        ], style={'textAlign': 'left'})
                )
            ]), 
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H6("В датасете содержатся показатели, большинство из которых предоставлено Росстатом, вот ключевые из них:"),
                        html.P("ВВП: валовой внутренний продукт является одним из важнейших показателей экономического развития региона;", className="display-20"),
                        html.P("Воронки отсталости: рассчитанные на базе ВВП,  отражают собой механизм потери отдельными регионами возможностей для развития вследствие отставания во времени;", className="display-20"),
                        html.P("Доходы регионального бюджета: денежные поступления, складывающиеся из доходов от региональных налогов и сборов.", className="display-20"),
                        html.P("Расходы регионального бюджета: денежные средства, направляемые из бюджетного фонда на финансовое обеспечение выполняемых задач и функций региона.", className="display-20"),
                        html.P("Сальдо: сальдо регионального бюджета представляет собой соотношение между доходной и расходной частями бюджета;", className="display-20"),
                        html.P("Доля инновационно активных организаций: доля компаний, занимающихся инновациями;", className="display-20"),
                        html.P("Доля инновационных продуктов: доля инновационной продукции региона (товаров, услуг), созданной с использованием результатов интеллектуальной деятельности;", className="display-20"),
                        html.P("Инвестиции в основной капитал на душу населения: показывает объем инвестиций в основной капитал, что является индикатором будущего экономического роста.", className="display-20"),
                    ], style={'textAlign': 'left'})
                )
            ]),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H2(""),
                        html.H4("Подготовка данных"),
                        html.P("Для дальнейшего анализа данные были обработаны и подготовлены. С получившимся датасетом можно ознакомиться по ссылке:", className="display-18"),
                        html.P("https://docs.google.com/spreadsheets/d/e/2PACX-1vRWse4Knyb73VWoIywsaDSMAbRmHnJKhYlfPqM7sUOdk9hlJam1kZIRSmIjqJbjZKMg-OfWP37HROJu/pubhtml.", className="display-18"),                    
                        ], style={'textAlign': 'left'})
                )
            ]),
            dbc.Row ([
                dbc.Col(
                        html.Div([
                        html.H4(""),
                        html.H4("Визуализация данных"),
                    ], style={'textAlign': 'left'})
                )
            ]),
            dbc.Row ([
                dbc.Col(
                        html.Div([                        
                        html.P("Код для визуализации данных был написан нами с использованием средств python.", className="display-18"),                    
                        html.P("Полностью код можно посмотреть на GitHub"),
                        html.P("(Макарова - https://github.com/Anastas1aMakarova/Russian_Regional_Economy_Analysis)", className="display-18"),
                        html.P("(Калинина - https://github.com/Kal1n1na/Russian_Regional_Economy_Analysis).", className="display-18"),
                        ], style={'textAlign': 'left'})
                )
            ]),  
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
    figure = px.treemap(
        filtered_data,
        names='Region',
        values=indication,
        parents=[''] * len(filtered_data),  
        color='Region',
        color_continuous_scale=px.colors.sequential.Blues,
        labels={'Region':'Регион', 'Year':'Год',
                'Доля инновационных продуктов':'Доля инновационных продуктов', 'ВВП':'ВВП',
                'Доля инновационно активных организации':'Доля инновационно-активных организаций',
                'Инвестиции в основной капитал на душу населения':'Инвестиции в основной капитал на душу населения'},
    )

    figure.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=800, width=1000, showlegend=False)
    return figure


@callback(
    Output('tabletop', 'children'),
    [Input('crossfilter-ind0', 'value'),
    Input('crossfilter-year0', 'value')]
)
def update_table(indication, year):
    vvp_count = df[(df['Year'] == year)].sort_values(by=indication, ascending=False)
    vvp_table = vvp_count.iloc[0:10][['Region', indication]]
    vvp_table.columns = ['Регион', indication] 
    table = dbc.Table.from_dataframe(
        vvp_table, striped=True, bordered=True, hover=True, index=False,
    )
    return table

@callback(
    Output('card_1', 'children'),
    Output('card_2', 'children'),
    Output('card_3', 'children'),
    [Input('crossfilter-year0', 'value')]
)
def update_card1(year):
    df_count=df[(df['Year'] <= year) ]

    c1=df_count['Доходы регионального бюджета'].sum()
    c2=df_count['Расходы регионального бюджета'].sum()
    c3=df_count['Сальдо регионального бюджета'].sum()
    
    return c1,c2,c3

@callback(
    Output('region-badge1', 'children'),
    [Input('crossfilter-reg', 'value')]
)
def update_region_badge(reg):
    return reg

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
        y='ВВП',
        markers=False,
        labels={'Year':'Год', 'ВВП':'ВВП на душу населения'},
    )
    figure.update_layout(
        xaxis=dict(
            tickvals=filtered_data['Year'].unique(),
            ticktext=filtered_data['Year'].unique().astype(int).astype(str)
        )
    )
    return figure

@callback(
    Output('region-badge2', 'children'),
    [Input('crossfilter-reg', 'value')]
)
def update_region_badge(reg):
    return reg

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
        y='Сальдо регионального бюджета',
        markers=False,
        labels={'Year':'Год', 'Сальдо регионального бюджета':'Сальдо региональнного бюджета'},
    )
    figure.update_layout(
        xaxis=dict(
            tickvals=filtered_data['Year'].unique(),
            ticktext=filtered_data['Year'].unique().astype(int).astype(str)
        )
    )
    return figure

@callback(
    Output('region-badge3', 'children'),
    [Input('crossfilter-reg', 'value')]
)
def update_region_badge(reg):
    return reg

@callback(
    Output('dox', 'figure'),
    [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_dox(reg, year):
    filtered_data = df[(df['Year'] <= year) & (df['Region'] == reg)] 
    fig = px.line(
        filtered_data,
        x='Year',
        y=['Доходы регионального бюджета', 'Расходы регионального бюджета'],
        markers=False,
        labels={'Year':'Год', 'value':'Значение'},
    )
    fig.update_layout(
        xaxis=dict(
            tickvals=filtered_data['Year'].unique(),
            ticktext=filtered_data['Year'].unique().astype(int).astype(str)
        ),
        legend_title_text='Тип бюджета'
    )
    return fig

@callback(
    Output('region-badge4', 'children'),
    [Input('crossfilter-reg', 'value')]
)
def update_region_badge(reg):
    return reg

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
        y='Инвестиции в основной капитал на душу населения',
        markers=False,
        labels={'Year':'Год', 'Инвестиции в основной капитал на душу населения':'Инвестиции в основной капитал на душу населения'},
    )
    figure.update_layout(
        xaxis=dict(
            tickvals=filtered_data['Year'].unique(),
            ticktext=filtered_data['Year'].unique().astype(int).astype(str)
        )
    )
    return figure

@callback(
    Output('region-badge5', 'children'),
    [Input('crossfilter-reg', 'value')]
)
def update_region_badge(reg):
    return reg

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
        y='Глубина воронки',
        labels={'Year':'Год', 'Глубина воронки':'Глубина воронки отсталости'},
    )
    figure.update_layout(
        xaxis=dict(
            tickvals=filtered_data['Year'].unique(),
            ticktext=filtered_data['Year'].unique().astype(int).astype(str)
        )
    )
    return figure


@callback(
    Output('cards_1', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_cards2(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    dow2=df_count.iloc[0]['Доходы регионального бюджета']
    dow1=df_count2.iloc[0]['Доходы регионального бюджета']

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = dow2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': dow1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        autosize=False,
        width=280,
        height=280,
        )
    cards_1 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Доходы регионального бюджета"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center'}) # , "height": "1rem"
            
    return cards_1

@callback(
    Output('cards_2', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card2(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    ras2=df_count.iloc[0]['Расходы регионального бюджета']
    ras1=df_count2.iloc[0]['Расходы регионального бюджета']
    
    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = ras2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': ras1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        #autosize=False,
        width=280,
        height=280,
        )
    cards_2 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Расходы регионального бюджета"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center'}) # , "height": "1rem"
            
    return cards_2

@callback(
    Output('cards_3', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card3(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    sal2=df_count.iloc[0]['Сальдо регионального бюджета']
    sal1=df_count2.iloc[0]['Сальдо регионального бюджета']

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = sal2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': sal1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        autosize=False,
        width=280,
        height=280,
        )
    cards_3 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Сальдо регионального бюджета"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center'}) # , "height": "1rem"
            
    return cards_3

@callback(
    Output('cards_4', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card4(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    inn2=df_count.iloc[0]['Доля инновационных продуктов']
    inn1=df_count2.iloc[0]['Доля инновационных продуктов']

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = inn2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': inn1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        autosize=False,
        width=280,
        height=280,
        )
    cards_4 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Доля инновационных продуктов"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center'}) # , "height": "1rem"
            
    return cards_4

@callback(
    Output('cards_5', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card5(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    inn_act2=df_count.iloc[0]['Доля инновационно активных организации']
    inn_act1=df_count2.iloc[0]['Доля инновационно активных организации']

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = inn_act2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': inn_act1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        autosize=False,
        width=280,
        height=280,
        )
    cards_5 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Доля инновационно активных организации"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center'}) # , "height": "1rem"
            
    return cards_5

@callback(
    Output('cards_6', 'children'),
     [Input('crossfilter-reg', 'value'),
     Input('crossfilter-year1', 'value')
    ]
)
def update_card6(reg, year):
    df_count=df[(df['Year'] == year) & (df['Region'] == reg)]
    df_count2=df[(df['Year'] == year - 1) & (df['Region'] == reg)]

    inv2=df_count.iloc[0]['Инвестиции в основной капитал на душу населения']
    inv1=df_count2.iloc[0]['Инвестиции в основной капитал на душу населения']

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = inv2,
        number = {'prefix': ""},
        delta = {'position': "top", 'relative': True,'reference': inv1},
        domain = {'x': [0, 1], 'y': [0.25, 0.75]}))
    fig.update_layout(
        autosize=False,
        width=280,
        height=280,
        )
    cards_6 = dbc.Card([
        dbc.Row([
            dbc.CardHeader("Инвестиции в основной капитал на душу населения"),
                 ]),
        dbc.Row([
            html.Div([
                dcc.Graph(figure=fig),
                ], style={'textAlign': 'center'})
            ],)
            ], style={'textAlign': 'center','font-size': '0.8em'}) #, "height": "1rem"
            
    return cards_6

@callback(
    Output('rusmap', 'figure'),
    [Input('crossfilter-ind2', 'value')]
)
def update_rusmap(indication):
    # Assume df is a Pandas DataFrame with the required columns
    filtered_data = df[(df['Year'] <= 2023)]
    
    # Assume counties is a valid GeoJSON object
    figure = px.choropleth_mapbox(
        filtered_data,
        geojson=counties,
        featureidkey='properties.cartodb_id',
        color=indication,  # Replace with a valid column name
        locations='cartodb_id',
        color_continuous_scale=px.colors.sequential.Blues,
        mapbox_style="carto-positron",
        zoom=20,
        opacity=0.5,
        hover_name='Region',
        hover_data={'Region': True, 'Year': True, 'cartodb_id': False,
                    'ВВП': True, 'Доля инновационно активных организации': True,
                    'Доля инновационных продуктов': True, 'Инвестиции в основной капитал на душу населения': True,
                    'Okrug': False},
        labels={'Region': 'Регион', 'Year': 'Год',
                'Доля инновационных продуктов': 'Доля иннвационных продуктов', 'ВВП': 'ВВП',
                'Доля инновационно активных организации': 'Доля иннвационно-активных организаций',
                'Инвестиции в основной капитал на душу населения': 'Инвестиции в капитал'},
        animation_frame='Year'  # Make sure Year is a numeric or datetime column
    )
    
    figure.update_layout(mapbox_style="carto-positron",
                        margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='world',
                        mapbox_zoom=1.8, mapbox_center = {"lat": 65, "lon": 95}, height=500, width=800,
                        showlegend=False)
    return figure

if __name__ == '__main__':
        app.run_server(debug=True)
