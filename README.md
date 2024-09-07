
---

# 🌐 Lattes Data Scraper - Automate Data Extraction from Lattes Platform

![Lattes Scraper](https://img.shields.io/badge/Python-3.x-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg)
![FastAPI](https://img.shields.io/badge/twoCaptcha-1.x-yellow.svg)
![License](https://img.shields.io/github/license/mashape/apistatus.svg)

### 🚀 Scrape academic profiles effortlessly, bypassing CAPTCHAs with automation.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Modules Breakdown](#-modules-breakdown)
- [License](#-license)
- [API Payment Notice](#-api-payment-notice)

---

## 🌟 Overview

This project is a **web scraping tool** designed to extract structured data from academic profiles on the **Lattes Platform**, a database of researchers in Brazil. By leveraging **Selenium WebDriver** and **TwoCaptcha** API, the scraper can solve CAPTCHAs, automate navigation, and extract relevant data like:

- Name
- Nationality
- Academic Titles (e.g., PhD, Master's)
- Languages
- Scientific Productions

---

## ✨ Features

- **Captcha Bypass**: Automatically solves reCAPTCHA using the TwoCaptcha API.
- **Headless Data Extraction**: Scrapes key details such as academic titles, languages, and publications.
- **Error Handling**: Captures and handles common errors during scraping.
- **Modular Design**: Separate modules for scraping, captcha-solving, and driver management following SOLID principles.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/lattes-scraper.git
cd lattes-scraper
```

### 2. Set Up Your Environment

1. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. **Install Required Packages**:

    ```bash
    pip install -r requirements.txt
    ```

### 3. Set Up Environment Variables

Create a `.env` file in the root directory and add your TwoCaptcha API key:

```bash
API_KEY=your_twocaptcha_api_key
```

---

## 💻 Usage

After installing the dependencies and setting up your API key, you can start scraping profiles from the Lattes Platform by passing the URL of the profile to scrape.

### Run the Scraper

```bash
python main.py --url "https://lattes.cnpq.br/example"
```

### Example Output

```bash
{
    'nome_lattes': 'João Silva',
    'nacionalidade': 'Brazil',
    'titulo': 'Doutorado',
    'idiomas': ['Portuguese', 'English'],
    'producoes': 'List of scientific productions...'
}
```

### Arguments

- `--url`: The URL of the Lattes academic profile you want to scrape. This is a required argument.

---

## 🧩 Modules Breakdown

### 1. **`drivers/web_driver.py`**
This module handles setting up and tearing down the Selenium WebDriver, which is used to automate browser interaction.

- **`setup_driver()`**: Initializes and returns the WebDriver.
- **`close_driver()`**: Safely closes the WebDriver after use.

### 2. **`captcha/captcha_solver.py`**
Solves CAPTCHAs using the TwoCaptcha service. Extracts the reCAPTCHA site key and submits the solution automatically.

- **`get_site_key()`**: Retrieves the reCAPTCHA site key from the page.
- **`solve_recaptcha()`**: Solves the reCAPTCHA and injects the solution into the page.

### 3. **`scrapers/lattes_scraper.py`**
Scrapes key data points from a Lattes profile.

- **`scrap_lattes_data()`**: Scrapes all data fields (name, nationality, academic title, languages, etc.).
- **`scrap_nome_lattes()`**: Extracts the name from the profile.
- **`scrap_nacionalidade()`**: Extracts the nationality.
- **`scrap_academic_title()`**: Determines the highest academic title achieved.
- **`scrap_idiomas()`**: Extracts the list of languages spoken.
- **`scrap_producoes()`**: Scrapes the list of scientific productions.

### 4. **`main.py`**
The main entry point of the application, responsible for orchestrating the scraping and solving CAPTCHAs.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 💳 API Payment Notice

**TwoCaptcha API** is a paid service. You will need to create an account on [TwoCaptcha](https://2captcha.com/), purchase credits, and obtain your API key to use this tool effectively. Solving CAPTCHAs requires a balance on your TwoCaptcha account.

---

### 🚀 Happy Scraping! 🌐

---