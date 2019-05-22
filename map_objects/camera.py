from constants import MAP_HEIGHT, MAP_WIDTH, CAMERA_WIDTH, CAMERA_HEIGHT


class Camera:
    def __init__(self):
        self.width = CAMERA_WIDTH
        self.height = CAMERA_HEIGHT
        self.x = 0
        self.y = 0

    def move_camera(self, target, fov):
        # new camera coordinates (top-left corner of the screen relative to the map)
        # coordinates so that the target is at the center of the screen
        x = target.x - self.width / 2
        y = target.y - self.height / 2
        # make sure the camera doesn't see outside the map
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > MAP_WIDTH - self.width - 1:
            x = MAP_WIDTH - self.width - 1
        if y > MAP_HEIGHT - self.height - 1:
            y = MAP_HEIGHT - self.height - 1
        if x != self.x or y != self.y:
            fov.recompute = True
        (self.x, self.y) = (x, y)

    def to_camera_coordinates(self, x, y):
        # convert coordinates on the map to coordinates on the screen
        (x, y) = (x - self.x, y - self.y)
        if (x < 0 or y < 0 or x >= self.width or y >= self.height):
            return (None, None)  # if it's outside the view, return nothing
        else:
            return (int(x), int(y))
