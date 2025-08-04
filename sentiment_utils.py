from transformers import pipeline

# Load once globally
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiments(segments):
    """
    segments: List of dicts with keys 'start', 'end', 'text'
    Returns: List with same dicts + sentiment label and score
    """
    results = []
    for segment in segments:
        text = segment['text']
        analysis = sentiment_pipeline(text[:512])[0]  # truncate to max length
        results.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": text,
            "sentiment": analysis["label"],
            "score": analysis["score"]
        })
    return results
