class CapsuleMachine:
    def __init__(self, water_capacity: int) -> None:
        self.water_capacity = water_capacity
        self.water_amount = water_capacity

    def _make_drink(
        self, water_cost: int, success_message: str, failure_message: str
    ) -> bool:
        if self.water_amount < water_cost:
            print(failure_message)
            return False

        self.water_amount -= water_cost
        print(success_message)
        return True

    def make_espresso(self) -> bool:
        return self._make_drink(
            40, "Making an espresso", "Not enough water to make an espresso"
        )

    def make_lungo(self) -> bool:
        return self._make_drink(
            110, "Making a lungo", "Not enough water to make a lungo"
        )

    def fill_water(self, amount: int) -> int:
        self.water_amount = min(self.water_capacity, self.water_amount + amount)
        print(f"Current water amount is {self.water_amount} mL")

        return self.water_amount

    def get_water_amount(self) -> int:
        return self.water_amount


def test_capsule_machine() -> None:
    capsule_machine = CapsuleMachine(1000)

    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 1000
    ), f"Expected water amount to be 1000 mL, but got {water_amount} mL"

    [capsule_machine.make_lungo() for _ in range(8)]
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 120
    ), f"Expected water amount to be 120 mL, but got {water_amount} mL"

    capsule_machine.make_espresso()
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 80
    ), f"Expected water amount to be 80 mL, but got {water_amount} mL"

    capsule_machine.make_lungo()
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 80
    ), f"Expected water amount to be 80 mL, but got {water_amount} mL"

    capsule_machine.fill_water(30)
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 110
    ), f"Expected water amount to be 110 mL, but got {water_amount} mL"

    capsule_machine.make_lungo()
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 0
    ), f"Expected water amount to be 0 mL, but got {water_amount} mL"
