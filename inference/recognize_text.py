import os
import cv2
import easyocr
import re # Import regular expression module for post-processing

# --- Configuration Paths ---
# Directory containing the cropped license plate images (output from detect_and_crop.py)
# Changed path to be relative to the project root, assuming script is run from project root.
cropped_plates_dir = 'outputs/cropped_plates'
# Path to save the final predictions CSV
predictions_csv_path = 'outputs/predictions.csv'

# --- Initialize EasyOCR Reader ---
print("Initializing EasyOCR reader...")
# Initialize the reader for English language ('en').
# Set 'gpu=True' if you have a CUDA-enabled GPU for faster processing.
# If you are on CPU, set 'gpu=False'.
try:
    reader = easyocr.Reader(['en'], gpu=False) # Keep gpu=False as you're on CPU
    print("✅ EasyOCR reader initialized successfully.")
except Exception as e:
    print(f"Error initializing EasyOCR: {e}")
    print("Please ensure EasyOCR is installed (`pip install easyocr`) and check GPU compatibility if 'gpu=True' is used.")
    exit() # Exit if reader cannot be initialized

# --- Post-processing Function ---
def clean_license_plate_text(text):
    """
    Cleans the raw OCR text to resemble a typical license plate format.
    - Converts common OCR errors (e.g., 'O' to '0', 'I' to '1').
    - Removes non-alphanumeric characters (except for specific cases if needed).
    - Removes extra spaces.
    """
    # Convert to uppercase for consistency
    cleaned_text = text.upper()

    # Common OCR error substitutions (can be expanded based on error analysis)
    cleaned_text = cleaned_text.replace('O', '0') # Often 'O' recognized as '0'
    cleaned_text = cleaned_text.replace('I', '1') # Often 'I' recognized as '1'
    cleaned_text = cleaned_text.replace('S', '5') # Often 'S' recognized as '5'
    cleaned_text = cleaned_text.replace('B', '8') # Often 'B' recognized as '8'
    cleaned_text = cleaned_text.replace('Z', '2') # Often 'Z' recognized as '2'
    cleaned_text = cleaned_text.replace('G', '6') # Often 'G' recognized as '6'

    # Remove any character that is not a letter (A-Z) or a digit (0-9)
    # This aggressive filtering is good for strict alphanumeric plates
    cleaned_text = re.sub(r'[^A-Z0-9]', '', cleaned_text)

    # Remove any remaining multiple spaces (if any were left after initial cleaning)
    cleaned_text = re.sub(r'\s+', '', cleaned_text)

    return cleaned_text

# --- Perform OCR on Cropped Plates ---
print(f"\nStarting character recognition for cropped plates in: {cropped_plates_dir}")
predictions = []
processed_count = 0
skipped_count = 0

# --- DEBUGGING STEP: Print absolute path and check existence ---
absolute_cropped_plates_dir = os.path.abspath(cropped_plates_dir)
print(f"Attempting to access absolute path: {absolute_cropped_plates_dir}")

if not os.path.isdir(absolute_cropped_plates_dir):
    print(f"Error: Directory not found or is not a directory: {absolute_cropped_plates_dir}")
    print("Please ensure 'detect_and_crop.py' ran successfully and created this directory with images.")
    exit()
# --- END DEBUGGING STEP ---


# Get a sorted list of image names to ensure consistent processing order
image_names = sorted(os.listdir(cropped_plates_dir))

for img_name in image_names:
    img_path = os.path.join(cropped_plates_dir, img_name)

    # Skip if not a file or not a common image extension
    if not os.path.isfile(img_path) or not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        print(f"Skipping non-image file in cropped directory: {img_name}")
        skipped_count += 1
        continue

    # Load the cropped image
    img_bgr = cv2.imread(img_path)
    if img_bgr is None:
        print(f"Warning: Could not read cropped image: {img_path}. Skipping OCR.")
        skipped_count += 1
        continue

    # Convert BGR to RGB for EasyOCR
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Perform OCR
    try:
        results = reader.readtext(img_rgb)
        
        # Extract text from results. EasyOCR can return multiple text boxes.
        # For license plates, we typically concatenate all detected text or take the most confident one.
        # Here, we concatenate all text detected in the image.
        raw_text = ""
        if results:
            # Sort results by x-coordinate to ensure correct order of characters/words
            results.sort(key=lambda x: x[0][0][0]) # Sort by x-coordinate of top-left corner
            for (bbox, text, prob) in results:
                raw_text += text + " " # Add a space between detected segments

        raw_text = raw_text.strip() # Remove leading/trailing spaces

        # Apply post-processing to clean the recognized text
        cleaned_text = clean_license_plate_text(raw_text)

        predictions.append({'image_name': img_name, 'predicted_text': cleaned_text})
        processed_count += 1
        print(f"Processed {img_name}: Raw='{raw_text}', Cleaned='{cleaned_text}'")

    except Exception as e:
        print(f"Error during OCR for {img_name}: {e}. Skipping.")
        skipped_count += 1
        predictions.append({'image_name': img_name, 'predicted_text': ''}) # Append empty string for failed OCR
        continue

# --- Save Predictions to CSV ---
print(f"\nSaving predictions to CSV: {predictions_csv_path}")
try:
    # Convert list of dictionaries to pandas DataFrame and save
    import pandas as pd # Import pandas here as it's used for CSV saving
    df_predictions = pd.DataFrame(predictions)
    df_predictions.to_csv(predictions_csv_path, index=False)
    print(f"✅ Predictions saved successfully to {predictions_csv_path}")
except Exception as e:
    print(f"Error saving predictions to CSV: {e}")

print(f"\nOCR processing complete. Processed {processed_count} images, Skipped {skipped_count}.")
print("Next, you will run the full pipeline and evaluate the results.")
