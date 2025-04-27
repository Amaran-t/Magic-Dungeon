def generate_world_map(width=100, height=100):
    grid = [["." for _ in range(width)] for _ in range(height)]

    # Нарисуем стену вокруг центра
    for i in range(40, 61):
        grid[40][i] = "W"
        grid[60][i] = "W"
        grid[i][40] = "W"
        grid[i][60] = "W"

    return grid
