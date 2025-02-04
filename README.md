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

**Register Your Own API Keys**
   - Register at [Edamam](https://developer.edamam.com/) and create a new application to obtain your API key and ID.
   - Replace `YOUR_API_ID` and `YOUR_API_KEY` in the code with your actual values.

2. Run the script:
    ```bash
    python nutrition_calculator.py
    ```

3. Follow the prompts to enter food items and their quantities.
