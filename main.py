from IPython.display import HTML

# Simulation parameters
field_width = 12
field_height = 9
obstacles_list = [(2, 2), (3, 5), (7, 1), (5, 5)]
start_row = 0
start_col = 0
simulation_speed = 150  # in milliseconds

class FarmField:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)  # 0: unvisited, 1: visited, -1: obstacle
        if obstacles:
            for obs_row, obs_col in obstacles:
                if 0 <= obs_row < self.height and 0 <= obs_col < self.width:
                    self.grid[obs_row, obs_col] = -1

    def mark_visited(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width and self.grid[row, col] != -1:
            self.grid[row, col] = 1

    def is_obstacle(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row, col] == -1
        return False

class Rover:
    def __init__(self, farm_field, start_row, start_col):
        self.farm_field = farm_field
        self.current_row = start_row
        self.current_col = start_col
        self.path_history = []

    def update_position(self, new_row, new_col):
        self.current_row = new_row
        self.current_col = new_col
        self.path_history.append((new_col, new_row)) # Store as (x, y) for plotting

    def move_zigzag(self):
        path = []
        for row in range(self.farm_field.height):
            if row % 2 == 0:
                for col in range(self.farm_field.width):
                    if not self.farm_field.is_obstacle(row, col):
                        path.append((row, col))
            else:
                for col in range(self.farm_field.width - 1, -1, -1):
                    if not self.farm_field.is_obstacle(row, col):
                        path.append((row, col))
        return path

# Instantiate the field and rover
field = FarmField(field_width, field_height, obstacles=obstacles_list)
rover = Rover(field, start_row, start_col)
zigzag_path = rover.move_zigzag()

# Set up the animation
fig, ax = plt.subplots(figsize=(field_width, field_height))
cmap = plt.cm.colors.ListedColormap(['white', 'green', 'black'])
bounds = [-1.5, -0.5, 0.5, 1.5]
norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
im = ax.imshow(field.grid, cmap=cmap, norm=norm, origin='lower', extent=[0, field_width, 0, field_height])
ax.set_title('Farm Field Simulation')
ax.set_xlabel('Width')
ax.set_ylabel('Height')
ax.set_xticks(np.arange(field_width + 1))
ax.set_yticks(np.arange(field_height + 1))
ax.grid(True, which='both', color='gray', linewidth=0.5)
rover_marker, = ax.plot([], [], 'ro', markersize=10)
rover_trail, = ax.plot([], [], 'r-', linewidth=2)

def update(frame):
    if frame < len(zigzag_path):
        row, col = zigzag_path[frame]
        rover.update_position(row, col)
        field.mark_visited(row, col)

    im.set_data(field.grid)
    rover_marker.set_data([col + 0.5], [row + 0.5])

    if rover.path_history:
        trail_x, trail_y = zip(*rover.path_history)
        rover_trail.set_data([x + 0.5 for x in trail_x], [y + 0.5 for y in trail_y])

    return im, rover_marker, rover_trail

ani = animation.FuncAnimation(fig, update, frames=len(zigzag_path), interval=simulation_speed, blit=True)

HTML(ani.to_jshtml())