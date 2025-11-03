from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EmotionalIntelligenceEngine:
    def __init__(self):
        self.sentimentanalyzer = SentimentIntensityAnalyzer()
        self.emotionpatterns = {
            "anxiety": {"keywords": ["worried", "anxious", "scared", "panic", "nervous", "fear", "stress"]},
            "depression": {"keywords": ["sad", "hopeless", "empty", "worthless", "tired", "meaningless"]},
            "anger": {"keywords": ["angry", "frustrated", "furious", "annoyed", "irritated", "rage"]},
            "grief": {"keywords": ["loss", "died", "miss", "gone", "funeral", "bereaved"]},
            "trauma": {"keywords": ["flashback", "nightmare", "triggered", "ptsd", "abuse", "accident"]},
            "relationships": {"keywords": ["relationship", "partner", "marriage", "divorce", "breakup", "lonely"]}
        }
        self.cognitivedistortions = {
            "allornothing": ["always", "never", "completely", "totally", "everything", "nothing"],
            "catastrophizing": ["disaster", "terrible", "awful", "end of world", "ruined"],
            "mindreading": ["they think", "everyone believes", "people assume"],
            "fortunetelling": ["will never", "going to fail", "won't work", "bound to"],
            "emotionalreasoning": ["feel like", "seems like", "must be because I feel"],
            "shouldstatements": ["should", "must", "ought to", "have to"],
            "labeling": ["I am", "he is", "she is", "stupid", "failure", "loser", "worthless"],
            "personalization": ["my fault", "because of me", "I caused", "I'm responsible"]
        }

    def analyzeemotionalstate(self, text):
        textlower = text.lower()
        sentimentscores = self.sentimentanalyzer.polarity_scores(text)
        detectedemotions = [e for e, p in self.emotionpatterns.items() if any(k in textlower for k in p["keywords"])]
        detecteddistortions = [d for d, p in self.cognitivedistortions.items() if any(k in textlower for k in p)]
        crisiskeywords = ["suicide", "kill myself", "end it all", "want to die", "hurt myself", "self harm"]
        crisislevel = "high" if any(k in textlower for k in crisiskeywords) else "low"
        return {
            "primaryemotions": detectedemotions[:2],
            "sentiment": sentimentscores,
            "cognitivedistortions": detecteddistortions,
            "crisislevel": crisislevel}