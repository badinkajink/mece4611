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

def move_servos(moves, time=75, by_id=False):
    for i in moves:
        motor = i[0]
        if by_id:
            if motor > 8 or motor < 1:
                print("Enter a motor id between 1 and 8")
                return
            id = i[0]
            motor = m_servos[id - 1]

        if isinstance(i[1], str):
            key = i[1]
            if key not in ("h", "u", "l"):
                print("Usage: 'h' - home, 'u' - upper, 'l' - lower")
                return
            if key == "h":
                ctrl.move(motor.motor_id, motor.home, time)
            elif key == "u":
                ctrl.move(motor.motor_id, motor.upper, time)
            elif key == "l":
                ctrl.move(motor.motor_id, motor.lower, time)
        else:
            ctrl.move(motor.motor_id, i[1], time)

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

def seq_1():
    sequence = [
        [(1, 627), (2, 640), (3, 461), (4, 559), (5, 637), (6, 412), (7, 637), (8, 743)],
        [(1, 628), (2, 635), (3, 461), (4, 559), (5, 619), (6, 407), (7, 635), (8, "l")],
        [(1, 628), (2, 635), (3, 461), (4, "h"), (5, 619), (6, 407), (7, 635), (8, 436)],
        [(1, 628), (2, 632), (3, 461), (4, 699), (5, 610), (6, 399), (7, "h"), (8, 440)],
        [(1, 630), (2, 629), (3, "h"), (4, 704), (5, 606), (6, 401), (7, 490), (8, 440)],
        [(1, 354), (2, 633), (3, 603), (4, 704), (5, 605), (6, 401), (7, 434), (8, 439)],
        [(1, 354), (2, 634), (3, 603), (4, 704), (5, "h"), (6, 402), (7, 434), (8, 439)],
        [(1, "u"), (2, 632), (3, 603), (4, 704), (5, 485), (6, 402), (7, 434), (8, 439)],
        [(1, 625), (2, 634), (3, 600), (4, 695), (5, 490), (6, 254), (7, 434), (8, 438)],
        [(1, 627), (2, 635), (3, "u"), (4, 704), (5, 481), (6, 402), (7, 434), (8, 440)],
        [(1, 627), (2, 634), (3, 602), (4, "u"), (5, 484), (6, 402), (7, 434), (8, 438)],
        [(1, 625), (2, 637), (3, "u"), (4, 558), (5, 484), (6, 401), (7, 439), (8, 433)],
        [(1, 629), (2, 637), (3, 458), (4, 558), (5, "l"), (6, 252), (7, 439), (8, 433)],
        [(1, 630), (2, 637), (3, 458), (4, 558), (5, 629), (6, 253), (7, "u"), (8, 447)],
        [(1, 626), (2, 634), (3, 457), (4, 555), (5, 627), (6, 409), (7, 636), (8, 453)]
    ]

    for pos in sequence:
        move_servos(pos, by_id=True)
        time.sleep(0.075)

# util function to extract moves
def get_move_from_pos():
    move = []
    for i in m_servos:
        id = i.motor_id
        move.append((id, ctrl.get_position(id)))
    return move

if __name__ == "__main__":
    # print(flj1.motor_id)
    # home()
    # print(flj2.home)
    # time.sleep(2.0)
    # move_servos(pos1, 500)
    # get_servo_telem()
    # print(get_move_from_pos())
    # pos = [(1, 630), (2, 640), (3, 462), (4, 557), (5, 637), (6, 412), (7, 637), (8, 473)]
    # move_servos(pos, by_id=True)
    seq_1()