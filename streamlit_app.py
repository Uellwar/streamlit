#!/usr/bin/env python
# coding: utf-8

get_ipython().system('pip instal plotly')
get_ipython().system('pip instal plotly-express')
get_ipython().system('pip install dash')

import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output 


df_full = pd.read_csv('dados_limpos/df_full.csv')

# Funções
# Plotagem de histograma(para dados quantitativos) e contagem de valores por classe(para dados categóricos)
def plot_custom(typevis, df=None,x=None,y=None,titulo=None,histnorm=None, labelx=None, labely=None, marginal=None, text_auto='.2',label_y_visible=True, values_axis_y=True,categoryorder=None,nbins=10, color=None,showlegend=False):
  
  if (typevis == 'histogram'):
    fig = px.histogram(df,
                            x=x,
                            title=titulo,
                            height=675,
                            width=1200,
                            color_discrete_sequence=['#03DAC5'],
                            marginal=marginal,
                            text_auto=text_auto,
                            nbins=nbins,
                            histnorm=histnorm)
  
  if (typevis == 'bar'):
    fig = px.bar(df,
                 height=450,
                 width=800,
                 text_auto=text_auto,
                 title=titulo,
                 color_discrete_sequence=['#03DAC5'],
                 )

  if (typevis == 'box'):
    fig = px.box(df,
                x=x,
                y=y,
                color=color,
                title=titulo,
                height=450,
                width=800,)

  fig.update_xaxes(showgrid=False, categoryorder=categoryorder)
  fig.update_yaxes(showgrid=False)
  fig.update_yaxes(visible=label_y_visible, showticklabels=values_axis_y)
  fig.update_layout(margin=dict(t=100, b=0, l=70, r=40),
                    xaxis_tickangle=360,
                    xaxis_title=labelx, yaxis_title=labely,
                    showlegend=showlegend,
                    plot_bgcolor='#383838', paper_bgcolor='#383838',
                    title_font=dict(size=25, color='#a5a7ab', family="Muli, sans-serif"),
                    font=dict(color='#8a8d93',size=18),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
  return fig


app = Dash(__name__)

# Import
df = df_full.copy()

# ------------------------------------------------------------------------------
# Layout
app.layout = html.Div([

    html.H1("Análise de Dados CEPON", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_drop",
                 options=[
                     {"label": "Gênero", "value":'SEXO'},
                     {"label": "Renda Familiar", "value":'RENDA FAMILIAR'},
                     {"label": "Especialidades", "value":'GRUPO ESPECIALIDADE'},
                     {"label": "Idade", "value":'IDADE ANOS'},
                     {"label": "Índice Burnout", "value":'Indice Burnout Soma Total'},],
                 multi=False,
                 value='SEXO',
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_graph', figure={})

])


# ------------------------------------------------------------------------------
# Connectando os gráficos com os componentes
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_graph', component_property='figure')],
    [Input(component_id='slct_drop', component_property='value')]
)
def update_graph(option_slctd):
    container = "Infos do grafico {} selecionado: ".format(option_slctd.title())

    dff = df.copy()
    fig = plot_custom(df=dff,
            x=option_slctd,
            titulo='Porcentagem da Distribuição de {}'.format(option_slctd.title()),
            labely='Percentual',
            typevis='histogram',
            histnorm='percent',
            categoryorder='max descending',
            text_auto='.4')

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
