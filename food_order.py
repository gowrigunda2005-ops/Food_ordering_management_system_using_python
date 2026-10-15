
from datetime import date


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1245"

users = [
    {
        "name": "User One",
        "mobile": "1234567890",
        "username": "user1",
        "password": "1234"
    }
]

restaurants = ["Food Plaza", "Spice Hub"]

food_items = [
    {"name": "Pizza", "price": 200.0, "cost": 100.0, "restaurant": "Food Plaza"},
    {"name": "Burger", "price": 100.0, "cost": 80.0, "restaurant": "Food Plaza"},
    {"name": "Fries", "price": 70.0, "cost": 50.0, "restaurant": "Spice Hub"}
]
orders = []
next_order_id = 1
def get_number(message, minimum=1):
    while True:
        try:
            number = int(input(message))
            if number < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            return number
        except ValueError:
            print("Invalid input. Please enter a number.")


def find_food(name):
    for item in food_items:
        if item["name"].lower() == name.lower():
            return item
    return None


def print_food_menu():
    if not food_items:
        print("No food items available.")
        return

    print("\n--- FOOD MENU ---")
    for item in food_items:
        print(
            f'{item["name"]} | Restaurant: {item["restaurant"]} | '
            f'Price: Rs.{item["price"]:.2f}'
        )



def admin_login():
    for attempt in range(3):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Admin login successful!")
            admin_dashboard()
            return

        print("Invalid username or password.")

    print("Maximum login attempts reached.")



def manage_restaurants():
    while True:
        print("\n--- MANAGE RESTAURANTS ---")
        print("1. View restaurants")
        print("2. Add restaurant")
        print("3. Remove restaurant")
        print("4. Back")

        choice = get_number("Choose option: ")

        if choice == 1:
            if restaurants:
                for restaurant in restaurants:
                    print("-", restaurant)
            else:
                print("No restaurants available.")

        elif choice == 2:
            name = input("Enter restaurant name: ").strip()

            if not name:
                print("Restaurant name cannot be empty.")
            elif any(r.lower() == name.lower() for r in restaurants):
                print("Restaurant already exists.")
            else:
                restaurants.append(name)
                print("Restaurant added successfully.")

        elif choice == 3:
            name = input("Enter restaurant name to remove: ").strip()
            match = next(
                (r for r in restaurants if r.lower() == name.lower()),
                None
            )

            if match is None:
                print("Restaurant not found.")
            elif any(
                item["restaurant"].lower() == match.lower()
                for item in food_items
            ):
                print("Remove its food items before removing this restaurant.")
            else:
                restaurants.remove(match)
                print("Restaurant removed.")

        elif choice == 4:
            break

        else:
            print("Invalid option.")



def manage_food_items():
    while True:
        print("\n--- MANAGE FOOD ITEMS ---")
        print("1. View food items")
        print("2. Add food item")
        print("3. Remove food item")
        print("4. View profit per item")
        print("5. Back")

        choice = get_number("Choose option: ")

        if choice == 1:
            print_food_menu()
            for item in food_items:
                print(f'Cost: Rs.{item["cost"]:.2f}')

        elif choice == 2:
            name = input("Enter food name: ").strip()

            if not name:
                print("Food name cannot be empty.")
                continue

            if find_food(name):
                print("Food item already exists.")
                continue

            if not restaurants:
                print("Please add a restaurant first.")
                continue

            print("Available restaurants:")
            for index, restaurant in enumerate(restaurants, start=1):
                print(f"{index}. {restaurant}")

            restaurant_number = get_number("Select restaurant number: ")

            if restaurant_number > len(restaurants):
                print("Invalid restaurant number.")
                continue

            try:
                price = float(input("Enter selling price: Rs."))
                cost = float(input("Enter cost price: Rs."))

                if price < 0 or cost < 0:
                    print("Prices cannot be negative.")
                    continue

            except ValueError:
                print("Enter valid prices.")
                continue

            food_items.append({
                "name": name,
                "price": price,
                "cost": cost,
                "restaurant": restaurants[restaurant_number - 1]
            })

            print("Food item added successfully.")

        elif choice == 3:
            name = input("Enter food item to remove: ").strip()
            item = find_food(name)

            if item:
                food_items.remove(item)
                print("Food item removed.")
            else:
                print("Food item not found.")

        elif choice == 4:
            if not food_items:
                print("No food items available.")

            for item in food_items:
                profit = item["price"] - item["cost"]
                print(f'{item["name"]}: Profit = Rs.{profit:.2f}')

        elif choice == 5:
            break

        else:
            print("Invalid option.")



def print_order(order):
    print(
        f'\nOrder ID: {order["id"]} | User: {order["user"]} | '
        f'Date: {order["date"]}'
    )

    for item in order["items"]:
        print(
            f'{item["name"]} x {item["quantity"]} = '
            f'Rs.{item["subtotal"]:.2f}'
        )

    print(f'Total: Rs.{order["total"]:.2f}')


def view_all_orders():
    print("\n--- ALL ORDERS ---")

    if not orders:
        print("No orders placed yet.")
        return

    for order in orders:
        print_order(order)


def show_reports():
    print("\n--- SYSTEM REPORTS ---")
    print("Total restaurants:", len(restaurants))
    print("Total food items:", len(food_items))
    print("Total orders:", len(orders))
    print("Total registered users:", len(users))


def dashboard_overview():
    total_sales = sum(order["total"] for order in orders)
    total_profit = sum(
        item["profit"] * item["quantity"]
        for order in orders
        for item in order["items"]
    )

    print("\n--- DASHBOARD OVERVIEW ---")
    print("Restaurants:", len(restaurants))
    print("Food items:", len(food_items))
    print("Orders:", len(orders))
    print("Users:", len(users))
    print(f"Total sales: Rs.{total_sales:.2f}")
    print(f"Estimated profit: Rs.{total_profit:.2f}")


def daily_profit_report():
    print("\n--- DAILY PROFIT REPORT ---")

    if not orders:
        print("No orders placed yet.")
        return

    daily_data = {}

    for order in orders:
        day = order["date"]
        daily_data.setdefault(day, {"sales": 0, "profit": 0})

        daily_data[day]["sales"] += order["total"]

        for item in order["items"]:
            daily_data[day]["profit"] += (
                item["profit"] * item["quantity"]
            )

    for day, data in sorted(daily_data.items()):
        print(f"\nDate: {day}")
        print(f'Sales: Rs.{data["sales"]:.2f}')
        print(f'Profit: Rs.{data["profit"]:.2f}')



def admin_dashboard():
    while True:
        print("\n========== ADMIN DASHBOARD ==========")
        print("1. Manage restaurants")
        print("2. Manage food items")
        print("3. View orders")
        print("4. Reports")
        print("5. Dashboard overview")
        print("6. Daily profit report")
        print("7. Logout")

        choice = get_number("Choose option: ")

        if choice == 1:
            manage_restaurants()
        elif choice == 2:
            manage_food_items()
        elif choice == 3:
            view_all_orders()
        elif choice == 4:
            show_reports()
        elif choice == 5:
            dashboard_overview()
        elif choice == 6:
            daily_profit_report()
        elif choice == 7:
            print("Admin logged out.")
            break
        else:
            print("Invalid option.")



def register_user():
    print("\n--- USER REGISTRATION ---")

    name = input("Enter your name: ").strip()
    mobile = input("Enter your mobile number: ").strip()
    username = input("Choose a username: ").strip()

    if not name or not username:
        print("Name and username are required.")
        return

    if not mobile.isdigit() or len(mobile) != 10:
        print("Enter a valid 10-digit mobile number.")
        return

    if any(u["username"].lower() == username.lower() for u in users):
        print("Username already exists.")
        return

    password = input("Choose a password: ")

    if not password:
        print("Password cannot be empty.")
        return

    users.append({
        "name": name,
        "mobile": mobile,
        "username": username,
        "password": password
    })

    print("Registration successful. Please log in.")



def user_login():
    for attempt in range(3):
        username = input("Enter username: ").strip()
        password = input("Enter password: ")

        current_user = next(
            (
                user for user in users
                if user["username"].lower() == username.lower()
                and user["password"] == password
            ),
            None
        )

        if current_user:
            print(f'Welcome, {current_user["name"]}!')
            user_dashboard(current_user)
            return

        print("Invalid username or password.")

    print("Maximum login attempts reached.")



def browse_restaurants():
    print("\n--- RESTAURANTS ---")

    if not restaurants:
        print("No restaurants available.")
        return

    for restaurant in restaurants:
        print("-", restaurant)


def add_to_cart(cart):
    if not food_items:
        print("No food items available.")
        return

    print_food_menu()
    name = input("Enter food item name: ").strip()
    item = find_food(name)

    if not item:
        print("Food item not found.")
        return

    quantity = get_number("Enter quantity: ")

    cart.append({
        "name": item["name"],
        "quantity": quantity
    })

    print("Item added to cart.")


def view_cart(cart):
    print("\n--- YOUR CART ---")

    if not cart:
        print("Your cart is empty.")
        return

    total = 0

    for cart_item in cart:
        item = find_food(cart_item["name"])

        if item:
            subtotal = item["price"] * cart_item["quantity"]
            total += subtotal
            print(
                f'{item["name"]} x {cart_item["quantity"]} '
                f'= Rs.{subtotal:.2f}'
            )

    print(f"Cart total: Rs.{total:.2f}")


def place_order(user, cart):
    global next_order_id

    if not cart:
        print("Your cart is empty.")
        return

    order_items = []
    total = 0

    for cart_item in cart:
        item = find_food(cart_item["name"])

        if item is None:
            continue

        quantity = cart_item["quantity"]
        subtotal = item["price"] * quantity
        profit = item["price"] - item["cost"]

        order_items.append({
            "name": item["name"],
            "quantity": quantity,
            "price": item["price"],
            "subtotal": subtotal,
            "profit": profit
        })

        total += subtotal

    if not order_items:
        print("No valid items in the cart.")
        return

    order = {
        "id": next_order_id,
        "user": user["username"],
        "date": str(date.today()),
        "items": order_items,
        "total": total
    }

    orders.append(order)
    next_order_id += 1
    cart.clear()

    print("Order placed successfully!")
    print(f'Your order ID is {order["id"]}.')
    print(f"Total amount: Rs.{total:.2f}")


def view_my_orders(user):
    print("\n--- MY ORDER HISTORY ---")

    my_orders = [
        order for order in orders
        if order["user"] == user["username"]
    ]

    if not my_orders:
        print("You have not placed any orders yet.")
        return

    for order in my_orders:
        print_order(order)


def user_dashboard(user):
    cart = []

    while True:
        print("\n========== USER DASHBOARD ==========")
        print("1. Browse restaurants")
        print("2. View food menu")
        print("3. Add item to cart")
        print("4. View cart")
        print("5. Place order")
        print("6. View my orders")
        print("7. Logout")

        choice = get_number("Choose option: ")

        if choice == 1:
            browse_restaurants()
        elif choice == 2:
            print_food_menu()
        elif choice == 3:
            add_to_cart(cart)
        elif choice == 4:
            view_cart(cart)
        elif choice == 5:
            place_order(user, cart)
        elif choice == 6:
            view_my_orders(user)
        elif choice == 7:
            print("User logged out.")
            break
        else:
            print("Invalid option.")



def main():
    while True:
        print("\n===== FOOD ORDERING MANAGEMENT SYSTEM =====")
        print("1. Admin Login")
        print("2. User Login")
        print("3. User Registration")
        print("4. Exit")

        choice = get_number("Choose option: ")

        if choice == 1:
            admin_login()
        elif choice == 2:
            user_login()
        elif choice == 3:
            register_user()
        elif choice == 4:
            print("Thank you for using our system!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
