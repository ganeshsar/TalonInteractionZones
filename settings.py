# Some changes may require a full restart of Talon.

# If true, interaction zones will be automatically shown when Talon is loaded
DEFAULT_SHOW = False
# The default file to load for interaction zones (without extension)
DEFAULT_FILE_NAME = "default"

# Adjust the transparency of the zones overlay images [0, 255], where 255 is full opaque and 0 is invisible.
ZONES_ALPHA = 100
# Adjust the transparency of the zones text [0, 255], where 255 is full opaque and 0 is invisible.
ZONES_TEXT_ALPHA = 255

# Customize the position in screen pixels of the zone toggle switch (0,0 is the top left of the screen)
ZONE_TOGGLE_OVERRIDE_POSITION = False
ZONE_TOGGLE_OVERRIDE_X = 500
ZONE_TOGGLE_OVERRIDE_Y = 500
# Customize the sizing in screen pixels of the zone toggle switch (0,0 is the top left of the screen)
ZONE_TOGGLE_OVERRIDE_SIZE = False
ZONE_TOGGLE_OVERRIDE_WIDTH = 60
ZONE_TOGGLE_OVERRIDE_HEIGHT = 30
# Adjust the transparency of the zones toggle switch (top centre of the screen) [0, 255], where 255 is full opaque and 0 is invisible.
ZONE_TOGGLE_SWITCH_ALPHA = 128

# If true, the current window name will be displayed right below the toggle switch for the zones (small text on top of screen)
# Useful if you want to use the AutoZone change feature or are wondering what the name of a window is to talon.
SHOW_WINDOW_NAME = False

# Automatically change the zones depending on the active window. This requires that the file name contains the name of the window.
# EX: For window "user - Visual Studio Code", the file name should probably contain Visual Studio Code.
# If no matching file can be found for a window, the file with the above set DEFAULT_FILE_NAME will be used.
EXPERIMENTAL_AUTO_ZONE_CHANGE = False
