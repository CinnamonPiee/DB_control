import questionary
from database.db_manager import DBManager


def main_dbms() -> None:
    while True:
        print()
        answer = questionary.select(
            "Choose a DBMS:",
            choices=[
                "MySQL",
                "EXIT",
            ],
        ).ask()
        if answer == "EXIT":
            print()
            print("Goodbye!")
            break
        else:
            host = questionary.text("Enter host:").ask()
            user = questionary.text("Enter user:").ask()
            password = questionary.password("Enter password:").ask()
            db_manager = DBManager(dbm=answer)
            if db_manager.connect(host=host, user=user, password=password):
                main(dbm=answer, host=host, user=user, password=password)


def main(dbm: str = None, host: str = None, user: str = None, password: str = None):
    db_manager = DBManager(dbm=dbm)
    while True:
        print()
        answer = questionary.select(
            "===== Menu =====",
            choices=[
                "1. Create database",
                "2. Create table",
                "3. Add data",
                "4. View data",
                "5. Edit data",
                "6. Delete data",
                "7. Delete table",
                "8. Delete database",
                "EXIT",
            ],
        ).ask()

        if answer == "1. Create database":
            db_name = questionary.text("Enter database name:").ask()
            db_manager.create_database(db_name, user, host, password)

        elif answer == "2. Create table":
            data: list = {}
            db_name = questionary.text("Enter database name:").ask()
            if db_manager.check_db_name(db_name, user, host, password):
                table_name = questionary.text("Enter table name: ").ask()
                fields_count = questionary.select(
                    "Enter how much field you need create: ",
                    choices=[
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "8",
                        "10",
                        "Another count",
                        "EXIT",
                    ],
                ).ask()
                if fields_count == "Another count":
                    fields_count = questionary.text("Enter count for fields: ").ask()
                elif fields_count == "EXIT":
                    break
                for i in range(int(fields_count)):
                    field_name = questionary.text("Enter field name:").ask()
                    field_type = questionary.select(
                        "Choose field type: ",
                        choices=[
                            "TINYINT",
                            "SMALLINT",
                            "MEDIUMINT",
                            "INT",
                            "BIGINT",
                            "FLOAT",
                            "DOUBLE",
                            "DECIMAL",
                            "CHAR",
                            "VARCHAR",
                            "TEXT",
                            "BINARY",
                            "VARBINARY",
                            "DATE",
                            "YEAR",
                            "TIME",
                            "DATETIME",
                            "TIMESTAMP",
                            "ENUM",
                            "SET",
                            "EXIT",
                        ],
                    ).ask()
                    if field_type == "DECIMAL":
                        field_type_total_number = questionary.text("Enter total number of digits: ").ask()
                        field_type_decimal_places= questionary.text("Enter number of decimal places: ").ask()
                        field_type += f"({field_type_total_number}, {field_type_decimal_places})"
                    elif field_type == "CHAR":
                        field_type_fixed_string_length = questionary.text("Enter fixed string length (from 0 to 255): ").ask()
                        field_type += f"({field_type_fixed_string_length})"
                    elif field_type == "VARCHAR":
                        field_type_maximum_string_length = questionary.text("Enter maximum string length (from 0 to 65,535): ").ask()
                        field_type += f"({field_type_maximum_string_length})" 
                    elif field_type == "EXIT":
                        break
                    field_type_more: questionary.Question = questionary.checkbox(
                        "Choose additional options: ",
                        choices=[
                            "NOT NULL",
                            "NULL",
                            "UNIQUE",
                        ],
                    ).ask()
                    data[field_name] = [field_type, field_type_more]
                db_manager.create_table(table_name, data, db_name, user, host, password)
            else:
                break

        elif answer == "3. Add data":
            db_name = questionary.text("Enter database name:").ask()
            if db_manager.check_db_name(db_name, user, host, password):
                table_name = questionary.text("Enter table name: ").ask()
            else:
                break

        elif answer == "4. View data":
            pass

        elif answer == "5. Edit data":
            pass

        elif answer == "6. Delete data":
            pass

        elif answer == "7. Delete table":
            pass

        elif answer == "8. Delete database":
            pass

        elif answer == "EXIT":
            break


if __name__ == "__main__":
    main_dbms()