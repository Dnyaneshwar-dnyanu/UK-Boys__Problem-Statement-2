# ----------------------------------------
# STORAGE
# ----------------------------------------
vowels = {
    'ಅ','ಆ','ಇ','ಈ','ಉ','ಊ','ಋ','ಎ','ಏ','ಐ','ಒ','ಓ','ಔ'
}

kannada_consonants = {
    'ಕ','ಖ','ಗ','ಘ','ಙ',
    'ಚ','ಛ','ಜ','ಝ','ಞ',
    'ಟ','ಠ','ಡ','ಢ','ಣ',
    'ತ','ಥ','ದ','ಧ','ನ',
    'ಪ','ಫ','ಬ','ಭ','ಮ',
    'ಯ','ರ','ಲ','ವ',
    'ಶ','ಷ','ಸ','ಹ',
    'ಳ','ಕ್ಷ','ಜ್ಞ'
}

vowel_signs = {
    'ಾ': 'ಆ',
    'ಿ': 'ಇ',
    'ೀ': 'ಈ',
    'ು': 'ಉ',
    'ೂ': 'ಊ',
    'ೃ': 'ಋ',
    'ೆ': 'ಎ',
    'ೇ': 'ಏ',
    'ೈ': 'ಐ',
    'ೊ': 'ಒ',
    'ೋ': 'ಓ',
    'ೌ': 'ಔ'
}


# ----------------------------------------
# FUNCTION 1: LAST VOWEL OF WORD1
# ----------------------------------------
def get_last_vowel(word):
    last = word[-1]

    # case 1: ends with full vowel
    if last in vowels:
        return last

    # case 2: ends with vowel sign
    if last in vowel_signs:
        return vowel_signs[last]

    # case 3: ends with consonant → inherent vowel = ಅ
    return 'ಅ'



# ----------------------------------------
# FUNCTION 2: FIRST VOWEL OF WORD2
# ----------------------------------------

def get_first_vowel(word):

    if not word:
        return ""

    # CASE 1: Starts with vowel directly
    if word[0] in vowels:
        return word[0]

    # CASE 2: Starts with consonant + vowel sign
    if len(word) > 1 and word[1] in vowel_signs:
        return vowel_signs[word[1]]

    # CASE 3: Starts with consonant only → default inherent vowel "ಅ"
    return 'ಅ'

def get_vowel_sign(vowel):
    vowel_to_sign = {
        'ಅ': '',
        'ಆ': 'ಾ',
        'ಇ': 'ಿ',
        'ಈ': 'ೀ',
        'ಉ': 'ು',
        'ಊ': 'ೂ',
        'ಋ': 'ೃ',
        'ಎ': 'ೆ',
        'ಏ': 'ೇ',
        'ಐ': 'ೈ',
        'ಒ': 'ೊ',
        'ಓ': 'ೋ',
        'ಔ': 'ೌ'
    }

    return vowel_to_sign.get(vowel, '')

def remove_last_vowel_sound(word):
    last = word[-1]

    # 1️⃣ If word ends with vowel-sign (ಾ,ಿ,ೀ,ು,ೂ,ೆ,ೇ,ೈ,ೊ,ೋ,ೌ)
    if last in vowel_signs:
        return word[:-1]

    # 2️⃣ If word ends with standalone vowel (ಅ,ಆ,ಇ,ಈ,ಉ,ಊ,ಎ,ಏ...)
    # if last in vowels:
    #     return word[:-1]

    # 3️⃣ If ends with consonant → keep as it is
    return word


def remove_first_vowel(word):
    # Case 1: starts with a vowel (ಅ ಆ ಇ ಈ…)
    if word[0] in vowels:
        return word[1:]   # safe because vowel is always a single char

    # Case 2: starts with consonant + vowel sign
    if len(word) > 1 and word[1] in vowel_signs:
        return word[0] + word[2:]

    return word

# ----------------------------------------
# FUNCTION 3: APPLY YOUR SANDHI LOGIC HERE
# ----------------------------------------

def generate_possible_combinations(word1, word2, last_vowel, first_vowel):
    results = []   # store all possible outputs here

    # -----------------------------------------------
    # RULE 1: Transform first consonant (k → g, t → d, p → b)
    # -----------------------------------------------
    if len(word1) <= 1:
        results.append(word1 + word2)
        
    if word2[0] in ['ಕ', 'ತ', 'ಪ']:
        mapping = {'ಕ': 'ಗ', 'ತ': 'ದ', 'ಪ': 'ಬ'}
        new_first = mapping[word2[0]] + word2[1:]
        results.append(word1 + new_first)

    # -----------------------------------------------
    # RULE 2: last_vowel == ಅ / ಆ
    # -----------------------------------------------
    if last_vowel in ['ಅ', 'ಆ']:

        # CASE A: first vowel = ಅ / ಆ  → replace with ಆ
        if first_vowel in ['ಅ', 'ಆ']:
            new_word1 = remove_last_vowel_sound(word1) + 'ಾ'
            new_word = new_word1 + word2[1:]
            results.append(new_word)

        # CASE B: first vowel = ಇ / ಈ → replace with ಈ
        if first_vowel in ['ಇ', 'ಈ']:
            new_word1 = remove_last_vowel_sound(word1) + 'ೀ'
            new_word = new_word1 + word2[1:]
            results.append(new_word)

        # CASE C: first vowel = ಉ / ಊ → replace with ಊ
        if first_vowel in ['ಉ', 'ಊ']:
            new_word1 = remove_last_vowel_sound(word1) + 'ೂ'
            new_word = new_word1 + word2[1:]
            results.append(new_word)

        # CASE D: first vowel = ಏ / ಐ → vowel becomes ಐ
        if first_vowel in ['ಏ', 'ಐ']:
            new_word1 = remove_last_vowel_sound(word1) + 'ೈ'
            new_word = new_word1 + word2[1:]
            results.append(new_word)

        # CASE E: first vowel = ಓ / ಔ → vowel becomes ಔ
        if first_vowel in ['ಓ', 'ಔ']:
            new_word1 = remove_last_vowel_sound(word1) + 'ೌ'
            new_word = new_word1 + word2[1:]
            results.append(new_word)

    # -----------------------------------------------
    # RULE 3: last_vowel == ಇ / ಈ AND first_vowel == ಇ / ಈ
    # -----------------------------------------------
    if last_vowel in ['ಇ', 'ಈ'] and first_vowel in ['ಇ', 'ಈ']:
        new_word1 = remove_last_vowel_sound(word1) + 'ೀ'
        results.append(new_word1 + word2[1:])

    # -----------------------------------------------
    # RULE 4: last_vowel == ಉ / ಊ AND first_vowel == ಉ / ಊ
    # -----------------------------------------------
    if last_vowel in ['ಉ', 'ಊ'] and first_vowel in ['ಉ', 'ಊ']:
        new_word1 = remove_last_vowel_sound(word1) + 'ೂ'
        results.append(new_word1 + word2[1:])

    # -----------------------------------------------
    # RULE 5: If last_vowel in [ಆ,ಇ,ಈ,ಎ,ಏ,ಐ,ಓ] 
    #         then first_vowel replaced with ಯ
    # -----------------------------------------------
    if last_vowel in ['ಆ', 'ಇ', 'ಈ', 'ಎ', 'ಏ', 'ಐ', 'ಓ']:
        if first_vowel in ['ಅ', 'ಅಂ'] : 
            new_word = word1 + 'ಯ' + remove_first_vowel(word2)
            results.append(new_word)
        else :
            new_word = word1 + 'ಯ' + get_vowel_sign(first_vowel) + remove_first_vowel(word2)
            results.append(new_word)

    # -----------------------------------------------
    # RULE 6: If last_vowel in [ಉ,ಊ,ಋ,ಓ,ಔ]
    #         then first_vowel replaced with ವ
    # -----------------------------------------------
    if last_vowel in ['ಉ', 'ಊ', 'ಋ', 'ಓ', 'ಔ']:
        if first_vowel in ['ಅ', 'ಅಂ'] : 
            new_word = word1 + 'ವ' + remove_first_vowel(word2)
            results.append(new_word)
        else :
            new_word = word1 + 'ವ' + get_vowel_sign(first_vowel) + remove_first_vowel(word2)
            results.append(new_word)

    # Remove duplicates
    results = list(set(results))
    
    if len(results):
        return results

    combined = word1 + word2   # temporary fallback
    results = list(set(combined))
    return results

# ----------------------------------------
# FUNCTION 4: JOIN TWO WORDS
# ----------------------------------------
def join_words(word1, word2):
    if not word1 or not word2:
        return [""]
    last_vow = get_last_vowel(word1)
    first_vow = get_first_vowel(word2)

    print("word1:", word1, "| last vowel:", last_vow)
    print("word2:", word2, "| first vowel:", first_vow)

    result = generate_possible_combinations(word1, word2, last_vow, first_vow)
    return result


# ----------------------------------------
# TEST
# ----------------------------------------
import csv

# --------------------------------------------------
# READ TRUE TEST CASES
# --------------------------------------------------
def load_true_tests(file_path):
    test_cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row["word1"].strip() or not row["word2"].strip():
                continue  # skip empty rows

            test_cases.append({
                "word1": row["word1"],
                "word2": row["word2"],
                "expected": row["expected_result"],
                "rule": row["sandhi_rule_used"]
            })
    return test_cases


# --------------------------------------------------
# READ FALSE TEST CASES
# --------------------------------------------------
def load_false_tests(file_path):
    test_cases = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row["word1"].strip() or not row["word2"].strip():
                continue

            test_cases.append({
                "word1": row["word1"],
                "word2": row["word2"],
                "incorrect": row["incorrect_attempt"],
                "why_wrong": row["why_wrong"],
                "correct": row["correct_version"]
            })
    return test_cases


# --------------------------------------------------
# RUN TESTS (TRUE OR FALSE)
# --------------------------------------------------
def run_tests(case_type="true"):
    if case_type == "true":
        tests = load_true_tests("test_cases/true_test_cases.csv")
        print("\n📌 Running TRUE Sandhi Test Cases\n")
        for t in tests:
            w1, w2, expected = t["word1"], t["word2"], t["expected"]
            result = join_words(w1, w2)
            print(f"{w1} + {w2} → {result} | expected = {expected}")

    elif case_type == "false":
        tests = load_false_tests("test_cases/false_test_cases.csv")
        print("\n❌ Running FALSE Sandhi Test Cases\n")
        for t in tests:
            w1, w2 = t["word1"], t["word2"]
            incorrect = t["incorrect"]
            correct = t["correct"]
            why_wrong = t["why_wrong"]

            result = join_words(w1, w2)

            print(f"{w1} + {w2}")
            print(f"User attempt: {incorrect} ❌ ({why_wrong})")
            print(f"Model output: {result}")
            print(f"Correct: {correct}\n")


# --------------------------------------------------
# USER INPUT SELECTOR
# --------------------------------------------------
mode = input("Enter test type (true / false): ").strip().lower()

if mode in ["true", "t"]:
    run_tests("true")
elif mode in ["false", "f"]:
    run_tests("false")
else:
    print("Invalid choice. Please enter 'true' or 'false'.")
