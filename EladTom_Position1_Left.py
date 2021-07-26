from tkinter import *
import tkinter
from PIL import Image, ImageTk
from pyrep import PyRep
import math
from pyrep.backend import sim
from pyrep.robots.arms.ur5 import UR5
from pyrep.robots.arms.ur5 import Arm
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
from pynput import keyboard
import random
from multiprocessing import Process
import time

# code v2 - positions: jkl kick: asd

def run():
    pr = PyRep()
    pr.launch('/home/user/Documents/TomAndElad/All_Parts_kick_left.ttt', headless=False)
    pr.start()
    ballHandle = sim.simGetObjectHandle('Sphere')
    pi = math.pi
    agent = UR5()

    def move_arm(position, quaternion, ignore_collisions=False):
        arm_path = agent.get_linear_path(position,
                                         quaternion=quaternion,
                                         ignore_collisions=ignore_collisions)
        arm_path.visualize()
        done = False
        while not done:
            print('arm in movement')
            done = arm_path.step()
            pr.step()
        arm_path.clear_visualization()

    def rotate_arm(rotation_angle):
        joint_positions = agent.get_joint_positions()
        joint_positions[5] = rotation_angle
        joint_positions[4] = 0
        agent.set_joint_positions(
            [joint_positions[0], joint_positions[1], joint_positions[2], joint_positions[3], joint_positions[4],
             joint_positions[5]])

    # left dummies
    left = Dummy('left')
    left_left = Dummy('left_left')
    left_center = Dummy('left_center')
    left_right = Dummy('left_right')

    # center dummies
    center = Dummy('center')
    center_left = Dummy('center_left')
    center_center = Dummy('center_center')
    center_right = Dummy('center_right')

    # right dummies
    right = Dummy('right')
    right_left = Dummy('right_left')
    right_center = Dummy('right_center')
    right_right = Dummy('right_right')

    ball = Shape('Sphere')
    print(ball.get_position())
    # start position
    start_position = agent.get_joint_positions()

    def set_position(position):
        move_arm(position.get_position(), position.get_quaternion(), True)
        if position == left:
            rotate_arm(pi / 6)
        if position == center:
            rotate_arm(pi / 100)
        elif position == right:
            rotate_arm(-pi / 6)

    def kick(direction):
        move_arm(direction.get_position(), direction.get_quaternion(), True)
        move_arm(center.get_position(), center.get_quaternion(), True)
        agent.set_joint_positions(start_position)

    kickk = 0

    def randomposition():
        x = random.uniform(0.04, 0.35)
        y = -1.71
        ball.set_position([x, y, 0.035])
        v = 0.3
        sim.simSetObjectFloatParameter(ballHandle, 3001, v)

    exit1 = 0
    randomposition()
    position = 'k'

    with keyboard.Events() as events:

        while exit1 != 'e':

            print('while beginning')
            pr.step()
            print('with beginning')

            event = events.get(1 / 200)
            click_down = (str(event).split('(')[0] == "Press") #making a variable that equals to "press"
            print('after event.get(0.005)')
            pr.step()

            print('after step after event.get')
            if event is None:
                pr.step()
                print('event is none>continue (starting while again)')
                continue
            elif not click_down: # if event is "press": skip. if event is not "press" (its "release") then get in the loop
                # pr.step()
                print('event is none>continue (starting while again)')
                continue
            if event.key == keyboard.KeyCode.from_char('e'):
                exit1 = 'e'
                continue
            if event.key == keyboard.KeyCode.from_char('n'):
                randomposition()
                continue
            if event.key == keyboard.KeyCode.from_char('j'):
                position = 'j'
            if event.key == keyboard.KeyCode.from_char('k'):
                position = 'k'
            if event.key == keyboard.KeyCode.from_char('l'):
                position = 'l'
            if event.key == keyboard.KeyCode.from_char('a'):
                kickk = 'a'
            if event.key == keyboard.KeyCode.from_char('s'):
                kickk = 's'
            if event.key == keyboard.KeyCode.from_char('d'):
                kickk = 'd'

            if position == 'j':
                set_position(left)
                if kickk == 'a':
                    kick(left_left)
                    position = 'k'
                    kickk = 0
                    continue
                if kickk == 's':
                    kick(left_center)
                    position = 'k'
                    kickk = 0
                    continue
                if kickk == 'd':
                    kick(left_right)
                    position = 'k'
                    kickk = 0
                    continue

                continue

            if position == 'k':
                set_position(center)
                if kickk == 'a':
                    kick(center_left)
                    kickk = 0
                    continue
                if kickk == 's':
                    kick(center_center)
                    kickk = 0
                    continue
                if kickk == 'd':
                    kick(center_right)
                    kickk = 0
                    continue

                continue

            if position == 'l':
                set_position(right)
                if kickk == 'a':
                    kick(right_left)
                    position = 'k'
                    kickk = 0
                    continue
                if kickk == 's':
                    kick(right_center)
                    position = 'k'
                    kickk = 0
                    continue
                if kickk == 'd':
                    kick(right_right)
                    position = 'k'
                    kickk = 0
                    continue

                continue
        # end while
    pr.stop()
    pr.shutdown()
    # end with


def exit2345():
    global exit1
    exit1 = 'e'
    w.destroy()


w = Tk()
w.geometry('1050x1000')
w.title('Simulation Menu')

btn2 = Button(w, text='Play!', bd='5', command=w.destroy)
btn2.pack(side='top')

btn3 = Button(w, text='Exit', bd='5', command=exit2345)
btn3.pack(side='top')

image1 = Image.open("/home/user/Desktop/robot-playing-soccer-14497062.jpg")
image2 = image1.resize((10, 10), Image.ANTIALIAS)  # cant crop the image somehow..

test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test
label1.place(x='0', y='80')

w.mainloop()

run()