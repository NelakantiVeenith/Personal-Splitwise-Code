# main.py
import resources
import database

# import pandas as pd

print("Welcome to Personal Splitwise!")

username = input("Please enter your username: ")

conn = database.connect_to_database()

if conn is not None:
    cursor = conn.cursor()

    # Check if the user exists in the database
    cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{username}_head'")
    result = cursor.fetchone()

    if result:
        username_a = username + '_head'
        con = database.connect_to_database2(username_a)
        cursor = con.cursor()
        print("Welcome back, existing user!")
        # Continue with existing user logic
        print("Do you want to:")
        print("1. Select an existing group")
        print("2. Create a new group")
        user_choice = input("Enter the option number (1 or 2): ")
        if user_choice == "1":
            # Check for existing groups
            cursor.execute("SHOW TABLES LIKE '%\_grp'")
            existing_groups = [table[0] for table in cursor.fetchall()]

            if existing_groups:
                print("Existing groups:")
                for i, group in enumerate(existing_groups, start=1):
                    print(f"{i}. {group}")

                # Allow the user to select a group or perform other actions
                selected_group_index = int(
                    input("Enter the number of the group you want to select (or 0 to perform other "
                          "actions): "))

                if selected_group_index > 0 and selected_group_index <= len(existing_groups):
                    selected_group = existing_groups[selected_group_index - 1]
                    print(f"You selected group '{selected_group}'.")
                    # Implement logic to manage the selected group
                    print("Do you want to:")
                    print("1. View the group table")
                    print("2. Add a member to the group")
                    print("3. Add expense to split")
                    print("4. Add or Negate amount from an individual member of the group")
                    print("5. Exit")
                    user_choice_a = input("Enter the option number (1 or 2 or 3 or 4 or 5): ")

                    if user_choice_a == "1":
                        resources.view_group(selected_group, f"{username}_head")

                    elif user_choice_a == "2":
                        # Implement code to add a member to the group and create their table
                        resources.new_member(selected_group, f"{username}_head")

                    elif user_choice_a == "3":
                        resources.split_among(f"{username}_head", selected_group)
                        # Implement code to add an expense to split among the group
                        # ...

                    elif user_choice_a == "4":
                        # Implement code to add or negate an amount from an individual member of the group
                        resources.add_or_negate(f"{username}_head", selected_group)

                    elif user_choice_a == "5":
                        print("Exiting the group...")

                    else:
                        print("Invalid choice. Please select a valid option (1 or 2).")

                # Implement further actions related to the selected group
                else:
                    print("Invalid input. Please select a valid group.")
            else:
                print("You don't have any existing groups. You can create a new group.")

        elif user_choice == "2":
            resources.new_group(username_a)
    # Implement logic to create a new group or perform other actions
    else:
        print("User does not exist. Creating a new database for you...")
        # Create a new database with the user's name
        cursor.execute(f"CREATE DATABASE {username}_Head")
        print(f"Database {username}_Head created!")
        # Continue with new user logic
        cursor.execute(f"USE {username}_Head")  # Switch to the user's database

        # Create a new group table
        resources.new_group(f"{username}_head")

else:
    print("Unable to connect to the database. Please check your credentials.")
