import re
import io
import sys
from config import COUNTER_FILE


def extract_python_code(script: str) -> str:
    """Extracts the Python code block from a given script."""
    match = re.search(r"```python\n(.*?)\n```", script, re.DOTALL)
    return match.group(1) if match else ""


def execute_code(code: str) -> str:
    """Executes Python code and captures the output or error."""
    old_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        exec(code)
    except Exception as e:
        print(f"Error: {e}")
    sys.stdout = old_stdout
    return buffer.getvalue()


def write_count(x):
    """
    Writes the value of x to a text file called 'counter_file.txt'.
    If the file doesn't exist, it creates a new file and writes the value.
    If the file exists, it replaces the previous value with the new value.
    """
    with open(COUNTER_FILE, 'w') as file:
        file.write(str(x))


def retrieve_count():
    """
    Reads the value from the 'counter_file.txt' file.
    If the file exists, it returns the integer value.
    If the file doesn't exist, it returns 0.
    """
    try:
        with open(COUNTER_FILE, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def extract_rows(text):
    """Extract non-empty rows from text."""
    return [line for line in text.strip().split('\n') if line.strip()]


def extract_last_words(rows):
    """Extract the last word from each row."""
    return [row.split()[-1] for row in rows]


def extract_first_column(input_text):
    """Extract the first column (word) from each line."""
    lines = input_text.strip().split("\n")
    return "\n".join(line.split()[0] for line in lines if line.strip())


def load_labels_from_file(file_path):
    """Load labels from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return ""


def tokenize_text(text):
    """Convert plain text to words separated by newlines."""
    # Simple tokenization - split by spaces and punctuation
    import string
    
    words = []
    current_word = ""
    
    for char in text:
        if char.isalnum() or char in "'-":
            current_word += char
        else:
            if current_word:
                words.append(current_word)
                current_word = ""
            if char.strip() and char in string.punctuation:
                words.append(char)
    
    if current_word:
        words.append(current_word)
    
    return "\n".join(words)


def compare_columns_ignore_position(text1, text2):
    """Compare two texts by extracting last words and calculating match percentage."""
    rows1, rows2 = extract_rows(text1), extract_rows(text2)
    last_words1 = {row.split()[-1] for row in rows1}
    last_words2 = {row.split()[-1] for row in rows2}

    common_words = last_words1 & last_words2
    total_unique = len(last_words1 | last_words2)

    return {
        "match_percentage": (len(common_words) / total_unique) * 100 if total_unique > 0 else 0,
        "common_words": list(common_words),
        "missing_in_text1": list(last_words2 - last_words1),
        "missing_in_text2": list(last_words1 - last_words2),
    }


def compare_columns_with_missing_rows(text1, text2):
    """Compare two texts row by row and identify non-matching rows."""
    rows1, rows2 = extract_rows(text1), extract_rows(text2)
    min_rows = min(len(rows1), len(rows2))
    words1 = extract_last_words(rows1[:min_rows])
    words2 = extract_last_words(rows2[:min_rows])

    matches = sum(word1 == word2 for word1, word2 in zip(words1, words2))
    non_matching_rows = [(rows1[i], rows2[i]) for i in range(min_rows) if words1[i] != words2[i]]

    return {
        "match_percentage": (matches / min_rows) * 100 if min_rows > 0 else 0,
        "non_matching_rows": non_matching_rows,
        "missing_in_text1": rows2[len(rows1):] if len(rows1) < len(rows2) else [],
        "missing_in_text2": rows1[len(rows2):] if len(rows2) < len(rows1) else [],
    }