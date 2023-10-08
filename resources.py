import database
import pandas as pd
import datetime


def new_group(username):
    con = database.connect_to_database2(username)
    cursor = con.cursor()
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
    con.commit()

    while True:
        print("\nSelect an option:")
        print("1. See outstanding balances")
        print("2. Add an expense to split among the group")
        print("3. Add an individual expense")
        print("4. Add an amount paid by other members")
        print("5. Exit")

        option = input("Enter the option number: ")

        if option == "1":
            view_group(group_table_name, username)
            # Implement code to see outstanding balances
            pass
        elif option == "2":
            split_among(username, group_table_name)
            # Implement code to add an expense to split among the group
            pass
        elif option == "3":
            add_or_negate(username, group_table_name)
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
    con.close()
    # Continue with the rest of the code for the main menu, group management, etc.
    cursor.close()
    con.close()


def view_group(selected_group, username):
    con = database.connect_to_database2(username)
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM {selected_group}")
    group_data = cursor.fetchall()
    if group_data:
        print("Group Members:")
        df = pd.DataFrame(group_data, columns=["S_no", "Name", "Outstanding_Due"])
        for i, row in df.iterrows():
            member_name = row["Name"]
            member_table_name = f"{member_name}_mem"

            # Fetch and sum the Aggregate column from the member's table
            cursor.execute(f"SELECT SUM(Aggregate) FROM {member_table_name}")
            sum_aggregate = cursor.fetchone()[0]

            # Update the Outstanding_Due column in the group table with the sum
            df.at[i, "Outstanding_Due"] = sum_aggregate
        print(df)
    else:
        print("The selected group is empty.")


def new_member(selected_group, username):
    con = database.connect_to_database2(username)
    cursor = con.cursor()
    member_name = input("Enter the full name of the new member: ")
    cursor.execute(
        f"INSERT INTO {selected_group} (Name, Outstanding_Due) VALUES ('{member_name}', 0.0)")
    member_table_name = f"{member_name}_mem"
    cursor.execute(f"CREATE TABLE {member_table_name} (Date DATE, Mem_Spent FLOAT, You_Spent FLOAT, Aggregate FLOAT)")
    print(f"Member '{member_name}' added to the group, and a table '{member_table_name}' created.")

    con.commit()


def split_among(username, selected_group):
    con = database.connect_to_database2(username)
    cursor = con.cursor()

    try:
        amount_to_split = float(input("Enter the amount to split among the members: "))

        # Fetch the members of the selected group
        cursor.execute(f"SELECT Name FROM {selected_group}")
        group_members = cursor.fetchall()

        if group_members:
            num_members = len(group_members)

            # Calculate the amount to be added or subtracted from each member
            amount_per_member = amount_to_split / num_members
            amount_per_member = round(amount_per_member, 2)

            # Get the current date dynamically
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")

            # Iterate through each member and update their respective table
            for member in group_members:
                member_name = member[0]
                member_table_name = f"{member_name}_mem"

                # Update the member's table with the current date, Mem_Spent = 0, You_Spent = -amount_per_member
                # and calculate Aggregate as the sum of Mem_Spent and You_Spent
                cursor.execute(f"INSERT INTO {member_table_name} (Date, Mem_Spent, You_Spent, Aggregate) "
                               f"VALUES ('{current_date}', 0, {-amount_per_member}, 0 - {amount_per_member})")
                print(f"Added expense of {amount_per_member} to '{member_name}'")

            # Commit changes after updating all member tables
            con.commit()

        else:
            print("There are no members in the group to split the expense.")

    except ValueError:
        print("Invalid input. Please enter a valid numerical amount.")


def add_or_negate(username, selected_group):
    con = database.connect_to_database2(username)
    cursor = con.cursor()
    t = 1
    while t == 1:
        # Ask the user whether they want to add or negate the amount
        print("Do you want to:")
        print("1. Add the amount you spent on an individual member")
        print("2. Negate an amount from an individual member")
        user_action = input("Enter the option number (1 or 2): ")

        # Fetch the members of the selected group
        cursor.execute(f"SELECT Name FROM {selected_group}")
        group_members = cursor.fetchall()

        if group_members:
            # Display the list of group members
            print("Select a member:")
            for i, member in enumerate(group_members, start=1):
                print(f"{i}. {member[0]}")

            try:
                member_choice = int(input("Enter the number of the member: "))

                if 1 <= member_choice <= len(group_members):
                    selected_member_name = group_members[member_choice - 1][0]
                    member_table_name = f"{selected_member_name}_mem"
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

                    try:
                        amount = float(input("Enter the amount (up to 2 decimal places): "))
                        amount = round(amount, 2)

                        if user_action == "1":
                            # Adding amount to the member
                            cursor.execute(f"INSERT INTO {member_table_name} (Date, Mem_Spent, You_Spent, Aggregate) "
                                           f"VALUES ('{current_date}', 0, {-amount}, 0 - {-amount})")
                            print(f"Added {amount} to '{selected_member_name}'")

                        elif user_action == "2":
                            # Negating amount from the member
                            cursor.execute(f"INSERT INTO {member_table_name} (Date, Mem_Spent, You_Spent, Aggregate) "
                                           f"VALUES ('{current_date}', {amount}, 0, {amount})")
                            print(f"Negated {amount} from '{selected_member_name}'")

                        # Commit changes after updating the member's table
                        con.commit()

                    except ValueError:
                        print("Invalid amount. Please enter a valid numerical amount.")

                else:
                    print("Invalid member selection. Please choose a valid member.")

            except ValueError:
                print("Invalid input for member selection. Please enter a valid number.")

        else:
            print("There are no members in the group to perform this action.")

        t = int(input("Enter any number expect 1 to exit \n 1 to continue"))
