"""Random Forest Prediction Script for Smart Fish Aquaculture System.

This script loads the trained Random Forest model and exposes helper
functions to predict the aquaculture environment status (Optimal / Non-Optimal)
based on sensor input values.

Feature order (must match training order):
    [air_quality, temperature, turbidity, tds, ph, nh3, do]
"""

import joblib
import numpy as np
import os


# Resolve model path relative to this script:
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(CURRENT_DIR, "..", "models")
MODEL_PATH = os.path.join(MODELS_DIR, "random_forest_model.joblib")

# Load the trained Random Forest model
model = joblib.load(MODEL_PATH)


def predict_status_rf(air_quality, temperature, turbidity, tds, ph, nh3, do):
    """Return 'Optimal' or 'Non-Optimal' for given sensor readings.

    Parameters
    ----------
    air_quality : float
        Air quality in ppm (MQ135).
    temperature : float
        Water temperature in °C.
    turbidity : float
        Turbidity (NTU).
    tds : float
        Total Dissolved Solids (ppm).
    ph : float
        pH value of the water (0–14).
    nh3 : float
        Ammonia concentration (mg/L).
    do : float
        Dissolved oxygen (mg/L).

    Returns
    -------
    str
        'Optimal' if prediction == 1 else 'Non-Optimal'.
    """
    sample = np.array([[air_quality, temperature, turbidity, tds, ph, nh3, do]])
    prediction = model.predict(sample)[0]

    return "Optimal" if prediction == 1 else "Non-Optimal"


if __name__ == "__main__":
    # Example usage with dummy values.
    example_air_quality = 120.0
    example_temperature = 29.0
    example_turbidity = 45.0
    example_tds = 250.0
    example_ph = 7.4
    example_nh3 = 0.5
    example_do = 6.0

    status = predict_status_rf(
        example_air_quality,
        example_temperature,
        example_turbidity,
        example_tds,
        example_ph,
        example_nh3,
        example_do,
    )

    print("Input sample:")
    print(f"  Air Quality (ppm): {example_air_quality}")
    print(f"  Temperature (°C): {example_temperature}")
    print(f"  Turbidity (NTU): {example_turbidity}")
    print(f"  TDS (ppm): {example_tds}")
    print(f"  pH: {example_ph}")
    print(f"  NH3 (mg/L): {example_nh3}")
    print(f"  DO (mg/L): {example_do}")
    print("\nPredicted Aquaculture Environment Status:", status)
