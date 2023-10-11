from .capsule_machine import CapsuleMachine


class CustomerCapsuleMachine(CapsuleMachine):
    def __init__(self, water_capacity: int) -> None:
        super().__init__(water_capacity)

        self.money_received = 0

    def receive_payment(self, amount: int) -> None:
        if amount >= 50:
            self.money_received += 50
            amount -= 50
        elif amount >= 20:
            self.money_received += 20
            amount -= 20
        else:
            self.money_received += 1
            amount -= 1

        if amount > 0:
            print("You provided an amount which wasn't 1kr, 20kr or 50kr")
            self.return_change(amount)

        print(f"You have payed {self.money_received} kr so far")

    def make_espresso(self) -> bool:
        if self.money_received < 42:
            print("You haven't payed enough money yet")

            if self.money_received > 0:
                self.cancel_payment()

            return False

        self.money_received -= 42

        if self.money_received > 0:
            print("You payed more than required for the espresso")
            self.return_change(self.money_received)
            self.money_received = 0

        success = super().make_espresso()

        if self.water_amount <= 100:
            print(
                "Capsule machine has at most 100 mL water remaining. Consider refilling the water"
            )

        return success

    def cancel_payment(self) -> None:
        print(f"Cancelling payment and refunding {self.money_received} kr")
        self.money_received = 0

    def return_change(self, change: int) -> None:
        print(f"Refunding {change} kr")

    def make_lungo(self) -> bool:
        success = super().make_lungo()

        if self.water_amount <= 100:
            print(
                "Capsule machine has at most 100 mL water remaining. Consider refilling the water"
            )

        return success
