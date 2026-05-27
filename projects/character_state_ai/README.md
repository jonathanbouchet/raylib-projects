## Motivatiob
- a player / enemy chase demo

### Requirements
- [ ] both characters should derive from a base class
- [ ] state machine for both movement: `idle`, `walk`, `run` and status: `patrol`, `chase`, `dead` 
- [ ] use pathfinding for the enemy movement: [python-pathfinding](https://github.com/brean/python-pathfinding) 
- [ ] other solutions for pathfinding:
    - use `way points` for the AI to patrol 
    - use fix trajectory (circle)
- [ ] some debug UI visuals
- [x] idea for the player's control -> through mouse click, so that I can experime t with `Lerp`