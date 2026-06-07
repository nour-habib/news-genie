from models import Article

# Credibility scores: 0-100 (higher = more trustworthy)
TRUSTED_SOURCES = {
    # Major News Agencies
    "Reuters": 98,
    "Associated Press": 98,
    "BBC": 95,
    "Agence France-Presse": 95,

    # Major US Publications
    "The New York Times": 95,
    "The Washington Post": 94,
    "The Wall Street Journal": 93,
    "NPR": 92,
    "The Guardian": 92,
    "CNN": 85,
    "NBC News": 85,
    "ABC News": 85,
    "CBS News": 85,

    # Major International Publications
    "The Telegraph": 90,
    "The Times": 90,
    "The Independent": 88,
    "The Economist": 92,
    "Financial Times": 92,
    "The Japan Times": 90,
    "The Sydney Morning Herald": 88,

    # Tech & Business
    "TechCrunch": 85,
    "The Verge": 85,
    "CNBC": 88,
    "Bloomberg": 92,
    "Business Insider": 80,

    # Sports
    "ESPN": 85,
    "Sports Illustrated": 82,
}


def validate_source(article: Article) -> dict:
    """
    Validate the credibility of a news source.
    Returns a dict with credibility score and trust level.
    """
    source_name = article.source

    # Check if source is in trusted list
    credibility_score = TRUSTED_SOURCES.get(source_name)

    if credibility_score is None:
        # Unknown source
        trust_level = "unverified"
        credibility_score = 50
    elif credibility_score >= 90:
        trust_level = "highly trusted"
    elif credibility_score >= 80:
        trust_level = "trusted"
    else:
        trust_level = "moderately trusted"

    return {
        "source": source_name,
        "credibility_score": credibility_score,
        "trust_level": trust_level
    }


def get_source_rating(article: Article) -> str:
    """Returns a simple trust rating label."""
    validation = validate_source(article)
    return validation["trust_level"]
