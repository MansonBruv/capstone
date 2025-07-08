# scripts/generate_secret_code.py
import uuid
import requests # Import the requests library to fetch content from a URL
import random # Import the random library for phrase selection
import os

# URL to the secrets.txt file on GitHub
SECRETS_FILE_URL = "https://raw.githubusercontent.com/fhdsl/reproducibility_capstone/main/resources/secrets.txt"

def get_random_secret_phrase():
    """
    Fetches the secrets.txt file from a URL, parses its content,
    and returns a randomly selected phrase.
    """
    try:
        # Fetch the content of the secrets file from the URL
        response = requests.get(SECRETS_FILE_URL)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Decode content and split into lines
        phrases = response.text.strip().split('\n')
        
        # Filter out any empty lines that might result from splitting
        phrases = [phrase.strip() for phrase in phrases if phrase.strip()]

        if not phrases:
            print(f"Warning: No valid phrases found in {SECRETS_FILE_URL}")
            return "NO_PHRASES_FOUND" # Fallback if file is empty or only whitespace

        # Randomly choose one phrase from the list
        random_phrase = random.choice(phrases)
        return random_phrase

    except requests.exceptions.RequestException as e:
        print(f"Error fetching secrets file from URL '{SECRETS_FILE_URL}': {e}")
        return "ERROR_FETCHING_SECRETS" # Fallback on network/request error
    except Exception as e:
        print(f"An unexpected error occurred during secret phrase extraction: {e}")
        return "UNKNOWN_EXTRACTION_ERROR" # Fallback for any other unexpected error

def generate_secret_code():
    """
    Generates a unique base code (UUID) and combines it with a
    randomly selected secret phrase fetched from an external file.
    """
    base_code = str(uuid.uuid4())
    
    # Retrieve a random secret phrase
    # This replaces the previous logic of reconstructing parts from local files.
    secret_phrase_to_inject = get_random_secret_phrase()
    
    # Combine the base unique code with the randomly chosen secret phrase, separated by a hyphen
    combined_code = f"{base_code}-{secret_phrase_to_inject}"

    return combined_code

if __name__ == "__main__":
    # When this script is executed, it prints the combined secret code to standard output.
    # The GitHub Actions workflow captures this output.
    print(generate_secret_code())
