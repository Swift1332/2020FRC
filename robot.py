#!/usr/bin/env python3

import ctre
import navx
import wpilib
from magicbot import MagicRobot
from networktables import NetworkTables
from wpilib.drive import DifferentialDrive

from components.component1 import Component1
from components.component2 import Component2


class MyRobot(MagicRobot):

    #
    # Define components here
    #

    component1: Component1
    component2: Component2

    # You can even pass constants to components
    SOME_CONSTANT = 1

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # TODO: create button example here

        self.some_motor_1 = wpilib.Talon(0)
        self.some_motor_1.setInverted(True)

        self.some_motor_2 = wpilib.Talon(1)
        self.some_motor_2.setInverted(True)

        self.left_middle_motor = ctre.WPI_TalonFX(1)
        self.right_middle_motor = ctre.WPI_TalonFX(4)

        self.left_front_motor = ctre.WPI_TalonFX(0)
        self.left_front_motor.follow(self.left_middle_motor)

        self.left_back_motor = ctre.WPI_TalonFX(2)
        self.left_back_motor.follow(self.left_middle_motor)

        self.right_front_motor = ctre.WPI_TalonFX(3)
        self.right_front_motor.follow(self.right_middle_motor)

        self.right_back_motor = ctre.WPI_TalonFX(5)
        self.right_back_motor.follow(self.right_middle_motor)

        self.navx = navx.AHRS(wpilib.SPI.Port.kMXP)

        NetworkTables.initialize()
        self.dashboard = NetworkTables.getTable("SmartDashboard")

        # self.some_motor_2.setInverted(True)

        self.joystick = wpilib.Joystick(0)
        self.joystick.setThrottleChannel(1)
        self.joystick.setZChannel(4)

        self.drivetrain = DifferentialDrive(
            self.left_middle_motor, self.right_middle_motor
        )

    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""

        try:
            # self.component2.do_something(self.joystick.getThrottle())
            self.drivetrain.arcadeDrive(
                self.joystick.getThrottle(), self.get_joystick_z_inverted(), True
            )

            # if button one
            if self.joystick.getRawButton(1):
                self.left_middle_motor.set(0.15)
            elif self.joystick.getRawButton(2):
                self.left_middle_motor.set(-0.15)

            self.dashboard.putNumber("Pitch", self.navx.getPitch())
            self.dashboard.putNumber("Yaw", self.navx.getYaw())
            self.dashboard.putNumber("Roll", self.navx.getRoll())

        except Exception:
            self.onException()

    def get_joystick_z_inverted(self):
        return self.joystick.getZ() * -1


if __name__ == "__main__":
    wpilib.run(MyRobot)
