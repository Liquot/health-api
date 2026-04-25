import joblib
from rules import supplement_advice, diet_advice, menstrual_diet, warning_engine

# Load trained model
import joblib
import os

model = None

def load_model():
    global model
    if model is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "newmodel.pkl")
        model = joblib.load(model_path)
    return model


# ------------------ SUPPLEMENT ADVICE ------------------
def supplement_advice(pred):
    s = []

    if pred[0]: s.append("Iron tablets")
    if pred[1]: s.append("Vitamin B12")
    if pred[2]: s.append("Vitamin D3")
    if pred[3]: s.append("Calcium")
    if pred[4]: s.append("Protein supplements")

    return s


# ------------------ DIET ADVICE ------------------
def diet_advice(data, pred):
    d = []

    # Iron
    if pred[0]:
        if data['diet_type'] == 0:
            d.append("Spinach, beetroot, jaggery")
        else:
            d.append("Chicken, liver, eggs")

    # B12
    if pred[1]:
        if data['diet_type'] == 0:
            d.append("Milk, paneer")
        else:
            d.append("Fish, meat")

    # Vitamin D
    if pred[2]:
        d.append("Sunlight exposure + dairy")

    # Protein
    if pred[4]:
        if data['diet_type'] == 0:
            d.append("Dal, soy, tofu")
        else:
            d.append("Eggs, chicken")

    return d


# ------------------ MAIN FUNCTION ------------------
def get_recommendation(data):

    input_data = [[
        data['hemoglobin'], data['b12'], data['vitamin_d'], data['age'],
        data['calcium'], data['cholesterol'], data['protein'], data['diet_type'],
        data['genetic_iron_deficiency'], data['genetic_b12_deficiency'],
        data['genetic_vitd_deficiency'], data['family_diabetes'],
        data['family_heart_disease'], data['gender'], data['cycle_phase'],
        data['heavy_bleeding'], data['pcos_risk']
    ]]

    model = load_model()
    prediction = model.predict(input_data)

    pred = prediction[0]

    return {
        "values": data,
        "supplements": supplement_advice(pred),
        "diet": diet_advice(data, pred) + menstrual_diet(data),
        "warnings": warning_engine(data, pred)
    }