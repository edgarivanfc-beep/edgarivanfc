"""
Dashboard: Resultados 1ª Convocatoria CNE
Generación Eléctrica e Interconexión al SEN — DOF 17/10/2025

Despliegue: Render.com  |  Repositorio: github.com/edgarivanfc-beep/edgarivanfc
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback, ctx
import dash_bootstrap_components as dbc

# ── Datos completos con columnas ocultas ──────────────────────────────────────
datos_raw = [
    # GCR, Región, Tecnología, Año EOO, Capacidad MW, Inversión MDP,
    # Subestación (nombre corto), SubEstación (nombre largo), kV, Entidad,
    # MW Asignados, MW Faltantes
    ("Noreste",    "23-Saltillo",       "Eólica",        "2028",      300,    76.0,    "Derramadero",                            "DERRAMADERO",                                                                                                          400, "Coahuila",           0.00,   300.00),
    ("Oriental",   "46-Veracruz",       "Fotovoltaica",  "2030",      250,    44.0,    "Manlio Fabio Altamirano",                "MANLIO FABIO ALTAMIRANO",                                                                                              230, "Veracruz",           0.00,   250.00),
    ("Peninsular", "69-Valladolid",     "Eólica",        "2028-2029", 350,  2439.0,    "SE Maniobras LT Norte-Kanasín Potencia", "SE MANIOBRAS QUE ENTRONCA LAS DOS LT NORTE - KANASÍN POTENCIA",                                                       230, "Yucatán",          120.00,   230.00),
    ("Noreste",    "27-Güémez",         "Eólica",        "2028",      200,   176.0,    "Jiménez",                                "JIMÉNEZ",                                                                                                              115, "Tamaulipas",         0.00,   200.00),
    ("Oriental",   "58-Grijalva",       "Fotovoltaica",  "2029",      200,   150.0,    "Tapachula Potencia",                     "TAPACHULA POTENCIA",                                                                                                   115, "Chiapas",            0.00,   200.00),
    ("Occidental", "37-San Luis de",    "Fotovoltaica",  "2027-2029", 180,     None,   "Santa Fe",                               "SANTA FE",                                                                                                             115, "Guanajuato",         0.00,   180.00),
    ("Occidental", "33-San Luis",       "Eólica",        "2029",      170,     None,   "El Potosí",                              "EL POTOSÍ",                                                                                                            230, "San Luís Potosí",    0.00,   170.00),
    ("Occidental", "33-San Luis",       "Fotovoltaica",  "2027",      130,   756.0,    "San Diego Peñuelas",                     "SAN DIEGO PEÑUELAS",                                                                                                   115, "Guanajuato",         0.00,   130.00),
    ("Oriental",   "46-Veracruz",       "Fotovoltaica",  "2029",      130,    31.0,    "Santa Fe (Veracruz)",                    "SANTA FE",                                                                                                             115, "Veracruz",           0.00,   130.00),
    ("Noreste",    "21-Matamoros",      "Eólica",        "2027",      120,    38.0,    "Matamoros Potencia",                     "MATAMOROS POTENCIA",                                                                                                   138, "Tamaulipas",         0.00,   120.00),
    ("Oriental",   "48-Morelos",        "Fotovoltaica",  "2028",      120,    40.0,    "Yautepec Potencia",                      "YAUTEPEC POTENCIA",                                                                                                    115, "Morelos",            0.00,   120.00),
    ("Occidental", "33-San Luis",       "Eólica",        "2028",      100,  1017.0,    "Charcas Potencia",                       "CHARCAS POTENCIA",                                                                                                     115, "San Luís Potosí",    0.00,   100.00),
    ("Occidental", "31-",               "Fotovoltaica",  "2028",      100,     None,   "Lagos Galera",                           "LAGOS GALERA",                                                                                                         115, "Jalisco",            0.00,   100.00),
    ("Oriental",   "59-Tabasco",        "Fotovoltaica",  "2029",      100,    40.0,    "Cárdenas Dos",                           "CÁRDENAS DOS",                                                                                                         115, "Tabasco",            0.00,   100.00),
    ("Occidental", "31-",               "Fotovoltaica",  "2028",       90,   479.0,    "La Virgen",                              "LA VIRGEN",                                                                                                            115, "Jalisco",            0.00,    90.00),
    ("Central",    "42-Tula-Pachuca",   "Fotovoltaica",  "2030",       80,    45.0,    "Nochistongo",                            "NOCHISTONGO",                                                                                                          115, "Hidalgo",            0.00,    80.00),
    ("Noreste",    "25-Huasteca",       "Eólica",        "2027",       80,   106.0,    "SE Maniobras LT Libramiento-Mante",      "SE DE MANIOBRAS PARA ENTRONCAR LA LT LIBRAMIENTO - MANTE",                                                            115, "Tamaulipas",         0.00,    80.00),
    ("Occidental", "29-Tepic",          "Fotovoltaica",  "2029",       80,    97.0,    "Acaponeta",                              "ACAPONETA",                                                                                                            115, "Nayarit",            0.00,    80.00),
    ("Peninsular", "68-Dzitnup",        "Eólica",        "2028",      320,   139.0,    "Dzitnup",                                "DZITNUP",                                                                                                              400, "Yucatán",          252.00,    68.00),
    ("Central",    "43-Toluca",         "Fotovoltaica",  "2028",       30,    91.0,    "Villa Guerrero",                         "VILLA GUERRERO",                                                                                                       115, "Estado de México",   0.00,    30.00),
    ("Norte",      "13-Cuauhtémoc",     "Fotovoltaica",  "2029",       30,    35.0,    "Cuauhtémoc",                             "CUAUHTÉMOC",                                                                                                           115, "Chihuahua",          0.00,    30.00),
    ("Noreste",    "19-Nuevo",          "Eólica",        "2028",      140,    38.0,    "Falcon Mexicano",                        "FALCON MEXICANO",                                                                                                      138, "Tamaulipas",       130.50,     9.50),
    ("Oriental",   "61-Juchitán",       "Eólica",        "2028",      200,    31.0,    "Juchitan Dos",                           "JUCHITAN DOS",                                                                                                         115, "Oaxaca",           200.00,     0.00),
    ("Peninsular", "76-Chetumal",       "Eólica",        "2028",      200,    41.0,    "Xul-ha",                                 "XUL-HA",                                                                                                               115, "Quintana Roo",     200.00,     0.00),
    ("Occidental", "31-",               "Fotovoltaica",  "2029",       90,   126.0,    "Ojo Caliente",                           "OJO CALIENTE",                                                                                                         115, "Zacatecas",         99.00,    -9.00),
    ("Occidental", "34-Salamanca",      "Fotovoltaica",  "2027",       90,     None,   "El Toro",                                "EL TORO",                                                                                                              115, "Guanajuato",       107.00,   -17.00),
    ("Central",    "42-Tula-Pachuca",   "Fotovoltaica",  "2027-2028", 440,   991.0,    "SE Maniobras KM 110-Pachuca Potencia",   "SE MANIOBRAS QUE ENTRONCA LAS DOS LT ENTRE SE KILÓMETRO 110 - PACHUCA POTENCIA",                                       230, "Hidalgo",          459.27,   -19.27),
    ("Occidental", "38-Querétaro",      "Fotovoltaica",  "2027",      100,  2516.0,    "Tequisquiapan",                          "TEQUISQUIAPAN",                                                                                                        115, "Querétaro",        122.40,   -22.40),
    ("Occidental", "38-Querétaro",      "Fotovoltaica",  "2028",      220,     None,   "SE Maniobras LT San Juan-Dañú",          "SE DE MANIOBRAS PARA ENTRONCAR LA LT SAN JUAN PONTENCIA- DAÑÚ",                                                        230, "Hidalgo",          246.29,   -26.29),
    ("Oriental",   "46-Veracruz",       "Fotovoltaica",  "2028",      120,    31.0,    "Piedras Negras",                         "PIEDRAS NEGRAS",                                                                                                       115, "Veracruz",         147.00,   -27.00),
    ("Oriental",   "47-Puebla",         "Fotovoltaica",  "2027",      200,   215.0,    "SE Maniobras LT Tecali-Oriente",         "SE MANIOBRAS QUE ENTRONCA LAS LT TECALI 73560 ORIENTE, TECALI 73010 GUADALUPE ANALCO Y TECALI 73820 BUGAMBILIAS",      115, "Puebla",           231.00,   -31.00),
    ("Peninsular", "64-Escárcega",      "Fotovoltaica",  "2028",      300,   139.0,    "Escárcega",                              "ESCÁRCEGA",                                                                                                            400, "Campeche",         350.57,   -50.57),
    ("Peninsular", "64-Escárcega",      "Fotovoltaica",  "2028",      600,  2036.0,    "SE Maniobras LT Escárcega-Ticul",        "SE MANIOBRAS QUE ENTRONCA LAS DOS LT ESCÁRCEGA- TICUL",                                                                400, "Campeche",         694.27,   -94.27),
    ("Noreste",    "25-Huasteca",       "Fotovoltaica",  "2028",      110,    27.0,    "Puerto Altamira Eléctrica",              "PUERTO ALTAMIRA ELÉCTRICA",                                                                                            115, "Tamaulipas",       207.52,   -97.52),
]

cols = ["GCR", "Región", "Tecnología", "Año EOO", "Capacidad_MW", "Inversión_MDP",
        "SE_Corto", "SubEstación", "kV", "Entidad", "MW_Asignados", "MW_Faltantes"]
df = pd.DataFrame(datos_raw, columns=cols)

# ── Estatus y métricas derivadas ───────────────────────────────────────────────
def clasificar(row):
    if row["MW_Faltantes"] > 0 and row["MW_Asignados"] == 0:
        return "Desierta total"
    elif row["MW_Faltantes"] > 0 and row["MW_Asignados"] > 0:
        return "Desierta parcial"
    elif row["MW_Faltantes"] == 0:
        return "Cubierta exacta"
    else:
        return "Sobreasignada"

df["Estatus"]    = df.apply(clasificar, axis=1)
df["% Asignado"] = (df["MW_Asignados"] / df["Capacidad_MW"] * 100).round(1)
df["kV_str"]     = df["kV"].astype(str) + " kV"

COLOR_MAP = {
    "Desierta total":   "#d62728",
    "Desierta parcial": "#ff7f0e",
    "Cubierta exacta":  "#2ca02c",
    "Sobreasignada":    "#1f77b4",
}
BADGE_COLOR = {
    "Desierta total":   "danger",
    "Desierta parcial": "warning",
    "Cubierta exacta":  "success",
    "Sobreasignada":    "info",
}
EMOJI = {
    "Desierta total":   "🔴",
    "Desierta parcial": "🟡",
    "Cubierta exacta":  "🟢",
    "Sobreasignada":    "🔵",
}

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="CNE · 1ª Convocatoria Generación Eléctrica",
)
server = app.server   # ← necesario para Render / gunicorn

# ── Layout ────────────────────────────────────────────────────────────────────
def btn(label, btn_id, color="primary", size="sm"):
    return dbc.Button(label, id=btn_id, n_clicks=0,
                      color=color, size=size, className="me-1 mb-1")

app.layout = dbc.Container(fluid=True, style={"fontFamily": "Segoe UI, sans-serif"}, children=[

    # Encabezado
    dbc.Row(dbc.Col(html.Div([
        html.H4("🔌 CNE · 1ª Convocatoria de Generación Eléctrica e Interconexión al SEN",
                className="text-white mb-1"),
        html.Small(
            "DOF 17/10/2025  ·  34 subestaciones evaluadas  ·  "
            "Fuente: Resultados 1a Conv Gen Electr — CNE",
            className="text-white-50",
        ),
    ], className="p-3 mb-3 rounded",
       style={"background": "linear-gradient(90deg,#1b4f72,#2980b9)"}),
    )),

    # KPIs
    dbc.Row(id="kpi-row", className="mb-3 g-2"),

    # ── Filtros ──────────────────────────────────────────────────────────────
    dbc.Card(dbc.CardBody([
        dbc.Row([

            # Filtro 1 — GCR
            dbc.Col([
                html.Label("🗺️  Región GCR", className="fw-bold small mb-1"),
                html.Div([
                    btn("Todas", "f-gcr-todas"),
                ] + [btn(r, f"f-gcr-{r}", color="outline-primary")
                     for r in sorted(df["GCR"].unique())]),
                dcc.Store(id="s-gcr", data="Todas"),
            ], md=5),

            # Filtro 2 — Tecnología
            dbc.Col([
                html.Label("⚡  Tecnología", className="fw-bold small mb-1"),
                html.Div([
                    btn("Todas",        "f-tec-todas",   color="success"),
                    btn("Eólica",       "f-tec-eolica",  color="outline-success"),
                    btn("Fotovoltaica", "f-tec-foto",    color="outline-success"),
                ]),
                dcc.Store(id="s-tec", data="Todas"),
            ], md=3),

            # Filtro 3 — Tensión kV
            dbc.Col([
                html.Label("🔋  Nivel de tensión", className="fw-bold small mb-1"),
                html.Div([
                    btn("Todos",  "f-kv-todos",  color="warning"),
                    btn("115 kV", "f-kv-115",    color="outline-warning"),
                    btn("138 kV", "f-kv-138",    color="outline-warning"),
                    btn("230 kV", "f-kv-230",    color="outline-warning"),
                    btn("400 kV", "f-kv-400",    color="outline-warning"),
                ]),
                dcc.Store(id="s-kv", data="Todos"),
            ], md=4),

        ]),
    ]), className="mb-3 shadow-sm"),

    # Gráficas fila 1
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-faltantes", config={"displayModeBar": False}), md=8),
        dbc.Col(dcc.Graph(id="pie-estatus",   config={"displayModeBar": False}), md=4),
    ], className="mb-3"),

    # Gráficas fila 2
    dbc.Row([
        dbc.Col(dcc.Graph(id="bar-gcr", config={"displayModeBar": False}), md=4),
        dbc.Col(dcc.Graph(id="bar-tec", config={"displayModeBar": False}), md=4),
        dbc.Col(dcc.Graph(id="bar-inv", config={"displayModeBar": False}), md=4),
    ], className="mb-3"),

    # Tabla
    dbc.Row(dbc.Col([
        html.H6("📋 Detalle de subestaciones", className="fw-bold"),
        html.Div(id="tabla-detalle"),
    ], className="mb-4")),

    html.Footer(
        "Fuente: CNE — Resultados 1ª Convocatoria Generación Eléctrica · DOF 17/10/2025  |  "
        "Elaborado con Plotly Dash",
        className="text-muted small text-center pb-3",
    ),
])


# ── Callbacks: stores ─────────────────────────────────────────────────────────
@callback(Output("s-gcr", "data"),
          Input("f-gcr-todas", "n_clicks"),
          *[Input(f"f-gcr-{r}", "n_clicks") for r in sorted(df["GCR"].unique())],
          prevent_initial_call=True)
def cb_gcr(*_):
    bid = ctx.triggered_id
    return "Todas" if bid == "f-gcr-todas" else bid.replace("f-gcr-", "")


@callback(Output("s-tec", "data"),
          Input("f-tec-todas",  "n_clicks"),
          Input("f-tec-eolica", "n_clicks"),
          Input("f-tec-foto",   "n_clicks"),
          prevent_initial_call=True)
def cb_tec(*_):
    bid = ctx.triggered_id
    if bid == "f-tec-eolica": return "Eólica"
    if bid == "f-tec-foto":   return "Fotovoltaica"
    return "Todas"


@callback(Output("s-kv", "data"),
          Input("f-kv-todos", "n_clicks"),
          Input("f-kv-115",   "n_clicks"),
          Input("f-kv-138",   "n_clicks"),
          Input("f-kv-230",   "n_clicks"),
          Input("f-kv-400",   "n_clicks"),
          prevent_initial_call=True)
def cb_kv(*_):
    bid = ctx.triggered_id
    mapping = {"f-kv-115": "115", "f-kv-138": "138",
               "f-kv-230": "230", "f-kv-400": "400"}
    return mapping.get(bid, "Todos")


# ── Callback principal ────────────────────────────────────────────────────────
@callback(
    Output("kpi-row",       "children"),
    Output("bar-faltantes", "figure"),
    Output("pie-estatus",   "figure"),
    Output("bar-gcr",       "figure"),
    Output("bar-tec",       "figure"),
    Output("bar-inv",       "figure"),
    Output("tabla-detalle", "children"),
    Input("s-gcr", "data"),
    Input("s-tec", "data"),
    Input("s-kv",  "data"),
)
def actualizar(gcr, tec, kv):
    d = df.copy()
    if gcr != "Todas":
        d = d[d["GCR"] == gcr]
    if tec != "Todas":
        d = d[d["Tecnología"] == tec]
    if kv != "Todos":
        d = d[d["kV"].astype(str) == kv]

    # ── KPIs ─────────────────────────────────────────────────────────────────
    total_se  = len(d)
    mw_conv   = d["Capacidad_MW"].sum()
    mw_asig   = d["MW_Asignados"].sum()
    mw_falt   = d[d["MW_Faltantes"] > 0]["MW_Faltantes"].sum()
    inv_total = d["Inversión_MDP"].sum(skipna=True)
    desiertas = (d["MW_Faltantes"] > 0).sum()
    pct       = round(mw_asig / mw_conv * 100, 1) if mw_conv else 0

    def kcard(titulo, valor, color, sub=""):
        return dbc.Col(dbc.Card(dbc.CardBody([
            html.H3(valor, className="mb-0 fw-bold", style={"color": color}),
            html.P(titulo, className="mb-0 small text-muted"),
            html.Small(sub, className="text-muted"),
        ]), className="shadow-sm border-0 text-center h-100"), md=2)

    kpis = [
        kcard("Subestaciones",        total_se,                "#2980b9"),
        kcard("MW convocados",        f"{int(mw_conv):,}",     "#6c3483"),
        kcard("MW asignados",         f"{int(mw_asig):,}",     "#27ae60", f"({pct}%)"),
        kcard("MW sin asignar",       f"{int(mw_falt):,}",     "#d62728"),
        kcard("SE desiertas",         desiertas,               "#e67e22"),
        kcard("Inversión estimada",   f"${inv_total:,.0f} M",  "#8e44ad", "MDP (c/dato)"),
    ]

    # ── Barra horizontal MW faltantes ─────────────────────────────────────────
    ds = d.sort_values("MW_Faltantes", ascending=True)
    bar_colors = [COLOR_MAP[e] for e in ds["Estatus"]]

    fig_bar = go.Figure(go.Bar(
        x=ds["MW_Faltantes"],
        y=ds["SE_Corto"],
        orientation="h",
        marker_color=bar_colors,
        customdata=ds[["GCR","Región","Tecnología","Capacidad_MW",
                        "MW_Asignados","Entidad","Estatus","kV",
                        "Inversión_MDP","% Asignado"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "GCR: %{customdata[0]}  |  Región: %{customdata[1]}<br>"
            "Tecnología: %{customdata[2]}  |  Tensión: %{customdata[7]} kV<br>"
            "Capacidad: %{customdata[3]} MW<br>"
            "Asignados: %{customdata[4]} MW  (%{customdata[9]}%)<br>"
            "<b>Faltantes: %{x} MW</b><br>"
            "Entidad: %{customdata[5]}<br>"
            "Inversión estimada: $%{customdata[8]:,.0f} MDP<br>"
            "Estatus: %{customdata[6]}<extra></extra>"
        ),
    ))
    fig_bar.add_vline(x=0, line_width=1.5, line_dash="dash", line_color="#555")
    fig_bar.update_layout(
        title="MW Faltantes por subestación<br>"
              "<sub>Negativo = sobreasignada  ·  Positivo = sin cubrir</sub>",
        xaxis_title="MW Faltantes",
        height=max(420, len(d) * 23 + 90),
        margin=dict(l=10, r=20, t=70, b=40),
        plot_bgcolor="#fafafa", paper_bgcolor="#fff",
        font=dict(size=11),
    )

    # ── Pie estatus ───────────────────────────────────────────────────────────
    cnt = d["Estatus"].value_counts().reset_index()
    cnt.columns = ["Estatus", "n"]
    cnt["label"] = cnt["Estatus"].map(lambda e: f"{EMOJI.get(e,'')} {e}")
    fig_pie = px.pie(cnt, names="label", values="n",
                     color="Estatus", color_discrete_map=COLOR_MAP,
                     title="Distribución por estatus", hole=0.42)
    fig_pie.update_traces(textinfo="percent+value")
    fig_pie.update_layout(showlegend=False, height=310,
                          margin=dict(l=5, r=5, t=50, b=5))

    # ── Barras GCR ────────────────────────────────────────────────────────────
    gcr_g = (d.groupby("GCR")[["Capacidad_MW", "MW_Asignados"]]
              .sum()
              .assign(MW_Falt=lambda x: (x["Capacidad_MW"] - x["MW_Asignados"]).clip(lower=0))
              .reset_index()
              .sort_values("MW_Falt", ascending=False))
    fig_gcr = px.bar(gcr_g, x="GCR", y=["MW_Asignados", "MW_Falt"],
                     barmode="stack", text_auto=True,
                     color_discrete_map={"MW_Asignados": "#27ae60", "MW_Falt": "#d62728"},
                     title="Capacidad por GCR",
                     labels={"value": "MW", "variable": ""})
    fig_gcr.update_layout(height=310, margin=dict(l=5, r=5, t=50, b=40),
                          legend=dict(orientation="h", y=-0.3))

    # ── Barras Tecnología ─────────────────────────────────────────────────────
    tec_g = (d.groupby("Tecnología")[["Capacidad_MW", "MW_Asignados"]]
              .sum()
              .assign(MW_Falt=lambda x: (x["Capacidad_MW"] - x["MW_Asignados"]).clip(lower=0))
              .reset_index())
    fig_tec = px.bar(tec_g, x="Tecnología", y=["MW_Asignados", "MW_Falt"],
                     barmode="stack", text_auto=True,
                     color_discrete_map={"MW_Asignados": "#27ae60", "MW_Falt": "#d62728"},
                     title="Capacidad por tecnología",
                     labels={"value": "MW", "variable": ""})
    fig_tec.update_layout(height=310, margin=dict(l=5, r=5, t=50, b=40),
                          legend=dict(orientation="h", y=-0.3))

    # ── Inversión por GCR (solo registros con dato) ───────────────────────────
    inv_g = (d.dropna(subset=["Inversión_MDP"])
              .groupby("GCR")["Inversión_MDP"]
              .sum()
              .reset_index()
              .sort_values("Inversión_MDP", ascending=False))
    fig_inv = px.bar(inv_g, x="GCR", y="Inversión_MDP",
                     text_auto=".0f",
                     color="Inversión_MDP",
                     color_continuous_scale="Blues",
                     title="Inversión estimada por GCR (MDP)",
                     labels={"Inversión_MDP": "MDP"})
    fig_inv.update_layout(height=310, margin=dict(l=5, r=5, t=50, b=40),
                          coloraxis_showscale=False)

    # ── Tabla ─────────────────────────────────────────────────────────────────
    dt = d.sort_values(["MW_Faltantes", "GCR"], ascending=[False, True])

    header = html.Thead(html.Tr([
        html.Th("GCR"), html.Th("Región"), html.Th("Subestación"),
        html.Th("Entidad"), html.Th("Tecnología"), html.Th("kV"),
        html.Th("Año EOO"), html.Th("Cap. MW"), html.Th("Asig. MW"),
        html.Th("Falt. MW"), html.Th("% Asig."), html.Th("Inv. MDP"),
        html.Th("Estatus"),
    ], className="table-dark small"))

    rows = []
    for _, r in dt.iterrows():
        inv_str = f"${r['Inversión_MDP']:,.0f}" if pd.notna(r["Inversión_MDP"]) else "—"
        falt_color = "#d62728" if r["MW_Faltantes"] > 0 else "#27ae60"
        rows.append(html.Tr([
            html.Td(r["GCR"]),
            html.Td(r["Región"]),
            html.Td(r["SE_Corto"], style={"fontSize": "0.78rem", "maxWidth": "200px"}),
            html.Td(r["Entidad"]),
            html.Td(r["Tecnología"]),
            html.Td(f'{r["kV"]} kV'),
            html.Td(r["Año EOO"]),
            html.Td(f'{int(r["Capacidad_MW"]):,}'),
            html.Td(f'{r["MW_Asignados"]:,.1f}'),
            html.Td(html.Strong(f'{r["MW_Faltantes"]:,.1f}'),
                    style={"color": falt_color}),
            html.Td(f'{r["% Asignado"]}%'),
            html.Td(inv_str),
            html.Td(dbc.Badge(
                f'{EMOJI.get(r["Estatus"],"")} {r["Estatus"]}',
                color=BADGE_COLOR.get(r["Estatus"], "secondary"),
                className="fw-normal",
            )),
        ]))

    tabla = dbc.Table(
        [header, html.Tbody(rows)],
        bordered=True, hover=True, responsive=True,
        striped=True, size="sm", className="small",
    )

    return kpis, fig_bar, fig_pie, fig_gcr, fig_tec, fig_inv, tabla


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
