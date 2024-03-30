GREEN = 0
RED = 1


def create_grid(row = 0, col = 0) -> list[list[int]]:
    if not row:
        row = int(input("nombre de lignes : "))
    if not col:
        col = int(input("nombre de colonnes : "))
    return [[GREEN for _ in range(col)] for _ in range(row)]


def display_grid(grid: list[list[int]]) -> None:
    nb_col = len(grid[0])
    to_print = '    ' + "".join([f"|  {i} " + f"{' ' if i < 10 else ''}" for i in range(1, nb_col + 1)]) + "\n"
    for index, row in enumerate(grid):
        to_print += '----' + "|-----" * nb_col + "\n" \
                    + f" {index + 1} " \
                    + f"{' ' if index < 9 else ''}" \
                    + "".join([f"|  {col}  " for col in row]) + "\n"
    print(to_print)


def get_coords(grid: list[list[int]]) -> tuple[int, int]:
    max_row = len(grid)
    max_col = len(grid[0])
    while not 0 < (row := int(input("numéro ligne : "))) <= max_row:
        print("Pas dans la grille")
    while not 0 < (col := int(input("numéro colonne : "))) <= max_col:
        print("Pas dans la grille")
    return row - 1, col - 1


def is_victory(grid):
    for row in grid:
        for col in row:
            if col == GREEN:
                return False
    return True


def make_move(grid, row, col):
    max_row, max_col = len(grid), len(grid[0])
    for _r in (-1, 0, 1):
        for _c in (-1, 0, 1):
            if (_r != 0 or _c != 0) and 0 <= row + _r < max_row and 0 <= col + _c < max_col:
                grid[row + _r][col + _c] = (grid[row + _r][col + _c] + 1) % 2


def main():
    grid = create_grid()
    display_grid(grid)
    while not is_victory(grid):
        print("Nouveau tour :")
        row, col = get_coords(grid)
        # print(row, col)
        # grid[row][col] = RED
        make_move(grid, row, col)
        display_grid(grid)


if __name__ == '__main__':
    main()
