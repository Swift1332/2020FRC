import wpilib

from constants import *


class Drivetrain:

    differential_drive: wpilib.drive.DifferentialDrive
    test_servo: wpilib.Servo

    def on_enable(self):
        pass

    def set_inputs(self, throttle, turn):

        self.throttle = throttle
        self.turn = turn

    def execute(self):
        # print("Something in there that we'll recognizee when we see it")
        self.differential_drive.arcadeDrive(
            self.throttle, self.turn, DRIVETRAIN_SQUARED_INPUTS
        )
        self.test_servo.set(self.throttle)
