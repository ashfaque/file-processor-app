import os
from PIL import Image, ImageOps


def process_single_image(input_path, output_dir, filename, options):
    """
    Processes a single image based on user UI options.
    options = dict containing quality, format, flip_h, flip_v, rotate, crop_pixels
    """
    try:
        with Image.open(input_path) as img:

            # --- 1. Format Conversion Prep ---
            target_format = options.get("format", "ORIGINAL").upper()
            if target_format == "ORIGINAL":
                # Extract format from original extension, default to JPEG
                ext = os.path.splitext(filename)[1].lower()
                target_format = "PNG" if ext == ".png" else "JPEG"

            # If saving to JPEG, drop Alpha (transparency) channel if it exists
            if target_format == "JPEG" and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # --- 2. Transformations ---
            if options.get("flip_h"):
                img = ImageOps.mirror(img)
            if options.get("flip_v"):
                img = ImageOps.flip(img)

            rotate_val = options.get("rotate", 0)
            if rotate_val != 0:
                # expand=True prevents corners from being cut off during rotation
                img = img.rotate(-rotate_val, expand=True)

            # --- 3. Cropping (NOW WITH SAFETY CHECKS) ---
            crop_px = options.get("crop", {})
            if any(crop_px.values()):
                width, height = img.size

                # Get crop values, default to 0, and use max() to prevent negative numbers
                c_left = max(0, crop_px.get("left", 0))
                c_top = max(0, crop_px.get("top", 0))
                c_right = max(0, crop_px.get("right", 0))
                c_bottom = max(0, crop_px.get("bottom", 0))

                # SAFETY CHECK: Only crop if the requested crop leaves at least 1 pixel of image
                # If they ask to crop 1000px from a 800px image, we just skip the crop and keep the image safe.
                if (c_left + c_right) < width and (c_top + c_bottom) < height:
                    left = c_left
                    top = c_top
                    right = width - c_right
                    bottom = height - c_bottom
                    img = img.crop((left, top, right, bottom))
                else:
                    print(f"⚠️ Warning: Skipped cropping for {filename}. Image too small for requested crop.")

            # --- 4. Save and Compress ---
            base_name = os.path.splitext(filename)[0]
            new_ext = f".{target_format.lower()}"
            if new_ext == ".jpeg":
                new_ext = ".jpg"

            final_output_path = os.path.join(output_dir, f"{base_name}{new_ext}")

            quality = options.get("quality", 65)

            if target_format == "PNG":
                img.save(final_output_path, format="PNG", optimize=True)
            else:
                img.save(final_output_path, format=target_format, optimize=True, quality=quality)

        return True, f"Success: {filename}"

    except Exception as e:
        return False, f"Error processing {filename}: {str(e)}"
