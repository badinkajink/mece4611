import sys, time
import serial
import lewansoul_lx16a
from math import sin, cos
import matplotlib.pyplot as plt
from servos import *

SERIAL_PORT = 'COM3'

ser = serial.Serial(SERIAL_PORT, 115200, timeout=1)
if not ser.isOpen():
    ser.open()

ctrl = lewansoul_lx16a.ServoController(ser)

# known positions:
'''
wheelie: everything set to home
pos1: [(flj1, upper), (frj1, upper)]
'''
# stable? ish
pos_test = [(flj1, flj1.upper), (frj1, frj1.upper), (blj2, 650), (brj2, 210), (flj2, 600), (frj2, 600), (brj1, 600), (blj1, 370)]

# ok i'm brute forcing this
# stable, step 1
pos_1 = [(flj1, 482), (flj2, 487), (frj1, 629), (frj2, 732), (brj1, 639), (brj2, 200), (blj1, 336), (blj2, 668)]
# move front joint 1 forward
pos_2 = [(flj1, 630), (flj2, 484), (frj1, 457), (frj2, 694), (brj1, 639), (brj2, 200), (blj1, 337), (blj2, 668)]
# move front joints 2 forward
pos_3 = [(flj1, 630), (flj2, 652), (frj1, 457), (frj2, 542), (brj1, 639), (brj2, 200), (blj1, 337), (blj2, 668)]
# move front joints 1 backward
pos_4 = [(flj1, 489), (flj2, 652), (frj1, 613), (frj2, 542), (brj1, 639), (brj2, 200), (blj1, 336), (blj2, 668)]
# move back joints 1 forward
pos_5 = [(flj1, 625), (flj2, 652), (frj1, 458), (frj2, 545), (brj1, 495), (brj2, 191), (blj1, 496), (blj2, 672)]
# move back joints 2 backward
pos_6 = [(flj1, 625), (flj2, 650), (frj1, 458), (frj2, 545), (brj1, 492), (brj2, 451), (blj1, 497), (blj2, 440)]
# move front joints 1,2 backward
pos_7 = [(flj1, 482), (flj2, 487), (frj1, 629), (frj2, 732)]
# move back joints 1 forward
pos_8 = [(flj1, 625), (flj2, 650), (frj1, 457), (frj2, 547), (brj1, 343), (brj2, 453), (blj1, 624), (blj2, 443)]
# move back joints 2 backward
pos_9 = [(flj1, 625), (flj2, 650), (frj1, 457), (frj2, 547), (brj1, 343), (brj2, brj2.lower), (blj1, 624), (blj2, blj2.lower)]
# move front joints 2 backward to lower pos
pos_10 = [(flj2, flj2.lower), (frj2, frj2.lower)]
# move front joints 1 home
pos_11 = [(flj1, flj1.home), (frj1, frj1.home)]
# cycle back to pos_1

def home():
    for i in m_servos:
        ctrl.move(i.motor_id, i.home, 2000)

def move_servos(moves, time=500, by_id=False):
    for i in moves:
        if by_id:
            ctrl.move(i[0], i[1], time)
        else:
            ctrl.move(i[0].motor_id, i[1], time)

def crawl():
    move_servos(pos_1, 500)
    time.sleep(1.0)
    # move_servos(pos_2, 500)
    # time.sleep(1.0)
    # move_servos(pos_4, 500)
    # time.sleep(1.0)
    # move_servos(pos_3, 500)
    # time.sleep(1.0)
    move_servos(pos_5, 500)
    time.sleep(1.0)
    move_servos(pos_6, 500)
    time.sleep(1.0)

# one iteration of crawl motion
def crawl_2():
    ctrl.move(6, 324)
    time.sleep(1.0)
    ctrl.move(2, 636)
    time.sleep(1.0)
    ctrl.move(7, 636)
    time.sleep(1.0)
    ctrl.move(4, 853)
    time.sleep(1.0)
    ctrl.move(6, 416)
    time.sleep(1.0)
    ctrl.move(4, frj2.upper)
    time.sleep(1.0)

# small stomp, then big stomp
def double_stomp():
    ctrl.move(7, blj1.upper)
    ctrl.move(5, brj1.upper)
    move_servos(pos_5, 500)
    time.sleep(1.0)
    move_servos(pos_6, 500)
    time.sleep(1.0)
    move_servos(pos_5, 500)
    time.sleep(1.0)
    move_servos(pos_6, 500)
    time.sleep(1.0)


def get_servo_telem():
    for i in m_servos:
        id = i.motor_id
        print(f"Servo name: {i.name}")
        print("Servo id: {}".format(id))
        print("Position: {}".format(ctrl.get_position(id)))

# util function to extract moves
def get_move_from_pos():
    move = []
    for i in m_servos:
        id = i.motor_id
        move.append((i.name, ctrl.get_position(id)))
    return move

if __name__ == "__main__":
    # print(flj1.motor_id)
    # home()
    # print(flj2.home)
    # time.sleep(2.0)
    # move_servos(pos1, 500)
    # get_servo_telem()
    # move = str(get_move_from_pos())
    # print(move)
    # crawl()
    # double_stomp()
    crawl_2()
    # home()