# app.py
from getpass import getpass

from Database.ConnectDB import ConnectDB
from Database.AddDB import AddDB
from Information.UserInformation import UserInformation
from Information.InputInformation import InputInformation
from Database.SaveDB import SaveDB
from Database.RecallDB import RecallDB
from Dashboard import Dashboard


def setup_database(connector: ConnectDB) -> None:
    add_db = AddDB(connector)
    add_db.setup_all()


def login_flow(user_info: UserInformation) -> int:
    """
    シンプルなログインフロー。
    戻り値: user_id
    """
    while True:
        print("1) Login  2) Register  0) Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = getpass("Password: ")
            user_id = user_info.authenticate(username, password)
            if user_id is not None:
                print("Login success.")
                return user_id
            print("Login failed.")
        elif choice == "2":
            username = input("New username: ").strip()
            password = getpass("New password: ")
            if user_info.register(username, password):
                print("Register success. Please login.")
            else:
                print("Register failed (maybe already exists).")
        elif choice == "0":
            raise SystemExit
        else:
            print("Invalid choice.")


def input_loop(user_id: int, save_db: SaveDB, dashboard: Dashboard) -> None:
    """
    簡易なCLI入力ループ
    """
    while True:
        print("\n1) Add record  2) Show dashboard  0) Exit")
        choice = input("Select: ").strip()

        if choice == "1":
            date_str = input("Date (YYYY-MM-DD): ").strip()
            price_str = input("Price: ").strip()
            item = input("Item: ").strip()

            info = InputInformation.from_strings(user_id, date_str, price_str, item)
            if save_db.save_record(info):
                print("Saved.")
            else:
                print("Save failed.")
        elif choice == "2":
            dashboard.show_all(user_id)
        elif choice == "0":
            print("Bye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    # DB接続設定（ConnectDB 内のデフォルトを変えてもOK）
    connector = ConnectDB()
    setup_database(connector)

    user_info = UserInformation(connector)
    user_id = login_flow(user_info)

    save_db = SaveDB(connector)
    recall_db = RecallDB(connector)
    dashboard = Dashboard(recall_db)

    input_loop(user_id, save_db, dashboard)
