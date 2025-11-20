import pandas as pd

class FuzzyMatcher:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.words_list = dictionary['word'].tolist()
    
    def simple_similarity(self, word1, word2):
        """Simple similarity measure for Kannada words"""
        # Basic implementation - in practice, use a proper library
        # For now, we'll use a simple character overlap
        set1 = set(word1)
        set2 = set(word2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
    
    def get_suggestions(self, word, limit=3):
        """Get similar words using simple similarity"""
        similarities = []
        
        for dict_word in self.words_list:
            similarity = self.simple_similarity(word, dict_word)
            similarities.append((dict_word, similarity))
        
        # Sort by similarity (descending) and get top matches
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and return
        return [word for word, sim in similarities[:limit] if sim > 0.3]

# Alternative: Install fuzzywuzzy for better matching
"""
# Uncomment this if you install fuzzywuzzy
# pip install fuzzywuzzy python-Levenshtein

from fuzzywuzzy import process

class AdvancedFuzzyMatcher(FuzzyMatcher):
    def get_suggestions(self, word, limit=3):
        \"\"\"Get fuzzy matches using fuzzywuzzy\"\"\"
        matches = process.extract(word, self.words_list, limit=limit)
        return [match[0] for match in matches if match[1] > 70]
"""