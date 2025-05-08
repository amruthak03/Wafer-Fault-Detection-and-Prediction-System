# Wafer-Fault-Detection-and-Prediction-System

This project implements a robust machine-learning pipeline for detecting faults in semiconductor wafers using sensor data. It features an end-to-end workflow including data ingestion, validation, preprocessing, transformation, model training, evaluation, and deployment. The final model is served via a Flask web application with a user-friendly interface that allows real-time predictions on uploaded sensor data files.

### Project Objective
In semiconductor manufacturing, early detection of faulty wafers can significantly reduce rework costs and improve yield. This system classifies wafers based on historical sensor readings to predict whether a wafer is faulty or not, enabling preemptive action in industrial settings.

### Features
- Modular ML Pipeline: Includes modules for ingestion, validation, transformation, training, and prediction.
- Automated Data Validation: Schema checks, null/missing value handling, and data drift detection.
- Model Selection: Automatically selects the best-performing algorithm based on evaluation metrics.
- Interactive Web Interface: Upload CSV files and receive instant predictions using a Flask app.
- SQLite Integration: Logs model predictions and feedback for future retraining.

### Technologies Used
- Python
- Flask
- SQLite
- scikit-learn, Pandas, NumPy
- HTML/CSS

### Model Performance
- Training Accuracy: 92.5%
- Validation Accuracy: ~91%
- Algorithms evaluated: Random Forest, XGBoost, SVM, Logistic Regression
- Final model selected based on cross-validation and performance metrics

### Future Improvements
- Dockerize the application for containerized deployment
- Integrate with cloud storage for scalable data ingestion
- Deploy via RESTful API (FastAPI or Flask-RESTful)
