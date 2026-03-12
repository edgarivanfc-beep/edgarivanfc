"""
Dashboard: Resultados 1ª Convocatoria CNE
Generación Eléctrica e Interconexión al SEN — DOF 17/10/2025
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

datos_raw = [
    ("Noreste",    "23-Saltillo",     "Eólica",        "2028",      300,   76.0,  "Derramadero",                          400, "Coahuila",           0.00,   300.00),
    ("Oriental",   "46-Veracruz",     "Fotovoltaica",  "2030",      250,   44.0,  "Manlio Fabio Altamirano",              230, "Veracruz",           0.00,   250.00),
    ("Peninsular", "69-Valladolid",   "Eólica",        "2028-2029", 350, 2439.0,  "SE Maniobras LT Norte-Kanasín",        230, "Yucatán",          120.00,   230.00),
    ("Noreste",    "27-Güémez",       "Eólica",        "2028",      200,  176.0,  "Jiménez",                              115, "Tamaulipas",         0.00,   200.00),
    ("Oriental",   "58-Grijalva",     "Fotovoltaica",  "2029",      200,  150.0,  "Tapachula Potencia",                   115, "Chiapas",            0.00,   200.00),
    ("Occidental", "37-San Luis de",  "Fotovoltaica",  "2027-2029", 180,    0.0,  "Santa Fe (Guanajuato)",                115, "Guanajuato",         0.00,   180.00),
    ("Occidental", "33-San Luis",     "Eólica",        "2029",      170,    0.0,  "El Potosí",                            230, "San Luís Potosí",    0.00,   170.00),
    ("Occidental", "33-San Luis",     "Fotovoltaica",  "2027",      130,  756.0,  "San Diego Peñuelas",                   115, "Guanajuato",         0.00,   130.00),
    ("Oriental",   "46-Veracruz",     "Fotovoltaica",  "2029",      130,   31.0,  "Santa Fe (Veracruz)",                  115, "Veracruz",           0.00,   130.00),
    ("Noreste",    "21-Matamoros",    "Eólica",        "2027",      120,   38.0,  "Matamoros Potencia",                   138, "Tamaulipas",         0.00,   120.00),
    ("Oriental",   "48-Morelos",      "Fotovoltaica",  "2028",      120,   40.0,  "Yautepec Potencia",                    115, "Morelos",            0.00,   120.00),
    ("Occidental", "33-San Luis",     "Eólica",        "2028",      100, 1017.0,  "Charcas Potencia",                     115, "San Luís Potosí",    0.00,   100.00),
    ("Occidental", "31-Jalisco",      "Fotovoltaica",  "2028",      100,    0.0,  "Lagos Galera",                         115, "Jalisco",            0.00,   100.00),
    ("Oriental",   "59-Tabasco",      "Fotovoltaica",  "2029",      100,   40.0,  "Cárdenas Dos",                         115, "Tabasco",            0.00,   100.00),
    ("Occidental", "31-Jalisco",      "Fotovoltaica",  "2028",       90,  479.0,  "La Virgen",                            115, "Jalisco",            0.00,    90.00),
    ("Central",    "42-Tula-Pachuca", "Fotovoltaica",  "2030",       80,   45.0,  "Nochistongo",                          115, "Hidalgo",            0.00,    80.00),
    ("Noreste",    "25-Huasteca",     "Eólica",        "2027",       80,  106.0,  "SE Maniobras LT Libramiento-Mante",    115, "Tamaulipas",         0.00,    80.00),
    ("Occidental", "29-Tepic",        "Fotovoltaica",  "2029",       80,   97.0,  "Acaponeta",                            115, "Nayarit",            0.00,    80.00),
    ("Peninsular", "68-Dzitnup",      "Eólica",        "2028",      320,  139.0,  "Dzitnup",                              400, "Yucatán",          252.00,    68.00),
    ("Central",    "43-Toluca",       "Fotovoltaica",  "2028",       30,   91.0,  "Villa Guerrero",                       115, "Estado de México",   0.00,    30.00),
    ("Norte",      "13-Cuauhtémoc",   "Fotovoltaica",  "2029",       30,   35.0,  "Cuauhtémoc",                           115, "Chihuahua",          0.00,    30.00),
    ("Noreste",    "19-Nuevo",        "Eólica",        "2028",      140,   38.0,  "Falcon Mexicano",                      138, "Tamaulipas",       130.50,     9.50),
    ("Oriental",   "61-Juchitán",     "Eólica",        "2028",      200,   31.0,  "Juchitan Dos",                         115, "Oaxaca",           200.00,     0.00),
    ("Peninsular", "76-Chetumal",     "Eólica",        "2028",      200,   41.0,  "Xul-ha",                               115, "Quintana Roo",     200.00,     0.00),
    ("Occidental", "31-Jalisco",      "Fotovoltaica",  "2029",       90,  126.0,  "Ojo Caliente",                         115, "Zacatecas",         99.00,    -9.00),
    ("Occidental", "34-Salamanca",    "Fotovoltaica",  "2027",       90,    0.0,  "El Toro",                              115, "Guanajuato",       107.00,   -17.00),
    ("Central",    "42-Tula-Pachuca", "Fotovoltaica",  "2027-2028", 440,  991.0,  "SE Maniobras KM 110-Pachuca",          230, "Hidalgo",          459.27,   -19.27),
    ("Occidental", "38-Querétaro",    "Fotovoltaica",  "2027",      100, 2516.0,  "Tequisquiapan",                        115, "Querétaro",        122.40,   -22.40),
    ("Occidental", "38-Querétaro",    "Fotovoltaica",  "2028",      220,    0.0,  "SE Maniobras LT San Juan-Dañú",        230, "Hidalgo",          246.29,   -26.29),
    ("Oriental",   "46-Veracruz",     "Fotovoltaica",  "2028",      120,   31.0,  "Piedras Negras",                       115, "Veracruz",         147.00,   -27.00),
    ("Oriental",   "47-Puebla",       "Fotovoltaica",  "2027",      200,  215.0,  "SE Maniobras LT Tecali-Oriente",       115, "Puebla",           231.00,   -31.00),
    ("Peninsular", "64-Escárcega",    "Fotovoltaica",  "2028",      300,  139.0,  "Escárcega",                            400, "Campeche",         350.57,   -50.57),
    ("Peninsular", "64-Escárcega",    "Fotovoltaica",  "2028",      600, 2036.0,  "SE Maniobras LT Escárcega-Ticul",      400, "Campeche",         694.27,   -94.27),
    ("Noreste",    "25-Huasteca",     "Fotovoltaica",  "2028",      110,   27.0,  "Puerto Altamira Eléctrica",            115, "Tamaulipas",       207.52,   -97.52),
]

cols = ["GCR", "Region", "Tecnologia", "Anio_EOO", "Capacidad_MW", "Inversion_MDP",
        "SE_Corto", "kV", "Entidad", "MW_Asignados", "MW_Faltantes"]
df = pd.DataFrame(datos_raw, columns=cols)

def clasificar(row):
    if row["MW_Faltantes"] > 0 and row["MW_Asignados"] == 0:
        return "Desierta total"
    elif row["MW_Faltantes"] > 0 and row["MW_Asignados"] > 0:
        return "Desierta parcial"
    elif row["MW_Faltantes"] == 0:
        return "Cubierta exacta"
    else:
        return "Sobreasignada"

df["Estatus"]  = df.apply(clasificar, axis=1)
df["Pct_Asig"] = (df["MW_Asignados"] / df["Capacidad_MW"] * 100).round(1)

COLOR_MAP  = {"Desierta total":"#d62728","Desierta parcial":"#ff7f0e","Cubierta exacta":"#2ca02c","Sobreasignada":"#1f77b4"}
BADGE_COLOR= {"Desierta total":"danger","Desierta parcial":"warning","Cubierta exacta":"success","Sobreasignada":"info"}
EMOJI      = {"Desierta total":"🔴","Desierta parcial":"🟡","Cubierta exacta":"🟢","Sobreasignada":"🔵"}

GCR_OPTS = [{"label":"Todas","value":"Todas"}]+[{"label":g,"value":g} for g in sorted(df["GCR"].unique())]
TEC_OPTS = [{"label":"Todas","value":"Todas"},{"label":"Eólica","value":"Eolica"},{"label":"Fotovoltaica","value":"Fotovoltaica"}]
KV_OPTS  = [{"label":"Todos","value":"Todos"}]+[{"label":f"{k} kV","value":str(k)} for k in sorted(df["kV"].unique())]

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], title="CNE - 1a Convocatoria Generacion Electrica")
server = app.server

app.layout = dbc.Container(fluid=True, style={"fontFamily":"Segoe UI, sans-serif"}, children=[
    dbc.Row(dbc.Col(html.Div([
        html.H4("CNE - 1a Convocatoria de Generacion Electrica e Interconexion al SEN", className="text-white mb-1"),
        html.Small("DOF 17/10/2025  |  34 subestaciones evaluadas  |  Fuente: CNE", className="text-white-50"),
    ], className="p-3 mb-3 rounded", style={"background":"linear-gradient(90deg,#1b4f72,#2980b9)"}))),
    dbc.Row(id="kpi-row", className="mb-3 g-2"),
    dbc.Card(dbc.CardBody(dbc.Row([
        dbc.Col([html.Label("Region GCR", className="fw-bold small mb-1"),
                 dbc.RadioItems(id="filtro-gcr", options=GCR_OPTS, value="Todas", inline=True,
                                input_checked_class_name="btn-check",
                                label_class_name="btn btn-sm btn-outline-primary me-1 mb-1",
                                label_checked_class_name="active")], md=5),
        dbc.Col([html.Label("Tecnologia", className="fw-bold small mb-1"),
                 dbc.RadioItems(id="filtro-tec", options=TEC_OPTS, value="Todas", inline=True,
                                input_checked_class_name="btn-check",
                                label_class_name="btn btn-sm btn-outline-success me-1 mb-1",
                                label_checked_class_name="active")], md=3),
        dbc.Col([html.Label("Nivel de tension (kV)", className="fw-bold small mb-1"),
                 dbc.RadioItems(id="filtro-kv", options=KV_OPTS, value="Todos", inline=True,
                                input_checked_class_name="btn-check",
                                label_class_name="btn btn-sm btn-outline-warning me-1 mb-1",
                                label_checked_class_name="active")], md=4),
    ])), className="mb-3 shadow-sm"),
    dbc.Row([dbc.Col(dcc.Graph(id="bar-faltantes", config={"displayModeBar":False}), md=8),
             dbc.Col(dcc.Graph(id="pie-estatus",   config={"displayModeBar":False}), md=4)], className="mb-3"),
    dbc.Row([dbc.Col(dcc.Graph(id="bar-gcr", config={"displayModeBar":False}), md=4),
             dbc.Col(dcc.Graph(id="bar-tec", config={"displayModeBar":False}), md=4),
             dbc.Col(dcc.Graph(id="bar-inv", config={"displayModeBar":False}), md=4)], className="mb-3"),
    dbc.Row(dbc.Col([html.H6("Detalle de subestaciones", className="fw-bold"), html.Div(id="tabla-detalle")], className="mb-4")),
    html.Footer("Fuente: CNE - Resultados 1a Convocatoria Generacion Electrica | DOF 17/10/2025", className="text-muted small text-center pb-3"),
])

@app.callback(
    Output("kpi-row","children"), Output("bar-faltantes","figure"), Output("pie-estatus","figure"),
    Output("bar-gcr","figure"),   Output("bar-tec","figure"),       Output("bar-inv","figure"),
    Output("tabla-detalle","children"),
    Input("filtro-gcr","value"), Input("filtro-tec","value"), Input("filtro-kv","value"),
)
def actualizar(gcr, tec, kv):
    d = df.copy()
    if gcr != "Todas":   d = d[d["GCR"] == gcr]
    if tec == "Eolica":  d = d[d["Tecnologia"] == "Eólica"]
    elif tec == "Fotovoltaica": d = d[d["Tecnologia"] == "Fotovoltaica"]
    if kv != "Todos":    d = d[d["kV"].astype(str) == kv]

    mw_conv = d["Capacidad_MW"].sum(); mw_asig = d["MW_Asignados"].sum()
    mw_falt = d[d["MW_Faltantes"]>0]["MW_Faltantes"].sum()
    inv_tot = d[d["Inversion_MDP"]>0]["Inversion_MDP"].sum()
    pct = round(mw_asig/mw_conv*100,1) if mw_conv else 0

    def kcard(t,v,c,s=""):
        return dbc.Col(dbc.Card(dbc.CardBody([html.H3(v,className="mb-0 fw-bold",style={"color":c}),
                                              html.P(t,className="mb-0 small text-muted"),html.Small(s,className="text-muted")]),
                                className="shadow-sm border-0 text-center h-100"),md=2)
    kpis = [kcard("Subestaciones",len(d),"#2980b9"), kcard("MW convocados",f"{int(mw_conv):,}","#6c3483"),
            kcard("MW asignados",f"{int(mw_asig):,}","#27ae60",f"({pct}%)"), kcard("MW sin asignar",f"{int(mw_falt):,}","#d62728"),
            kcard("SE desiertas",(d["MW_Faltantes"]>0).sum(),"#e67e22"), kcard("Inversion estimada",f"${inv_tot:,.0f} M","#8e44ad","MDP")]

    ds = d.sort_values("MW_Faltantes",ascending=True)
    fig_bar = go.Figure(go.Bar(x=ds["MW_Faltantes"], y=ds["SE_Corto"], orientation="h",
        marker_color=[COLOR_MAP.get(e,"#aaa") for e in ds["Estatus"]],
        customdata=ds[["GCR","Tecnologia","Capacidad_MW","MW_Asignados","Entidad","Estatus","kV","Inversion_MDP","Pct_Asig"]].values,
        hovertemplate="<b>%{y}</b><br>GCR: %{customdata[0]} | Tec: %{customdata[1]}<br>Tension: %{customdata[6]} kV<br>Cap: %{customdata[2]} MW<br>Asig: %{customdata[3]} MW (%{customdata[8]}%)<br><b>Falt: %{x} MW</b><br>Entidad: %{customdata[4]}<br>Inv: $%{customdata[7]:,.0f} MDP<br>%{customdata[5]}<extra></extra>"))
    fig_bar.add_vline(x=0,line_width=1.5,line_dash="dash",line_color="#555")
    fig_bar.update_layout(title="MW Faltantes por subestacion<br><sub>Negativo=sobreasignada | Positivo=sin cubrir</sub>",
        xaxis_title="MW Faltantes", height=max(420,len(d)*23+90), margin=dict(l=10,r=20,t=70,b=40),
        plot_bgcolor="#fafafa", paper_bgcolor="#fff", font=dict(size=11))

    cnt = d["Estatus"].value_counts().reset_index(); cnt.columns=["Estatus","n"]
    cnt["label"] = cnt["Estatus"].map(lambda e: f"{EMOJI.get(e,'')} {e}")
    fig_pie = px.pie(cnt,names="label",values="n",color="Estatus",color_discrete_map=COLOR_MAP,title="Distribucion por estatus",hole=0.42)
    fig_pie.update_traces(textinfo="percent+value"); fig_pie.update_layout(showlegend=False,height=310,margin=dict(l=5,r=5,t=50,b=5))

    gcr_g=(d.groupby("GCR")[["Capacidad_MW","MW_Asignados"]].sum().assign(Falt=lambda x:(x["Capacidad_MW"]-x["MW_Asignados"]).clip(lower=0)).reset_index().sort_values("Falt",ascending=False))
    fig_gcr=px.bar(gcr_g,x="GCR",y=["MW_Asignados","Falt"],barmode="stack",text_auto=True,color_discrete_map={"MW_Asignados":"#27ae60","Falt":"#d62728"},title="Capacidad por GCR",labels={"value":"MW","variable":""})
    fig_gcr.update_layout(height=310,margin=dict(l=5,r=5,t=50,b=40),legend=dict(orientation="h",y=-0.3))

    tec_g=(d.groupby("Tecnologia")[["Capacidad_MW","MW_Asignados"]].sum().assign(Falt=lambda x:(x["Capacidad_MW"]-x["MW_Asignados"]).clip(lower=0)).reset_index())
    fig_tec=px.bar(tec_g,x="Tecnologia",y=["MW_Asignados","Falt"],barmode="stack",text_auto=True,color_discrete_map={"MW_Asignados":"#27ae60","Falt":"#d62728"},title="Capacidad por tecnologia",labels={"value":"MW","variable":""})
    fig_tec.update_layout(height=310,margin=dict(l=5,r=5,t=50,b=40),legend=dict(orientation="h",y=-0.3))

    inv_g=(d[d["Inversion_MDP"]>0].groupby("GCR")["Inversion_MDP"].sum().reset_index().sort_values("Inversion_MDP",ascending=False))
    fig_inv=px.bar(inv_g,x="GCR",y="Inversion_MDP",text_auto=".0f",color="Inversion_MDP",color_continuous_scale="Blues",title="Inversion estimada por GCR (MDP)",labels={"Inversion_MDP":"MDP"})
    fig_inv.update_layout(height=310,margin=dict(l=5,r=5,t=50,b=40),coloraxis_showscale=False)

    dt=d.sort_values(["MW_Faltantes","GCR"],ascending=[False,True])
    header=html.Thead(html.Tr([html.Th("GCR"),html.Th("Region"),html.Th("Subestacion"),html.Th("Entidad"),html.Th("Tecnologia"),html.Th("kV"),html.Th("Año EOO"),html.Th("Cap.MW"),html.Th("Asig.MW"),html.Th("Falt.MW"),html.Th("% Asig"),html.Th("Inv.MDP"),html.Th("Estatus")],className="table-dark small"))
    rows=[]
    for _,r in dt.iterrows():
        fc="#d62728" if r["MW_Faltantes"]>0 else "#27ae60"
        rows.append(html.Tr([html.Td(r["GCR"]),html.Td(r["Region"]),html.Td(r["SE_Corto"],style={"fontSize":"0.78rem"}),html.Td(r["Entidad"]),html.Td(r["Tecnologia"]),html.Td(f'{r["kV"]} kV'),html.Td(r["Anio_EOO"]),html.Td(f'{int(r["Capacidad_MW"]):,}'),html.Td(f'{r["MW_Asignados"]:,.1f}'),html.Td(html.Strong(f'{r["MW_Faltantes"]:,.1f}'),style={"color":fc}),html.Td(f'{r["Pct_Asig"]}%'),html.Td(f'${r["Inversion_MDP"]:,.0f}' if r["Inversion_MDP"]>0 else "-"),html.Td(dbc.Badge(f'{EMOJI.get(r["Estatus"],"")} {r["Estatus"]}',color=BADGE_COLOR.get(r["Estatus"],"secondary"),className="fw-normal"))]))
    tabla=dbc.Table([header,html.Tbody(rows)],bordered=True,hover=True,responsive=True,striped=True,size="sm",className="small")
    return kpis,fig_bar,fig_pie,fig_gcr,fig_tec,fig_inv,tabla

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
```

**Paso 2 — Actualizar `requirements.txt`** (mismo proceso, reemplaza con esto):
```
dash==2.18.2
dash-bootstrap-components==1.6.0
plotly==5.24.1
pandas==2.2.3
gunicorn==21.2.0
