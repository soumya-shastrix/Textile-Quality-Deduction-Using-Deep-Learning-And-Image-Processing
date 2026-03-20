import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
# Load the image
import sqlite3

import cv2

conn = sqlite3.connect('Textile.db')
with conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM imgsave")
    rows = cursor.fetchall()
    for row in rows:
        filename = row[0]
import cv2
import numpy as np
import matplotlib.pyplot as plt


# Function to detect defects
def detect_fabric_defect(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 1: Preprocessing
    # Apply Gaussian blur to smooth the image
    blurred_image = cv2.GaussianBlur(image_gray, (5, 5), 0)

    # Step 2: Edge Detection using Canny
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)

    # Step 3: Find contours of detected edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Count large contours (indicative of defects)
    defect_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum size of the defect to be detected
            defect_count += 1

    # Step 5: Classification based on the number of defects
    if defect_count > 0:

        return "Defected", defect_count  # More than 0 defects detected
    else:
        return "Good", defect_count  # No defects detected


# Main function to display the result
def main():
    # Path to your fabric image
    fabric_image_path =filename

    # Get result
    fabric_status, defect_count = detect_fabric_defect(fabric_image_path)

    # Print result
    print(f"Fabric Status: {fabric_status}")
    print(f"Number of Defects Detected: {defect_count}")

    # Load the original fabric image to display
    image = cv2.imread(fabric_image_path)

    # If defected, highlight the defects in the image
    if fabric_status == "Defected":
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(image_gray, (5, 5), 0)
        edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                # Draw contours on the fabric image
                cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)  # Red color for defects

    # Display results
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(f"Fabric Status: {fabric_status}")
    plt.axis('off')
    plt.show()


if __name__ == "__main__":
    main()