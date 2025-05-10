from dish import Dish
from patterns.strategy import PricingStrategy, RegularPricing, DiscountPricing


class Order:
    def __init__(self, customer, pricing_strategy: PricingStrategy):
        self.dishes: list[Dish] = []
        self.customer = customer
        self.pricing_strategy = pricing_strategy

    def add_dish_to_order(self, dish: Dish):
        self.dishes.append(dish)

    def calculate_total_price(self) -> float:
        return self.pricing_strategy.calculate_total(self.dishes)


class OfflineOrder(Order):
    def __init__(self, customer):
        super().__init__(customer, RegularPricing())


class OnlineOrder(Order):
    def __init__(self, customer):
        super().__init__(customer, DiscountPricing())
