import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, 
    confusion_matrix, 
    classification_report
)
import seaborn as sns

class ClassificationDemo:
    def __init__(self):
        # Load dataset
        self.data = load_breast_cancer()
        self.X = self.data.data
        self.y = self.data.target
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        # Initialize classifiers
        self.classifiers = {
            'Logistic Regression': LogisticRegression(max_iter=1000),
            'Decision Tree': DecisionTreeClassifier(random_state=42),
            'Random Forest': RandomForestClassifier(random_state=42),
            'Support Vector Machine': SVC(probability=True, random_state=42)
        }
    
    def train_and_evaluate(self):
        """
        Train and evaluate multiple classifiers
        """
        results = {}
        
        for name, classifier in self.classifiers.items():
            # Train the classifier
            classifier.fit(self.X_train_scaled, self.y_train)
            
            # Predict
            y_pred = classifier.predict(self.X_test_scaled)
            
            # Evaluate
            results[name] = {
                'Accuracy': accuracy_score(self.y_test, y_pred),
                'Confusion Matrix': confusion_matrix(self.y_test, y_pred),
                'Classification Report': classification_report(self.y_test, y_pred)
            }
        
        return results
    
    def visualize_results(self, results):
        """
        Visualize classification results
        """
        # Accuracy Comparison
        plt.figure(figsize=(10, 6))
        accuracies = [results[clf]['Accuracy'] for clf in results]
        plt.bar(list(results.keys()), accuracies)
        plt.title('Classifier Accuracy Comparison')
        plt.xlabel('Classifiers')
        plt.ylabel('Accuracy')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_feature_importance(self):
        """
        Plot feature importances for Random Forest
        """
        rf_classifier = self.classifiers['Random Forest']
        feature_importance = rf_classifier.feature_importances_
        feature_names = self.data.feature_names
        
        plt.figure(figsize=(10, 6))
        indices = np.argsort(feature_importance)[::-1]
        plt.title("Top 10 Feature Importances")
        plt.bar(range(10), feature_importance[indices][:10])
        plt.xticks(range(10), [feature_names[i] for i in indices[:10]], rotation=45)
        plt.tight_layout()
        plt.show()