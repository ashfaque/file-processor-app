import os
import tempfile
import shutil
from dash import Input, Output, State, dcc, html, ctx, ALL
from core.utils import save_dash_upload, create_zip_archive
from core.logic import process_single_image


def register_callbacks(app):

    # --- CALLBACK 1: Manage File Memory (Add or Delete) ---
    @app.callback(
        Output("file-store", "data"),
        Output("upload-data", "contents"),
        Output("upload-data", "filename"),
        Input("upload-data", "contents"),
        Input({"type": "delete-btn", "index": ALL}, "n_clicks"),
        State("upload-data", "filename"),
        State("file-store", "data"),
        prevent_initial_call=True,
    )
    def manage_files(uploaded_contents, delete_clicks, uploaded_filenames, current_store):
        current_store = current_store or {}
        triggered = ctx.triggered_id

        if triggered == "upload-data":
            if uploaded_contents and uploaded_filenames:
                for content, filename in zip(uploaded_contents, uploaded_filenames):
                    current_store[filename] = content

        elif isinstance(triggered, dict) and triggered.get("type") == "delete-btn":
            filename_to_delete = triggered.get("index")
            if filename_to_delete in current_store:
                del current_store[filename_to_delete]

        return current_store, None, None

    # --- CALLBACK 2: Render the UI List ---
    @app.callback(Output("file-list-ui", "children"), Input("file-store", "data"))
    def update_ui_list(store_data):
        if not store_data:
            return html.Div("No files queued for processing.", className="file-list-empty")

        items = []
        for filename in store_data.keys():
            items.append(
                html.Div(
                    className="file-list-item",
                    children=[
                        html.Span(f"📄 {filename}"),
                        html.Button("❌", id={"type": "delete-btn", "index": filename}, className="delete-btn"),
                    ],
                )
            )
        return items

    # --- CALLBACK 3: Process the Files ---
    @app.callback(
        Output("download-zip", "data"),
        Output("status-message", "children"),
        Input("process-btn", "n_clicks"),
        State("file-store", "data"),
        State("slider-quality", "value"),
        State("dropdown-format", "value"),
        State("dropdown-rotate", "value"),
        State("check-flip", "value"),
        State("crop-left", "value"),
        State("crop-top", "value"),
        State("crop-right", "value"),
        State("crop-bottom", "value"),
        prevent_initial_call=True,
    )
    def process_and_download(n_clicks, file_store, quality, fmt, rotate, flip_options, c_l, c_t, c_r, c_b):
        if not file_store:
            return None, "⚠️ Please upload at least one file first."

        filenames = list(file_store.keys())
        contents = list(file_store.values())
        flip_options = flip_options or []

        options = {
            "quality": quality if quality is not None else 65,
            "format": fmt if fmt is not None else "ORIGINAL",
            "rotate": int(rotate) if rotate is not None else 0,
            "flip_h": "H" in flip_options,
            "flip_v": "V" in flip_options,
            "crop": {"left": c_l or 0, "top": c_t or 0, "right": c_r or 0, "bottom": c_b or 0},
        }

        temp_base = tempfile.mkdtemp()
        input_dir = os.path.join(temp_base, "input")
        output_dir = os.path.join(temp_base, "output")
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        try:
            for content, name in zip(contents, filenames):
                save_dash_upload(content, name, input_dir)

            for filename in os.listdir(input_dir):
                input_path = os.path.join(input_dir, filename)
                process_single_image(input_path, output_dir, filename, options)

            # --- Check how many files we processed ---
            processed_files = os.listdir(output_dir)

            if len(processed_files) == 1:
                # If only 1 file, read it directly and send it (no zip)
                single_filename = processed_files[0]
                file_path = os.path.join(output_dir, single_filename)
                with open(file_path, "rb") as f:
                    file_data = f.read()
                return dcc.send_bytes(file_data, single_filename), "✅ Successfully processed 1 file!"

            else:
                # If multiple files, zip them up as usual
                zip_path = os.path.join(temp_base, "processed_media.zip")
                create_zip_archive(output_dir, zip_path)

                with open(zip_path, "rb") as f:
                    zip_data = f.read()

                return (
                    dcc.send_bytes(zip_data, "processed_media.zip"),
                    f"✅ Successfully processed {len(filenames)} files!",
                )

        except Exception as e:
            return None, f"❌ An error occurred: {str(e)}"

        finally:
            if os.path.exists(temp_base):
                shutil.rmtree(temp_base)
