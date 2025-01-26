# Nutritional-Value-Calculator
This is a Python program that allows users to input various food items and their quantities, then calculates the calories and macronutrients (proteins, fats, and carbohydrates) for the entered quantity and for 100 grams. The program uses the Edamam API to fetch nutritional data.


## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/nutrition-calculator.git
    ```
2. Navigate to the project directory:
    ```bash
    cd nutrition-calculator
    ```
3. Install the required packages:
    ```bash
    pip install requests
    ```

## Usage

1. **Option 1: Use Provided API Keys**
   - You can use the provided API key and ID below:
     - API ID: `b2c2c93a`
     - API Key: `82201f3c1f217d614654d1bb53541973`

2. **Option 2: Register Your Own API Keys**
   - Register at [Edamam](https://developer.edamam.com/) and create a new application to obtain your API key and ID.
   - Replace `YOUR_API_ID` and `YOUR_API_KEY` in the code with your actual values.

3. Run the script:
    ```bash
    python nutrition_calculator.py
    ```

4. Follow the prompts to enter food items and their quantities.
