from cart import ShoppingCartList


class ShippingFacade:
    """Facade Pattern: hides weight calculation, zone lookup, and carrier-API
    stubs behind a single calculate_shipping(cart, zone) call."""

    _ZONE_MULTIPLIERS = {"domestic": 1.0, "international": 1.5}
    _BASE_RATE = 5.0
    _RATE_PER_KG = 2.0

    @staticmethod
    def _calculate_weight(cart: ShoppingCartList) -> float:
        total_weight = 0.0
        for item in cart.to_list():
            total_weight += item.product.get_weight() * item.quantity
        return total_weight

    @staticmethod
    def _lookup_zone_multiplier(zone: str) -> float:
        return ShippingFacade._ZONE_MULTIPLIERS.get(zone.strip().lower(), 1.0)

    @staticmethod
    def _carrier_quote(weight: float, zone_multiplier: float) -> float:
        # Stub standing in for a real carrier API call.
        return (ShippingFacade._BASE_RATE + weight * ShippingFacade._RATE_PER_KG) * zone_multiplier

    @staticmethod
    def calculate_shipping(cart: ShoppingCartList, zone: str) -> float:
        weight = ShippingFacade._calculate_weight(cart)
        multiplier = ShippingFacade._lookup_zone_multiplier(zone)
        return ShippingFacade._carrier_quote(weight, multiplier)
