
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the given text.
    Returns: "Positive", "Neutral", or "Negative"

    How VADER works:
    - It gives a 'compound' score between -1.0 and +1.0
    - Above +0.05  → Positive
    - Below -0.05  → Negative
    - In between   → Neutral
    """
    sia = SentimentIntensityAnalyzer()

    scores = sia.polarity_scores(text)

    compound = scores['compound']

    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

URGENCY_KEYWORDS = [
    # Emergency / Time-sensitive words
    "urgent", "urgently", "emergency", "asap", "immediately", "right now",
    "as soon as possible",

    # Financial / Security threats
    "fraud", "scam", "theft", "stolen", "hack", "hacked", "unauthorized",
    "suspicious", "blocked", "account blocked",

    # System / Service failures
    "not working", "broken", "crashed", "failed", "failure", "error",
    "cannot access", "can't access", "unable to", "stopped working",

    # Delays and deadlines
    "delay", "delayed", "overdue", "pending since", "no response",
    "waiting for days", "waiting for weeks", "still not resolved",

    # Safety and severity
    "critical", "serious", "severe", "dangerous", "life", "health",
    "safety", "risk", "threat",

    # Escalation language
    "escalate", "manager", "lawsuit", "legal action", "complaint",
    "consumer forum", "police"
]


def detect_urgency(text):
    """
    Checks if the complaint contains any urgency keywords.
    Returns: "High" or "Low"
    """
    text_lower = text.lower()

    for keyword in URGENCY_KEYWORDS:
        if keyword in text_lower:
            return "High"  # Found an urgency keyword → High urgency

    return "Low"  # No urgency keywords found → Low urgency

def determine_priority(sentiment, urgency):
    """
    Combines sentiment and urgency to give a final priority level.

    Priority Matrix:
    ┌──────────────┬──────────────┬──────────────┐
    │              │  High Urgency│  Low Urgency │
    ├──────────────┼──────────────┼──────────────┤
    │   Negative   │   CRITICAL   │    MEDIUM    │
    │   Neutral    │    HIGH      │     LOW      │
    │   Positive   │    HIGH      │     LOW      │
    └──────────────┴──────────────┴──────────────┘

    Returns: "Critical", "High", "Medium", or "Low"
    """
    if sentiment == "Negative" and urgency == "High":
        return "Critical"   # Worst case: angry AND urgent
    elif urgency == "High":
        return "High"       # Urgent but not necessarily angry
    elif sentiment == "Negative":
        return "Medium"     # Negative tone but not time-sensitive
    else:
        return "Low"        # Positive/Neutral and not urgent

def analyze_complaint(title, description):
    """
    Takes the complaint title and description,
    runs all three analyses, and returns results as a dictionary.

    Usage:
        result = analyze_complaint("My internet is down", "It has been broken for 3 days, urgent fix needed!")
        print(result)
        # Output: {'sentiment': 'Negative', 'urgency': 'High', 'priority': 'Critical'}
    """
   
    full_text = f"{title} {description}"

   
    sentiment = analyze_sentiment(full_text)
    urgency = detect_urgency(full_text)
    priority = determine_priority(sentiment, urgency)

    return {
        "sentiment": sentiment,
        "urgency": urgency,
        "priority": priority
    }
