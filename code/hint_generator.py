import pandas as pd

class HintGenerator:
    def __init__(self, compound_words):
        self.compound_words = compound_words
    
    def get_hints(self, word, limit=5):
        """Get common word combinations for a given word"""
        # Find compounds where the word appears as first or second word
        hints_first = self.compound_words[self.compound_words['word1'] == word]
        hints_second = self.compound_words[self.compound_words['word2'] == word]
        
        # Combine and sort by frequency
        all_hints = pd.concat([hints_first, hints_second])
        
        # Simple frequency mapping
        frequency_map = {'high': 3, 'medium': 2, 'low': 1}
        all_hints['freq_score'] = all_hints['frequency'].map(frequency_map)
        all_hints = all_hints.sort_values('freq_score', ascending=False)
        
        return all_hints.head(limit)[['word1', 'word2', 'combined']].to_dict('records')
    
    def get_common_compounds(self, word_type=None, limit=10):
        """Get frequently used compounds"""
        frequency_map = {'high': 3, 'medium': 2, 'low': 1}
        compounds = self.compound_words.copy()
        compounds['freq_score'] = compounds['frequency'].map(frequency_map)
        
        return compounds.sort_values('freq_score', ascending=False).head(limit)