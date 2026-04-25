# rules.py

def supplement_advice(pred):
    s = []

    if pred[0]: s.append("Iron tablets")
    if pred[1]: s.append("Vitamin B12 capsules")
    if pred[2]: s.append("Vitamin D supplements")
    if pred[3]: s.append("Calcium supplements")
    if pred[4]: s.append("Protein supplements")

    return s


def diet_advice(data, pred):
    d = []

    if pred[0]:
        if data['diet_type'] == 0:
            d.append("Spinach, beetroot, jaggery")
        else:
            d.append("Chicken, liver, eggs")

    if pred[1]:
        if data['diet_type'] == 0:
            d.append("Milk, paneer")
        else:
            d.append("Fish, meat")

    if pred[2]:
        d.append("Sunlight exposure + dairy")

    return d


def menstrual_diet(data):
    m = []

    if data['gender'] == 1:
        if data['cycle_phase'] == 0:
            m.append("Warm soups, iron-rich foods")
        elif data['cycle_phase'] == 3:
            m.append("Reduce sugar, eat nuts & bananas")

    return m


def warning_engine(data, pred):
    w = []

    if data['cholesterol'] > 200:
        w.append("Avoid oily food")

    if pred[6]:
        w.append("Heart risk detected")

    if pred[5]:
        w.append("Monitor blood sugar")

    if data['gender'] == 1 and data['heavy_bleeding'] == 1:
        w.append("Heavy bleeding detected")

    return w