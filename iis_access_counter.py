import os
import re
import yaml
import sqlite3
from collections import defaultdict

class LogParser:
    def __init__(self, config_path="config.yaml"):
        self.config = self.load_config(config_path)
        self.log_directory = self.config.get('log_directory')
        self.access_count_file = self.config.get('access_count_file')
        self.database_file = self.config.get('database_file')  # Database file path from config
        self.access_counts = defaultdict(int)
        # Regex to match application endpoints (excluding assets like css, js, images, etc.)
        self.log_entry_pattern = re.compile(r'GET\s+(/[^.\s]*)(?=\s|$)')  # Matches any path not containing a dot before a space or end of line

        # Initialize SQLite database
        self.init_database()

    def load_config(self, file_path):
        """Loads configuration from a YAML file."""
        with open(file_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
        print("Configuration loaded successfully.")
        return config

    def init_database(self):
        """Initializes the SQLite database and creates a table for access counts."""
        print("Initializing the SQLite database...")
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_counts (
                    application TEXT PRIMARY KEY,
                    count INTEGER NOT NULL
                )
            ''')
        print("Database initialized successfully.")

    def parse_log_file(self, file_path):
        """Parses a single log file to count accesses per application."""
        print(f"Parsing file: {file_path}")
        encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']  # List of encodings to try
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    for line in file:
                        match = self.log_entry_pattern.search(line)
                        if match:
                            app_name = match.group(1)
                            self.access_counts[app_name] += 1
                print(f"Completed parsing file: {file_path} with encoding {encoding}")
                return  # Exit the loop and function on successful parsing
            except UnicodeDecodeError:
                print(f"Warning: Could not decode {file_path} using '{encoding}' encoding. Trying next encoding...")
        
        print(f"Error: Failed to parse {file_path} with all attempted encodings.")

    def parse_logs(self):
        """Parses all log files in all 'w3svc' folders under the specified directory."""
        print(f"Starting to parse log files in directory: {self.log_directory}")
        for subdir in os.listdir(self.log_directory):
            subdir_path = os.path.join(self.log_directory, subdir)
            if os.path.isdir(subdir_path) and subdir.lower().startswith('w3svc'):
                print(f"Entering folder: {subdir_path}")
                for filename in os.listdir(subdir_path):
                    if filename.endswith(".log"):
                        file_path = os.path.join(subdir_path, filename)
                        self.parse_log_file(file_path)
        print(f"Completed parsing all log files in directory: {self.log_directory}")

    def save_access_counts(self):
        """Saves the access counts to a file and inserts into the SQLite database."""
        print(f"Saving access counts to {self.access_count_file} and the database {self.database_file}...")
        try:
            # Write to text file
            with open(self.access_count_file, 'w', encoding='utf-8') as file:
                for app_name, count in self.access_counts.items():
                    file.write(f"{app_name}: {count}\n")
            print(f"Access counts saved to {self.access_count_file}")

            # Insert into SQLite database
            with sqlite3.connect(self.database_file) as conn:
                cursor = conn.cursor()
                for app_name, count in self.access_counts.items():
                    cursor.execute('''
                        INSERT INTO access_counts (application, count) 
                        VALUES (?, ?) 
                        ON CONFLICT(application) DO UPDATE SET count = count + excluded.count
                    ''', (app_name, count))
                conn.commit()
            print(f"Access counts saved to database {self.database_file}")
        except UnicodeEncodeError as e:
            print(f"Error: Failed to write to {self.access_count_file} due to encoding issue: {e}")

    def run(self):
        """Runs the full parsing and saving process."""
        print("Starting the IIS log parsing process...")
        self.parse_logs()
        self.save_access_counts()
        print("IIS log parsing process completed successfully.")

if __name__ == "__main__":
    parser = LogParser()
    parser.run()
