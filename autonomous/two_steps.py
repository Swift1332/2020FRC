from magicbot import AutonomousStateMachine, timed_state, tunable


class TwoSteps(AutonomousStateMachine):

    MODE_NAME = "Two Steps"
    DEFAULT = False

    drive_speed = tunable(-1)

    @timed_state(duration=2, next_state="do_something", first=True)
    def dont_do_something(self):
        """This happens first"""
        print("Do something 1")

    @timed_state(duration=5)
    def do_something(self):
        """This happens second"""
        print("Do something 2")
