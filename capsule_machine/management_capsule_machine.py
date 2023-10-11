from .capsule_machine import CapsuleMachine


class ManagementCapsuleMachine(CapsuleMachine):
    def make_tea(self) -> None:
        self._make_drink(200, "Making tea", "Not enough water to make tea")

    def pour_water(self) -> None:
        self._make_drink(
            150, "Pouring a glass of water", "Not enough water for a glass of water"
        )


def test_management_capsule_machine() -> None:
    capsule_machine = ManagementCapsuleMachine(1500)

    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 1500
    ), f"Expected water amount to be 1500, but got {water_amount}"

    capsule_machine.make_tea()
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 1300
    ), f"Expected water amount to be 1300, but got {water_amount}"

    [capsule_machine.pour_water() for _ in range(9)]
    water_amount = capsule_machine.get_water_amount()
    assert (
        water_amount == 100
    ), f"Expected water amount to be 100, but got {water_amount}"
