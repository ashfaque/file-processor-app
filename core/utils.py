import os
import base64
import zipfile


def save_dash_upload(contents, filename, target_dir):
    """Decodes Dash's base64 upload and saves it to a local temp folder."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    file_path = os.path.join(target_dir, filename)
    with open(file_path, "wb") as f:
        f.write(decoded)
    return file_path


def create_zip_archive(source_dir, output_zip_path):
    """Zips all files in a directory into a single archive."""
    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Ensure the files inside the zip don't have absolute folder paths attached
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    return output_zip_path
