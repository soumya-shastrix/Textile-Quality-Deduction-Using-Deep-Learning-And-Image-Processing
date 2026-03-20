Textile Quality Deduction Using Deep Learning And Image Processing

Problem Statement (Fabric Industry)
In the fabric/textile industry, product quality is extremely important.  Many fabrics contain defects like holes, scratches, stains, or broken threads.  
Most industries still depend on manual inspection, which is:
-Time consuming  
- Error-prone due to human fatigue  
- Difficult to maintain accuracy for large-scale production 
So, there is a need for an automatic defect detection system to improve fabric quality and reduce production loss.

What We Came Up With (Solution)
We developed a “Fabric Defect Detection System” using **Image Processing and Deep Learning**.  This project helps to automatically detect defects in fabric images.  
It provides a Flask-based web application where users can register/login, upload fabric images, and view defect detection output.

 Project Workflow
1. User registers and logs into the web application  
2. User uploads a fabric image  
3. Image preprocessing is performed (resize, grayscale, noise removal)  
4. Edge detection is applied using **Canny Algorithm**  
5. The deep learning model analyzes the fabric image  
6. If defect is detected, the system highlights the defective area  
7. The final result is displayed to the user



Dataset
Fabric images dataset includes:
  - Defective fabric images
  - Non-defective fabric images  
- Dataset is used for training and testing the deep learning model  
- Data preprocessing was applied before training for better accuracy  

Model & Evaluation
- Trained Deep Learning model is saved as:
  - `best_model.hdf5`
- Model performance can be evaluated using:
  - Accuracy
  - Loss
- The model helps detect defects with better consistency than manual inspection

Features
-User Registration & Login
- Upload Fabric Image
- Detect Fabric Defect
- Shows final result with defect highlighted
Tech Stack
- Python
- Flask
- OpenCV
- TensorFlow / Keras
- HTML

How to Run
1. Install required libraries:
```bash
pip install -r requirements.txt
2 Run the Flask application:
3 Open in browser:

Future Improvements
1. Detect multiple defect types (tear, stain, hole, etc.)
2. Improve accuracy using a larger dataset?
3. Deploy the web app online (Render / AWS) 
Textile Quality Deduction Using Deep Learning And Image Processing

z
