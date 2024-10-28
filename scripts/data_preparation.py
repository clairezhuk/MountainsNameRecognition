import os
import string

def read_text_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

read_text_file.__doc__= """
Reads text content from a specified .txt file.

Parameters:
    file_path (str): Path to the text file.

Returns:
    str: Content of the file as a single string.

Raises:
    FileNotFoundError: If the file does not exist at the specified path.
"""

def process_text_to_conll(text):
    train_lines = []  # To store training data
    test_lines = []   # To store testing data
    sentences = text.strip().split('.\n')  # Split by sentence delimiters

    sentence_counter = 1  # Track sentence index for train/test split

    for sentence in sentences:
        tokens = []  # Tokens in the current sentence
        tags = []    # Tags corresponding to each token
        words = sentence.split()  # Split sentence into words
        next_mountain = False  # Track if we are inside a mountain name
        next_geo = False       # Track if we are inside a location name

        for word_with_coma in words:
            word = word_with_coma.strip(',')  # Remove trailing commas
            # Identify mountain names
            if word.startswith('|'):
                next_mountain = not word.endswith('|')
                tag = 'B-mountain' if not next_mountain else 'I-mountain'
            # Identify geographical names
            elif word.startswith('/'):
                next_geo = not word.endswith('/')
                tag = 'B-location' if not next_geo else 'I-location'
            else:
                tag = 'O'  # Non-entity words

            token = word.strip(string.punctuation)  # Clean punctuation from token
            tokens.append(token)  # Store token
            tags.append(tag)      # Store tag

        # Combine tokens and tags in CoNLL format
        conll_sentence = [f"{token}\t{tag}" for token, tag in zip(tokens, tags)]
        conll_sentence.append("")  # Blank line after each sentence

        # Append to train or test data based on sentence counter
        if sentence_counter % 5 == 0:
            test_lines.extend(conll_sentence)
        else:
            train_lines.extend(conll_sentence)

        sentence_counter += 1  # Increment for next sentence

    return "\n".join(train_lines), "\n".join(test_lines)  # Join sentences with line breaks
process_text_to_conll.__doc__="""
    Converts labeled text into CoNLL format and splits sentences into training and testing sets.

    Parameters:
        text (str): Text content to process.

    Returns:
        tuple: Two strings representing CoNLL-formatted training and testing data.

    Notes:
        - Sentences are split by '.\n' and '.' delimiters.
        - Mountain names are denoted by surrounding pipes '|MountainName|'.
        - Other geographical names are marked with slashes '/LocationName/'.
        - Data is divided into train and test sets (80/20 split).
    """

def save_conll_file(conll_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(conll_data)
save_conll_file.__doc__="""
    Writes CoNLL-formatted data to a specified file.

    Parameters:
        conll_data (str): CoNLL data to save.
        output_path (str): Path to the output file.
    """

def main():
    input_file_path = '../data/raw/sentences.txt'  # Input file path
    text = read_text_file(input_file_path)  # Read text data

    # Process text into CoNLL format with train/test split
    train_data, test_data = process_text_to_conll(text)

    # Paths to save train and test data
    train_output_file_path = '../data/processed/train_file.conll'
    test_output_file_path = '../data/processed/test_file.conll'

    # Save data
    save_conll_file(train_data, train_output_file_path)
    save_conll_file(test_data, test_output_file_path)

    print(f"Train file saved to {train_output_file_path}")
    print(f"Test file saved to {test_output_file_path}")

main.__doc__="""
    Main function to execute the full workflow:
        1. Read text data.
        2. Process text into CoNLL format.
        3. Save train and test sets in respective files.
    """
# Run the main function
if __name__ == '__main__':
    main()
