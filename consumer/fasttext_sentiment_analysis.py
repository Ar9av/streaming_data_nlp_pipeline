import pandas as pd
import fasttext
        
class FastTextSentiment():
    def __init__(self, model_file: str=None) -> None:
        self.model = fasttext.load_model(model_file)

    def score(self, text: str) -> int:
        labels, probabilities = self.model.predict(text, 1)
        pred = int(labels[0][-1])
        return labels, probabilities
