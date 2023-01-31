"""
This is an example of a simple goal reflex agent. The example in question is about a vacuum cleaner whose duty is
to clean the room nx1 it is located in (GOAL). It starts from a fixed position of the room (INITIAL STATE). It can move
left and right and it also can suck trash. The agent never stops, and it always performs an action per iteration. We
suppose the agent has an infinite power supply (it can move forever).

REFLEX AGENT: Vacuum cleaner.
ENVIRONMENT: nx1 room.
PERFORMANCE MEASURE: Cleaning as much as possible.
GOAL: Clean the room (always achievable in this example)
INITIAL STATE: Set to 0 by developer.
ACTUATOR: Move right, Move left or Suck.
COST: Each action is worth one unit of battery
MAX COST: Infinite
"""

from typing import *
import time


class Environment(object):
    def __init__(self, environment: Dict[int, int]):
        self.environment = environment

    def print(self) -> None:
        return print(self.environment)

    def get_environment(self, state: int) -> Dict[str, int]:
        """
        This function works as the sensors of the reflex agent. Given in what state the agent currently is, this
        function returns how the environment is nearby.
        :param state: int. State of the reflex agent
        :return: Dict[str, int]. How the environment is nearby the agent.
        """
        if state - 1 > 0:
            left = self.environment[state - 1]
        else:
            left = None

        if state + 1 < len(self.environment):
            right = self.environment[state + 1]
        else:
            right = None

        centre = self.environment[state]

        percept = {'Left': left, 'Right': right, 'Centre': centre}
        return percept

    def update_environment(self, state: int) -> Dict[int, int]:
        """
        Applies changes done to environment by reflex agent. In this example, this function is in charge of cleaning
        the environment.
        :param state: int. State of the agent
        :return: Update: Dict[int, int]. Updated environment.
        """
        self.environment[state] = 0
        return self.environment

    def is_clean(self) -> bool:
        """
        This function checks if all the rooms are cleaned
        :return: bool. False if there is still trash in the room, returns True otherwise.
        """
        for room in self.environment:
            if self.environment[room] == 1:
                return False        # not cleaned
        return True                 # cleaned


class Vacuum_cleaner(Environment):
    INITIAL_STATE = 0
    MOVE_COST = +1
    SUCK_COST = +1

    def __init__(self, environment):
        super().__init__(environment=environment)
        self.state = self.INITIAL_STATE
        self.previous_state = 0
        self.cost = 0
        self.performance = 0

    def print(self) -> None:
        """
        This function displays the current state of the vacuum cleaner
        :return:
        """
        return super().print()

    def run(self) -> None:
        finished = False
        while not finished:
            if super().is_clean():       # While the goal is not fulfilled...
                finished = True
                return print('Finished. Total cost:', self.cost)
            print('I was in', self.previous_state, 'and now I am in', self.state)
            percept = super().get_environment(self.state)
            actions = self.agent_function(percept=percept)
            if len(actions) > 1:
                # We check the previous state to avoid entering on a loop
                if self.previous_state == self.state - 1:
                    avoid = self.move_left
                elif self.previous_state == self.state + 1:
                    avoid = self.move_right
                else:
                    avoid = None
                action = pick_action(actions=actions, avoid=avoid)
            else:
                action = pick_action(actions)

            # Actuator
            action()
            self.print()
            time.sleep(2)
            print()

    def agent_function(self, percept) -> Dict[Callable, int]:
        # Get percept of environment
        rule = {}                              # create empty set of rules

        # Check percept and global rules. Notice these rules are always constant. You can create a function to
        # specifically check this rules.
        if percept['Left'] is None:            # met a frontier on the left
            rule['Move left?'] = False
        else:
            rule['Move left?'] = True

        if percept['Right'] is None:           # met a frontier on the right
            rule['Move right?'] = False
        else:
            rule['Move right?'] = True

        if percept['Centre'] == 1:             # can be cleaned
            rule['Suck?'] = True
        else:
            rule['Suck?'] = False

        actions = self.get_actions(rule=rule)
        return actions

    def get_actions(self, rule: Dict[str, bool]) -> Dict[Callable, int]:
        """
        This function, given a set of rules of what the agent can and cannot do, it returns the actions the reflex
        agent can do, the subtraction of the performance and cost of each action
        :param rule: Dict[str, bool]. Set of rules
        :return: Dict[Callable, int]. Dictionary containing the actions the reflex agent can do as keys, and the
        subtraction of the performance and cost of each action as their values.
        """
        actions = {}                # create empty set of actions

        # Check rules and append action if possible
        if rule['Move left?']:
            cost = +1
            performance = -1
            actions[self.move_left] = performance - cost

        if rule['Move right?']:
            cost = +1
            performance = -1
            actions[self.move_right] = performance - cost

        if rule['Suck?']:
            cost = +1
            performance = +1
            actions[self.suck] = performance - cost

        return actions

    def move_left(self) -> None:
        print('Moving left...')
        self.previous_state = self.state
        self.cost += 1
        self.performance -= 1
        self.state -= 1
        return

    def move_right(self) -> None:
        print('Moving right...')
        self.previous_state = self.state
        self.cost += 1
        self.performance -= 1
        self.state += 1
        return

    def suck(self) -> None:
        print('Cleaning trash...')
        self.cost += 1
        self.performance -= 1
        self.state = self.state
        super().update_environment(state=self.state)
        return


def pick_action(actions: Dict[Callable, int], avoid: Callable = None) -> Callable:
    """
    This function picks the action that has the best performance / cost ratio from the range of possible actions
    the reflex agent can perform. If a loop is detected, you may want to avoid some actions to break it. This is a
    method not a class function.
    :param actions: Dict[Callable, int]. Possible actions and their performance / cost ratio.
    :param avoid: Callable. Action to be avoided
    :return: Callable. Best action available.
    """
    action_to_pick = None
    for action in actions:
        if action_to_pick is None:
            if action != avoid:
                action_to_pick = action
        elif actions[action] > actions[action_to_pick] and action != avoid:        # Has a better ratio...
            action_to_pick = action
    return action_to_pick


def main():
    room = {0: 0, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1}
    reflex_agent = Vacuum_cleaner(room)
    return reflex_agent.run()


if __name__ == '__main__':
    main()
