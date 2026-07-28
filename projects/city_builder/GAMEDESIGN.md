**Purpose: city builder game design document**
## Overview
- pixel art car driving simulator
- isometric view

## Base

- [ ] Game Loop:
    - 1. start from a loaded (predefined map) or start from scratch:
        - 3 type of tiles: grass, water, sand
    - 2. player places entities: buildings, roads accordingly the tile type
    - 3. player instantiates and manages car entity
- [x] Assets Management:
    - premade kenney assets or made with `PixiEditor`
- [ ] Save System
- [ ] Time System
- [x] Input:
    - entity placement / tile selection : mouse
    - map movement: keyboard: arrow keys and WASD
- [ ] Entity Management
- [ ] Resource manager
    - loads from JSON constants (like game width, height) and path to assets
    - this allows a fast iteration when changing / trying parameters
- [ ] Multiple game screens
- [ ] Loading predefined maps
- [ ] Assets placement on the map

## Rendering

- [x] Camera
    - the camera scrolls with input from the user (arrow keys or WASD)
    - initially the camera moved when the mouse was hitting the border of the screen but the flow was not good. 
    - with this setup, the player uses both hands 
- [ ] ~~Shaders~~
- [ ] Animation 
- [ ] UI for tiles to place:
    - composed of a `UIContainer` that holds several `UIElement`
    - the `UIContainer` is globally positioned on the game screen while each `UIElement` are placed (locally) relative to the top left corner of the `UIContainer`
- [ ] ~~Particles~~

## World

- [ ] Player
- [ ] Collisions
- [ ] AI / PathFinding
- [ ] Scene

## GamePlay

- [ ] Stats
- [ ] ~~Combat~~
- [ ] Inventory
- [ ] Equipment
- [ ] Abilities

## Narrative

- [ ] Dialogue
- [ ] Quests
- [ ] NPC Schedules