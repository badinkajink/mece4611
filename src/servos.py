class Servo:
    j1_rom = 157
    j2_rom = 142

    def __init__(self, motor_id, name, side, joint, home):
        self.motor_id = motor_id
        self.name     = name
        self.joint    = joint
        self.home     = home
        j_rom = self.j1_rom if joint == 1 else self.j2_rom
        if side == "left":
            self.upper = home + j_rom
            self.lower = home - j_rom
        else: # right
            self.upper = home - j_rom
            self.lower = home + j_rom

flj1 = Servo(
            motor_id  = 1,
            name  = "flj1", # front left joint 1
            side  = "left",
            joint = 1,
            home  = 466)

flj2 = Servo(
            motor_id  = 2,
            name  = "flj2", # front left joint 2
            side  = "left",
            joint = 2,
            home  = 489)
frj1 = Servo(
            motor_id  = 3,
            name  = "frj1", # front right joint 1
            side  = "right",
            joint = 1,
            home  = 606)

frj2 = Servo(
            motor_id  = 4,
            name  = "frj2", # front right joint 2
            side  = "right",
            joint = 2,
            home  = 706)
brj1 = Servo(
            motor_id  = 5,
            name  = "brj1", # back right joint 1
            side  = "right",
            joint = 1,
            home  = 481)
brj2 = Servo(
            motor_id  = 6,
            name  = "brj2", # back right joint 2
            side  = "right",
            joint = 2,
            home  = 274)
blj1 = Servo(
            motor_id  = 7,
            name  = "blj1", # back left joint 1
            side  = "left",
            joint = 1,
            home  = 486)
blj2 = Servo(
            motor_id  = 8,
            name  = "blj2", # back left joint 2
            side  = "left",
            joint = 2,
            home  = 586)

m_servos = [flj1, flj2, frj1, frj2, brj1, brj2, blj1, blj2]