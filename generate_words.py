import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import pandas as pd
from collections import defaultdict
import logging

class KannadaWordExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Common word patterns for classification
        self.noun_indicators = ['ವಾದ', 'ತ್ವ', 'ಕಾರ', 'ಗಾರ', 'ಅಣು', 'ಆನ', 'ವಂತ']
        self.verb_indicators = ['ಇಸು', 'ಅಡು', 'ಆಡು', 'ಓಡು', 'ಏರು', 'ಇಳಿ']
        self.adjective_indicators = ['ಇಯ', 'ಆದ', 'ಊನ', 'ಒತ್ತ', 'ಅಲ್ಲ']
        self.prefix_indicators = ['ಮಹಾ', 'ಸು', 'ದು', 'ಅ', 'ಪ್ರ', 'ಉಪ', 'ಅನು', 'ಸಂ', 'ವಿ', 'ಅಭಿ']
        
        self.vowels = ['ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ', 'ಎ', 'ಏ', 'ಐ', 'ಒ', 'ಓ', 'ಔ']
        self.combining_endings = ['ಕ', 'ಗ', 'ಡ', 'ಣ', 'ತ', 'ದ', 'ನ', 'ಪ', 'ಬ', 'ಮ', 'ಯ', 'ರ', 'ಲ', 'ವ']

    def get_kannada_wikipedia_pages(self, num_pages=50):
        """Get list of Kannada Wikipedia pages"""
        base_url = "https://kn.wikipedia.org/w/api.php"
        
        pages = []
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'random',
            'rnnamespace': 0,
            'rnlimit': num_pages
        }
        
        try:
            response = self.session.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            for page in data['query']['random']:
                pages.append({
                    'title': page['title'],
                    'pageid': page['id']
                })
            
            self.logger.info(f"Retrieved {len(pages)} random Wikipedia pages")
            return pages
            
        except Exception as e:
            self.logger.error(f"Error fetching Wikipedia pages: {e}")
            return []

    def extract_kannada_words_from_page(self, page_title):
     try:
          url = f"https://kn.wikipedia.org/wiki/{page_title}"
          response = self.session.get(url)
          soup = BeautifulSoup(response.text, "html.parser")
          
          text = soup.get_text(separator=" ")
          
          kannada_pattern = re.compile(r"[ಀ-೿]+")
          number_pattern = re.compile(r"^[೦-೯]+$")
          words = kannada_pattern.findall(text)

          filtered = [
                w for w in words
                if len(w) >= 2 and not number_pattern.fullmatch(w)
            ]
          return list(set(filtered))

     except Exception as e:
          self.logger.error(f"Error: {e}")
          return []

               
     except Exception as e:
          self.logger.error(f"Error extracting words from {page_title}: {e}")
          return []

    def get_english_meaning(self, word):
    # Common dictionary first
     common_words = {
        'ಮಹಾ': 'great',
        'ಮನೆ': 'house',
        'ಆತ್ಮ': 'soul',
        'ಪುಸ್ತಕ': 'book',
        'ನದಿ': 'river',
        'ರಾಜ': 'king',
        'ನಗರ': 'city',
        'ವಿಜ್ಞಾನ': 'science',
        'ಇತಿಹಾಸ': 'history'
     }

     if word in common_words:
        return common_words[word]

    # Google unofficial translate
     try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "kn",
            "tl": "en",
            "dt": "t",
            "q": word
        }
        response = requests.get(url, params=params)
        result = response.json()
        return result[0][0][0]
     except:
        return "Meaning not found"


    def determine_word_type(self, kannada_word):
        """Determine the type of word (noun, verb, adjective, etc.)"""
        # Check for common suffixes and patterns
        if any(kannada_word.endswith(indicator) for indicator in self.noun_indicators):
            return 'noun'
        elif any(kannada_word.endswith(indicator) for indicator in self.verb_indicators):
            return 'verb'
        elif any(kannada_word.endswith(indicator) for indicator in self.adjective_indicators):
            return 'adjective'
        elif any(kannada_word.startswith(indicator) for indicator in self.prefix_indicators):
            return 'prefix'
        else:
            # Default to noun for most Kannada words from Wikipedia
            return 'noun'

    def get_last_sound(self, kannada_word):
        """Extract the last sound of a Kannada word"""
        if not kannada_word:
            return 'ಅ'
        
        last_char = kannada_word[-1]
        
        # If it ends with a vowel
        if last_char in self.vowels:
            return last_char
        
        # For consonants, return the consonant
        return last_char

    def can_combine(self, kannada_word, word_type):
        """Determine if word can combine with others"""
        if word_type == 'prefix':
            return 'yes'
        
        # Words ending with vowels can usually combine
        if kannada_word[-1] in self.vowels:
            return 'yes'
        
        # Some common combining patterns
        if kannada_word[-1] in self.combining_endings:
            return 'yes'
        
        return 'no'

    def process_words(self, num_pages=20, delay=1):
        """Main function to process words from Wikipedia"""
        all_words_data = []
        
        # Get Wikipedia pages
        pages = self.get_kannada_wikipedia_pages(num_pages)
        
        for i, page in enumerate(pages):
            self.logger.info(f"Processing page {i+1}/{len(pages)}: {page['title']}")
            
            # Extract words from page
            words = self.extract_kannada_words_from_page(page['title'])
            
            for word in words[:10]:  # Process first 10 words from each page to avoid duplicates
                try:
                    # Get English meaning
                    meaning = self.get_english_meaning(word)
                    
                    # Determine word type
                    word_type = self.determine_word_type(word)
                    
                    # Get last sound
                    last_sound = self.get_last_sound(word)
                    
                    # Determine if can combine
                    combinable = self.can_combine(word, word_type)
                    
                    word_data = {
                        'word': word,
                        'meaning': meaning,
                        'word_type': word_type,
                        'last_sound': last_sound,
                        'can_combine': combinable
                    }
                    
                    all_words_data.append(word_data)
                    self.logger.info(f"Processed: {word} -> {meaning}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing word {word}: {e}")
                    continue
            
            # Be respectful to the server
            time.sleep(delay)
        
        return all_words_data

    def save_to_csv(self, words_data, filename):
        """Save processed words to CSV file"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['word', 'meaning', 'word_type', 'last_sound', 'can_combine'])
            writer.writeheader()
            writer.writerows(words_data)
        
        self.logger.info(f"Saved {len(words_data)} words to {filename}")

    def enhance_with_predefined_words(self, words_data):
        """Add predefined common words to enhance the dataset"""
        predefined_words = [
            {'word': 'ಮಹಾ', 'meaning': 'great', 'word_type': 'prefix', 'last_sound': 'ಆ', 'can_combine': 'yes'},
            {'word': 'ಮನೆ', 'meaning': 'house', 'word_type': 'noun', 'last_sound': 'ಎ', 'can_combine': 'yes'},
            {'word': 'ಆತ್ಮ', 'meaning': 'soul', 'word_type': 'noun', 'last_sound': 'ಆ', 'can_combine': 'yes'},
            {'word': 'ಪುಸ್ತಕ', 'meaning': 'book', 'word_type': 'noun', 'last_sound': 'ಕ', 'can_combine': 'yes'},
            {'word': 'ರಾಜ', 'meaning': 'king', 'word_type': 'noun', 'last_sound': 'ಅ', 'can_combine': 'yes'},
            {'word': 'ನಗರ', 'meaning': 'city', 'word_type': 'noun', 'last_sound': 'ಅ', 'can_combine': 'yes'},
            {'word': 'ಗುರು', 'meaning': 'teacher', 'word_type': 'noun', 'last_sound': 'ಉ', 'can_combine': 'yes'},
            {'word': 'ಭಾಷೆ', 'meaning': 'language', 'word_type': 'noun', 'last_sound': 'ಎ', 'can_combine': 'yes'},
            {'word': 'ನದಿ', 'meaning': 'river', 'word_type': 'noun', 'last_sound': 'ಇ', 'can_combine': 'yes'},
            {'word': 'ಉದಯ', 'meaning': 'rise', 'word_type': 'noun', 'last_sound': 'ಅ', 'can_combine': 'yes'},
        ]
        
        # Remove duplicates
        existing_words = {word['word'] for word in words_data}
        for word in predefined_words:
            if word['word'] not in existing_words:
                words_data.append(word)
        
        return words_data

def main():
    extractor = KannadaWordExtractor()

    print("Starting Kannada word extraction from Wikipedia...")

    # --------------------------------------------
    # 1️⃣ LOAD EXISTING WORDS IF FILE EXISTS
    # --------------------------------------------
    existing_file = "kannada_words_wikipedia.csv"
    existing_words = []

    try:
        df = pd.read_csv(existing_file)
        for _, row in df.iterrows():
            existing_words.append({
                "word": row["word"],
                "meaning": row["meaning"],
                "word_type": row["word_type"],
                "last_sound": row["last_sound"],
                "can_combine": row["can_combine"]
            })
        print(f"Loaded {len(existing_words)} existing words.")
    except FileNotFoundError:
        print("No existing CSV found. Starting fresh...")

    # --------------------------------------------
    # 2️⃣ SCRAPE NEW WORDS
    # --------------------------------------------
    new_words_data = extractor.process_words(num_pages=1000, delay=1.5)

    # Add predefined common words
    new_words_data = extractor.enhance_with_predefined_words(new_words_data)

    print(f"New words extracted: {len(new_words_data)}")

    # --------------------------------------------
    # 3️⃣ MERGE OLD + NEW WORDS
    # --------------------------------------------
    combined = existing_words + new_words_data

    # --------------------------------------------
    # 4️⃣ REMOVE DUPLICATES
    # --------------------------------------------
    unique = []
    seen = set()

    for w in combined:
        if w["word"] not in seen:
            unique.append(w)
            seen.add(w["word"])

    print(f"Total unique words: {len(unique)}")

    # --------------------------------------------
    # 5️⃣ SAVE UPDATED FILE
    # --------------------------------------------
    extractor.save_to_csv(unique, existing_file)

    # --------------------------------------------
    # 6️⃣ PRINT SAMPLE
    # --------------------------------------------
    print("\nSample of extracted words:")
    print("=" * 80)

    for i, word in enumerate(unique[:20]):
        print(
            f"{i+1:2d}. {word['word']:15} - {word['meaning']:25} "
            f"({word['word_type']:8}) Last: {word['last_sound']:2} Combine: {word['can_combine']}"
        )

    print("\n🎉 Updated words saved successfully!")


if __name__ == "__main__":
    main()