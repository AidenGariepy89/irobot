from irobot_edu_sdk.backend import bluetooth
from irobot_edu_sdk.robots import event, hand_over, Robot, Root
from irobot_edu_sdk.music import Note
import behavior
from behavior import Robo
import music
import state
import color

robot: Robot = Root(bluetooth.Bluetooth())

robo = None


@event(robot.when_bumped, [True, False])
async def left_bumped(robot: Robot):
    global robo
    await robo.state_lb(robo)


@event(robot.when_bumped, [False, True])
async def right_bumped(robot: Robot):
    global robo
    await robo.state_rb(robo)


@event(robot.when_touched, [True, False, False, False])
async def top_left_touched(robot: Robot):
    global robo
    await robo.state_tlt(robo)


@event(robot.when_touched, [False, False, True, False])
async def bottom_left_touched(robot: Robot):
    global robo
    await robo.state_blt(robo)


@event(robot.when_play)
async def play(robot: Robot):
    global robo
    robo = Robo(robot)
    await robo.play_song(music.intro_song)
    await robo.set_state("LEFT_BUMPER", state.set_sides)
    await robo.set_state("RIGHT_BUMPER", state.shape_state_setter)
    await robo.set_state("TOP_LEFT_TOUCH", state.reset)
    await robo.set_state("BOTTOM_LEFT_TOUCH", state.console)
    await robo.set_color(color.RED)


robot.play()
