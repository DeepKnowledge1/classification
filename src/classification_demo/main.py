from classification_demo.classifier import ClassificationDemo

def main():
    # Create demo instance
    demo = ClassificationDemo()
    
    # Train and evaluate
    results = demo.train_and_evaluate()
    
    # Print detailed results
    for name, metrics in results.items():
        print(f"\n{name} Results:")
        print(f"Accuracy: {metrics['Accuracy']:.2%}")
        print("Classification Report:")
        print(metrics['Classification Report'])
    
    # Visualize results
    demo.visualize_results(results)
    demo.plot_feature_importance()

if __name__ == "__main__":
    main()