# SIM Card Region Replacer

A Python script that automatically detects, removes, and replaces a SIM card region in product images using OpenCV.

---

## How It Works

The script scans images in a designated folder, detects the SIM card region using contour detection, and replaces it with a corresponding replacement image. The result is saved to a separate output folder — leaving the originals untouched.

---

## Folder Structure

```
project/
│
├── main.py                  # The main script
│
└── images/                  # Place your original images here
    ├── image1.png
    ├── image2.png
    ├── images_sim/          # Replacement SIM images (named: <original>_sim.png)
    │   ├── image1_sim.png
    │   └── image2_sim.png
    └── images_updated/      # Output folder (auto-created by the script)
        ├── image1_updated.png
        └── image2_updated.png
```

---

## Requirements

- Python 3.x
- OpenCV
- NumPy

Install dependencies with:

```bash
pip install opencv-python numpy
```

---

## Usage

1. Place your original images inside the `images/` folder (next to the script).
2. Create an `images_sim/` subfolder inside `images/` and add the replacement SIM images. Each replacement must be named after its corresponding original with `_sim` appended — for example, `photo1.png` → `photo1_sim.png`.
3. Run the script:

```bash
python main.py
```

4. Find the processed images in `images/images_updated/`, named as `<original>_updated.png`.

---

## Detection Logic

The script uses the following steps to locate the SIM card region:

1. Converts the image to **grayscale**.
2. Applies **binary inverse thresholding** (threshold value: 100) to isolate dark regions.
3. Finds **external contours** using OpenCV's `findContours`.
4. Filters contours by a minimum size of **width > 100px** and **height > 50px**.
5. Takes the **first matching contour** as the SIM region and replaces it.

> **Note:** The size thresholds (`w > 100`, `h > 50`) may need to be adjusted depending on your image resolution and SIM card size.

---

## Notes

- The script processes all valid image files in the `images/` folder. Subfolders (`images_sim`, `images_updated`) are automatically skipped.
- If no replacement image is found for a given original, that image is skipped with an error message.
- The replacement SIM image is **automatically resized** to fit the detected region.
- Supported input formats: any format readable by OpenCV (PNG, JPG, BMP, etc.).
- Output images are always saved as **PNG**.
