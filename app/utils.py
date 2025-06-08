import re
import pytesseract
from PIL import Image
from io import BytesIO
import json

from app.groq_client import analyze_text_with_groq

# Set tesseract path (adjust for your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def preprocess_image(image):
    """Preprocess image for better OCR results"""
    from PIL import ImageFilter, ImageEnhance
    import numpy as np

    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')

    # Resize image if it's too small (OCR works better on larger images)
    width, height = image.size
    if width < 1000 or height < 1000:
        # Scale up by 2x if image is small
        new_width = width * 2
        new_height = height * 2
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Increase contrast by 50%

    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)  # Increase sharpness

    # Apply noise reduction filter
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # Apply unsharp mask for better text clarity
    image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Optional: Apply adaptive thresholding for better text/background separation
    # Convert to numpy array for advanced processing
    img_array = np.array(image)

    # Simple thresholding - you can make this more sophisticated
    threshold = np.mean(img_array)
    img_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)

    # Convert back to PIL Image
    image = Image.fromarray(img_array, mode='L')

    return image


async def extract_lab_results(file):
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Preprocess image for better OCR
        processed_image = preprocess_image(image)

        # Extract text using OCR
        raw_text = pytesseract.image_to_string(processed_image, config='--psm 6')
        print(f"OCR extracted text: {raw_text}")  # Debug log

        if not raw_text.strip():
            return {
                "success": False,
                "error": "No text could be extracted from the image",
                "results": None
            }

        # Use Groq to analyze and structure the text
        structured_data = await analyze_text_with_groq(raw_text)

        if not structured_data:
            return {
                "success": False,
                "error": "Failed to analyze the extracted text",
                "results": None
            }

        # Convert to your expected format with additional fields
        lab_results = {
            "patient_name": structured_data.get("patient_name"),
            "doctor_name": structured_data.get("doctor_name"),
            "clinic_name": structured_data.get("clinic_name"),
            "test_date": structured_data.get("test_date"),
            "report_date": structured_data.get("report_date"),
            "tests": []
        }

        # Process test results
        for test in structured_data.get("tests", []):
            # Convert Groq format to your LaboratoryTest format
            lab_test = {
                "parameter": test.get("name", "Unknown"),
                "value": extract_numeric_value(test.get("value", "")),
                "unit": test.get("unit", ""),
                "reference_range": test.get("reference_range", ""),
                "status": test.get("status", "Unknown")
            }

            # Try to extract reference min/max
            ref_min, ref_max = parse_reference_range(test.get("reference_range", ""))
            if ref_min is not None:
                lab_test["reference_min"] = ref_min
            if ref_max is not None:
                lab_test["reference_max"] = ref_max

            lab_results["tests"].append(lab_test)

        return {
            "success": True,
            "results": lab_results,
            "error": None
        }

    except Exception as e:
        print(f"Error in extract_lab_results: {e}")
        return {
            "success": False,
            "error": f"Error processing file: {str(e)}",
            "results": None
        }


def extract_numeric_value(value_str):
    """Extract numeric value from string"""
    if isinstance(value_str, (int, float)):
        return float(value_str)

    # Try to extract number from string
    import re
    match = re.search(r'(\d+\.?\d*)', str(value_str))
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass
    return None


def parse_reference_range(range_str):
    """Parse reference range string to get min/max values"""
    if not range_str:
        return None, None

    # Look for patterns like "70-100", "12.0-15.5", "4.0 - 11.0"
    pattern = r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)'
    match = re.search(pattern, range_str)

    if match:
        try:
            return float(match.group(1)), float(match.group(2))
        except ValueError:
            pass

    return None, None

# async def extract_lab_results(file):

# contents = await file.read()
# image = Image.open(BytesIO(contents))
#
# # Extract full raw text
# raw_text = pytesseract.image_to_string(image)
#
# # Extract metadata from full text
# metadata = extract_metadata(raw_text)
#
# # Structured data extraction
# data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
# rows = []
# current_row = []
# last_top = None
#
# for i in range(len(data['text'])):
#     if int(data['conf'][i]) > 50:
#         word = data['text'][i].strip()
#         top = data['top'][i]
#
#         if last_top is None:
#             last_top = top
#
#         if abs(top - last_top) > 10:
#             if current_row:
#                 rows.append(current_row)
#             current_row = []
#             last_top = top
#
#         current_row.append(word)
#
# if current_row:
#     rows.append(current_row)
#
# test_results = []
# for row in rows:
#     if len(row) >= 4:
#         param = row[0]
#         value = try_float(row[1])
#         unit = row[-1]
#         ref_range = extract_range(row[2:-1])
#         if try_float(row[1]) is not None:  # Only accept valid numbers
#             test_results.append({
#                 "parameter": param,
#                 "value": value,
#                 "unit": unit,
#                 "reference_min": ref_range[0],
#                 "reference_max": ref_range[1],
#                 "semantic_class": None
#             })
#
# return {
#     "success": True,
#     "results": {
#         "metadata": metadata,
#         "tests": test_results
#     }
# }
