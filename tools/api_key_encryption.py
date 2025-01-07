from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

def encrypt_api_key():
    """
    Encrypt the API key stored in the .env file and save the encrypted key and encryption key to files.
    """
    # Load the .env file
    load_dotenv(dotenv_path="C:/AiApiHomeAssignment/AiApiHomeAssignment/config/.env")

    # Retrieve the API key from the .env file
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY not found in .env file")

    # Generate a key for encryption
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)

    # Encrypt the API key
    encrypted_api_key = cipher_suite.encrypt(api_key.encode())

    # Save the encryption key and encrypted API key to files
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(encryption_key)
    with open("encrypted_api_key.enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_api_key)

    print("API key encrypted and saved successfully.")

def load_api_key():
    """
    Load and decrypt the API key from the encrypted file using the encryption key.

    Returns:
        str: The decrypted API key.
    """
    # Load the encryption key
    with open("encryption_key.key", "rb") as key_file:
        encryption_key = key_file.read()

    # Load the encrypted API key
    with open("encrypted_api_key.enc", "rb") as encrypted_file:
        encrypted_api_key = encrypted_file.read()

    # Decrypt the API key
    cipher_suite = Fernet(encryption_key)
    api_key = cipher_suite.decrypt(encrypted_api_key).decode()

    return api_key

# Example usage:
# encrypt_api_key()
# print(load_api_key())
