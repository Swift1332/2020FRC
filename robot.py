#!/usr/bin/env python3

import ctre
import navx
import rev
import wpilib
from magicbot import MagicRobot
from networktables import NetworkTables
from wpilib.drive import DifferentialDrive

from components.drivetrain import Drivetrain
from constants import *


class MyRobot(MagicRobot):

    # Define components here

    drivetrain: Drivetrain

    def createObjects(self):
        """Initialize all wpilib motors & sensors"""

        # TODO: create button example here

        # DriveTrain

        self.left_middle_motor = ctre.WPI_TalonFX(LEFT_MIDDLE_MOTOR_CAN_ID)
        self.left_middle_motor.setInverted(True)
        self.right_middle_motor = ctre.WPI_TalonFX(RIGHT_MIDDLE_MOTOR_CAN_ID)
        self.right_middle_motor.setInverted(True)

        self.left_front_motor = ctre.WPI_TalonFX(LEFT_FRONT_MOTOR_CAN_ID)
        self.left_front_motor.follow(self.left_middle_motor)
        self.left_front_motor.setInverted(ctre.TalonFXInvertType.FollowMaster)

        self.left_back_motor = ctre.WPI_TalonFX(LEFT_BACK_MOTOR_CAN_ID)
        self.left_back_motor.follow(self.left_middle_motor)
        self.left_back_motor.setInverted(ctre.TalonFXInvertType.FollowMaster)

        self.right_front_motor = ctre.WPI_TalonFX(RIGHT_FRONT_MOTOR_CAN_ID)
        self.right_front_motor.follow(self.right_middle_motor)
        self.right_front_motor.setInverted(ctre.TalonFXInvertType.FollowMaster)

        self.right_back_motor = ctre.WPI_TalonFX(RIGHT_BACK_MOTOR_CAN_ID)
        self.right_back_motor.follow(self.right_middle_motor)
        self.right_back_motor.setInverted(ctre.TalonFXInvertType.FollowMaster)

        # Other Motors

        self.elevator_motor = rev.CANSparkMax(
            ELEVATOR_MOTOR_CAN_ID, rev.MotorType.kBrushless
        )
        self.shooter_motor = rev.CANSparkMax(
            SHOOTER_MOTOR_CAN_ID, rev.MotorType.kBrushless
        )
        self.shooter_motor.setInverted(True)

        self.lift_motor = rev.CANSparkMax(LIFT_MOTOR_CAN_ID, rev.MotorType.kBrushless)

        self.intake_motor = ctre.WPI_VictorSPX(INTAKE_MOTOR_CAN_ID)

        self.navx = navx.AHRS(wpilib.SPI.Port.kMXP)

        NetworkTables.initialize()
        self.dashboard = NetworkTables.getTable("SmartDashboard")

        self.pdp = wpilib.PowerDistributionPanel(PDP_CAN_ID)

        self.elevator_solenoid = wpilib.DoubleSolenoid(PCM_PORT_2, PCM_PORT_3)
        self.climber_solenoid = wpilib.DoubleSolenoid(PCM_PORT_0, PCM_PORT_1)

        self.test_servo = wpilib.Servo(0)

        # JOYSTICK AND BUTTONS

        self.joystick_0 = wpilib.Joystick(JOYSTICK_0)
        self.joystick_1 = wpilib.Joystick(JOYSTICK_1)

        self.joystick_0.setThrottleChannel(JOYSTICK_0_THROTTLE_CHANNEL)
        self.joystick_0.setZChannel(JOYSTICK_0_Z_CHANNEL)

        self.joystick_1.setThrottleChannel(JOYSTICK_1_THROTTLE_CHANNEL)
        self.joystick_1.setZChannel(JOYSTICK_1_Z_CHANNEL)

        self.differential_drive = DifferentialDrive(
            self.left_middle_motor, self.right_middle_motor
        )

    def teleopInit(self):
        self.climber_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
        self.elevator_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)

    #
    # No autonomous routine boilerplate required here, anything in the
    # autonomous folder will automatically get added to a list
    #

    def teleopPeriodic(self):
        """Place code here that does things as a result of operator
           actions"""

        try:
            # self.component2.do_something(self.joystick_0.getThrottle())
            self.drivetrain.set_inputs(
                self.joystick_0.getThrottle(), self.get_joystick_z_inverted()
            )

            # BUTTONS
            if self.joystick_0.getRawButton(DRIVER_JOYSTICK_BUTTON_A):
                self.lift_motor.set(LIFTER_SPEED_UP)
            elif self.joystick_0.getRawButton(DRIVER_JOYSTICK_BUTTON_B):
                self.lift_motor.set(LIFTER_SPEED_DOWN)
            else:
                self.lift_motor.set(MOTOR_NEUTRAL)

            if self.joystick_1.getRawButton(CODRIVER_JOYSTICK_BUTTON_A):
                self.elevator_motor.set(ELEVATOR_SPEED_UP)
            elif self.joystick_1.getRawButton(CODRIVER_JOYSTICK_BUTTON_B):
                self.elevator_motor.set(ELEVATOR_SPEED_DOWN)
            else:
                self.elevator_motor.set(MOTOR_NEUTRAL)

            if self.joystick_1.getRawButton(CODRIVER_JOYSTICK_BUTTON_X):
                self.elevator_solenoid.set(wpilib.DoubleSolenoid.Value.kReverse)
            elif self.joystick_1.getRawButton(CODRIVER_JOYSTICK_BUTTON_Y):
                self.elevator_solenoid.set(wpilib.DoubleSolenoid.Value.kForward)

            if self.joystick_1.getThrottle() > TRIGGER_ACTIVATION_THRESHOLD:
                self.intake_motor.set(INTAKE_SPEED_IN)
            else:
                self.intake_motor.set(MOTOR_NEUTRAL)

            if self.joystick_1.getZ() > TRIGGER_ACTIVATION_THRESHOLD:
                self.shooter_motor.set(SHOOTER_SPEED_SHOOT)
            else:
                self.shooter_motor.set(MOTOR_NEUTRAL)

            self.dashboard.putNumber("Pitch", self.navx.getPitch())
            self.dashboard.putNumber("Yaw", self.navx.getYaw())
            self.dashboard.putNumber("Roll", self.navx.getRoll())

        except Exception:
            self.onException()

    def get_joystick_z_inverted(self):
        return self.joystick_0.getZ() * -1


if __name__ == "__main__":
    wpilib.run(MyRobot)
