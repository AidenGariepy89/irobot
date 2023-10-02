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
    await robo.set_color(color.RED)
    robo.currently_running = False

    await robo.play_song(music.end_song)


async def reset(robo: Robo):
    await robo.r.play_note(Note.E5, 0.1)
    robo.set_defaults()
    await robo.set_color(color.RED)
    await robo.set_state("LEFT_BUMPER", set_sides)
    await robo.set_state("RIGHT_BUMPER", shape_state_setter)


async def console(robo: Robo):
    await robo.r.play_note(Note.G5_SHARP, 0.1)
    user_input = input("Shape sides: ")
    if user_input == 'q':
        return
    robo.shape_sides = int(user_input)
    user_input = input("Shape side length (cm): ")
    if user_input == 'q':
        return
    robo.shape_sidelength = int(user_input) / robo.base_speed
    await robo.set_state("LEFT_BUMPER", start_shape_draw)
    await robo.set_color(color.GREEN)
    await robo.state_lb(robo)
    await robo.set_color(color.RED)
    robo.set_defaults()
