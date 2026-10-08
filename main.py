# ONLINE SHOPPING TRENDS ANALYSIS

import csv
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt


# DATA INPUT 
def load_data(filename):
    products = []
    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                "id": int(row["Product_ID"]),
                "name": row["Product_Name"],
                "category": row["Category"],
                "price": float(row["Price"]),
                "rating": float(row["Rating"]),
                "purchases": int(row["Purchases"])
            })
    return products


#  BASIC PYTHON ANALYSIS 
def average_price(products):
    prices = [p["price"] for p in products]
    return sum(prices) / len(prices)


def average_rating(products):
    ratings = [p["rating"] for p in products]
    return sum(ratings) / len(ratings)


def most_purchased(products):
    return max(products, key=lambda p: p["purchases"])


def highest_rated(products):
    return max(products, key=lambda p: p["rating"])


def most_expensive(products):
    return max(products, key=lambda p: p["price"])


def category_purchases(products):
    result = {}
    for product in products:
        category = product["category"]
        if category not in result:
            result[category] = 0
        result[category] += product["purchases"]
    return result


def expensive_products(products, limit=2000):
    return [p for p in products if p["price"] > limit]


# Demonstrates reduce()
def total_purchases_with_reduce(products):
    purchases = [p["purchases"] for p in products]
    return reduce(lambda x, y: x + y, purchases)


# Demonstrates map()
def discounted_prices(products):
    prices = [p["price"] for p in products]
    return list(map(lambda x: round(x * 0.90, 2), prices))


# Demonstrates filter()
def highly_rated_products(products):
    return list(filter(lambda p: p["rating"] >= 4.5, products))


#  NUMPY ANALYSIS 
def numpy_analysis(products):
    prices = np.array([p["price"] for p in products])
    ratings = np.array([p["rating"] for p in products])
    purchases = np.array([p["purchases"] for p in products])

    print("\nNUMPY STATISTICS")
    print("-" * 40)
    print("Average Price:", round(np.mean(prices), 2))
    print("Minimum Price:", np.min(prices))
    print("Maximum Price:", np.max(prices))
    print("Average Rating:", round(np.mean(ratings), 2))
    print("Total Purchases:", np.sum(purchases))
    print("Price Array Shape:", prices.shape)
    print("Price Array Size:", prices.size)
    print("Price Array Dimension:", prices.ndim)


#  VISUALIZATION
def create_graphs(products):
    categories = list(category_purchases(products).keys())
    category_values = list(category_purchases(products).values())

    names = [p["name"] for p in products]
    prices = np.array([p["price"] for p in products])
    ratings = np.array([p["rating"] for p in products])
    purchases = np.array([p["purchases"] for p in products])

    # 1. Bar chart
    plt.figure(figsize=(9, 5))
    plt.bar(categories, category_values)
    plt.title("Purchases by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Purchases")
    plt.tight_layout()
    plt.savefig("graphs/purchases_by_category.png")
    plt.close()

    # 2. Scatter plot
    plt.figure(figsize=(8, 5))
    plt.scatter(prices, ratings)
    plt.title("Price vs Product Rating")
    plt.xlabel("Price (INR)")
    plt.ylabel("Rating")
    plt.tight_layout()
    plt.savefig("graphs/price_vs_rating.png")
    plt.close()

    # 3. Histogram
    plt.figure(figsize=(8, 5))
    plt.hist(ratings, bins=6)
    plt.title("Distribution of Product Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Number of Products")
    plt.tight_layout()
    plt.savefig("graphs/rating_distribution.png")
    plt.close()

    # 4. Pie chart
    plt.figure(figsize=(7, 7))
    plt.pie(category_values, labels=categories, autopct="%1.1f%%")
    plt.title("Purchase Distribution by Category")
    plt.tight_layout()
    plt.savefig("graphs/category_distribution.png")
    plt.close()

    # 5. Box plot
    plt.figure(figsize=(7, 5))
    plt.boxplot(prices)
    plt.title("Product Price Distribution")
    plt.ylabel("Price (INR)")
    plt.tight_layout()
    plt.savefig("graphs/price_boxplot.png")
    plt.close()

    # 6. Top 5 products
    top5 = sorted(products, key=lambda p: p["purchases"], reverse=True)[:5]
    top_names = [p["name"] for p in top5]
    top_values = [p["purchases"] for p in top5]

    plt.figure(figsize=(9, 5))
    plt.bar(top_names, top_values)
    plt.title("Top 5 Most Purchased Products")
    plt.xlabel("Product")
    plt.ylabel("Purchases")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("graphs/top_5_products.png")
    plt.close()

    print("\n6 graphs saved inside the 'graphs' folder.")


#  PRODUCT CLASS 
class Product:
    def __init__(self, name, category, price, rating, purchases):
        self.name = name
        self.category = category
        self.price = price
        self.rating = rating
        self.purchases = purchases

    def display(self):
        print(f"{self.name} | {self.category} | ₹{self.price:.0f} | "
              f"Rating: {self.rating} | Purchases: {self.purchases}")


class ElectronicProduct(Product):
    def product_type(self):
        return "Electronic Product"


#  MENU
def show_products(products):
    print("\nPRODUCT LIST")
    print("-" * 75)
    for p in products:
        print(f'{p["name"]:22} | {p["category"]:12} | '
              f'₹{p["price"]:7.0f} | {p["rating"]:.1f} | {p["purchases"]}')


def show_summary(products):
    most = most_purchased(products)
    rated = highest_rated(products)
    expensive = most_expensive(products)
    categories = category_purchases(products)
    popular_category = max(categories, key=categories.get)

    print("\n" + "=" * 55)
    print("ONLINE SHOPPING TRENDS - SUMMARY")
    print("=" * 55)
    print("Total Products       :", len(products))
    print("Average Price        : ₹", round(average_price(products), 2))
    print("Average Rating       :", round(average_rating(products), 2))
    print("Total Purchases      :", total_purchases_with_reduce(products))
    print("Most Purchased       :", most["name"], "-", most["purchases"])
    print("Highest Rated        :", rated["name"], "-", rated["rating"])
    print("Most Expensive       :", expensive["name"], "- ₹", int(expensive["price"]))
    print("Most Popular Category:", popular_category)
    print("=" * 55)


def main():
    products = load_data("shopping_data.csv")

    while True:
        print("\n" + "=" * 55)
        print("     ONLINE SHOPPING TRENDS ANALYSIS")
        print("=" * 55)
        print("1. Show all products")
        print("2. Show project summary")
        print("3. Show expensive products")
        print("4. Show highly rated products")
        print("5. NumPy statistical analysis")
        print("6. Generate graphs")
        print("7. Demonstrate OOP")
        print("8. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            show_products(products)

        elif choice == "2":
            show_summary(products)

        elif choice == "3":
            print("\nProducts above ₹2000:")
            for p in expensive_products(products):
                print(p["name"], "- ₹", int(p["price"]))

        elif choice == "4":
            print("\nProducts with rating >= 4.5:")
            for p in highly_rated_products(products):
                print(p["name"], "-", p["rating"])

        elif choice == "5":
            numpy_analysis(products)

        elif choice == "6":
            create_graphs(products)

        elif choice == "7":
            p = products[5]
            obj = ElectronicProduct(p["name"], p["category"], p["price"],
                                    p["rating"], p["purchases"])
            obj.display()
            print("Type:", obj.product_type())

        elif choice == "8":
            print("Thank you for using the project.")
            break

        else:
            print("Invalid choice. Please enter 1 to 8.")


if __name__ == "__main__":
    main()
