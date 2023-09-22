from irobot_edu_sdk.backend import bluetooth
from irobot_edu_sdk.robots import event, hand_over, Robot, Root
from irobot_edu_sdk.music import Note
from color import Color


class Robo:
    STATE_HOLDERS = [
        "LEFT_BUMPER",
        "RIGHT_BUMPER",
        "TOP_LEFT_TOUCH",
        "BOTTOM_LEFT_TOUCH",
    ]

    shape_sides: int = 0
    shape_sidelength: int = 0

    base_speed: int = 4

    currently_running: int = False

    state_lb = None
    state_rb = None
    state_tlt = None
    state_blt = None

    r: Root = None

    def __init__(self, r: Root):
        self.r = r

    def set_defaults(self):
        self.shape_sides = 0
        self.shape_sidelength = 0

    async def set_color(self, color: Color):
        await self.r.set_lights_rgb(color.r, color.g, color.b)

    async def set_state(self, state_holder, new_state):
        if state_holder == self.STATE_HOLDERS[0]:
            self.state_lb = new_state
        elif state_holder == self.STATE_HOLDERS[1]:
            self.state_rb = new_state
        elif state_holder == self.STATE_HOLDERS[2]:
            self.state_tlt = new_state
        elif state_holder == self.STATE_HOLDERS[3]:
            self.state_blt = new_state

    async def draw_regular_shape(self):
        """Draws the final shape
        """
        print(f"SIDES: {self.shape_sides}, " +
              f"LENGTH: {self.shape_sidelength * self.base_speed}")

        if self.shape_sides < 3:
            self.shape_sides = 3

        if self.shape_sidelength < 1:
            self.shape_sidelength = 1

        await self.r.set_marker(self.r.MARKER_DOWN)

        for side in range(self.shape_sides):
            await self.r.move(self.base_speed * self.shape_sidelength)
            await self.r.turn_right(360 / self.shape_sides)

        await self.r.set_marker(self.r.MARKER_UP)

    async def play_song(self, song: [(Note, float)]):
        for note in song:
            print(note[0], note[1])
            await self.r.play_note(note[0], note[1])
