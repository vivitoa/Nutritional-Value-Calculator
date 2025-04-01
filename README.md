
# Nutritional Value Calculator 🥗📊

A Python GUI application that calculates nutritional values for food items and
recipes using the Edamam API. Track calories, proteins, fats, and carbohydrates
for individual ingredients or entire meals!


## Features ✨
- **Dark Theme GUI** - Modern and eye-friendly interface
- **Dual Modes** - Calculate for single items or full recipes
- **Nutrition Breakdown** - Get values for both total quantity and 100g
- **Error Handling** - Input validation and API error messages
- **Recipe Saving** - Export nutrition data to text files
- **Undo Functionality** - Remove accidental entries easily

## Installation 🛠️

### 1. Clone Repository
```bash
git clone https://github.com/vivitoa/Nutritional-Value-Calculator.git
cd Nutritional-Value-Calculator
```

### 2. Install Dependencies
```bash
pip install requests python-dotenv
```

### 3. API Setup
1. Register at [Edamam Developer Portal](https://developer.edamam.com/)
2. Create new application to get API credentials
3. Create `.env` file in project root:
```ini
API_ID=your_app_id_here
API_KEY=your_api_key_here
```

## Usage 🚀
1. **Launch Application**
```bash
python nutrition_calculator.py
```

2. **Choose Mode**
- **Single Food Mode**:
  - Enter food name and quantity
  - See instant nutrition breakdown

- **Recipe Mode**:
  - Enter dish name
  - Add ingredients with quantities
  - View total nutrition when done
  - Save recipe with nutrition data

3. **Controls**
- `Enter` to submit forms
- `Delete` to remove ingredients
- `Tab` to navigate between fields

## Technologies Used 💻
- **Python 3** - Core programming language
- **Tkinter** - GUI development
- **Edamam API** - Nutrition data source
- **requests** - API communication
- **dotenv** - Environment management

## License 📄
MIT License - See [LICENSE](LICENSE) file

---

**Important Note:** You must obtain your own API credentials from [Edamam](https://developer.edamam.com/) for the application to work.

⭐ Feel free to star the repository if you find this useful!  
🐛 Report issues in GitHub repository  
💡 Suggestions and contributions welcome!
```

