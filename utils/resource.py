def recommend_resources(severity_score, population_affected=1000):
    base = {
        'Water (litres)': 5,
        'Food Kits': 1,
        'Medical Units': 0.01,
        'Tents': 0.2,
        'Rescue Teams': 0.005
    }
    severity_factor = 1 if severity_score < 30 else 1.5 if severity_score < 70 else 2.5
    return {resource: int(population_affected * qty * severity_factor) for resource, qty in base.items()}
