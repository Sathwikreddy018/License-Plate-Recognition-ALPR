# **License Plate Recognition (ALPR) System**

This repository contains a simplified implementation of an **Automatic License Plate Recognition (ALPR)** system using **YOLOv8** for license plate detection and **EasyOCR** for character recognition.

## **Features**

- **YOLOv8** model for high-accuracy license plate detection.
- **EasyOCR** for text extraction from detected plates.
- **End-to-end pipeline** for processing and evaluation.

## **How It Works**

1. **Detection**: The YOLOv8 model detects license plates in vehicle images.  
2. **OCR**: Cropped plate regions are processed using EasyOCR to extract text.  
3. **Post-processing**: OCR output is cleaned and standardized.  
4. **Prediction Output**: Results are saved in a CSV file.

## **Setup**

```bash
# Clone the repository
git clone https://github.com/Sathwikreddy018/License-Plate-Recognition-ALPR.git
cd License-Plate-Recognition-ALPR

# Create virtual environment
python -m venv venv

# Activate environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## **Download the Dataset**

- [Google Drive Dataset](https://drive.google.com/drive/folders/1ThHnUQjkCNTOKXnvySVfpHZxZbYsFfMQ)  
- Extract and place the `data/` folder in the project root.

## **Run the Pipeline**

Open the Jupyter notebook:

```bash
jupyter notebook

