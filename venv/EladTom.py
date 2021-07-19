from tkinter import *
import tkinter
from PIL import Image, ImageTk
from tkinter import messagebox
#code v1 - positions asd kick jkl

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
version=0
processes = 1

# SCENE_FILE = '/home/user/Documents/TomAndElad/All_Parts_2.0.ttt'
# pr = PyRep()
# pr.launch(SCENE_FILE, headless=False)
# pr.start()




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
            print('ka')
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

    #left dummies
    left = Dummy('left')
    left_left = Dummy('left_left')
    left_center = Dummy('left_center')
    left_right = Dummy('left_right')

    #center dummies
    center = Dummy('center')
    center_left = Dummy('center_left')
    center_center = Dummy('center_center')
    center_right = Dummy('center_right')

    #right dummies
    right = Dummy('right')
    right_left = Dummy('right_left')
    right_center = Dummy('right_center')
    right_right = Dummy('right_right')

    ball = Shape('Sphere')
    print(ball.get_position())
    #start position
    start_position = agent.get_joint_positions()


    def set_position(position):
        move_arm(position.get_position(), position.get_quaternion(), True)
        if position == left:
            rotate_arm(pi / 6)
        elif position == right:
            rotate_arm(-pi / 6)

    def kick(direction):
        move_arm(direction.get_position(), direction.get_quaternion(), True)
        move_arm(center.get_position(), center.get_quaternion(), True)
        agent.set_joint_positions(start_position)

    kickk=0
    position = 0
    exit = 0

    def randomposition():
        x = random.uniform(-0.16, 0.55)
        y = -1.71
        print(x)
        print(y)
        ball.set_position([x, y, 0.035])
        v = 3 * random.random()
        sim.simSetObjectFloatParameter(ballHandle, 3001, v)
        # sim.simSetObjectFloatParameter(ballHandle,3000,1)

    randomposition()

    while exit != 'e':
        position='s'
        print('0')
        pr.step()
        with keyboard.Events() as events:
            print('0.5')
            pr.step()
            event = events.get(0.005)
            print('1')
            pr.step()
            if event is None:
                pr.step()
                print('2')
                continue
            if event.key == keyboard.KeyCode.from_char('e'):
                exit='e'
                continue
            if event.key == keyboard.KeyCode.from_char('n'):
                randomposition()
                continue
            if event.key == keyboard.KeyCode.from_char('a'):
                position = 'a'
            if event.key == keyboard.KeyCode.from_char('s'):
                position = 's'
            if event.key == keyboard.KeyCode.from_char('d'):
                position = 'd'
            if event.key == keyboard.KeyCode.from_char('j'):
                kickk = 'j'
            if event.key == keyboard.KeyCode.from_char('k'):
                kickk = 'k'
            if event.key == keyboard.KeyCode.from_char('l'):
                kickk = 'l'

            if position == 'a':
                set_position(left)
                if kickk == 'j':
                    kick(left_left)
                    position='s'
                    kickk=0
                    continue
                if kickk == 'k':
                    kick(left_center)
                    position = 's'
                    kickk = 0
                    continue
                if kickk == 'l':
                    kick(left_right)
                    position = 's'
                    kickk = 0
                    continue
                continue

            if position == 's':
                set_position(center)
                if kickk == 'j':
                    kick(center_left)
                    kickk = 0
                    continue
                if kickk == 'k':
                    kick(center_center)
                    kickk = 0
                    continue
                if kickk == 'l':
                    kick(center_right)
                    kickk = 0
                    continue
                continue

            if position == 'd':
                set_position(right)
                if kickk == 'j':
                    kick(right_left)
                    position = 's'
                    kickk = 0
                    continue
                if kickk == 'k':
                    kick(right_center)
                    position = 's'
                    kickk = 0
                    continue
                if kickk == 'l':
                    kick(right_right)
                    position = 's'
                    kickk = 0
                    continue
                continue


    pr.stop()
    pr.shutdown()


w=Tk()
w.geometry('700x700')
w.title('Simulation Menu')

def versionmaker1(version):
    version = 1


def versionmaker2(version):
    version = 2


btn1 = Button(w, text = 'Play Version 1!', bd = '5',  command = versionmaker1(version))
btn1.pack(side = 'top')

btn2 = Button(w, text = 'Play Version 2!', bd = '5',  command = versionmaker2(version))
btn2.pack(side = 'top')

btn2 = Button(w, text = 'Play!', bd = '5',  command = w.destroy)
btn2.pack(side = 'top')

image1 = Image.open("/home/user/Desktop/robot-playing-soccer-14497062.jpg")
image2 = image1.resize((10, 10), Image.ANTIALIAS)#cant crop the image somehow..

test = ImageTk.PhotoImage(image1)
label1 = tkinter.Label(image=test)
label1.image = test
label1.place(x='0', y='120')

w.mainloop()
print(version)


processes = [Process(target=run, args=()) for i in range(processes)]
[p.start() for p in processes]
[p.join() for p in processes]