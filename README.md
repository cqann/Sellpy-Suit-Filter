# Sellpy Scraper

## Overview

**Sellpy Scraper** is a Python-based web scraping tool designed to automate the process of collecting product information from [Sellpy](https://www.sellpy.se), specifically targeting men's suits and jackets. The scraper navigates through multiple pages, extracts relevant product URLs based on specified measurement criteria, and ensures that progress is saved between sessions. This makes it an ideal tool for users who want to efficiently gather data without manually browsing through numerous pages.

## Features

-   **Automated Web Scraping**: Utilizes Selenium and BeautifulSoup to navigate and extract data from Sellpy.
-   **Dynamic Page Navigation**: Automatically continues scraping until there are no more products matching the specified criteria.
-   **Persistent Storage**: Saves fitting articles and tracks checked articles to avoid duplicates and ensure progress is retained between runs.
-   **Configurable Parameters**: Easily adjust the target URL and measurement ranges through a simple configuration file.
-   **User-Friendly**: Designed for users with minimal Python experience.

## Table of Contents

-   [Sellpy Scraper](#sellpy-scraper)
    -   [Overview](#overview)
    -   [Features](#features)
    -   [Table of Contents](#table-of-contents)
    -   [Requirements](#requirements)
    -   [Installation](#installation)
    -   [Configuration](#configuration)
    -   [Running the Script](#running-the-script)
    -   [Output Files](#output-files)
    -   [Troubleshooting](#troubleshooting)
    -   [Contributing](#contributing)
    -   [License](#license)

## Requirements

Before using the Sellpy Scraper, ensure you have the following:

-   **Operating System**: Windows, macOS, or Linux
-   **Python**: Version 3.10 or higher
-   **Pipenv**: Python dependency manager
-   **Internet Connection**: Required for accessing Sellpy and downloading necessary packages
-   **Web Browser**: Google Chrome

## Installation

Follow these steps to set up and run the Sellpy Scraper on your machine using `pipenv`:

### 1. Install Python

If you don't have Python installed:

-   **Download Python**: Visit the [official Python website](https://www.python.org/downloads/) and download the latest version compatible with your operating system.
-   **Install Python**:
    -   **Windows**: Run the installer and follow the prompts. Ensure you check the box that says "Add Python to PATH" during installation.
    -   **macOS**: Use the installer or install via Homebrew with `brew install python`.
    -   **Linux**: Install via your distribution's package manager, e.g., `sudo apt-get install python3`.

### 2. Install Pipenv

`pipenv` is a tool that combines `pip` and virtual environments for managing project dependencies.

-   **Install Pipenv**:

    ```bash
    pip install pipenv
    ```

    _If you encounter permission issues, you might need to use `pip install --user pipenv` or run the command with `sudo` on Unix-based systems._

-   **Verify Installation**:

    ```bash
    pipenv --version
    ```

    You should see output similar to:

    ```
    pipenv, version 2023.11.17
    ```

### 3. Clone or Download the Repository

If you haven't already, clone the repository or download the script files to your local machine.

```bash
git clone https://github.com/yourusername/sellpy-scraper.git
```

_Replace `yourusername` with your actual GitHub username if applicable._

### 4. Navigate to the Project Directory

```bash
cd sellpy-scraper
```

### 5. Install Required Python Packages with Pipenv

The scraper relies on several Python libraries. Use `pipenv` to install them:

1. **Initialize Pipenv Environment**:

    ```bash
    pipenv --python 3.11
    ```

2. **Install Dependencies**:

    ```bash
    pipenv install selenium webdriver-manager beautifulsoup4
    ```

    - **selenium**: Automates web browser interaction.
    - **webdriver-manager**: Automatically manages browser drivers.
    - **beautifulsoup4**: Parses HTML and XML documents.

3. **Activate the Virtual Environment**:

    ```bash
    pipenv shell
    ```

    Your terminal prompt should now indicate that you're inside the `pipenv` virtual environment.

### 6. Download Google Chrome

Ensure you have the latest version of [Google Chrome](https://www.google.com/chrome/) installed, as Selenium uses it for web interactions.

## Configuration

The scraper uses a configuration file (`config.txt`) to define its behavior. Follow these steps to set it up:

### 1. Create `config.txt`

In the same directory as your Python script, create a file named `config.txt`. You can use any text editor (e.g., Notepad, TextEdit, VS Code).

### 2. Define Configuration Parameters

Add the following content to `config.txt`:

```ini
initial_url=https://www.sellpy.se/search/Man/Kl%C3%A4der/Kavajer-%26-Kostymer/Kostymer?minPrice=200&material=Ull&material=Bomull&material=Linne&material=Kashmir&material=Mohair&material=Silke&material=Merinoull&color=Bl%C3%A5&color=Gr%C3%A5&brand=-H%26M&brand=-Zara+Man&brand=-Dressmann&brand=-Bl%C3%A4ck&brand=-Zara&brand=-GANT&brand=-H%26M+Man&brand=-Jack+%26+Jones&brand=-Premium+by+Jack+%26+Jones&brand=-Suitsupply&brand=-ESPRIT&brand=-Scotch+%26+Soda&brand=-H%26M+Modern+Classic&brand=-Riley&brand=-Bruuns+Bazaar&brand=-Calvin+Klein&condition=Mycket+bra&condition=Bra&condition=Nytt
# n_pages=23  # Optional: Uncomment and set if you prefer a fixed number of pages
arm_range=67,69
waist_range=86,92
shoulder_range=48,49
leg_range=83,90
```

### 3. Configuration Parameters Explained

-   **initial_url**: The starting URL for the scraper. This URL targets men's suits and jackets with specific filters applied (e.g., price, material, color, brand, condition). The initial_url can easily be created by going over into sellpy and browsing suits and adding your desired filter.
-   **n_pages** (Optional):

    -   **Purpose**: Sets a maximum number of pages to scrape.
    -   **Usage**: If you prefer the scraper to stop after a certain number of pages, uncomment this line and set your desired number. Comment with "#"
    -   **Example**: `n_pages=10` will limit the scraper to 10 pages.

-   **Measurement Ranges**:
    -   **arm_range**: Minimum and maximum acceptable arm measurements (e.g., `67,69`).
    -   **waist_range**: Minimum and maximum acceptable waist measurements.
    -   **shoulder_range**: Minimum and maximum acceptable shoulder measurements.
    -   **leg_range**: Minimum and maximum acceptable leg measurements.

**Note**: Ensure there are no spaces around the commas in the range values.

## Running the Script

Follow these steps to execute the Sellpy Scraper:

### 1. Activate the Pipenv Virtual Environment

If you haven't already activated the virtual environment, do so now:

```bash
pipenv shell
```

### 2. Prepare the Script

Ensure you have the Python script (e.g., `sellpy_scraper.py`) and `config.txt` in the same directory.

### 3. Run the Script

Execute the following command:

```bash
python sellpy_scraper.py
```

**Note**: Replace `sellpy_scraper.py` with the actual name of your Python script if different.

### 4. Monitor Progress

The script will print messages to the console indicating:

-   Which page it's navigating to.
-   Which articles are being processed.
-   Any articles added to the fitting list.
-   When the scraping process is complete.

## Output Files

The scraper generates two key output files:

### 1. `fit_articles.txt`

-   **Purpose**: Stores URLs of articles that meet the specified measurement criteria.
-   **Usage**: Review this file to see all the products that fit your requirements.
-   **Example Entry**:
    ```
    https://www.sellpy.se/product/12345
    ```

### 2. `checked_articles.txt`

-   **Purpose**: Keeps track of all processed article URLs to prevent reprocessing in future runs.
-   **Usage**: The scraper references this file to skip already checked articles, saving time and resources.
-   **Example Entry**:
    ```
    https://www.sellpy.se/product/12345
    https://www.sellpy.se/product/67890
    ```

**Note**: Both files are automatically created in the script's directory if they don't exist.

## Troubleshooting

If you encounter issues while using the Sellpy Scraper, consider the following solutions:

### 1. Python Not Found

-   **Issue**: Running `python` results in a "command not found" or similar error.
-   **Solution**: Ensure Python is installed and added to your system's PATH.
    -   **Windows**: Reinstall Python and check "Add Python to PATH" during installation.
    -   **macOS/Linux**: Verify Python installation with `python3 --version` and use `python3` instead of `python` if necessary.

### 2. Missing Python Packages

-   **Issue**: Errors indicating missing modules like `selenium` or `beautifulsoup4`.
-   **Solution**: Install the required packages using `pipenv`:

    ```bash
    pipenv install selenium webdriver-manager beautifulsoup4
    ```

### 3. ChromeDriver Issues

-   **Issue**: Errors related to ChromeDriver compatibility.
-   **Solution**:
    -   Ensure you have the latest version of Google Chrome installed.
    -   The `webdriver-manager` package should automatically handle ChromeDriver updates. If issues persist, consider manually updating ChromeDriver or verifying its installation.

### 4. Script Not Navigating Pages Correctly

-   **Issue**: The scraper stops prematurely or doesn't navigate to the next page.
-   **Solution**:
    -   Verify the `initial_url` in `config.txt` is correctly formatted.
    -   Ensure the termination message `"Finns inga fler varor som matchar dina aktiva filter"` hasn't changed on the website. If it has, update the script accordingly.

### 5. Measurement Extraction Issues

-   **Issue**: Articles are skipped despite meeting criteria.
-   **Solution**:
    -   Check that the measurement ranges in `config.txt` are correctly defined.
    -   Ensure the website's structure hasn't changed, affecting how measurements are extracted.

### 6. Browser Window Not Closing

-   **Issue**: After stopping the script, the browser window remains open.
-   **Solution**: The script uses a `try...finally` block to ensure the browser closes. If interrupted forcefully, you may need to manually close the browser.

## License

This project is licensed under the [MIT License](LICENSE).
