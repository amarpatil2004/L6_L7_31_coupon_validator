import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


class TestCouponDiscountCodeCoverage:
    """Tests designed to achieve full code (statement/line) coverage."""

    def test_cart_total_zero_or_negative_raises_value_error(self):
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", 0, True, "mon")

    def test_welcome_coupon_new_user(self):
        assert coupon_discount("WELCOME10", 200, True, "mon") == 20

    def test_welcome_coupon_existing_user(self):
        assert coupon_discount("WELCOME10", 200, False, "mon") == 0

    def test_weekend_coupon_sat_large_cart(self):
        assert coupon_discount("WEEKEND20", 600, False, "sat") == 120

    def test_weekend_coupon_sun_small_cart(self):
        assert coupon_discount("WEEKEND20", 400, False, "sun") == 50

    def test_weekend_coupon_weekday(self):
        assert coupon_discount("WEEKEND20", 600, False, "wed") == 0

    def test_flat100_coupon_above_threshold(self):
        assert coupon_discount("FLAT100", 400, False, "fri") == 100

    def test_flat100_coupon_below_threshold(self):
        assert coupon_discount("FLAT100", 250, False, "fri") == 0

    def test_unknown_coupon(self):
        assert coupon_discount("SAVE50", 500, True, "sat") == 0


class TestBestDiscountCodeCoverage:
    def test_best_discount_capped(self):
        # Cart 1000, 40% cap is 400. FLAT100 -> 100, WEEKEND20 on sat -> 200.
        # WEEKEND20 on 100 cart with cap 40: returns 50 > 40 -> capped at 40.
        assert best_discount(["WEEKEND20"], 100, False, "sat") == 40.0

    def test_best_discount_not_capped(self):
        # Cart 1000, cap is 400. FLAT100 gives 100 <= 400 -> 100
        assert best_discount(["FLAT100"], 1000, False, "mon") == 100


class TestIsExpiredCodeCoverage:
    def test_zero_or_negative_validity(self):
        assert is_expired(10, 5, 0) is True

    def test_positive_validity(self):
        assert is_expired(10, 5, 2) is True
