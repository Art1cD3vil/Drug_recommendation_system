import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np

class TumorClassifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tumor Classifier")
        
        # Load model
        self.model = tf.keras.models.load_model("brain_tumor_model.keras")
        
        # Define classes
        self.class_dict = {
            "glioma": 0,
            "Banana": 1,
            "apple": 2,
            # Add your classes here
        }
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        # Button to load image
        self.load_btn = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=10)
        
        # Image display
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)
    
    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            # Display image
            img = Image.open(file_path)
            img = img.resize((299, 299))  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk
            
            # Make prediction
            result = self.predict_tumor(file_path)
            self.result_label.configure(
                text=f"Tumor Type: {result['tumor_type']}\nConfidence: {result['confidence']:.2f}"
            )
    
    def predict_tumor(self, img_path):
        # Load and preprocess the image
        img = Image.open(img_path)
        resized_img = img.resize((299, 299))
        img_array = np.asarray(resized_img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Make prediction
        predictions = self.model.predict(img_array)
        probs = predictions[0]
        
        # Get the predicted class
        max_prob_index = np.argmax(probs)
        labels = list(self.class_dict.keys())
        tumor_type = labels[max_prob_index]
        confidence = probs[max_prob_index]
        
        return {
            "tumor_type": tumor_type,
            "confidence": float(confidence)
        }

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TumorClassifierApp(root)
    root.mainloop()