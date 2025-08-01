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

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sathwikreddy018/License-Plate-Recognition-ALPR.git
   cd License-Plate-Recognition-ALPR

2. **Create virtual environment**:
```bash
python -m venv venv

**Activate**:
```bash
.\venv\Scripts\activate     # Windows
source venv/bin/activate     # macOS/Linux

3. **Install dependencies**:
```bash
pip install -r requirements.txt

4. **Download the dataset**:

https://drive.google.com/drive/folders/1ThHnUQjkCNTOKXnvySVfpHZxZbYsFfMQ
Extract and place the data/ folder in the project root.

5. **Run the Pipeline**
Open the Jupyter notebook:

jupyter notebook

Navigate to notebooks/License_Plate_Recognition.ipynb and run all cells.

## **Output**
**Cropped Plates**: Saved in outputs/cropped_plates/
**Visualizations**: Detection results
**Predictions**: Final CSV located at outputs/predictions.csv

## **Future Improvements**
Fine-tune OCR with additional training data.

Experiment with larger YOLOv8 models.

Build a web app or API for deployment.

Author: Sathwik Reddy
Internship Assignment @ Soulpage IT Solutions Pvt. Ltd.




