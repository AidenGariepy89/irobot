from irobot_edu_sdk.backend import bluetooth
from irobot_edu_sdk.robots import event, hand_over, Robot, Root
from irobot_edu_sdk.music import Note
from behavior import Robo
import color
import music


async def set_sides(robo: Robo):
    robo.shape_sides += 1
    for i in range(robo.shape_sides):
        await robo.r.play_note(Note.C5, 0.1)


async def set_length(robo: Robo):
    robo.shape_sidelength += 1
    for i in range(robo.shape_sidelength):
        await robo.r.play_note(Note.D5, 0.1)


async def shape_state_setter(robo: Robo):
    if robo.state_lb == set_sides:
        robo.state_lb = set_length
        await robo.set_color(color.YELLOW)
    elif robo.state_lb == set_length:
        robo.state_lb = start_shape_draw
        await robo.set_color(color.GREEN)
    elif robo.state_lb == start_shape_draw:
        robo.state_lb = set_sides
        await robo.set_color(color.RED)

    await robo.play_song(music.confirm_song)


async def start_shape_draw(robo: Robo):
    robo.currently_running = True
    for i in range(3):
        await robo.r.play_note(Note.G5, 0.5)
    await robo.r.play_note(Note.C6, 0.5)

    await robo.draw_regular_shape()

    robo.shape_sides = 0
    robo.shape_sidelength = 0
    await robo.set_state("LEFT_BUMPER", set_sides)
    robo.currently_running = False

    await robo.play_song(music.end_song)
