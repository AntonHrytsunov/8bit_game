import datetime
import os

SAVE_FOLDER = "../game_save"
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

def get_latest_save():
    """Повертає найновіший файл збереження або None, якщо файлів нема."""
    saves = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".sav")]
    return max(saves, default=None, key=lambda f: os.path.getctime(os.path.join(SAVE_FOLDER, f)))

def create_new_save():
    """Створює новий файл збереження з поточною датою та часом у назві."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_path = os.path.join(SAVE_FOLDER, f"save_{timestamp}.sav")
    with open(save_path, "w") as file:
        file.write("{\"progress\": 0}")  # Мінімальне тестове збереження
        print("Створено новий файл збереження.")
    return save_path

def delete_all_saves():
    """Видаляє всі файли збереження перед початком нової гри."""
    for file in os.listdir(SAVE_FOLDER):
        file_path = os.path.join(SAVE_FOLDER, file)
        if os.path.isfile(file_path) and file.endswith(".sav"):
            os.remove(file_path)
    print("Всі збереження видалено.")
