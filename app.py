import dash
from dash import dcc, html
from callbacks import register_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, title="Universal Media Processor")

# Clean, simple inline CSS
STYLES = {
    "container": {"maxWidth": "800px", "margin": "0 auto", "padding": "20px", "fontFamily": "Arial"},
    "card": {"border": "1px solid #ddd", "padding": "20px", "borderRadius": "8px", "marginBottom": "20px"},
    "upload": {
        "width": "100%",
        "height": "100px",
        "lineHeight": "100px",
        "borderWidth": "2px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
        "cursor": "pointer",
    },
    "row": {"display": "flex", "gap": "20px", "marginBottom": "15px"},
    "file_list_container": {
        "maxHeight": "200px",
        "overflowY": "auto",
        "marginTop": "15px",
        "border": "1px solid #eee",
        "padding": "10px",
        "borderRadius": "5px",
        "backgroundColor": "#fafafa",
    },
}

app.layout = html.Div(
    style=STYLES["container"],
    children=[
        html.H1("Universal Media Processor"),
        html.P("Drag and drop your files. Adjust settings below and process."),
        # --- INVISIBLE APP MEMORY ---
        dcc.Store(id="file-store", data={}),
        # --- UPLOAD SECTION ---
        html.Div(
            style=STYLES["card"],
            children=[
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Drag and Drop or ", html.A("Click to Select Multiple Files")]),
                    style=STYLES["upload"],
                    multiple=True,
                ),
                html.Div(id="file-list-ui", style=STYLES["file_list_container"]),
            ],
        ),
        # --- CONTROLS SECTION ---
        html.Div(
            style=STYLES["card"],
            children=[
                html.H3("Processing Options"),
                html.Label("JPEG Compression Quality (Lower = Smaller File):"),
                dcc.Slider(
                    id="slider-quality",
                    min=10,
                    max=100,
                    step=1,
                    value=65,
                    marks={10: "10 (Lowest)", 65: "65 (Optimal)", 100: "100 (Highest)"},
                ),
                html.Br(),
                html.Div(
                    style=STYLES["row"],
                    children=[
                        html.Div(
                            [
                                html.Label("Convert Format:"),
                                dcc.Dropdown(
                                    id="dropdown-format",
                                    options=[
                                        {"label": "Keep Original", "value": "ORIGINAL"},
                                        {"label": "To JPEG", "value": "JPEG"},
                                        {"label": "To PNG", "value": "PNG"},
                                    ],
                                    value="ORIGINAL",
                                    clearable=False,  # 🛠️ FIX: Prevents user from clearing the dropdown
                                ),
                            ],
                            style={"flex": 1},
                        ),
                        html.Div(
                            [
                                html.Label("Rotate:"),
                                dcc.Dropdown(
                                    id="dropdown-rotate",
                                    options=[
                                        {"label": "None", "value": 0},
                                        {"label": "90° Clockwise", "value": 90},
                                        {"label": "90° Counter-Clockwise", "value": -90},
                                        {"label": "180°", "value": 180},
                                    ],
                                    value=0,
                                    clearable=False,  # 🛠️ FIX: Prevents user from clearing the dropdown
                                ),
                            ],
                            style={"flex": 1},
                        ),
                    ],
                ),
                html.Div(
                    style=STYLES["row"],
                    children=[
                        html.Div(
                            [
                                html.Label("Flip Image:"),
                                dcc.Checklist(
                                    id="check-flip",
                                    options=[
                                        {"label": " Horizontal  ", "value": "H"},
                                        {"label": " Vertical", "value": "V"},
                                    ],
                                    value=[],
                                    inline=True,
                                ),
                            ],
                            style={"flex": 1},
                        ),
                        html.Div(
                            [
                                html.Label("Crop Pixels (Left, Top, Right, Bottom):"),
                                html.Div(
                                    [
                                        dcc.Input(
                                            id="crop-left", type="number", placeholder="L", style={"width": "50px"}
                                        ),
                                        dcc.Input(
                                            id="crop-top", type="number", placeholder="T", style={"width": "50px"}
                                        ),
                                        dcc.Input(
                                            id="crop-right", type="number", placeholder="R", style={"width": "50px"}
                                        ),
                                        dcc.Input(
                                            id="crop-bottom", type="number", placeholder="B", style={"width": "50px"}
                                        ),
                                    ],
                                    style={"display": "flex", "gap": "5px"},
                                ),
                            ],
                            style={"flex": 1},
                        ),
                    ],
                ),
            ],
        ),
        # --- ACTION SECTION ---
        html.Button(
            "Process & Download ZIP",
            id="process-btn",
            n_clicks=0,
            style={"width": "100%", "padding": "15px", "fontSize": "16px", "cursor": "pointer"},
        ),
        html.Div(id="status-message", style={"marginTop": "20px", "fontWeight": "bold", "textAlign": "center"}),
        dcc.Download(id="download-zip"),
    ],
)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
