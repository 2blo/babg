import csv
from typing import Optional, Literal, Dict, Any
import matplotlib.pyplot as plt

Graph = Literal["bullet_speed"]

_SPEED_COL = "SPD"
_NAME_COL = "Name"

def _speed_col_to_int(col_value: str) -> Optional[int]:
    return int(col_value.split(" ")[0])

def _exclude_weapon(row: Dict[str, Any], graph: Graph) -> bool:
    if graph == "bullet_speed":
        if row[_SPEED_COL] is None or row[_SPEED_COL] == "":
            return True
        is_ar_or_sr = _speed_col_to_int(row[_SPEED_COL]) > 500
        if not is_ar_or_sr:
            return True
        return False

def visualize(file_path, graph: Graph): 
    names = []
    bullet_speeds = []

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if _exclude_weapon(row, graph):
                continue
            name = row[_NAME_COL]
            bullet_speed = _speed_col_to_int(row[_SPEED_COL])  # Assuming 'Bullet Speed' is the column header

            names.append(name)
            bullet_speeds.append(bullet_speed)

            # Perform operations with the extracted data
            print(f"Weapon: {name}, Bullet Speed: {bullet_speed}")

    # Sorting by bullet speeds
    names, bullet_speeds = zip(*sorted(zip(names, bullet_speeds), key=lambda x: x[1]))

    # Plotting the graph with rotated x-axis tick labels
    plt.bar(names, bullet_speeds, color='green')
    plt.xlabel('Weapon')
    plt.ylabel('Bullet Speed')
    plt.title('Bullet Speed for Each Weapon')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis tick labels
    plt.tight_layout()  # Adjust layout to prevent clipping of rotated x-axis tick labels
    plt.show()

if __name__ == "__main__":
    csv_file_path = "data/weapons_raw.csv"
    graph = "bullet_speed"

    try:
        visualize(csv_file_path, graph=graph)
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
    except csv.Error as e:
        print(f"Error reading CSV: {e}")
