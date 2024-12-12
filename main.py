

from classification.classifier import ClassificationDemo

def main():
    # Demonstrate the usage of the ClassificationDemo
    demo = ClassificationDemo()
    model, results = demo.train_and_evaluate()
    
    print("Classification Results:")
    print(f"Accuracy: {results['Accuracy']}")
    print(f"ROC AUC: {results['ROC AUC']}")
    
    demo.visualize_results(results)
    demo.plot_feature_importance(model)

if __name__ == '__main__':
    main()
    # modifying the brach