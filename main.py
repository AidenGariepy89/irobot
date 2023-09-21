from irobot_edu_sdk.backend import bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root
from irobot_edu_sdk.music import Note

robot: Robot = Root(bluetooth.Bluetooth())

intro_song = [
    (Note.C5, 0.26), (Note.C5, 0.13),
    (Note.D5, 0.26), (Note.E5, 0.13),
    (Note.G5, 0.26), (Note.E5, 0.13),
    (Note.D5, 0.26), (Note.F5, 0.13),
    (Note.E5, 0.26), (Note.C5, 0.13),
    (Note.C5, 0.13), (Note.D5, 0.13), (Note.E5, 0.13),
    (Note.D5, 0.26), (Note.B4, 0.13),
    (Note.G4, 0.26), (Note.E4, 0.13),
    (Note.C4, 0.39)
]

confirm_song = [
    (Note.E5, 0.1), (Note.G5, 0.1),
    (Note.C6, 0.1), (Note.E6, 0.1),
    (Note.G6, 0.1), (Note.C7, 0.1),
    (Note.G6, 0.1), (Note.E6, 0.1),
    (Note.C6, 0.1), (Note.G5, 0.1),
    (Note.E5, 0.1), (Note.C5, 0.1)
]

stages = [
    'side',
    'length',
    'run',
]

current_stage = stages[0]
sides = 0
length_multiplier = 0

base_speed = 8


async def play_song(robot: Robot, song: [(Note, float)]):
    for note in song:
        print(note[0], note[1])
        await robot.play_note(note[0], note[1])


async def draw_regular_shape(robot: Root):
    """Draws the final shape
    """
    global sides, length_multiplier, base_speed
    if sides < 1:
        sides = 3
    if length_multiplier < 1:
        length_multiplier = 1
    await robot.set_marker(robot.MARKER_DOWN)
    for side in range(sides):
        await robot.move(base_speed * length_multiplier)
        await robot.turn_right(360 / sides)
    await robot.set_marker(robot.MARKER_UP)


@event(robot.when_bumped, [True, False])
async def left_bumped(robot: Robot):
    global current_stage
    if current_stage == stages[0]:
        global sides
        sides += 1
        for i in range(sides):
            await robot.play_note(Note.C5, 0.25)
    elif current_stage == stages[1]:
        global length_multiplier
        length_multiplier += 1
        for i in range(length_multiplier):
            await robot.play_note(Note.C5, 0.25)
    else:
        for i in range(3):
            await robot.play_note(Note.G5, 1)
        await robot.play_note(Note.C6, 1)
        await draw_regular_shape(robot)
        sides = 0
        length_multiplier = 0
        current_stage = stages[0]


@event(robot.when_bumped, [False, True])
async def right_bumped(robot: Robot):
    await play_song(robot, confirm_song)
    global current_stage
    if current_stage == stages[0]:
        current_stage = stages[1]
        # await robot.set_lights(robot.LIGHT_ON, Color.BLUE)
    elif current_stage == stages[1]:
        current_stage = stages[2]
        # await robot.set_lights(1, Color.GREEN)
    else:
        current_stage = stages[0]
        # await robot.set_lights(1, Color.RED)


@event(robot.when_play)
async def play(robot: Robot):
    await play_song(robot, intro_song)
    # await robot.set_lights(1, Color.RED)


robot.play()
