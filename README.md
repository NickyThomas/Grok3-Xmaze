# Maze Runner 3D

Maze Runner 3D is a first-person maze navigation game built with Python, Pygame, and OpenGL. The objective is to navigate a textured 3D maze, reach the yellow goal cube, and avoid running out of time. The game features solid walls with accurate collision detection, a minimap, a countdown timer, jumping mechanics, and sprinting capabilities.

## Features

- **3D Graphics**: Rendered maze with textured walls, floor, and a ceiling featuring a blue sky with moving clouds.
- **Collision Detection**: Solid walls that prevent the player from passing through, ensuring a realistic navigation experience.
- **Minimap**: A top-left minimap showing the maze layout and player position.
- **Timer**: A 60-second countdown timer displayed at the top-middle of the screen in white text.
- **Movement**: WASD controls for movement, with sprinting (Left Shift) and jumping (Spacebar).
- **Mouse Look**: Mouse-based camera control for looking around.

## Controls

- **`W`**: Move forward
- **`S`**: Move backward
- **`A`**: Strafe left
- **`D`**: Strafe right
- **`Left Shift`**: Sprint (doubles movement speed)
- **`Spacebar`**: Jump (when on the ground)
- **`Mouse`**: Look around (horizontal and vertical camera rotation)
- **`Esc`**: Quit the game

## Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.6 or higher
- **Libraries**:
  - `Pygame`
  - `PyOpenGL`
  - `PyOpenGL_accelerate` (optional, for improved performance)
- **Dependencies**: Texture files (provided or custom):
  - `brick_texture.jpeg` (wall texture)
  - `floor_texture.jpeg` (floor texture)
  - `clouds.png` (ceiling clouds with transparency)

## Installation Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/NickyThomas/Grok3-Xmaze.git
cd Grok3-Xmaze


### 2. Set Up a Virtual Environment (Optional but Recommended)
Windows
python -m venv venv
venv\Scripts\activate

macOS/Linux
python3 -m venv venv
source venv/bin/activate


### 3. Install Dependencies
Install the required Python libraries:
* pip install pygame PyOpenGL PyOpenGL_accelerate

### 4. Prepare Texture Files
Place the texture files in an assets folder within the project directory:

* Create a folder named assets if it doesn’t exist
** mkdir assets

Copy the following files into assets/:

* brick_texture.jpeg
* floor_texture.jpeg
* clouds.png
* Alternatively, provide your own textures with the same names or modify the code to use different filenames.