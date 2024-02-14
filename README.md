# GestureController
Collection of hand/finger tracking tools that can be used as a gesture controller for interacting with computers. Simple controls include volume using a pinch/expansion of two fingers as well as general mouse functionality using fingertips.


## Mouse.py:
- Program tracks index finger tip and scales movement to mouse movement on screen
- Raising the pinky will activate a 'left click' wherever the cursor is

## VolumeControl.py
- Index and thumb tips are tracked
- Compute a distance to centerpoint between two finger tips
- Scale volume range within that distance - volume is modified based on movement of fingers