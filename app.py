import json
import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import dcc, html, Input, Output, State, ALL
from dash_iconify import DashIconify

from config import (
    EXPORT_COLUMNS,
    VIBES_PATTERNS, ELEMENTOS_PATTERNS, DEPTHS_PATTERNS,
)
from recommender import (
    load_data,
    find_books,
    analyze_reading_dna,
)
# ---------------------------------------------------------------------------
# Datos y app
# ---------------------------------------------------------------------------

df, tfidf_matrix, vectorizer = load_data("books_works.csv")

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    ],
)
app.title = "☀️ Summer Reading List Builder"
app.config.suppress_callback_exceptions = True


# ---------------------------------------------------------------------------
# Helpers de UI
# ---------------------------------------------------------------------------

def icon(fa_class, size=18, color="currentColor"):
    FA_MAP = {
        "fas fa-house-chimney-user":     "fa6-solid:house-chimney-user",
        "fas fa-face-grin-squint-tears": "fa6-solid:face-grin-squint-tears",
        "fas fa-lightbulb":              "fa6-solid:lightbulb",
        "fas fa-sun":                    "fa6-solid:sun",
        "fas fa-heart-circle-check":     "fa6-solid:heart-circle-check",
        "fas fa-wand-magic-sparkles":    "fa6-solid:wand-magic-sparkles",
        "fas fa-comments":               "fa6-solid:comments",
        "fas fa-magnifying-glass":       "fa6-solid:magnifying-glass",
        "fas fa-user-tie":               "fa6-solid:user-tie",
        "fas fa-earth-americas":         "fa6-solid:earth-americas",
        "fas fa-shuffle":                "fa6-solid:shuffle",
        "fas fa-face-grin-hearts":       "fa6-solid:face-grin-hearts",
        "fas fa-dove":                   "fa6-solid:dove",
        "fas fa-layer-group":            "fa6-solid:layer-group",
        "fas fa-compress":               "fa6-solid:compress",
        "fas fa-brain":                  "fa6-solid:brain",
        "fas fa-head-side-virus":        "fa6-solid:head-side-virus",
        "fas fa-users":                  "fa6-solid:users",
        "fas fa-dna":                    "fa6-solid:dna",
        "fas fa-circle-user":            "fa6-solid:circle-user",
        "fas fa-gem":                    "fa6-solid:gem",
        "fas fa-compass":                "fa6-solid:compass",
        "fas fa-heart":                  "fa6-solid:heart",
        "fas fa-star":                   "fa6-solid:star",
        "fas fa-download":               "fa6-solid:download",
        "fas fa-file-lines":             "fa6-solid:file-lines",
        "fas fa-broom":                  "fa6-solid:broom",
        "fas fa-book-open":              "fa6-solid:book-open",
    }
    return DashIconify(icon=FA_MAP.get(fa_class, "fa6-solid:circle-question"),
                       width=size, color=color)


def checkbox_id(prefix, name):
    return f"{prefix}-{name.replace(' ', '-').lower()}"


def match_badge_color(pct):
    if pct > 70: return "#66BB6A", "teal"
    if pct > 50: return "#FFCA28", "yellow"
    return "#42A5F5", "blue"


# ---------------------------------------------------------------------------
# Componentes reutilizables
# ---------------------------------------------------------------------------

def preference_card(name, data, prefix):
    """Card individual de preferencia con checkbox."""
    return dmc.GridCol([
        dmc.Card(
            withBorder=True, radius="md", shadow="sm",
            style={"height": "100%", "transition": "transform 0.2s ease"},
            children=[
                dmc.Checkbox(
                    id=checkbox_id(prefix, name),
                    label=dmc.Group([icon(data["icon"], 20), dmc.Text(name, fw=700)], gap="xs"),
                    checked=False, mb="xs",
                ),
                dmc.Text(data["description"], c="dimmed", size="sm", lh=1.4),
            ],
        )
    ], span=10, offset=1, mb="sm")


def preference_section(container_id, patterns, prefix, hidden=False):
    """Contenedor scrolleable con todas las cards de una categoría."""
    return html.Div(
        id=container_id,
        className="selection-cards-container",
        style={"display": "none"} if hidden else {},
        children=[dmc.Grid(justify="center", children=[
            preference_card(name, data, prefix)
            for name, data in patterns.items()
        ])],
    )


def dna_card(title, fa_icon, color, children):
    """Card del panel de DNA con borde de color."""
    return dmc.Card(
        withBorder=True, radius="md",
        style={"borderLeft": f"4px solid {color}", "height": "100%"},
        children=[
            dmc.Group([icon(fa_icon, 16, color), dmc.Text(title, fw=700, size="sm", c=color)],
                      gap="xs", mb="xs"),
            *children,
        ],
    )


def empty_dna_panel():
    return dmc.Stack([
        icon("fas fa-dna", 48, "#adb5bd"),
        dmc.Title("🧬 Your Reading DNA Awaits Discovery", order=4, c="dimmed", ta="center"),
        dmc.Text("Select your preferences to unlock your unique literary genetic profile!",
                 c="dimmed", ta="center"),
    ], align="center", py="xl")


def dna_panel(dna):
    """Renderiza el panel completo de Reading DNA."""
    p = dna["personality"]
    r = dna["rarity"]
    d = dna["discovery"]
    f = dna["flexibility"]
    m = dna["mood_map"]

    return html.Div([
        dmc.Stack([
            dmc.Group([icon("fas fa-dna", 22, "#9C27B0"),
                       dmc.Title("🧬 Your Reading DNA Profile", order=4, c="#333")],
                      justify="center"),
            dmc.Text("Your unique literary genetic makeup revealed!",
                     ta="center", c="dimmed", fs="italic", mb="sm"),
        ], align="center", gap="xs"),

        dmc.Grid(gutter="sm", mb="sm", children=[
            dmc.GridCol(dna_card("Reader Personality", "fas fa-circle-user", "#E91E63", [
                dmc.Text(p["type"], fw=600, mb=4),
                dmc.Text(f"Confidence: {p['confidence']}%", c="dimmed", size="xs"),
                dmc.Progress(value=p["confidence"], color="pink", size="sm", radius="xl", mt=4),
            ]), span={"base": 12, "md": 6}),

            dmc.GridCol(dna_card("Taste Rarity Index", "fas fa-gem", "#9C27B0", [
                dmc.Text(r["rarity"], fw=600, mb=4),
                dmc.Text(f"{r['percentile']}th percentile", c="dimmed", size="xs"),
                dmc.Text(r["description"], size="xs", lh=1.3, mt=4),
            ]), span={"base": 12, "md": 6}),
        ]),

        dmc.Grid(gutter="sm", mb="sm", children=[
            dmc.GridCol(dna_card("Discovery Potential", "fas fa-compass", "#FF9800", [
                dmc.Text(d["type"], fw=600, mb=4),
                dmc.Text(f"Likelihood: {d['likelihood']}%", c="dimmed", size="xs"),
                dmc.Text(d["prediction"], size="xs", lh=1.3, mt=4),
            ]), span={"base": 12, "md": 6}),

            dmc.GridCol(dna_card("Genre Flexibility", "fas fa-shuffle", "#4CAF50", [
                dmc.Text(f["flexibility"], fw=600, mb=4),
                dmc.Text(f"Adaptability: {f['score']}%", c="dimmed", size="xs"),
                dmc.Progress(value=f["score"], color="green", size="sm", radius="xl", mt=4, mb=4),
                dmc.Text(f["recommendation"], size="xs", lh=1.3),
            ]), span={"base": 12, "md": 6}),
        ]),

        dmc.Divider(my="sm"),

        dna_card("Reading Mood Map", "fas fa-heart", "#FF5722", [
            dmc.Text(m["description"], size="sm", mb="xs"),
            dmc.Group(gap="xs", wrap="wrap", children=[
                dmc.Badge(mood, variant="light", color="blue", size="md", radius="xl")
                for mood in m["primary_moods"]
            ]),
        ]),
    ])


def book_card(i, book):
    """Card de resultado para un libro recomendado."""
    border_color, badge_color = match_badge_color(book["match_percentage"])
    return dmc.GridCol([
        dmc.Card(
            withBorder=True, radius="md", shadow="sm",
            style={"border": f"3px solid {border_color}", "height": "100%",
                   "transition": "transform 0.2s ease"},
            children=[
                dmc.CardSection(
                    withBorder=True, inheritPadding=True, py="xs",
                    children=dmc.Group([
                        dmc.Text(f"📚 Match #{i + 1}", fw=600, size="sm"),
                        dmc.Badge(f"{book['match_percentage']:.0f}% Match",
                                  color=badge_color, variant="filled", radius="xl"),
                    ], justify="space-between"),
                ),
                dmc.Stack(mt="sm", gap="xs", children=[
                    dmc.Text(book["original_title"], fw=700, size="md",
                             style={"overflow": "hidden", "textOverflow": "ellipsis",
                                    "whiteSpace": "nowrap"}),
                    dmc.Text(f"✍️ {book['author']}", c="dimmed", size="sm"),
                    dmc.Text(f"⭐ {book['avg_rating']:.1f}/5 ({int(book['ratings_count'])} votes)",
                             size="sm"),
                    dmc.Button("View Details",
                               id={"type": "open-book-modal", "index": str(book.name)},
                               variant="outline", color="gray", fullWidth=True,
                               radius="md", mt="xs", n_clicks=0),
                ]),
            ],
        )
    ], span={"base": 12, "sm": 6, "md": 4, "lg": 3}, mb="md")


def book_modal(book_index):
    """Modal con el detalle de un libro."""
    book  = df.iloc[book_index]
    desc  = str(book["description"])
    desc  = desc[:500] + "..." if len(desc) > 500 else desc
    pages = int(book["num_pages"]) if book["num_pages"] > 0 else "N/A"
    year  = int(book["original_publication_year"]) if pd.notna(book["original_publication_year"]) else "N/A"

    def row(label, value):
        return dmc.Group([dmc.Text(label, fw=600, size="sm", w=130), dmc.Text(value, size="sm")],
                         gap="xs")

    return dmc.Modal(
        id="book-modal", opened=True, size="lg", radius="md",
        title=dmc.Group([icon("fas fa-book-open", 20), dmc.Text(book["original_title"], fw=700)], gap="xs"),
        children=[
            dmc.Title("📖 Book Details", order=5, mb="sm"),
            dmc.Stack(gap="xs", mb="md", children=[
                row("Author:",        book["author"]),
                row("Rating:",        f"{book['avg_rating']:.1f}/5"),
                row("Total Ratings:", f"{int(book['ratings_count']):,}"),
                row("Pages:",         str(pages)),
                row("Published:",     str(year)),
            ]),
            dmc.Divider(mb="md"),
            dmc.Title("📝 Description", order=5, mb="xs"),
            dmc.Text(desc, size="sm", lh=1.6, style={"textAlign": "justify"}),
            dmc.Group(justify="flex-end", mt="md", children=[
                dmc.Button("Close", id="close-modal", variant="outline", color="gray", radius="md"),
            ]),
        ],
    )


def how_it_works_section():
    """Panel educativo que explica brevemente el motor de recomendación."""
    steps = [
        {
            "icon": "fas fa-file-lines",
            "color": "#2196F3",
            "title": "① TF-IDF Vectorization",
            "body": (
                "Every book description is transformed into a numeric vector. "
                "Words that appear frequently in one book but rarely across all books "
                "receive a higher weight — making each book's fingerprint unique."
            ),
        },
        {
            "icon": "fas fa-compass",
            "color": "#FF9800",
            "title": "② Cosine Similarity",
            "body": (
                "Your selected preferences are also converted into a vector. "
                "The engine then measures the angle between your preference vector "
                "and each book's vector — the smaller the angle, the stronger the match."
            ),
        },
        {
            "icon": "fas fa-dna",
            "color": "#9C27B0",
            "title": "③ Reading DNA",
            "body": (
                "Beyond the score, your selections are mapped to personality traits, "
                "mood patterns and genre signals — building a literary profile "
                "that reflects how you actually read, not just what you read."
            ),
        },
    ]

    cards = [
        dmc.GridCol(
            dmc.Card(
                withBorder=True, radius="md",
                style={"borderTop": f"4px solid {s['color']}", "height": "100%"},
                children=[
                    dmc.Group([icon(s["icon"], 18, s["color"]),
                               dmc.Text(s["title"], fw=700, size="sm", c=s["color"])],
                              gap="xs", mb="sm"),
                    dmc.Text(s["body"], size="sm", c="dimmed", lh=1.6),
                ],
            ),
            span={"base": 12, "md": 4},
        )
        for s in steps
    ]

    return dmc.Card(
        withBorder=False, radius="md", shadow="sm", mt="xl",
        style={"background": "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
               "border": "1px solid #dee2e6"},
        children=[
            dmc.Stack(align="center", gap="xs", mb="lg", children=[
                dmc.Text("⚙️ How The Recommendation Engine Works",
                         fw=700, size="lg", c="#495057", ta="center"),
                dmc.Text("A quick look at the technology powering your results.",
                         c="dimmed", size="sm", ta="center", fs="italic"),
            ]),
            dmc.Grid(gutter="md", children=cards),
        ],
    )


def results_display(recommended):
    """Sección de resultados con todas las book cards."""
    return dmc.Card(
        withBorder=False, radius="md", shadow="lg",
        children=[
            dmc.CardSection(
                style={"background": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",
                       "padding": "20px 30px"},
                children=dmc.Stack([
                    dmc.Group([icon("fas fa-star", 24, "white"),
                               dmc.Title("Your Perfect Books Await", order=3, c="white")],
                              justify="center"),
                    dmc.Text(f"We found {len(recommended)} books that align with your preferences.",
                             ta="center", c="rgba(255,255,255,0.9)", size="lg"),
                ], align="center", gap="xs", py="sm"),
            ),
            dmc.CardSection(p="lg", children=[
                dmc.Group(justify="center", mb="lg", children=[
                    dmc.Button("Download CSV", id="download-csv-btn",
                               leftSection=icon("fas fa-download", 16),
                               variant="outline", color="green", radius="md"),
                    dmc.Button("Download TXT", id="download-txt-btn",
                               leftSection=icon("fas fa-file-lines", 16),
                               variant="outline", color="blue", radius="md"),
                ]),
                dmc.Grid(gutter="md", children=[book_card(i, b) for i, b in enumerate(recommended)]),
                how_it_works_section(),
            ]),
        ],
    )


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

app.layout = dmc.MantineProvider(children=html.Div([
    dcc.Store(id="last-recommendations", data=[]),
    dcc.Store(id="last-selections",      data={"vibes": [], "elementos": [], "depths": []}),
    dcc.Download(id="download-csv"),
    dcc.Download(id="download-txt"),

    dmc.Container(fluid=True, px="md", style={
        "background": "linear-gradient(135deg, #FAF7F0 0%, #F0E6D6 25%, #E8DCC0 50%, #DDD1B8 100%)",
        "minHeight": "100vh", "paddingTop": "16px", "paddingBottom": "32px",
    }, children=[

        # Header
        dmc.Paper(radius="xl", mb="xl", style={
            "padding": "25px 35px",
            "background": "linear-gradient(135deg, #FFE066 0%, #FF6B35 25%, #F7931E 50%, #FFD23F 75%, #06FFA5 100%)",
            "boxShadow": "0 10px 30px rgba(255,107,53,0.4)",
            "border": "2px solid rgba(255,255,255,0.3)",
        }, children=[
            dmc.Grid(align="center", children=[
                dmc.GridCol(span={"base": 12, "sm": 8}, children=[
                    dmc.Title("☀️ Your Perfect Summer Reading List Awaits", order=1, c="white",
                              style={"fontWeight": 800,
                                     "fontSize": "clamp(1.4rem, 4vw, 2.2rem)",
                                     "textShadow": "2px 2px 4px rgba(0,0,0,0.3)"}),
                ]),
                dmc.GridCol(span={"base": 12, "sm": 4}, children=[
                    dmc.Group(justify="flex-end", children=[
                        icon("fas fa-book-open", 52, "#FFD700"),
                    ]),
                ]),
            ]),
            dmc.Text("Curate your perfect literary escape for the sun-drenched days ahead.",
                     ta="center", c="rgba(255,255,255,0.85)", size="lg", fs="italic", mt="sm"),
        ]),

        # Main controls
        dmc.Grid(mb="xl", gutter="lg", style={"minHeight": "650px"}, children=[

            # Columna izquierda — preferencias
            dmc.GridCol(span={"base": 12, "lg": 6}, children=[
                dmc.Card(withBorder=False, radius="md", shadow="md", style={"height": "100%"}, children=[
                    dmc.CardSection(
                        style={"background": "linear-gradient(135deg, #4CAF50 0%, #81C784 100%)"},
                        children=dmc.Stack(gap=2, p="lg", children=[
                            dmc.Title("✨ Curate Your Reading Experience", order=3, c="white", fw=700),
                            dmc.Text("Choose your preferred reading style", c="rgba(255,255,255,0.7)"),
                        ]),
                    ),
                    dmc.CardSection(p="lg", children=[
                        dmc.RadioGroup(
                            id="selection-mode-radio", value="vibes", mb="md",
                            children=dmc.Group(gap="lg", wrap="wrap", children=[
                                dmc.Radio(label="🌈 Reading Vibes",     value="vibes"),
                                dmc.Radio(label="🎣 Engaging Elements", value="elements"),
                                dmc.Radio(label="🎭 Literary Depths",   value="depths"),
                            ]),
                        ),
                        dmc.Button("Clear All Selections", id="reset-selections-btn",
                                   leftSection=icon("fas fa-broom", 16),
                                   color="yellow", variant="light", fullWidth=True,
                                   radius="md", mb="lg", fw=700),
                        preference_section("vibes-container",    VIBES_PATTERNS,    "vibe"),
                        preference_section("elements-container", ELEMENTOS_PATTERNS,"elemento", hidden=True),
                        preference_section("depths-container",   DEPTHS_PATTERNS,   "depth",    hidden=True),
                    ]),
                ]),
            ]),

            # Columna derecha — búsqueda + DNA
            dmc.GridCol(span={"base": 12, "lg": 6}, children=[
                dmc.Card(withBorder=False, radius="md", shadow="md", style={"height": "100%"}, children=[
                    dmc.CardSection(
                        style={"background": "linear-gradient(135deg, #2196F3 0%, #64B5F6 100%)"},
                        children=dmc.Stack(gap=2, p="lg", children=[
                            dmc.Title("⚙️ Refine Your Search", order=3, c="white", fw=700),
                            dmc.Text("Specify how many literary treasures you seek",
                                     c="rgba(255,255,255,0.7)"),
                        ]),
                    ),
                    dmc.CardSection(p="lg", children=[
                        dmc.Grid(align="flex-end", mb="lg", children=[
                            dmc.GridCol(span={"base": 12, "md": 6}, children=[
                                dmc.NumberInput(id="num-books-input", label="How many books?",
                                               min=5, max=12, step=1, value=8, radius="md", w=150),
                            ]),
                            dmc.GridCol(span={"base": 12, "md": 6}, children=[
                                dmc.Button("Uncover My Perfect Books", id="find-books-btn",
                                           leftSection=icon("fas fa-magnifying-glass", 18),
                                           size="lg", radius="md", fullWidth=True, fw=700,
                                           style={"background": "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",
                                                  "border": "none", "color": "#333",
                                                  "boxShadow": "0 4px 15px rgba(255,165,0,0.4)"}),
                            ]),
                        ]),
                        dmc.Divider(my="md"),
                        html.Div(id="analysis-container",
                                 style={"maxHeight": "350px", "overflowY": "auto", "paddingRight": "8px"},
                                 children=[empty_dna_panel()]),
                    ]),
                ]),
            ]),
        ]),

        # Resultados
        html.Div(id="results-container", style={"marginBottom": "32px"}),

        # Footer
        dmc.Divider(mb="lg", opacity=0.5),
        dmc.Paper(radius="md", shadow="sm", p="lg", style={
            "background": "linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)",
            "border": "1px solid #dee2e6",
        }, children=dmc.Stack(align="center", gap="xs", children=[
            dmc.Title("☀️ Summer Reading List Builder", order=5, c="#495057", ta="center"),
            dmc.Text(["Built with ", html.Strong("Python"), " | ", html.Strong("Pandas"),
                      " | ", html.Strong("Scikit-learn"), " | ", html.Strong("Dash"), " | ", html.Strong("Dash Mantine Components")],
                     ta="center", c="dimmed", size="sm"),
            dmc.Text(["Developed by ", html.Strong("Alexander Cabrera",
                                                    style={"color": "#228be6"})],
                     ta="center", c="dimmed", size="sm"),
        ])),

        html.Div(id="book-modal-container", children=dmc.Modal(id="book-modal", opened=False)),
    ]),
]))


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------

@app.callback(
    Output("vibes-container", "style"),
    Output("elements-container", "style"),
    Output("depths-container", "style"),
    Input("selection-mode-radio", "value"),
)
def toggle_section(selected):
    base   = {"height": "400px", "overflowY": "auto", "paddingRight": "15px"}
    hidden = {**base, "display": "none"}
    order  = {"vibes": 0, "elements": 1, "depths": 2}
    active = order.get(selected, 0)
    return [hidden if i != active else base for i in range(3)]


@app.callback(
    [Output(checkbox_id("vibe", v),    "checked") for v in VIBES_PATTERNS] +
    [Output(checkbox_id("elemento", e),"checked") for e in ELEMENTOS_PATTERNS] +
    [Output(checkbox_id("depth", d),   "checked") for d in DEPTHS_PATTERNS],
    Input("reset-selections-btn", "n_clicks"),
    prevent_initial_call=True,
)
def reset_checkboxes(_):
    return [False] * (len(VIBES_PATTERNS) + len(ELEMENTOS_PATTERNS) + len(DEPTHS_PATTERNS))


@app.callback(
    Output("results-container", "children"),
    Output("book-modal", "opened", allow_duplicate=True),
    Output("book-modal-container", "children", allow_duplicate=True),
    Output("analysis-container", "children"),
    Output("last-recommendations", "data"),
    Output("last-selections", "data"),
    Input("find-books-btn", "n_clicks"),
    [State(checkbox_id("vibe", v),    "checked") for v in VIBES_PATTERNS] +
    [State(checkbox_id("elemento", e),"checked") for e in ELEMENTOS_PATTERNS] +
    [State(checkbox_id("depth", d),   "checked") for d in DEPTHS_PATTERNS] +
    [State("num-books-input", "value")],
    prevent_initial_call=True,
)
def find_and_display(n_clicks, *args):
    empty_modal = dmc.Modal(id="book-modal", opened=False)
    empty_store = {"vibes": [], "elementos": [], "depths": []}

    if not n_clicks:
        return html.Div(), False, empty_modal, empty_dna_panel(), [], empty_store

    nv, ne = len(VIBES_PATTERNS), len(ELEMENTOS_PATTERNS)
    vibes      = [v for v, sel in zip(VIBES_PATTERNS,    args[:nv])        if sel]
    elementos  = [e for e, sel in zip(ELEMENTOS_PATTERNS, args[nv:nv+ne])  if sel]
    depths     = [d for d, sel in zip(DEPTHS_PATTERNS,   args[nv+ne:-1])  if sel]
    n          = args[-1]

    selections = {"vibes": vibes, "elementos": elementos, "depths": depths}
    has_sel    = any([vibes, elementos, depths])
    dna_content = dna_panel(analyze_reading_dna(df, vibes, elementos, depths)) if has_sel else empty_dna_panel()

    if not has_sel:
        alert = dmc.Alert(title="🤔 What Sparks Your Interest?",
                          children="Select at least one preference to find your perfect books.",
                          color="blue", radius="md")
        return alert, False, empty_modal, dna_content, [], selections

    recommended = find_books(df, tfidf_matrix, vectorizer, vibes, elementos, depths, n)

    if not recommended:
        alert = dmc.Alert(title="😔 No Matches Found",
                          children="Try different combinations of preferences.",
                          color="yellow", radius="md")
        return alert, False, empty_modal, dna_content, [], selections

    books_data = [b.to_dict() if hasattr(b, "to_dict") else dict(b) for b in recommended]
    return results_display(recommended), False, empty_modal, dna_content, books_data, selections


@app.callback(
    Output("book-modal-container", "children", allow_duplicate=True),
    Output("book-modal", "opened", allow_duplicate=True),
    Input({"type": "open-book-modal", "index": ALL}, "n_clicks"),
    State("book-modal", "opened"),
    prevent_initial_call=True,
)
def open_modal(n_clicks, _):
    if not any(n_clicks) or all(n is None for n in n_clicks):
        raise dash.exceptions.PreventUpdate
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    idx = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
    try:
        return book_modal(int(idx)), True
    except Exception:
        err = dmc.Modal(id="book-modal", opened=True, title="Error",
                        children=[dmc.Text("Could not load book details."),
                                  dmc.Group(justify="flex-end", mt="md", children=[
                                      dmc.Button("Close", id="close-modal", variant="outline",
                                                 color="gray", radius="md")])])
        return err, True


@app.callback(
    Output("book-modal", "opened", allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    State("book-modal", "opened"),
    prevent_initial_call=True,
)
def close_modal(n_clicks, is_open):
    return False if n_clicks else is_open


@app.callback(
    Output("download-csv", "data"),
    Input("download-csv-btn", "n_clicks"),
    State("last-recommendations", "data"),
    prevent_initial_call=True,
)
def download_csv(n_clicks, data):
    if not n_clicks or not data:
        raise dash.exceptions.PreventUpdate
    df_exp  = pd.DataFrame(data)
    cols    = [c for c in EXPORT_COLUMNS if c in df_exp.columns]
    ts      = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    return dcc.send_data_frame(df_exp[cols].to_csv, f"summer_reading_list_{ts}.csv", index=False)


@app.callback(
    Output("download-txt", "data"),
    Input("download-txt-btn", "n_clicks"),
    State("last-recommendations", "data"),
    State("last-selections", "data"),
    prevent_initial_call=True,
)
def download_txt(n_clicks, data, selections):
    if not n_clicks or not data:
        raise dash.exceptions.PreventUpdate

    lines = ["☀️ YOUR SUMMER READING LIST ☀️", "=" * 50, ""]
    if selections.get("vibes"):
        lines.append(f"🌈 Vibes: {', '.join(selections['vibes'])}")
    if selections.get("elementos"):
        lines.append(f"🎣 Elements: {', '.join(selections['elementos'])}")
    if selections.get("depths"):
        lines.append(f"🎭 Depths: {', '.join(selections['depths'])}")
    lines += ["", "-" * 50, ""]

    for i, book in enumerate(data, 1):
        lines.append(f"{i}. {book.get('original_title', 'N/A')}")
        lines.append(f"   Author: {book.get('author', 'N/A')}")
        lines.append(f"   Rating: {book.get('avg_rating', 0):.1f}/5 ({book.get('ratings_count', 0)} votes)")
        lines.append(f"   Match: {book.get('match_percentage', 0):.0f}%")
        if book.get("num_pages", 0) > 0:
            lines.append(f"   Pages: {int(book['num_pages'])}")
        lines.append("")

    lines += ["", "=" * 50, "Generated by Summer Reading List Builder",
              f"Created on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"]

    ts = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    return dict(content="\n".join(lines), filename=f"summer_reading_list_{ts}.txt")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
server = app.server