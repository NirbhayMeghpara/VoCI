import pandas as pd
from transformers import pipeline
from rake_nltk import Rake
from collections import defaultdict, Counter

classifier = pipeline("sentiment-analysis")
rake = Rake()

def map_label(label, score, threshold=0.92):
    return label if score >= threshold else "NEUTRAL"

def analyze_reviews_file(file):
    df = pd.read_csv(file)
    required_columns = {'product_id', 'product_name', 'review_text'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"CSV must contain: {required_columns}")

    results = []
    phrase_summary = defaultdict(lambda: defaultdict(Counter))

    for _, row in df.iterrows():
        review_text = row['review_text']
        product_name = row['product_name']

        sentiment = classifier(review_text)[0]
        mapped_label = map_label(sentiment['label'], sentiment['score'])

        rake.extract_keywords_from_text(review_text)
        phrases = rake.get_ranked_phrases()[:5]

        results.append({
            "product_id": row['product_id'],
            "product_name": product_name,
            "review_text": review_text,
            "sentiment_label": mapped_label,
            "sentiment_score": round(sentiment['score'], 4),
            "key_phrases": phrases
        })

        for phrase in phrases:
            phrase_summary[product_name][phrase][mapped_label] += 1

    return {
        "message": "Analysis and aggregation complete",
        "total_reviews": len(results),
        "sample_results": results[:5],
        "aggregated_insights": phrase_summary
    }
