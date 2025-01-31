# IIS Access Counter

## Description

The IIS Access Counter is a Python application that parses IIS log files from specified directories to count the number of accesses for different applications. It filters out unnecessary asset requests (like CSS, images, and JavaScript) and outputs the results to a text file and a SQLite database.

## Features

- Parses log files in specified directories.
- Counts accesses per application while ignoring asset requests.
- Outputs results to a text file and a SQLite database.
- Configurable through a YAML file.

## Requirements

- Python 3.x
- Required Python libraries:
  - `pyyaml` for YAML configuration file handling.
  - `sqlite3` for database operations (included in Python standard library).

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/iis-access-counter.git
cd iis-access-counter
```
Install the required libraries (if not already installed):```pip install pyyaml``` or ```pip install requirements.txt```
    
Ensure you have access to the IIS log files you wish to parse.
    
## Configuration

The application uses a `config.yaml` file for configuration. Below is an example of how to structure the configuration file:
```yaml
log_directory: "\\\\serrver\\c$\\inetpub\\logs\\LogFiles"  # Path to the log directory
access_count_file: "access_counts.txt"                   # Output text file for access counts
database_file: "access_counts.db"                         # SQLite database file path
``` 

## Usage
Ensure your config.yaml is set up correctly.

Run the application: ```python iis_access_counter.py```
After execution, you will find:
 - A text file named access_counts.txt with the access counts for each application.
 - A SQLite database file named access_counts.db containing the same access counts.
