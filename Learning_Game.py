import math
from pyrep.robots.arms.ur5 import UR5
from pyrep.robots.arms.ur5 import Arm
from pyrep.objects.shape import Shape
from pyrep.objects.dummy import Dummy
import random
from pyrep import PyRep
from pyrep.objects.vision_sensor import VisionSensor
from pyrep.backend import sim
import numpy as np
import cv2
import csv
import pandas as pd
from collections import OrderedDict
prevX = 0  # global variable
prevY = 0
touch_wall=False
wrong_movement=False
temp=[]
final_results=[]
movement_counter=0

SCENE_FILE = '/home/user/Documents/DanielAndEran/ED_learning.ttt'
pr = PyRep()
pr.launch(SCENE_FILE, headless=False)
pr.start()
cam = VisionSensor("cam")
ball = Shape('Sphere')
ballHandle = sim.simGetObjectHandle('Sphere')
pi = math.pi
agent = UR5()

def tablecells():
    table = [[0, 0, 0, 0.30, 0, 0.10], [1, 0, 0.3, 0.6, 0, 0.1], [2, 0, 0.6, 0.9, 0, 0.1], [3, 0, 0.9, 1.2, 0, 0.1],[4, 0, 1.2, 1.5, 0, 0.1], [5, 0, 1.5, 1.8, 0, 0.1],
             [0, 1, 0, 0.3, 0.1, 0.2], [1, 1, 0.3, 0.6, 0.1, 0.2], [2, 1, 0.6, 0.9, 0.1, 0.2],[3, 1, 0.9, 1.2, 0.1, 0.2], [4, 1, 1.2, 1.5, 0.1, 0.2], [5, 1, 1.5, 1.8, 0.1, 0.2],
             [0, 2, 0, 0.3, 0.2, 0.3], [1, 2, 0.3, 0.6, 0.2, 0.3], [2, 2, 0.6, 0.9, 0.2, 0.3],[3, 2, 0.9, 1.2, 0.2, 0.3], [4, 2, 1.2, 1.5, 0.2, 0.3], [5, 2, 1.5, 1.8, 0.2, 0.3],
             [0, 3, 0, 0.3, 0.3, 0.4], [1, 3, 0.3, 0.6, 0.3, 0.4], [2, 3, 0.6, 0.9, 0.3, 0.4],[3, 3, 0.9, 1.2, 0.3, 0.4], [4, 3, 1.2, 1.5, 0.3, 0.4], [5, 3, 1.5, 1.8, 0.3, 0.4],
             [0, 4, 0, 0.3, 0.4, 0.5], [1, 4, 0.3, 0.6, 0.4, 0.5], [2, 4, 0.6, 0.9, 0.4, 0.5],[3, 4, 0.9, 1.2, 0.4, 0.5], [4, 4, 1.2, 1.5, 0.4, 0.5], [5, 4, 1.5, 1.8, 0.4, 0.5],
             [0, 5, 0, 0.3, 0.5, 0.6], [1, 5, 0.3, 0.6, 0.5, 0.6], [2, 5, 0.6, 0.9, 0.5, 0.6],[3, 5, 0.9, 1.2, 0.5, 0.6], [4, 5, 1.2, 1.5, 0.5, 0.6], [5, 5, 1.5, 1.8, 0.5, 0.6],
             [0, 6, 0, 0.3, 0.6, 0.7], [1, 6, 0.3, 0.6, 0.6, 0.7], [2, 6, 0.6, 0.9, 0.6, 0.7],[3, 6, 0.9, 1.2, 0.6, 0.7], [4, 6, 1.2, 1.5, 0.6, 0.7], [5, 6, 1.5, 1.8, 0.6, 0.7],
             [0, 7, 0, 0.3, 0.7, 0.8], [1, 7, 0.3, 0.6, 0.7, 0.8], [2, 7, 0.6, 0.9, 0.7, 0.8],[3, 7, 0.9, 1.2, 0.7, 0.8], [4, 7, 1.2, 1.5, 0.7, 0.8], [5, 7, 1.5, 1.8, 0.7, 0.8],
             [0, 8, 0, 0.3, 0.8, 0.9], [1, 8, 0.3, 0.6, 0.8, 0.9], [2, 8, 0.6, 0.9, 0.8, 0.9],[3, 8, 0.9, 1.2, 0.8, 0.9], [4, 8, 1.2, 1.5, 0.8, 0.9], [5, 8, 1.5, 1.8, 0.8, 0.9]]
    return table

def cellindex(table, x, y):  # return the index of the cell from a given x,y coordinates
    index = 0
    if  isinstance(x, str) or x is None:
        return [0,0]
    for i in range(len(table)):
        for j in range(len(table[i])):
            if x >= table[i][2] and x < table[i][3] and y >= table[i][4] and y < table[i][5]:
                return [table[i][0],table[i][1]]

game_board=tablecells()


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
tip= Dummy('UR5_tip')
start_position = agent.get_joint_positions()
'''
first array- robot_poitions: [0-right,1-center,2-left]
second array-ball_positions: [0- (4,8), 1- (4,7),2- (4,6),3- (4,5),4- (4,4),5- (4,3),6- (4,2),7- (4,1),8- (4,0),9- (2,8),10- (2,7),11- (2,6),12- (2,5),13- (2,4),14- (2,3),15- (2,2),16- (2,1),17- (2,0)
third array- vy: [0-(-0.2,-0.1),1-(-0.1,0),2-(0,0.1),3-(0.1,0.2)]
'''
states=np.array(np.meshgrid([0,1,2],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],[0,1,2,3])).T.reshape(-1,3)
actions=['move_right','move_left','kick_right','kick_center','kick_left','do_nothing']
actions_space_size= len(actions)
states_space_size= len(states)
q_table = []
initial_positions=[]
with open('Q_table27.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        q_table.append([float(val) for val in row])

num_runs=0
with open('test_policy.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        initial_positions.append([float(val) for val in row])

def ballCoordinates(img):  # work with image format without imread
    global prevX
    global prevY
    global touch_wall
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = img[450:962, 0:1024]  # region of interest
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # convert to hsv
    lower_red = np.array([0, 140, 140])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(imgHSV, lower_red, upper_red)  # binary mask put 1 if it  red in the image
    # get all non zero values
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask_red, connectivity=8)
    nb_components = nb_components - 1  # taking out the background which is also considered a componentbut
    Originx = 179
    Originy = 34
    if nb_components == 0:
        touch_wall = True
        return "no ball"
    x = centroids[1][0] - Originx  # centert of coordinate x
    y = centroids[1][1] - Originy
    x = (x / 723) * 1.8
    y = (y / 352) * 0.9
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if prevX == 0 and prevY == 0:  # first image to prev
        prevX = x
        prevY = y
        return [x, y]
    Vx = (x - prevX) / 0.05
    Vy = (y - prevY) / 0.05
    prevX = x
    prevY = y
    return [x, y, Vx, Vy]


def Frame_ballCoordinates():
    x = cam.capture_rgb()  # type is float32
    x = np.uint8(x * 256)  # convert to uint8 and format of BGR
    target = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    # lastTime = sim.simGetSimulationTime()
    # pr.step()
    return ballCoordinates(target)



def randomposition():
    global num_runs
    x = initial_positions[num_runs][0]
    y = -1.71
    ball.set_position([x, y, 0.035])
    vx = 0.55
    vy = initial_positions[num_runs][3]
    sim.simSetObjectFloatParameter(ballHandle, 3001, vx)
    sim.simSetObjectFloatParameter(ballHandle, 3000, vy)
    num_runs+=1
    return [x,y,vx,vy]


def move_arm(position, quaternion, ignore_collisions=False):
    arm_path = agent.get_linear_path(position,
                                     quaternion=quaternion,
                                     ignore_collisions=ignore_collisions)
    arm_path.visualize()
    done = False
    while not done:
        done = arm_path.step()
        Frame_ballCoordinates()
        pr.step()
    arm_path.clear_visualization()


def rotate_arm(rotation_angle):
    joint_positions = agent.get_joint_positions()
    joint_positions[5] = rotation_angle
    joint_positions[4] = 0
    agent.set_joint_positions(
        [joint_positions[0], joint_positions[1], joint_positions[2], joint_positions[3], joint_positions[4],
         joint_positions[5]])

def check_vy(vy):
    if vy>=-0.2 and vy<-0.1:
        return 0
    elif vy>=-0.1 and vy<0:
        return 1
    elif vy>=0 and vy<0.1:
        return 2
    else:
        return 3

def check_first_ball_position(ball_position):
    if ball_position is None or ball_position[1]==8:
        return 0
    elif ball_position[1]==7:
        return 1
    elif ball_position[1]==6:
        return 2
    elif ball_position[1]==5:
        return 3
    elif ball_position[1]==4:
        return 4
    elif ball_position[1]==3:
        return 5
    elif ball_position[1]==2:
        return 6
    elif ball_position[1]==1:
        return 7
    else:
        return 8


def check_second_ball_position(ball_position):
    if ball_position is None or ball_position[1]==8:
        return 9
    elif ball_position[1]==7:
        return 10
    elif ball_position[1]==6:
        return 11
    elif ball_position[1]==5:
        return 12
    elif ball_position[1]==4:
        return 13
    elif ball_position[1]==3:
        return 14
    elif ball_position[1]==2:
        return 15
    elif ball_position[1]==1:
        return 16
    else:
        return 17

def check_third_ball_position(ball_position):
    if ball_position is None or ball_position[1]==8:
        return 18
    elif ball_position[1]==7:
        return 19
    elif ball_position[1]==6:
        return 20
    elif ball_position[1]==5:
        return 21
    elif ball_position[1]==4:
        return 22
    elif ball_position[1]==3:
        return 23
    elif ball_position[1]==2:
        return 24
    elif ball_position[1]==1:
        return 25
    else:
        return 26



def search_state(robot_position1,ball_position1,vy1):
    rows=len(states)
    columns=len(states[0])
    for i in range(rows):
        for j in range(columns):
            if robot_position1==states[i][0] and ball_position1==states[i][1] and vy1==states[i][2]:
                return i

def act(action_that_chosen,first_time,moving_illegaly):
    global movement_counter
    pos=tip.get_position()
    reward=0
    if action_that_chosen==0:
        if moving_illegaly==False:
            move_arm([pos[0]-0.31, pos[1], pos[2]], center.get_quaternion(), True)
            movement_counter+=1
        current_position=tip.get_position()
        if moving_illegaly==False:
            check_rotation(current_position,pos)
            reward+=movingReward
        else:
            reward +=illegalReward
        if not first_time:
            reward += missReward
        return tip.get_position(), reward
    elif action_that_chosen==1:
        if moving_illegaly == False:
            move_arm([pos[0]+0.31, pos[1], pos[2]], center.get_quaternion(), True)
            movement_counter += 1
        current_position = tip.get_position()
        if moving_illegaly == False:
            check_rotation(current_position,pos)
            reward +=movingReward
        else:
            reward += missReward
        if not first_time:
            reward += missReward
        return tip.get_position(), reward
    elif action_that_chosen==5:
        reward += nothingReward
        if not first_time:
            reward += missReward
        return tip.get_position(), reward

    else:
        return kick(pos,action_that_chosen,first_time)


def check_rotation(current_position,pos):
    if current_position[0]>0.3:
        rotate_arm(pi/7)
    elif current_position[0]<0:
        rotate_arm(-pi/7)
    else:
        if pos[0]>0.3:
            rotate_arm(-pi / 50)
        else:
            rotate_arm(pi / 50)
        move_arm(center.get_position(), center.get_quaternion(), True)

def kick(pos,kick_from_states,first_time):
    global movement_counter
    reward=movingReward
    if kick_from_states==2:
        move_arm([pos[0]-0.08, -0.275, 0.05], center.get_quaternion(), True)
        movement_counter += 1
        ball_position_kick=Frame_ballCoordinates()
        if pos[0]<0:
            racket_index=[1,8]
        elif pos[0]>0 and pos[0]<0.3:
            racket_index=[1,5]
        else:
            racket_index=[1,2]
        if not first_time:
            reward+=hit_or_not(racket_index,ball_position_kick)
    elif kick_from_states==3:
        move_arm([pos[0], -0.275, 0.05], center.get_quaternion(), True)
        movement_counter += 1
        ball_position_kick=Frame_ballCoordinates()
        if pos[0]<0:
            racket_index=[1,7]
        elif pos[0]>0 and pos[0]<0.3:
            racket_index=[1,4]
        else:
            racket_index=[1,1]
        if not first_time:
            reward+=hit_or_not(racket_index,ball_position_kick)
    else:
        move_arm([pos[0]+0.1,-0.275,0.05],center.get_quaternion(),True)
        movement_counter += 1
        ball_position_kick=Frame_ballCoordinates()
        if pos[0]<0:
            racket_index=[1,6]
        elif pos[0]>0 and pos[0]<0.3:
            racket_index=[1,3]
        else:
            racket_index=[1,0]
        if not first_time:
            reward+=hit_or_not(racket_index,ball_position_kick)

    move_arm(pos, center.get_quaternion(), True)

    return pos,reward

def check_robot_in_states(new_pos):
    if new_pos[0] > 0.3:
        return 2
    elif new_pos[0] < 0:
        return 0
    else:
        return 1

def hit_or_not(robot_position_kick,ball_position_kick):
    ball_temp = Frame_ballCoordinates()[0]
    print(ball_temp)
    if isinstance(ball_temp,str):
        return missReward
    else:
        ball_position = cellindex(game_board, ball_position_kick[0], ball_position_kick[1])
        print(ball_position)
        if ball_position is None or robot_position_kick[0]>ball_position[0]:
            return missReward
        else:
            return hitReward


movingReward = -1  # prevent in vain moving
nothingReward = 0
missReward = -10
hitReward = 10
illegalReward=-10
num_episodes=100


learinng_rate=0.1   #alpha
discount_rate=0.99  #gamma
#exploration_rate=0.6110661188014018  #epsilon
exploration_rate=0.010201635219756281
max_exploration_rate=1
min_exploration_rate=0.01
exploration_decay_rate=0.001


rewards_current_episode = 0
first_robot_position = check_robot_in_states(tip.get_position())
temp=randomposition()
vy = temp[3]
vy_state = check_vy(vy)
# may not work
agent.set_joint_positions(start_position)
first_ball_position = cellindex(game_board, Frame_ballCoordinates()[0], Frame_ballCoordinates()[1])
ball_pos1 = check_first_ball_position(first_ball_position)
old_state = search_state(first_robot_position, ball_pos1, vy_state)
#Q-learning algorithm
for episode in range(num_episodes):
    #done=False

    reward_each_step = 0
    rewards_current_episode=0
    action=np.argmax(q_table[old_state])
    if (action==0 and first_robot_position==0) or (action==1 and first_robot_position==2):
        wrong_movement=True

    new_pos,reward_each_step=act(action,True,wrong_movement)
    rewards_current_episode += reward_each_step
    second_robot_position=check_robot_in_states(new_pos)
    wrong_movement = False

    while Frame_ballCoordinates()[0] >= 1.5:
        agent.set_joint_positions(agent.get_joint_positions())

    second_ball_position = cellindex(game_board, Frame_ballCoordinates()[0], Frame_ballCoordinates()[1])
    ball_pos2 = check_second_ball_position(second_ball_position)
    new_state=search_state(second_robot_position,ball_pos2,vy_state)

    reward_each_step = 0
    old_state=new_state

    action = np.argmax(q_table[old_state])
    if (action==0 and second_robot_position==0) or (action==1 and second_robot_position==2):
        wrong_movement=True

    new_pos, reward_each_step = act(action, True,wrong_movement)
    rewards_current_episode += reward_each_step
    third_robot_position = check_robot_in_states(new_pos)
    wrong_movement = False

    while Frame_ballCoordinates()[0] >= 0.6:
        agent.set_joint_positions(agent.get_joint_positions())

    third_ball_position = cellindex(game_board, Frame_ballCoordinates()[0], Frame_ballCoordinates()[1])
    ball_pos3=check_third_ball_position(third_ball_position)
    new_state = search_state(third_robot_position, ball_pos3, vy_state)
    reward_each_step = 0
    old_state = new_state

    action = np.argmax(q_table[old_state])
    if (action==0 and third_robot_position==0) or (action==1 and third_robot_position==2):
        wrong_movement=True

    new_pos,reward_each_step = act(action,False,wrong_movement)
    rewards_current_episode+=reward_each_step
    # update q table
    first_robot_position = check_robot_in_states(new_pos)
    wrong_movement = False

    temp.append(movement_counter)
    movement_counter=0
    temp1 = temp
    if(reward_each_step>0):
        temp1.append(1)
    else:
        temp1.append(0)
    final_results.append(temp1)
    touch_wall = False
    if episode<99:
        temp = randomposition()
    vy=temp[3]
    agent.set_joint_positions(agent.get_joint_positions())
    vy_state = check_vy(vy)
    first_ball_position = cellindex(game_board, Frame_ballCoordinates()[0], Frame_ballCoordinates()[1])
    ball_pos1 = check_first_ball_position(first_ball_position)
    new_state = search_state(first_robot_position, ball_pos1, vy_state)
    reward_each_step = 0
    old_state = new_state

    #exploration rate decay
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*(episode+8500))
    print(episode)
pr.stop()
pr.shutdown()

################ Writer #################

with open('test_learning.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(final_results)


'''
############ READER ############
reader1 = pd.read_csv('Qtable.csv',header=None)
print(reader1[4][2]) # first argument is the column and second is row
'''