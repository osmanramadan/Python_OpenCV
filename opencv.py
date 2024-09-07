
import cv2
import os
import numpy as np

# Function to detect, remove, and replace the SIM part in an image
def remove_and_replace_sim(image_path, sim_folder, updated_folder):
    # Load the original image
    img = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if img is None:
        print(f"Error: Could not read image {image_path}. Skipping.")
        return
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to highlight the SIM part (adjust as needed)
    thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # Find contours of the objects in the image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the filename without the extension
    filename = os.path.basename(image_path)
    name, _ = os.path.splitext(filename)

    # Load the replacement SIM part from the 'images_sim' folder (with "_sim" appended)
    replacement_sim_path = os.path.join(sim_folder, f'{name}_sim.png')
    replacement_sim = cv2.imread(replacement_sim_path)

    if replacement_sim is None:
        print(f"Error: Could not find replacement SIM image {replacement_sim_path}. Skipping.")
        return

    # Loop over contours to find the SIM card and replace it
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        roi = img[y:y+h, x:x+w]
        
        # Optional: Filter by size or aspect ratio to detect the correct SIM card
        if w > 100 and h > 50:  # Adjust size threshold as needed
            # Remove the SIM part by filling it with a background color (e.g., white)
            img[y:y+h, x:x+w] = (255, 255, 255)  # Replace with white background

            # Resize the replacement SIM part to fit the detected region
            resized_sim = cv2.resize(replacement_sim, (w, h))

            # Place the resized replacement SIM part in the same position
            img[y:y+h, x:x+w] = resized_sim
            
            print(f"Replaced SIM part in image: {filename}")
            break

    # Save the modified image in the updated folder
    output_path = os.path.join(updated_folder, f'{name}_updated.png')
    cv2.imwrite(output_path, img)
    print(f"Saved updated image as: {output_path}")

# Function to process all images in a folder, excluding certain subfolders
def process_images_in_folder(folder_path):
    # Path to the 'images_updated' folder inside the same folder
    updated_folder = os.path.join(folder_path, 'images_updated')
    
    # Path to the 'images_sim' folder (where SIM images are located)
    sim_folder = os.path.join(folder_path, 'images_sim')
    
    # Check if the 'images_sim' folder exists
    if not os.path.exists(sim_folder):
        print(f"Error: The 'images_sim' folder does not exist at {sim_folder}.")
        return
    
    # Create 'images_updated' folder if it does not exist
    if not os.path.exists(updated_folder):
        os.makedirs(updated_folder)
    
    # Loop over all files in the folder, excluding 'images_updated' and 'images_sim' folders
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Skip 'images_updated' and 'images_sim' folders
        if filename in ['images_updated', 'images_sim']:
            continue

        # Try to load the image to check if it's valid (this will accept all valid image formats)
        img = cv2.imread(file_path)
        if img is not None:  # If the image was successfully loaded
            print(f"Processing image: {filename}")
            remove_and_replace_sim(file_path, sim_folder, updated_folder)

# Path to the current code folder (the folder where the script is located)
current_folder = os.path.dirname(os.path.abspath(__file__))

# Path to the 'images' folder inside the current code folder
images_folder = os.path.join(current_folder, 'images')

# Check if the 'images' folder exists
if not os.path.exists(images_folder):
    print(f"Error: The 'images' folder does not exist at {images_folder}.")
else:
    # Call the function to process all images in the 'images' folder
    process_images_in_folder(images_folder)


# import cv2
# import pytesseract
# from pytesseract import Output

# # Load the image
# image_path = '2.png'
# img = cv2.imread(image_path)

# # Convert image to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Apply edge detection or thresholding to highlight the region
# thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

# # Find contours which can help in detecting the SIM card or desired part
# contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # Loop over contours to find the area of interest (SIM card)
# for contour in contours:
#     x, y, w, h = cv2.boundingRect(contour)
#     roi = img[y:y+h, x:x+w]
    
#     # Optional: Filter based on size or aspect ratio to detect the desired region
#     if w > 100 and h > 50:  # Example of size filtering
#         sim_card_region = roi
#         cv2.imshow("SIM Card Region", sim_card_region)
#         cv2.waitKey(0)

# # Use pytesseract to extract text from the region
# text = pytesseract.image_to_string(sim_card_region, config='--psm 6', output_type=Output.STRING)
# print("Extracted Text:", text)


# import cv2
# import os

# # Function to detect and save SIM part
# def detect_and_save_sim(image_path):
#     # Load the image
#     img = cv2.imread(image_path)

#     # Convert image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply edge detection or thresholding to highlight the region
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours which can help in detecting the SIM card or desired part
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the file name without extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Loop over contours to find the area of interest (SIM card)
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter based on size or aspect ratio to detect the desired region
#         if w > 100 and h > 50:  # Example of size filtering
#             sim_card_region = roi
            
#             # Save the cropped SIM card image with the original file name
#             output_path = f'{name}_sim_part.png'
#             cv2.imwrite(output_path, sim_card_region)
#             print(f"SIM card part saved as: {output_path}")
            
#             # Show the cropped image (optional for verification)
#             cv2.imshow("SIM Card Region", sim_card_region)
#             cv2.waitKey(0)
#             cv2.destroyAllWindows()

# # Path to the input image
# image_path = '2.png'

# # Call the function
# detect_and_save_sim(image_path)


# import cv2
# import os

# # Function to detect and save SIM part from an image
# def detect_and_save_sim(image_path):
#     # Load the image
#     img = cv2.imread(image_path)

#     # Convert image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply edge detection or thresholding to highlight the region
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours which can help in detecting the SIM card or desired part
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the file name without extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Loop over contours to find the area of interest (SIM card)
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter based on size or aspect ratio to detect the desired region
#         if w > 100 and h > 50:  # Example of size filtering (adjust as needed)
#             sim_card_region = roi
            
#             # Save the cropped SIM card image with the original file name
#             output_path = f'{name}_sim_part.png'
#             cv2.imwrite(output_path, sim_card_region)
#             print(f"SIM card part saved as: {output_path}")

#             # Show the cropped image (optional for verification)
#             # cv2.imshow("SIM Card Region", sim_card_region)
#             # cv2.waitKey(0)
#             # cv2.destroyAllWindows()

# # Function to process all images in a folder
# def process_images_in_folder(folder_path):
#     # Loop over all files in the folder
#     for filename in os.listdir(folder_path):
#         # Get full file path
#         file_path = os.path.join(folder_path, filename)
        
#         # Check if the file is an image (optional: add more extensions if needed)
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
#             print(f"Processing image: {filename}")
#             detect_and_save_sim(file_path)

# # Path to the folder containing images
# folder_path = 'C://Users//osman//Desktop//py'

# # Call the function to process all images in the folder
# process_images_in_folder(folder_path)




# import cv2
# import os

# # Function to detect and save SIM part from an image
# def detect_and_save_sim(image_path):
#     # Load the image
#     img = cv2.imread(image_path)
    
#     # Check if the image was loaded successfully
#     if img is None:
#         print(f"Error: Could not read image {image_path}. Skipping.")
#         return
    
#     # Convert image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply edge detection or thresholding to highlight the region
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours which can help in detecting the SIM card or desired part
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the file name without extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Loop over contours to find the area of interest (SIM card)
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter based on size or aspect ratio to detect the desired region
#         if w > 100 and h > 50:  # Example of size filtering (adjust as needed)
#             sim_card_region = roi
            
#             # Save the cropped SIM card image with the original file name
#             output_path = f'{name}_sim_part.png'
#             cv2.imwrite(output_path, sim_card_region)
#             print(f"SIM card part saved as: {output_path}")

# # Function to process all images in a folder
# def process_images_in_folder(folder_path):
#     # Loop over all files in the folder
#     for filename in os.listdir(folder_path):
#         # Get full file path
#         file_path = os.path.join(folder_path, filename)
        
#         # Try to load the image to check if it's valid (this will accept all valid image formats)
#         img = cv2.imread(file_path)
#         if img is not None:  # If the image was successfully loaded
#             print(f"Processing image: {filename}")
#             detect_and_save_sim(file_path)

# # Path to the current code folder (the folder where the script is located)
# current_folder = os.path.dirname(os.path.abspath(__file__))

# # Path to the 'images' folder inside the current code folder
# images_folder = os.path.join(current_folder, 'images')

# # Check if the 'images' folder exists
# if not os.path.exists(images_folder):
#     print(f"Error: The 'images' folder does not exist at {images_folder}.")
# else:
#     # Call the function to process all images in the 'images' folder
#     process_images_in_folder(images_folder)


# import cv2
# import os
# import numpy as np

# # Function to detect, remove, and replace the SIM part in an image
# def remove_and_replace_sim(image_path, sim_folder):
#     # Load the original image
#     img = cv2.imread(image_path)
    
#     # Check if the image was loaded successfully
#     if img is None:
#         print(f"Error: Could not read image {image_path}. Skipping.")
#         return
    
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply thresholding to highlight the SIM part (adjust as needed)
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours of the objects in the image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the filename without the extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Load the replacement SIM part from the same folder (with "_sim" appended)
#     replacement_sim_path = os.path.join(sim_folder, f'{name}_sim.png')
#     replacement_sim = cv2.imread(replacement_sim_path)

#     if replacement_sim is None:
#         print(f"Error: Could not find replacement SIM image {replacement_sim_path}. Skipping.")
#         return

#     # Loop over contours to find the SIM card and replace it
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter by size or aspect ratio to detect the correct SIM card
#         if w > 100 and h > 50:  # Adjust size threshold as needed
#             # Remove the SIM part by filling it with a background color (e.g., white)
#             img[y:y+h, x:x+w] = (255, 255, 255)  # Replace with white background

#             # Resize the replacement SIM part to fit the detected region
#             resized_sim = cv2.resize(replacement_sim, (w, h))

#             # Place the resized replacement SIM part in the same position
#             img[y:y+h, x:x+w] = resized_sim
            
#             print(f"Replaced SIM part in image: {filename}")
#             break

#     # Save the modified image (you can overwrite the original or save as new)
#     output_path = os.path.join(sim_folder, f'{name}_updated.png')
#     cv2.imwrite(output_path, img)
#     print(f"Saved updated image as: {output_path}")

# # Function to process all images in a folder
# def process_images_in_folder(folder_path):
#     # Loop over all files in the folder
#     for filename in os.listdir(folder_path):
#         # Get full file path
#         file_path = os.path.join(folder_path, filename)

#         # Try to load the image to check if it's valid (this will accept all valid image formats)
#         img = cv2.imread(file_path)
#         if img is not None:  # If the image was successfully loaded
#             print(f"Processing image: {filename}")
#             remove_and_replace_sim(file_path, folder_path)

# # Path to the current code folder (the folder where the script is located)
# current_folder = os.path.dirname(os.path.abspath(__file__))

# # Path to the 'images' folder inside the current code folder
# images_folder = os.path.join(current_folder, 'images')

# # Check if the 'images' folder exists
# if not os.path.exists(images_folder):
#     print(f"Error: The 'images' folder does not exist at {images_folder}.")
# else:
#     # Call the function to process all images in the 'images' folder
#     process_images_in_folder(images_folder)



# import cv2
# import os
# import numpy as np

# # Function to detect, remove, and replace the SIM part in an image
# def remove_and_replace_sim(image_path, sim_folder, updated_folder):
#     # Load the original image
#     img = cv2.imread(image_path)
    
#     # Check if the image was loaded successfully
#     if img is None:
#         print(f"Error: Could not read image {image_path}. Skipping.")
#         return
    
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply thresholding to highlight the SIM part (adjust as needed)
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours of the objects in the image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the filename without the extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Load the replacement SIM part from the same folder (with "_sim" appended)
#     replacement_sim_path = os.path.join(sim_folder, f'{name}_sim.png')
#     replacement_sim = cv2.imread(replacement_sim_path)

#     if replacement_sim is None:
#         print(f"Error: Could not find replacement SIM image {replacement_sim_path}. Skipping.")
#         return

#     # Loop over contours to find the SIM card and replace it
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter by size or aspect ratio to detect the correct SIM card
#         if w > 100 and h > 50:  # Adjust size threshold as needed
#             # Remove the SIM part by filling it with a background color (e.g., white)
#             img[y:y+h, x:x+w] = (255, 255, 255)  # Replace with white background

#             # Resize the replacement SIM part to fit the detected region
#             resized_sim = cv2.resize(replacement_sim, (w, h))

#             # Place the resized replacement SIM part in the same position
#             img[y:y+h, x:x+w] = resized_sim
            
#             print(f"Replaced SIM part in image: {filename}")
#             break

#     # Save the modified image in the updated folder
#     output_path = os.path.join(updated_folder, f'{name}_updated.png')
#     cv2.imwrite(output_path, img)
#     print(f"Saved updated image as: {output_path}")

# # Function to process all images in a folder
# def process_images_in_folder(folder_path):
#     # Path to the 'images_updated' folder inside the same folder
#     updated_folder = os.path.join(folder_path, 'images_updated')
    
#     # Create 'images_updated' folder if it does not exist
#     if not os.path.exists(updated_folder):
#         os.makedirs(updated_folder)
    
#     # Loop over all files in the folder
#     for filename in os.listdir(folder_path):
#         # Get full file path
#         file_path = os.path.join(folder_path, filename)

#         # Try to load the image to check if it's valid (this will accept all valid image formats)
#         img = cv2.imread(file_path)
#         if img is not None:  # If the image was successfully loaded
#             print(f"Processing image: {filename}")
#             remove_and_replace_sim(file_path, folder_path, updated_folder)

# # Path to the current code folder (the folder where the script is located)
# current_folder = os.path.dirname(os.path.abspath(__file__))

# # Path to the 'images' folder inside the current code folder
# images_folder = os.path.join(current_folder, 'images')

# # Check if the 'images' folder exists
# if not os.path.exists(images_folder):
#     print(f"Error: The 'images' folder does not exist at {images_folder}.")
# else:
#     # Call the function to process all images in the 'images' folder
#     process_images_in_folder(images_folder)


# import cv2
# import os
# import numpy as np

# # Function to detect, remove, and replace the SIM part in an image
# def remove_and_replace_sim(image_path, sim_folder, updated_folder):
#     # Load the original image
#     img = cv2.imread(image_path)
    
#     # Check if the image was loaded successfully
#     if img is None:
#         print(f"Error: Could not read image {image_path}. Skipping.")
#         return
    
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Apply thresholding to highlight the SIM part (adjust as needed)
#     thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

#     # Find contours of the objects in the image
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Extract the filename without the extension
#     filename = os.path.basename(image_path)
#     name, _ = os.path.splitext(filename)

#     # Load the replacement SIM part from the 'images_sim' folder (with "_sim" appended)
#     replacement_sim_path = os.path.join(sim_folder, f'{name}_sim.png')
#     replacement_sim = cv2.imread(replacement_sim_path)

#     if replacement_sim is None:
#         print(f"Error: Could not find replacement SIM image {replacement_sim_path}. Skipping.")
#         return

#     # Loop over contours to find the SIM card and replace it
#     for contour in contours:
#         x, y, w, h = cv2.boundingRect(contour)
#         roi = img[y:y+h, x:x+w]
        
#         # Optional: Filter by size or aspect ratio to detect the correct SIM card
#         if w > 100 and h > 50:  # Adjust size threshold as needed
#             # Remove the SIM part by filling it with a background color (e.g., white)
#             img[y:y+h, x:x+w] = (255, 255, 255)  # Replace with white background

#             # Resize the replacement SIM part to fit the detected region
#             resized_sim = cv2.resize(replacement_sim, (w, h))

#             # Place the resized replacement SIM part in the same position
#             img[y:y+h, x:x+w] = resized_sim
            
#             print(f"Replaced SIM part in image: {filename}")
#             break

#     # Save the modified image in the updated folder
#     output_path = os.path.join(updated_folder, f'{name}_updated.png')
#     cv2.imwrite(output_path, img)
#     print(f"Saved updated image as: {output_path}")

# # Function to process all images in a folder
# def process_images_in_folder(folder_path):
#     # Path to the 'images_updated' folder inside the same folder
#     updated_folder = os.path.join(folder_path, 'images_updated')
    
#     # Path to the 'images_sim' folder (where SIM images are located)
#     sim_folder = os.path.join(folder_path, 'images_sim')
    
#     # Check if the 'images_sim' folder exists
#     if not os.path.exists(sim_folder):
#         print(f"Error: The 'images_sim' folder does not exist at {sim_folder}.")
#         return
    
#     # Create 'images_updated' folder if it does not exist
#     if not os.path.exists(updated_folder):
#         os.makedirs(updated_folder)
    
#     # Loop over all files in the folder
#     for filename in os.listdir(folder_path):
#         # Get full file path
#         file_path = os.path.join(folder_path, filename)

#         # Try to load the image to check if it's valid (this will accept all valid image formats)
#         img = cv2.imread(file_path)
#         if img is not None:  # If the image was successfully loaded
#             print(f"Processing image: {filename}")
#             remove_and_replace_sim(file_path, sim_folder, updated_folder)

# # Path to the current code folder (the folder where the script is located)
# current_folder = os.path.dirname(os.path.abspath(__file__))

# # Path to the 'images' folder inside the current code folder
# images_folder = os.path.join(current_folder, 'images')

# # Check if the 'images' folder exists
# if not os.path.exists(images_folder):
#     print(f"Error: The 'images' folder does not exist at {images_folder}.")
# else:
#     # Call the function to process all images in the 'images' folder
#     process_images_in_folder(images_folder)

