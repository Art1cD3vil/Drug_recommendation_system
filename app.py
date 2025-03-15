from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ensure this folder exists in your project directory
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Load the treatment plan data
treatments_df = pd.read_csv('brain_tumor_treatment_summary.csv')

# Load the TensorFlow model (.keras format)
model = load_model('brain_tumor_model.keras')  # Updated to .keras format

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        gene_sequence = request.form['gene_sequence']  # Additional input for gene sequence

        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Load and preprocess the image
            img = keras_image.load_img(filepath, target_size=(224, 224))  # Adjust target size based on your model
            img_array = keras_image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Model expects batch dimension

            # Predict tumor type
            predictions = model.predict(img_array)
            predicted_tumor_type = "type_here_based_on_predictions"  # Replace with actual logic to get tumor type from predictions

            # Retrieve treatment information from the DataFrame
            treatment_info = treatments_df[treatments_df['Tumor Type'] == predicted_tumor_type].iloc[0]

            return render_template('results.html', treatment=treatment_info, gene_sequence=gene_sequence, tumor_type=predicted_tumor_type)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)