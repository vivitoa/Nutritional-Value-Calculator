import requests

API_ID = 'b2c2c93a'
API_KEY = '82201f3c1f217d614654d1bb53541973'
API_URL = 'https://api.edamam.com/api/nutrition-data'


def get_food_nutrition(food_name, quantity):
    params = {
        'app_id': API_ID,
        'app_key': API_KEY,
        'ingr': f"{quantity}g {food_name}"
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    if 'totalNutrients' in data:
        return {
            'Calories': data['calories'],
            'Protein': data['totalNutrients'].get('PROCNT', {}).get('quantity', 0),
            'Fat': data['totalNutrients'].get('FAT', {}).get('quantity', 0),
            'Carbs': data['totalNutrients'].get('CHOCDF', {}).get('quantity', 0)
        }
    else:
        print(f"Response data: {data}")
        return None


def main():
    food_list = []

    while True:
        food_name = input("Enter the food item (or 'done' to finish): ")
        if food_name.lower() == 'done':
            break

        quantity = float(input("Enter the quantity in grams: "))

        nutrition = get_food_nutrition(food_name, quantity)
        if nutrition:
            nutrition['Food'] = food_name
            nutrition['Quantity'] = quantity
            food_list.append(nutrition)

            print(f"\n{food_name.capitalize()} Nutrition for {quantity}g:")
            print(f"Calories: {nutrition['Calories']} kcal")
            print(f"Protein: {nutrition['Protein']} g")
            print(f"Fat: {nutrition['Fat']} g")
            print(f"Carbs: {nutrition['Carbs']} g")
        else:
            print(f"Could not find nutrition data for {food_name}.")

    choice = input("Would you like the results for the total quantity or per 100g? (Enter 'total' or '100g'): ").lower()

    if choice == 'total':
        total_nutrition = {'Calories': 0, 'Protein': 0, 'Fat': 0, 'Carbs': 0}

        for item in food_list:
            for key in total_nutrition:
                total_nutrition[key] += item[key]

        print("\nTotal Nutrition for the Recipe (for total quantity):")
        for key, value in total_nutrition.items():
            print(f"{key}: {value:.2f} {'kcal' if key == 'Calories' else 'g'}")

    elif choice == '100g':
        total_nutrition = {'Calories': 0, 'Protein': 0, 'Fat': 0, 'Carbs': 0}
        total_quantity = sum(item['Quantity'] for item in food_list)

        for item in food_list:
            for key in total_nutrition:
                total_nutrition[key] += item[key]

        print("\nTotal Nutrition for the Recipe (per 100g):")
        for key, value in total_nutrition.items():
            print(f"{key}: {(value / total_quantity) * 100:.2f} {'kcal' if key == 'Calories' else 'g'}")

    else:
        print("Invalid choice. Please restart the program and enter 'total' or '100g'.")


if __name__ == '__main__':
    main()