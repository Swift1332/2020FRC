from magicbot import AutonomousStateMachine, timed_state

from components.drivetrain import Drivetrain


class ForwardBack(AutonomousStateMachine):

    MODE_NAME = "Forward Back"
    DEFAULT = True

    drivetrain: Drivetrain

    drive_speed = 0.2

    @timed_state(duration=2, next_state="drive_backward", first=True)
    def drive_forward(self):
        self.drivetrain.set_inputs(self.drive_speed, 0.0)
        print("forward")
        self.drivetrain.execute()

    @timed_state(duration=5)
    def drive_backward(self):
        self.drivetrain.set_inputs(self.drive_speed * -1, 0.0)
        print("back")
        self.drivetrain.execute()
