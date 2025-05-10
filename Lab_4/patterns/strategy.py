from abc import ABC, abstractmethod
from dish import Dish


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_total(self, dishes: list[Dish]) -> float:
        pass


class RegularPricing(PricingStrategy):
    def calculate_total(self, dishes: list[Dish]) -> float:
        return sum(dish.price for dish in dishes)


class DiscountPricing(PricingStrategy):
    def calculate_total(self, dishes: list[Dish]) -> float:
        total = sum(dish.price for dish in dishes)
        return total * 0.9
