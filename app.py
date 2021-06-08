#!/usr/bin/python
# -*- coding: utf-8 -*-

# Otetaan tarvittavat kirjastot mukaan.

import numpy as np
import math
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import Flask
import dash_daq as daq
import os


# Perustetaan sovellus.

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key','secret')
app = dash.Dash(name = __name__, server = server,prevent_initial_callbacks=True)


app.title = 'Solidautoilu'



def kulutus(etäisyys, nopeus, auto, vakionopeus = 1):
    
    
    """
    
    Laskee kulutuksen perustuen ajettuun matkaan, nopeuteen sekä auton tyyppiin
    vakionopeuden ollessa 1 km / h ja kulmakertoimen 1.009.
    
    """
    
    kulutusluokka = {'A':3/100,
               'B':3.5/100,
              'C':4/100}[auto]
    
    kerroin = 1.009
    
    muutos = nopeus - vakionopeus
    
    # Huom. ei if-else lausetta!
    
    return {0: etäisyys *  kulutusluokka, 
            1: etäisyys * kulutusluokka * kerroin ** muutos, 
            -1: etäisyys * kulutusluokka * kerroin ** muutos}[np.sign(muutos)]


def aika(etäisyys, nopeus):
    
    
    """
    
    Laske annetun etäisyyden ajamiseen tarvitun ajan tunneissa ja minuuteissa.
    
    """
    
    aika = etäisyys / nopeus
    
    minuutit, tunnit = math.modf(aika)
    
       
    return (int(tunnit), int(minuutit * 60))


# Perustetaan aplikaation rakenne.
def serve_layout():
    return html.Div(children = [
        
                        html.H1('Solidautoilu',style={'width':'88%', 'margin':20, 'textAlign': 'center'}),
                        html.H2('Solidabiksen koodaushaasteeseen tehty autoilumittarisovellus',style={'width':'88%', 'margin':20, 'textAlign': 'center'}),
                        html.Br(),
                        html.P('Kesälomat lähestyvät ja monien katseet kääntyvät kohti kesämökkejä. Osalla nämä löytyvät lähempää, osalla taas matkustukseen kuluu pitkiäkin aikoja. Monesti tien päällä ollessa tuntuu siltä, että jos hieman vielä kiihdyttäisi, olisi perillä merkittävästi nopeammin… vai olisiko sittenkään? Ovatko voitetut minuutit kasvaneiden matkakustannusten arvoisia? Entä kuinka paljon matkustusajoneuvon tyyppi vaikuttaa tähän?'),
                        html.Br(),
                        html.P('Tämä autoilumittari-sovellus suorittaa vertailu matka-ajan ja polttoaineen kulutuksen välillä kahden eri valitun nopeuden mukaan: käyttäjä ilmoittaa saman matkustettavan etäisyyden samalla kulkuneuvotyypillä eri nopeuksilla ja sovellus laskee miten paljon nopeammin käyttäjä on perillä ja kuinka paljon enemmän polttoainetta tähän kuluu. Sovellus näyttää molemmista annetuista matkanopeuksista käytetyn ajan ja polttoaineen, sekä näiden kahden eron.'),
                        html.Br(),
                        html.P('Autojen bensankulutus kasvaa 1.009 kulmakertoimella. Eli jos auton nopeus kasvaa 1km/h, niin bensankulutus kasvaa 1.009 kertaiseksi. Eri autojen bensakulutus 1km/h nopeudella on ilmotettu autojen valintojen vieressä.'),
                        html.Br(),
                        html.A('Tämä tehtävä on myös vastaus Solidabiksen kesän 2021 koodihaasteeseen.', href='https://koodihaaste.solidabis.com/#/'),
                        html.Br(),
    
                        html.Div(className = 'row',
                                 children = [
                                     
                                     html.Div(className = 'six columns',children = [
                                                 html.H2('1. Valitse autosi tyyppi.'),
                                                 html.P('Alla on lueteltu bensakulutus 1km/h nopeudella.'),
                                                 dcc.RadioItems(id = 'autot',
                                                               options = [
                                                               
                                                               {'label':'Auto A: 3l / 100km', 'value': 'A'},
                                                               {'label':'Auto B: 3.5l / 100km', 'value': 'B'},
                                                               {'label':'Auto C: 4l / 100km', 'value': 'C'}
                                                               
                                                               ],
                                                                value = 'A',
                                                                labelStyle={'display': 'inline-block'}
                                                               )
                                                 ]
                                             ),
                                     html.Div(className = 'six columns',
                                             children = [
                                             
                                                 html.H2('2. Ilmoita ajamasi matka kilometreissä.'),
                                                 dcc.Input(id = 'matka', type = 'number', min = 1, value = 60, inputMode = 'numeric')
                                             
                                             ]
                                      )
                                ]
                                ),
                        html.Div(className = 'row',
                                 children = [
                                     
                                     html.Div(className = 'six columns',children = [
                                                 html.H2('3. Valitse ensimmäinen nopeusskenaario.'),
                                                 dcc.Slider(id = 'nopeus1',
                                                           min = 10,
                                                           max = 200,
                                                           step = 1,
                                                           value = 80,
                                                           marks = {10:'10 km/h',
                                                                   20:'20 km/h',
                                                                   50:'50 km/h',
                                                                   80:'80 km/h',
                                                                   100:'100 km/h',
                                                                   200: '200 km/h'}
                                                           ),
                                                  html.Div(id = 'nopeus1_output')
                                                 ]
                                             ),
                                     html.Div(className = 'six columns',children = [
                                                 html.H2('4. Valitse toinen nopeusskenaario.'),
                                                 dcc.Slider(id = 'nopeus2',
                                                           min = 10,
                                                           max = 200,
                                                           step = 1,
                                                           value = 100,
                                                           marks = {10:'10 km/h',
                                                                   20:'20 km/h',
                                                                   50:'50 km/h',
                                                                   80:'80 km/h',
                                                                   100:'100 km/h',
                                                                   200: '200 km/h'}
                                                           ),
                                                 html.Div(id = 'nopeus2_output')
                                                 ]
                                             )
                                ]
                                ),
               html.Div(
                                     style={'width':'88%', 'margin':20, 'textAlign': 'center'},
                                     children=[
                                         html.Button( '5. Suorita simulaatio', id = 'sim',n_clicks=0)
                            ]),
                       html.Div(id = 'valittu_matka',
                                     style={'width':'88%', 'margin':20, 'textAlign': 'center'},
                                     ),
    
                    html.Div(className = 'row', children=[
                    
                        
                                    html.Div(className = 'six columns', children = [
                                    
                                                html.Div(id = 'speed_1_result', style={'width':'88%', 'margin':20, 'textAlign': 'right'})
                                    
                                                    ]),
                                    html.Div(className = 'six columns', children = [
                                    
                                                html.Div(id = 'speed_2_result', style={'width':'88%', 'margin':20, 'textAlign': 'left'})
                                    
                                                    ])
                    
                                          ]
                            ),
                    html.Div(id = 'difference', className = 'row', style={'width':'88%', 'margin':20, 'textAlign': 'center'}),
                    html.Br(),
                    html.Label(['Tehnyt: Tuomas Poukkula.']),
                    html.A('Katso projekti Githubissa', href='https://github.com/tuopouk/autoilumittari'),
                    html.Br(),
                    html.A('Seuraa Twitterissä', href='https://twitter.com/TuomasPoukkula'),
                    html.Br(),
                    html.A(' ja LinkedInissä.', href='https://www.linkedin.com/in/tuomaspoukkula/')
                               
                   ]

                   )




#  Päivitetään ensimmäisen nopeusskenaarion valinta käyttäjälle.        
@app.callback(
    dash.dependencies.Output('nopeus1_output', 'children'),
    [dash.dependencies.Input('nopeus1', 'value')])
def update_output(value):
    return 'Valitsit {} km/h.'.format(value)   

#  Päivitetään toisen nopeusskenaarion valinta käyttäjälle. 
@app.callback(
    dash.dependencies.Output('nopeus2_output', 'children'),
    [dash.dependencies.Input('nopeus2', 'value')])
def update_output(value):
    return 'Valitsit {} km/h.'.format(value)   
    

    
# Päivitetään ajettava matka käyttäjälle.     
@app.callback(
    Output('valittu_matka','children'),
    [Input('sim', 'n_clicks')],
    [
    State('matka','value')

    ]
)
def update_selected_distance(n_click, matka ):
    
    
    
    return html.Div(children = [
        
        html.P('Ajettava matka: {} km.'.format(matka))
   ])
    
    
    
#  Päivitetään ensimmäisen nopeusskenaarion tulos.                                
@app.callback(
    Output('speed_1_result','children'),
    [Input('sim', 'n_clicks')],
    [State('autot','value'),
    State('matka','value'),
     State('nopeus1','value')

    ]
)
def update_speed_1_result(n_click, auto, matka, nopeus):
    
    consumption = kulutus(matka, nopeus, auto)
    tunnit, minuutit = aika(matka, nopeus)
    
    return html.Div(children = [
        html.H3('Skenaario A:'),
        html.P('Bensaa kuluisi noin {} litraa.'.format(round(consumption,2))),
        html.P('Keskikulutus olisi noin {} litraa / 100 km.'.format(round(100*consumption/matka,2))),
        html.P('Aikaa kuluisi noin {} tuntia ja {} minuuttia.'.format(int(tunnit), int(minuutit)).replace('0 tuntia ja ', '').replace('ja 0 minuuttia', '').replace('noin 1 tuntia ', 'noin yksi tunti ').replace(' .','.'))
   ])


#  Päivitetään toisen nopeusskenaarion tulos.   
@app.callback(
    Output('speed_2_result','children'),
    [Input('sim', 'n_clicks')],
    [State('autot','value'),
    State('matka','value'),
     State('nopeus2','value')

    ]
)
def update_speed_2_result(n_click, auto, matka, nopeus):
    
    consumption = kulutus(matka, nopeus, auto)
    tunnit, minuutit = aika(matka, nopeus)
    
    return html.Div(children = [
        html.H3('Skenaario B:'),
        html.P('Bensaa kuluisi noin {} litraa.'.format(round(consumption,2))),
        html.P('Keskikulutus olisi noin {} litraa / 100 km.'.format(round(100*consumption/matka,2))),
        html.P('Aikaa kuluisi noin {} tuntia ja {} minuuttia.'.format(int(tunnit), int(minuutit)).replace('0 tuntia ja ', '').replace('ja 0 minuuttia', '').replace('noin 1 tuntia ', 'noin yksi tunti ').replace(' .','.'))
   ])


# Päivitetään skenaarioiden vertailu.
@app.callback(
    Output('difference','children'),
    [Input('sim', 'n_clicks')],
    [State('autot','value'),
    State('matka','value'),
     State('nopeus1','value'),
     State('nopeus2','value')

    ]
)
def update_difference(n_click, auto, matka, nopeus1, nopeus2):
    
    consumption1 = kulutus(matka, nopeus1, auto)
    tunnit1, minuutit1 = aika(matka, nopeus1)
    keskikulutus1 = 100*consumption1/matka
    
    consumption2 = kulutus(matka, nopeus2, auto)
    tunnit2, minuutit2 = aika(matka, nopeus2)
    keskikulutus2 = 100*consumption2/matka
    
    
    kulutus_ero = consumption1 - consumption2
    
    keskikulutus_ero = keskikulutus1 - keskikulutus2
    
    aika_ero = (tunnit1  + minuutit1/60) - (tunnit2  + minuutit2/60)
    
    ero_min, ero_tunnit = math.modf(aika_ero)
    
   
    
    
    return html.Div(children = [
        html.H3('Vertailu:'),
        
        html.P({-1:'Skenaariossa A bensaa kuluisi noin {} litraa vähemmän.'.format(round(-kulutus_ero, 2)), 
                0: 'Molemmissa skenaarioissa bensaa kuluisi suunnilleen yhtä paljon.',
                1:'Skenaariossa B bensaa kuluisi noin {} litraa vähemmän.'.format(round(kulutus_ero, 2))}[np.sign(kulutus_ero)]),
        
        html.P({-1:'Skenaariossa A keskikulutus 100 kilometriä kohden olisi noin {} litraa vähemmän.'.format(round(-keskikulutus_ero, 2)), 
                0: 'Molemmissa skenaarioissa keskikulutus 100 kilometriä kohde olisi suunnilleen yhtä suuri.',
                1:'Skenaariossa B keskikulutus 100 kilometriä kohden olisi noin {} litraa vähemmän.'.format(round(keskikulutus_ero, 2))}[np.sign(keskikulutus_ero)]),
        
        html.P({-1:'Skenaario A olisi noin {} tuntia ja {} minuuttia nopeampi.'.format(int(abs(ero_tunnit)), int(abs(-ero_min)*60)), 
                0: 'Molemmat skenaariot olisivat suunnilleen yhtä nopeita.',
                1:'Skenaario B olisi noin {} tuntia ja {} minuuttia nopeampi.'.format(int(abs(ero_tunnit)), int(abs(ero_min)*60))}[np.sign(aika_ero)].replace('0 tuntia ja ','').replace('ja 0 minuuttia ', ''))

   ])





app.config['suppress_callback_exceptions']=True  
app.layout = serve_layout
# Ajetaan sovellus.
if __name__ == '__main__':
    app.run_server(debug=False)   
