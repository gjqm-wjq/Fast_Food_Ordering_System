# Fast Food Ordering System


# Declare Global Constant (Refer to Week 7 Topic 4.2 User Definition Function)
GST_RATE = 0.08  # 8%
DISCOUNTS = {
    "Student": 0.10,
    "Staff": 0.08,
    "Loyalty Member": 0.05
}

# Use nested dictionary to create a dataset (Refer to Week 12 Dictionary)

# Menu
menu = {
    "Burgers (FB10)": {
        # Outer dictionary (When user key in "Burgers" in the outer dictionary, the inner dictionary would appear {"B01", "B02", "B03", "B04"})
        "B01": ["Classic Beef Burger", 5.50],
        # Inner value is a list (The square brackets) Refer to week 8 (Array List Tuple)
        "B02": ["Chicken Burger", 5.00],
        "B03": ["Veggie Burger", 4.80],
        "B04": ["Spicy Chicken Burger", 5.30]
    },
    "Sides (FS20)": {
        "S01": ["French Fries", 2.50],
        "S02": ["Onion Rings", 2.80],
        "S03": ["Chicken Nuggets (6pc)", 3.50],
        "S04": ["Cheese Sticks (4pc)", 3.20]
    },
    "Drinks (FD30)": {
        "D01": ["Coke", 1.80],
        "D02": ["Sprite", 1.80],
        "D03": ["Ice Lemon Tea", 2.20],
        "D04": ["Mineral Water", 1.50]
    },
    "Desserts (FD40)": {
        "DS01": ["Chocolate Sundae", 2.80],
        "DS02": ["Vanilla Cone", 1.50],
        "DS03": ["Apple Pie", 2.30],
        "DS04": ["Strawberry Sundae", 2.80]
    },
    "Combos (FC50)": {
        "C01": ["Burger + Fries + Drink", 8.80],
        "C02": ["Nuggets + Fries + Drink", 8.50],
        "C03": ["Veggie Combo", 8.20],
        "C04": ["Kids Meal", 6.50]
    }
}

cart = {}  # Empty dictionary (This would store items that the user had selected)


# Stores items as {code: [name, quantity, price]}
# Example : {Burgers: [B01, 1, 5.50]}

def show_menu_by_category():
    while True:
        print("\nAvailable Categories:")
        print("0. Exit to Main Menu")
        categories = list(menu.keys())
        count = 1
        for category in categories:
            # Refer to Week 6 (Topic 3.3.2 Algorithm and Control Statements)
            print(f"{count}. {category}")
            count += 1

        choice = input("\nSelect a category by number (or '0' to cancel): ").strip()
        if choice == '0':
            return None

        try:
            # convert user choice from a string to number and subtract 1
            choice_idx = int(choice) - 1
            # list indexes start at 0, but we showed options starting at 1
            if 0 <= choice_idx < len(categories):
                # check if the number is valid input (between 0 to the total categories)
                selected_category = categories[choice_idx]
                print(f"\n{' ' + selected_category + ' Menu ':-^50}")
                print(f"{'Code':<4}  {'Item':^6}{'Price ($)':>38}")
                print("-" * 50)
                for code, (name, price) in menu[selected_category].items():# loop through all items in this category
                    print(f"{code:<4}:  {name:<25}{price:>17.2f}")
                return selected_category
            else:
                print("Invalid category number. Please try again.") #error handling
        except ValueError:
            print("Please enter a valid number.")#error handling


def add_to_cart():
    while True:
        # Refer back to Week 6 (3.3.1 Algorithm and Control Statements)
        category = show_menu_by_category()
        if not category:
            return  # User cancelled

        code = input("\nEnter item code (or '0' to go back): ").strip().upper() #Convert to uppercase to ensure item code matches regardless of input casing

        if code == '0':
            continue

        if code in menu[category]:
            try:
                qty = int(input(f"Enter quantity for {menu[category][code][0]} (1-100): "))
                if qty <= 0:
                    print("Quantity must be positive and not zero.")
                    continue
                elif qty > 100:
                    print("Maximum quantity allowed is 100. Please enter a smaller quantity.")
                    continue
                else:
                    if code in cart:
                        if cart[code][1] + qty > 100:
                           print(f"Cannot add {qty} more. Maximum quantity for {cart[code][0]} is 100.")
                           continue
                        else:
                            cart[code][1] += qty
                            action = "updated"
                    else:
                        cart[code] = [menu[category][code][0], qty, menu[category][code][1]]
                        action = "added"

                    print(f"\n{menu[category][code][0]} ({qty}x) {action} to cart.")
                    if input("\nAdd another item? (y/n): ").lower() != 'y':
                        break
            except ValueError:
                print("Please enter a valid quantity.") #error handling
        else:
            print("Invalid item code. Please try again. (etc; key in 'B01')") #error handling


def view_cart(detailed=True):
    if not cart:
        print("\nYour cart is empty.")
        return 0
    else:
        if detailed:
            print("\n{:^50}".format("------------------- Your Shopping Cart -------------------")) #User Interface
            print(f"{'Code':<6}{'Item':<25}{'Qty'}{'Price ($)':>11}{'Total ($)':>12}") #User Interface
            print("-" * 58)

        subtotal = 0
        for code, (name, qty, price) in cart.items():
            item_total = qty * price
            subtotal += item_total
            if detailed:
                print(f"{code:<4}: {name:<25}{qty:>3}{price:>8.2f}{item_total:>13.2f}") #User interface

        if detailed:
            #User Interface
            print("-" * 58)
            print(f"{'SUBTOTAL:':<49}{subtotal:>6.2f}")
        return subtotal


def edit_cart():
    while True:
        subtotal = view_cart()
        if not cart:
            return

        print("\nCart Options:")
        print("1. Remove Item")
        print("2. Update Quantity")
        print("3. Empty Cart")
        print("4. Back to Main Menu")


        # '.strip()' is to guards against accidental spaces, copy-pasted text with hidden newlines,
        choice = input("\nChoose an option (1-4): ").strip()

        if choice == '1':
            code = input("Enter item code to remove: ").upper()
            if code in cart:
                print(f"Removed {cart[code][0]} from cart.")
                del cart[code]
            else:
                print("Item not found in cart.")

        elif choice == '2':
            code = input("Enter item code to update: ").upper()
            if code in cart:
                try:
                    new_qty = int(input(f"New quantity for {cart[code][0]} (current: {cart[code][1]}): "))
                    if 0 < new_qty <= 100:
                        cart[code][1] = new_qty
                        print("Quantity updated.")
                    elif new_qty == 0:
                        del cart[code]
                        print("Item removed from cart.")
                    elif new_qty >100:
                        print("Quantity cannot exceed 100.")
                    else:
                        print("Quantity must be positive.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Item not found in cart.")

        elif choice == '3':
            confirm = input("Are you sure you want to empty your cart? (y/n): ").lower()
            if confirm == 'y':
                cart.clear()
                print("Cart emptied.")
                return

        elif choice == '4':
            return

        else:
            print("Invalid choice. Please try again.")


def checkout():
    subtotal = view_cart()
    if subtotal == 0:
        return

    while True:
        print("\nApply Discount (if applicable):")
        print("0. Exit back to Main Menu")
        print("1. Student (10%)")
        print("2. Staff (8%)")
        print("3. Loyalty Member (5%)")
        print("4. No Discount")

        discount_choice = input("\nSelect discount option (0-4): ").strip()
        discount_types = ["Student", "Staff", "Loyalty Member"]

        if discount_choice == "0":
            print("Returning back to Main Menu")
            return

        elif discount_choice in ['1', '2', '3']:
            discount_type = discount_types[int(discount_choice) - 1]
            discount_rate = DISCOUNTS[discount_type]
            break
        elif discount_choice == '4':
            discount_type = None
            discount_rate = 0
            break
        else:
            print("Invalid choice. Please try again.")

    discount_amt = subtotal * discount_rate
    gst_amt = (subtotal - discount_amt) * GST_RATE
    total = subtotal - discount_amt + gst_amt

    print("\n{:^58}".format("===================== FINAL RECEIPT ======================")) #User interface
    view_cart(detailed=True)
    if discount_rate > 0:
        #User interface
        print(f"{'DISCOUNT (' + discount_type + '):':<48}- {discount_amt:>5.2f}")
    print(f"{'GST (8%):':<49}{gst_amt:>6.2f}")
    print("=" * 58)
    print(f"{'TOTAL PAYABLE:':<49}{total:>6.2f}")
    print("\n{:^58}".format("--------------- Thank you for your order ! ---------------"))

    while True:
        again = input("\nWould you like to place another order? (y/n): ").strip().lower()
        if again == 'y':
            cart.clear()
            return
        elif again == 'n':
            print("\n Exiting system. Hope to see you soon!")
            exit()
        else:
            print("\n Invalid input. Please enter 'y' or 'n'.")


def main():
    while True:
        print("\n=== Welcome to the Fast Food Ordering System ===")
        for category, items in menu.items():
            print(f"\n============{category:^17}============")
            for code, (name, price) in items.items():
                print(f"{code:<4}: {name:<28}${price:>5.2f}")

        print("\n==== FAST FOOD ORDERING SYSTEM ====")
        print("1. Browse Menu & Add Items")
        print("2. View/Edit Cart")
        print("3. Checkout")
        print("4. Exit")

        choice = input("\nPlease select an option (1-4): ").strip()

        if choice == '1':
            add_to_cart()
        elif choice == '2':
            edit_cart()
        elif choice == '3':
            checkout()
        elif choice == '4':
            print("\n Thank you for using our ordering system. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()