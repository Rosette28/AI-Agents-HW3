"""Text validation utilities."""
from collections import Counter

MIN_WORDS_COUNT = 150
COLLAPSE_THRESHOLD = 0.12


def is_invalid_text(text: str) -> bool:
    """Detect text that is too short or suffers from repetition loops."""
    words = text.split()

    if len(words) < MIN_WORDS_COUNT:
        return True

    # Detect concatenated repetition loops like "AgentsAgentsAgents..."
    if any(len(w) > 80 for w in words):
        return True

    freq = Counter(words)

    _top_word, count = freq.most_common(1)[0]

    return count > len(words) * COLLAPSE_THRESHOLD
