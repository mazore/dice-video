# Dice Video
Live camera and video conversion to dice


## Usage


Download or clone the code, and run`pip install opencv-python`, and `pip install pygame` in command line

## Parameters


line6:  `DIE_WIDTH (line 6)`: Pixel width of the dice

line7:  `DRAW_PIXELS_NOT_CIRCLES`: Draw one pixels for dot (DIE_WIDTH < 20)

line8:  `RESOLUTION_FACTOR`: How much bigger the window is than the source

line9:  `BRIGHTNESS_STRETCH`: Exaggerate mid-range brightness

line10: `BRIGHTNESS_ADJUSTMENT`: Make final image brighter (increase) or darker (decrease)

line11: `INVERTED`: Invert brightness

line13 & 14: Camera input (13) or File input (14)

line53: Enable dice backgrounds

line61: Change dot color

line67 & 71: Change line color

line84: Change background color

line88: Un-comment to save images to a "Render" folder
