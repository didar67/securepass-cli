# 🔐 Advanced Password Generator & Saver Script using Python (with CLI, Logging, and File Handling)

import os
import sys
import string
import random
import logging
import datetime

# Logger setup
def initialize_logger():
    """Initialize logger with file and console handlers.  """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("password_manager.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

# Start logger
initialize_logger()

# Directory and file paths
PASSWORD_FOLDER = "generated_password"
PASSWORD_FILE = os.path.join(PASSWORD_FOLDER, 'password_records.txt')

#  ✅ Secure password generator function
def generate_secure_password(length = 12):
    """Generate a strong random password of given length."""
    try:
        characters = string.ascii_letters + string.punctuation + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        logging.info(f"Password succesfully generated with length {length}")

        return password  

    except (ValueError, TypeError) as error:
        logging.error(f"Issue generating password: {error}")
        raise

# ✅ Save generated password to file
def save_password_file(level, password):
    """Save the generated password with level and timestamp."""
    try:
       if not os.path.exists(PASSWORD_FOLDER):
         os.makedirs(PASSWORD_FOLDER)

       with open(PASSWORD_FILE, 'a') as file:
          timestamp = datetime.datetime.now().strftime("%b-%d-%Y %I:%M-%S %p")
          file.write(f"{timestamp} | {level}: {password}")

       logging.info(f"Saved password for level: {level}")

    except (FileNotFoundError, PermissionError) as error:
        logging.error(f"Failed to save password: {error}")
        raise

# ✅ Open password file using default system app (Windows only)
def reveal_password_file():
    """Open the saved password file with system's default viewer.
    
    ⚠️ Note: This method uses os.startfile(), which only works on Windows.
    For macOS or Linux:
        - Use subprocess.call(['open', file]) for macOS
        - Use subprocess.call(['xdg-open', file]) for Linux
    """

    try:
        os.startfile(PASSWORD_FILE)  # ⚠️ Works only on Windows
        logging.info("Opened password file successfully.")
   
    except FileNotFoundError as error:
        logging.error(f"Password file not found: {error}")
        print("Password file doesn't exist.")

    except Exception as error:
        logging.error(f"File not open: {error}")
        print("Manually need to open file.")

# ✅ Main script execution function
def run():
    """Handle CLI arguments and trigger appropriate actions."""
    try:
        if len(sys.argv)<2:
           print("Usage:")
           print(" python script.py generate <level> {length}")
           print(" python script.py open")
           sys.exit(1)

        action = sys.argv[1].lower()

        if action == "generate":
            if len(sys.argv)<3:
                print("Error: Please provide a level for password.")
                sys.exit(1)

            level = sys.argv[2].strip()
            try:
              length = int(sys.argv[3]) if len(sys.argv)>3 else 12

            except ValueError:
                print("Error: Length must be an integer.")
                sys.exit(1)

            password = generate_secure_password(length=length)
            save_password_file(level, password)
            print(f"Password for {level} created: {password}")

        elif action == 'open':
            reveal_password_file()

        else:
            print("Invalid command. Try 'generate' or 'open'")

    except Exception as error:
        logging.critical(f"Unexpected issue in main: {error}")
        print("Something went wrong. Check log file for details.")

# ✅  Entry point
if __name__ == "__main__" :
    run()