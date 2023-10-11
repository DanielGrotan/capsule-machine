import time
from typing import Callable

from .capsule_machine import CapsuleMachine, test_capsule_machine
from .command import Command
from .customer_capsule_machine import CustomerCapsuleMachine
from .management_capsule_machine import (ManagementCapsuleMachine,
                                         test_management_capsule_machine)


def default_success_condition(_) -> bool:
    return True


def default_type_constructor(user_input: str) -> str:
    return user_input


type AnyCapsuleMachine = CapsuleMachine | ManagementCapsuleMachine | CustomerCapsuleMachine

class CLI:
    def run(self) -> None:
        capsule_machine, commands = self._config_capsule_machine()

        enter_command_prompt = "\n\n" + "\n".join(f"{prefix} - {command.description}" if prefix != "" else command.description for prefix, command in commands.items()) + "\n\nEnter command: "

        while True:
            command = self._get_user_input(
                enter_command_prompt,
                success_condition=lambda user_input: user_input in commands,
                type_constructor=commands.__getitem__
            )

            command.execute(capsule_machine) # type: ignore
            if command.quit_after_execution:
                break

            time.sleep(1)


    def _config_capsule_machine(self):
        capsule_machine_commands = {
            "1": Command("Fill with water", self._fill_water_command),
            "2": Command("Make an espresso", self._make_espresso_command),
            "3": Command("Make a lungo", self._make_lungo_command),
            "*": Command("Run tests", self._run_capsule_machine_tests_command),
            "": Command("Press ENTER to quit the program", self._quit_program_command, True)
        }

        management_capsule_machine_commands = {
            "1": Command("Fill with water", self._fill_water_command),
            "2": Command("Make an espresso", self._make_espresso_command),
            "3": Command("Make a lungo", self._make_lungo_command),
            "4": Command("Make tea", self._make_tea_command),
            "5": Command("Pour a glass of water", self._pour_water_command),
            "*": Command("Run tests", self._run_management_capsule_machine_tests_command),
            "": Command("Press ENTER to quit the program", self._quit_program_command, True),
        }

        customer_capsule_machine_commands = {
            "1": Command("Fill with water", self._fill_water_command),
            "2": Command("Pay for an espresso", self._make_espresso_command),
            "3": Command("Make a lungo", self._make_lungo_command),
            "4": Command("Add money", self._add_money_command),
            "": Command("Press ENTER to quit the program", self._quit_program_command, True),
        }

        capsule_machine_configs = {
            "normal": (CapsuleMachine, capsule_machine_commands),
            "management": (ManagementCapsuleMachine, management_capsule_machine_commands),
            "customer": (CustomerCapsuleMachine, customer_capsule_machine_commands)
        }

        selected_capsule_machine_class, commands = self._get_user_input(
            f"Choose a capsule machine ({"/".join(capsule_machine_configs.keys())}): ",
            success_condition=lambda user_input: user_input in capsule_machine_configs,
            type_constructor=capsule_machine_configs.__getitem__
        )

        water_capacity = self._get_user_input(
            "How much water should the capsule machine be able to store (mL): ",
            success_condition=lambda user_input: user_input.isnumeric(),
            type_constructor=int,
        )

        return selected_capsule_machine_class(water_capacity), commands
    
    def _fill_water_command(self, capsule_machine: AnyCapsuleMachine) -> None:
        water_amount = self._get_user_input(
            "How much water do you want to fill (mL): ",
            success_condition=lambda user_input: user_input.isnumeric(),
            type_constructor=int
        )

        capsule_machine.fill_water(water_amount)

    def _make_espresso_command(self, capsule_machine: AnyCapsuleMachine) -> None:
        capsule_machine.make_espresso()
    
    def _make_lungo_command(self, capsule_machine: AnyCapsuleMachine) -> None:
        capsule_machine.make_lungo()

    def _make_tea_command(self, capsule_machine: ManagementCapsuleMachine) -> None:
        capsule_machine.make_tea()
    
    def _pour_water_command(self, capsule_machine: ManagementCapsuleMachine) -> None:
        capsule_machine.pour_water()
    
    def _run_capsule_machine_tests_command(self, _: AnyCapsuleMachine) -> None:
        print("Running tests...")
        test_capsule_machine()
        print("Finished running tests with no errors")
    
    def _run_management_capsule_machine_tests_command(self, _: AnyCapsuleMachine) -> None:
        print("Running tests...")
        test_management_capsule_machine()
        print("Finished running tests with no errors")
    
    def _add_money_command(self, capsule_machine: CustomerCapsuleMachine) -> None:
        amount = self._get_user_input(
            "How much money do you wish to add. 1, 20, or 50 kr (any extra gets refunded): ",
            success_condition=lambda user_input: user_input.isnumeric(),
            type_constructor=int
        )

        capsule_machine.receive_payment(amount)
    
    def _quit_program_command(self, _: AnyCapsuleMachine) -> None:
        pass


    def _get_user_input[T](
        self,
        prompt: str,
        success_condition: Callable[[str], bool] = default_success_condition,
        type_constructor: Callable[[str], T] = default_type_constructor,
    ) -> T:
        while True:
            user_input = input(prompt)

            if not success_condition(user_input):
                print("Invalid input, try again")
                continue

            return type_constructor(user_input)
