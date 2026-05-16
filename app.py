import dash
from dash import dcc, html
from callbacks import register_callbacks

# Initialize the Dash app
# Dash automatically serves files from the 'assets' folder, including style.css
app = dash.Dash(__name__, title="Universal Media Processor")

app.layout = html.Div(
    className="page-container",
    children=[
        html.Div(
            className="content-wrapper",
            children=[
                # --- HEADER ---
                html.Div(
                    className="header-section",
                    children=[
                        html.H1("Image Processor", className="main-title"),
                        html.P("Precision media processing engine.", className="sub-title"),
                    ],
                ),
                # --- INVISIBLE APP MEMORY ---
                dcc.Store(id="file-store", data={}),
                # --- UPLOAD SECTION ---
                html.Div(
                    className="ui-card",
                    children=[
                        html.Div("I. Workspace", className="card-title"),
                        dcc.Upload(
                            id="upload-data",
                            className="upload-area",
                            children=html.Div(["Drag and Drop or ", html.B("Select Media")], className="upload-text"),
                            multiple=True,
                        ),
                        html.Div(id="file-list-ui", className="file-list-container"),
                    ],
                ),
                # --- CONTROLS SECTION ---
                html.Div(
                    className="ui-card",
                    children=[
                        html.Div("II. Parameters", className="card-title"),
                        # Quality Slider
                        html.Div(
                            className="slider-container",
                            children=[
                                html.Label("Compression Ratio", className="input-label"),
                                dcc.Slider(
                                    id="slider-quality",
                                    min=10,
                                    max=100,
                                    step=1,
                                    value=65,
                                    marks={10: "Aggressive", 65: "Optimal", 100: "Lossless"},
                                ),
                            ],
                        ),
                        # Format & Rotate
                        html.Div(
                            className="input-row",
                            children=[
                                html.Div(
                                    className="input-group",
                                    children=[
                                        html.Label("Target Format", className="input-label"),
                                        dcc.Dropdown(
                                            id="dropdown-format",
                                            className="dash-dropdown",
                                            options=[
                                                {"label": "Preserve Original", "value": "ORIGINAL"},
                                                {"label": "Force JPEG", "value": "JPEG"},
                                                {"label": "Force PNG", "value": "PNG"},
                                            ],
                                            value="ORIGINAL",
                                            clearable=False,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="input-group",
                                    children=[
                                        html.Label("Rotation Matrix", className="input-label"),
                                        dcc.Dropdown(
                                            id="dropdown-rotate",
                                            className="dash-dropdown",
                                            options=[
                                                {"label": "0° (Default)", "value": 0},
                                                {"label": "90° Clockwise", "value": 90},
                                                {"label": "90° Counter-Clockwise", "value": -90},
                                                {"label": "180° Inverted", "value": 180},
                                            ],
                                            value=0,
                                            clearable=False,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        # Flip & Crop
                        html.Div(
                            className="input-row",
                            children=[
                                html.Div(
                                    className="input-group",
                                    children=[
                                        html.Label("Axis Mirroring", className="input-label"),
                                        html.Div(
                                            className="checkbox-container",
                                            children=[
                                                dcc.Checklist(
                                                    id="check-flip",
                                                    className="custom-checklist",
                                                    options=[
                                                        {"label": " X-Axis ", "value": "H"},
                                                        {"label": " Y-Axis ", "value": "V"},
                                                    ],
                                                    value=[],
                                                    inline=True,
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="input-group",
                                    children=[
                                        html.Label("Pixel Crop Bounds (L, T, R, B)", className="input-label"),
                                        html.Div(
                                            className="crop-input-wrapper",
                                            children=[
                                                dcc.Input(
                                                    id="crop-left",
                                                    type="number",
                                                    placeholder="L",
                                                    className="number-input",
                                                ),
                                                dcc.Input(
                                                    id="crop-top",
                                                    type="number",
                                                    placeholder="T",
                                                    className="number-input",
                                                ),
                                                dcc.Input(
                                                    id="crop-right",
                                                    type="number",
                                                    placeholder="R",
                                                    className="number-input",
                                                ),
                                                dcc.Input(
                                                    id="crop-bottom",
                                                    type="number",
                                                    placeholder="B",
                                                    className="number-input",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                # --- ACTION SECTION ---
                html.Button("Initialize Sequence", id="process-btn", n_clicks=0, className="process-btn"),
                html.Div(id="status-message", className="status-msg"),
                dcc.Download(id="download-zip"),
            ],
        ),
    ],
)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
