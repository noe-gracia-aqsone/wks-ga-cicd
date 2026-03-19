import gradio as gr
import numpy as np
import skops.io as sio

# Get the list of ALL types found in the file
all_untrusted_types = sio.get_untrusted_types(file="./model/drug_pipeline.skops")

# Print and review the list (e.g., ['numpy.dtype', 'sklearn.pipeline.Pipeline', ...])
# print(all_untrusted_types)

# Load the model, passing the complete list as the trusted argument
pipe = sio.load(
    "./model/drug_pipeline.skops", 
    trusted=all_untrusted_types
)

def predict_drug(age, sex, blood_pressure, cholesterol, na_to_k_ratio):
    """Predict drugs based on patient features.

    Args:
        age (int): Age of patient
        sex (str): Sex of patient 
        blood_pressure (str): Blood pressure level
        cholesterol (str): Cholesterol level
        na_to_k_ratio (float): Ratio of sodium to potassium in blood

    Returns:
        str: Predicted drug label
    """
    features = np.array(
        [[age, sex, blood_pressure, cholesterol, na_to_k_ratio]],
        dtype=object,
    )
    try:
        probabilities = pipe.predict_proba(features)[0]
        return {
            str(label): float(prob)
            for label, prob in zip(pipe.classes_, probabilities)
        }
    except Exception:
        predicted_drug = pipe.predict(features)[0]
        return str(predicted_drug)


inputs = [
    gr.Slider(15, 74, step=1, label="Age"),
    gr.Radio(["M", "F"], label="Sex"),
    gr.Radio(["HIGH", "LOW", "NORMAL"], label="Blood Pressure"),
    gr.Radio(["HIGH", "NORMAL"], label="Cholesterol"),
    gr.Slider(6.2, 38.2, step=0.1, label="Na_to_K"),
]
outputs = gr.Label(num_top_classes=5)

examples = [
    [30, "M", "HIGH", "NORMAL", 15.4],
    [35, "F", "LOW", "NORMAL", 8],
    [50, "M", "HIGH", "HIGH", 34],
]


title = "Drug Classification"
description = "Enter the details to correctly identify Drug type?"
article = "Automate training, evaluation, and deployment of models to Hugging Face using GitHub Actions."


gr.Interface(
    fn=predict_drug,
    inputs=inputs,
    outputs=outputs,
    examples=examples,
    title=title,
    description=description,
    article=article,
    # theme=gr.themes.Soft(),
).launch()
