# main.py
import database
import pandas as pd

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

        # Check for existing groups
        cursor.execute("SHOW TABLES LIKE '%\_grp'")
        existing_groups = [table[0] for table in cursor.fetchall()]

        if existing_groups:
            print("Existing groups:")
            for i, group in enumerate(existing_groups, start=1):
                print(f"{i}. {group}")

            # Allow the user to select a group or perform other actions
            selected_group_index = int(input("Enter the number of the group you want to select (or 0 to perform other "
                                             "actions): "))

            if selected_group_index > 0 and selected_group_index <= len(existing_groups):
                selected_group = existing_groups[selected_group_index - 1]
                print(f"You selected group '{selected_group}'.")
                # Implement logic to manage the selected group
                cursor.execute(f"SELECT * FROM {selected_group}")
                group_data = cursor.fetchall()

                if group_data:
                    print("Group Members:")
                    df = pd.DataFrame(group_data, columns=["S_no", "Name", "Outstanding_Due"])
                    print(df)
                else:
                    print("The selected group is empty.")

                # Implement further actions related to the selected group
            else:
                print("Invalid input. Please select a valid group.")
        else:
            print("You don't have any existing groups. You can create a new group.")
            # Implement logic to create a new group or perform other actions
    else:
        print("User does not exist. Creating a new database for you...")
        # Create a new database with the user's name
        cursor.execute(f"CREATE DATABASE {username}_Head")
        print(f"Database {username}_Head created!")
        # Continue with new user logic
        cursor.execute(f"USE {username}_Head")  # Switch to the user's database

        # Create a new group table
        group_name = input("Enter the name of your new group: ")
        group_table_name = f"{group_name}_grp"
        cursor.execute(f"CREATE TABLE {group_table_name} (S_no INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), "
                       f"Outstanding_Due FLOAT)")
        print(f"Group '{group_name}' created!")

        # Add members to the group
        num_members = int(input("How many members do you want to add to the group? "))
        for i in range(num_members):
            member_name = input(f"Enter the full name of member {i + 1}: ")
            cursor.execute(f"INSERT INTO {group_table_name} (Name, Outstanding_Due) VALUES ('{member_name}', 0.0)")
            member_table_name = f"{member_name}_mem"
            cursor.execute(f"CREATE TABLE {member_table_name} (Date DATE, Mem_Spent FLOAT, You_Spent FLOAT, Aggregate "
                           f"FLOAT)")
            print(f"Member '{member_name}' added to the group, and a table '{member_table_name}' created.")

        # Commit changes and close the cursor and connection
        conn.commit()
    while True:
        print("\nSelect an option:")
        print("1. See outstanding balances")
        print("2. Add an expense to split among the group")
        print("3. Add an individual expense")
        print("4. Add an amount paid by other members")
        print("5. Exit")

        option = input("Enter the option number: ")

        if option == "1":
            # Implement code to see outstanding balances
            pass
        elif option == "2":
            # Implement code to add an expense to split among the group
            pass
        elif option == "3":
            # Implement code to add an individual expense
            pass
        elif option == "4":
            # Implement code to add an amount paid by other members
            pass
        elif option == "5":
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose a valid option (1-5).")

    cursor.close()
    conn.close()
    # Continue with the rest of the code for the main menu, group management, etc.
    cursor.close()
    conn.close()
else:
    print("Unable to connect to the database. Please check your credentials.")
