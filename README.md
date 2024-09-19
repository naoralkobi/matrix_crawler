# Matrix Scraper using Selenium

This project is a web scraper that extracts news articles from a government website using Selenium. It fetches the articles' URLs, parses their content, and returns them as structured JSON data.

## Features

- Uses Selenium WebDriver to fetch and parse web pages.
- Extracts article titles, content, publish dates, and other metadata.
- Runs in headless mode for performance optimization.
- Can be extended to support other parsers.
- Utilizes a regex pattern to extract URLs from the HTML source.
  
## Requirements

- **Google Chrome** (Version: `129.0.6668.59 (Official Build) (arm64)`)
- **ChromeDriver** (Version: `129.0.6668.58`)
- **Python** `3.7+`
- **Selenium** `4.0+`
- Additional Python packages listed in the `requirements.txt`.

## Installation

### Step 1: Install Chrome

You must have the Chrome browser installed on your machine. The tested version for this project is:

- **Chrome Version**: `129.0.6668.59 (Official Build) (arm64)`

Make sure you are using the appropriate version for your machine's architecture.

### Step 2: Install ChromeDriver

You need to install ChromeDriver version `129.0.6668.58` to match your Chrome browser version. You can download it from the [official ChromeDriver site](https://chromedriver.chromium.org/downloads).

- For **Mac (arm64)**, you can download the appropriate driver:
  ```bash
  wget https://chromedriver.storage.googleapis.com/129.0.6668.58/chromedriver_mac64.zip
  unzip chromedriver_mac64.zip
  sudo mv chromedriver /usr/local/bin/chromedriver
  ```

### Step 3: Set Up a Virtual Environment

It's recommended to use a virtual environment for Python projects to manage dependencies. Run the following commands to create and activate a virtual environment:

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create a virtual environment
virtualenv venv

# Activate the virtual environment
source venv/bin/activate
```

### Step 4: Install Python Dependencies

Once your virtual environment is activated, install the required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```