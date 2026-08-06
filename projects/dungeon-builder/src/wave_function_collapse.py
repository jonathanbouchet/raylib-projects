import random
import copy

# 1. Define the unique tiles and their valid directional neighbors
# Format: 'TILE_NAME': {'UP': [...], 'DOWN': [...], 'LEFT': [...], 'RIGHT': [...]}
RULES = {
    '🌊': {'UP': ['🌊', '🏖️'], 'DOWN': ['🌊', '🏖️'], 'LEFT': ['🌊', '🏖️'], 'RIGHT': ['🌊', '🏖️']},
    '🏖️': {'UP': ['🌊', '🏖️', '🌲'], 'DOWN': ['🌊', '🏖️', '🌲'], 'LEFT': ['🌊', '🏖️', '🌲'], 'RIGHT': ['🌊', '🏖️', '🌲']},
    '🌲': {'UP': ['🏖️', '🌲', '🏔️'], 'DOWN': ['🏖️', '🌲', '🏔️'], 'LEFT': ['🏖️', '🌲', '🏔️'], 'RIGHT': ['🏖️', '🌲', '🏔️']},
    '🏔️': {'UP': ['🌲', '🏔️'], 'DOWN': ['🌲', '🏔️'], 'LEFT': ['🌲', '🏔️'], 'RIGHT': ['🌲', '🏔️']}
}

TILES = list(RULES.keys())
DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}
OPPOSITE = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT'
}

class WFCGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Initialize grid in a full superposition state (all tiles are possible everywhere)
        self.grid = [[copy.deepcopy(TILES) for _ in range(width)] for _ in range(height)]

    def is_collapsed(self):
        """Checks if all cells have narrowed down to exactly one state."""
        return all(len(self.grid[r][c]) == 1 for r in range(self.height) for c in range(self.width))

    def get_lowest_entropy_coords(self):
        """Finds uncollapsed cells with the fewest possible remaining choices."""
        min_entropy = float('inf')
        candidates = []

        for r in range(self.height):
            for c in range(self.width):
                options_count = len(self.grid[r][c])
                if options_count > 1: # Ignore fully collapsed cells
                    if options_count < min_entropy:
                        min_entropy = options_count
                        candidates = [(r, c)]
                    elif options_count == min_entropy:
                        candidates.append((r, c))
        
        return random.choice(candidates) if candidates else None

    def collapse_cell(self, row, col):
        """Forces a single random valid option onto the selected cell."""
        if not self.grid[row][col]:
            raise ValueError("Contradiction reached: A cell has 0 possible states.")
        chosen_tile = random.choice(self.grid[row][col])
        self.grid[row][col] = [chosen_tile]
        return row, col

    def propagate(self, start_row, start_col):
        """Propagates constraints outwards to update neighbors recursively."""
        queue = [(start_row, start_col)]

        while queue:
            r, c = queue.pop(0)
            current_options = self.grid[r][c]

            for direction, (dr, dc) in DIRECTIONS.items():
                nr, nc = r + dr, c + dc

                # Verify neighbor boundary limits
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    neighbor_options = self.grid[nr][nc]
                    if len(neighbor_options) <= 1:
                        continue # Already collapsed or empty, skip

                    # Find which neighbor choices are valid given current cell choices
                    valid_neighbor_tiles = set()
                    for current_tile in current_options:
                        valid_neighbor_tiles.update(RULES[current_tile][direction])

                    # Filter out rules that violate constraints
                    filtered_options = [t for t in neighbor_options if t in valid_neighbor_tiles]

                    # If changes occurred, update neighbor and add it to queue to propagate further
                    if len(filtered_options) != len(neighbor_options):
                        if not filtered_options:
                            raise ValueError("Contradiction reached during propagation.")
                        self.grid[nr][nc] = filtered_options
                        queue.append((nr, nc))

    def run(self):
        """Executes the loop until complete or a contradiction occurs."""
        while not self.is_collapsed():
            coords = self.get_lowest_entropy_coords()
            if not coords:
                break
            try:
                r, c = self.collapse_cell(*coords)
                self.propagate(r, c)
            except ValueError:
                print("⚠️ Contradiction encountered! Restarting generation...")
                self.__init__(self.width, self.height) # Reset grid and retry

    def display(self):
        """Renders the grid layout cleanly to the console."""
        for row in self.grid:
            print(" ".join(cell[0] if len(cell) == 1 else "❓" for cell in row))
        print("\n" + "="*20 + "\n")

# Run an instance of the generator
if __name__ == "__main__":
    generator = WFCGrid(width=10, height=8)
    generator.run()
    generator.display()
