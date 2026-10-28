import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


class TestCouponDiscountBranchCoverage:
    """Branch coverage tests ensuring every decision branch (True/False) is executed."""

    # Branch 1: cart_total <= 0
    def test_cart_total_zero(self):
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", 0, True, "mon")

    def test_cart_total_negative(self):
        with pytest.raises(ValueError, match="empty cart"):
            coupon_discount("WELCOME10", -100, True, "mon")

    # Branch 2: code == "WELCOME10"
    def test_welcome10_new_user(self):
        # code == "WELCOME10" (True), is_new_user (True)
        assert coupon_discount("WELCOME10", 250, True, "mon") == 25.0

    def test_welcome10_existing_user(self):
        # code == "WELCOME10" (True), is_new_user (False)
        assert coupon_discount("WELCOME10", 250, False, "mon") == 0

    # Branch 3: code == "WEEKEND20"
    def test_weekend20_sat_above_500(self):
        # day == "sat" (True), cart_total >= 500 (True)
        assert coupon_discount("WEEKEND20", 500, False, "sat") == 100.0

    def test_weekend20_sat_below_500(self):
        # day == "sat" (True), cart_total >= 500 (False)
        assert coupon_discount("WEEKEND20", 499, False, "sat") == 50

    def test_weekend20_sun_above_500(self):
        # day == "sun" (True), cart_total >= 500 (True)
        assert coupon_discount("WEEKEND20", 1000, False, "sun") == 200.0

    def test_weekend20_sun_below_500(self):
        # day == "sun" (True), cart_total >= 500 (False)
        assert coupon_discount("WEEKEND20", 300, False, "sun") == 50

    def test_weekend20_weekday(self):
        # day in ("sat", "sun") (False)
        assert coupon_discount("WEEKEND20", 600, False, "tue") == 0

    # Branch 4: code == "FLAT100"
    def test_flat100_above_300(self):
        # cart_total > 300 (True)
        assert coupon_discount("FLAT100", 301, False, "mon") == 100

    def test_flat100_exact_300_boundary(self):
        # cart_total > 300 (False at boundary 300)
        assert coupon_discount("FLAT100", 300, False, "mon") == 0

    def test_flat100_below_300(self):
        # cart_total > 300 (False below 300)
        assert coupon_discount("FLAT100", 150, False, "mon") == 0

    # Branch 5: unrecognized coupon code
    def test_unrecognized_code(self):
        assert coupon_discount("UNKNOWN_CODE", 500, True, "sat") == 0


class TestBestDiscountBranchCoverage:
    """Branch coverage tests for best_discount logic, loop, and cap."""

    def test_best_discount_empty_codes(self):
        # for loop does not execute
        assert best_discount([], 500, True, "sat") == 0

    def test_best_discount_multiple_codes_higher_then_lower(self):
        # Tests value > best (True for first coupon, False for second weaker coupon)
        # On Sunday with cart 600:
        # WEEKEND20 gives 120 -> best becomes 120 (True branch)
        # FLAT100 gives 100 -> 100 > 120 is False (False branch: line 25 -> 23)
        # cap is 600 * 0.4 = 240, best (120) <= cap -> returns 120 (False branch of best > cap)
        assert best_discount(["WEEKEND20", "FLAT100"], 600, False, "sun") == 120.0

    def test_best_discount_cap_exceeded(self):
        # Cart 100, cap = 40. WEEKEND20 on sat returns 50.
        # best (50) > cap (40) is True -> returns cap (40.0)
        assert best_discount(["WEEKEND20"], 100, False, "sat") == 40.0

    def test_best_discount_cap_exact_boundary(self):
        # Cart 250, cap = 100. FLAT100 on 350 is 100, cap is 140 -> returns 100.
        # For cart 250, FLAT100 gives 0.
        # Let's test exact cap: WELCOME10 with new user on cart 500 -> 50.
        # cap = 500 * 0.4 = 200. best <= cap.
        assert best_discount(["WELCOME10"], 500, True, "mon") == 50.0


class TestIsExpiredBranchCoverage:
    """Branch coverage tests for coupon expiration rules."""

    def test_is_expired_zero_days(self):
        # days_valid <= 0 (True: 0)
        assert is_expired(10, 5, 0) is True

    def test_is_expired_negative_days(self):
        # days_valid <= 0 (True: negative)
        assert is_expired(10, 5, -2) is True

    def test_is_expired_strictly_expired(self):
        # days_valid > 0 (False branch of <= 0)
        # today - start > days_valid (True: 10 - 5 = 5 > 3)
        assert is_expired(10, 5, 3) is True

    def test_is_expired_exact_boundary_not_expired(self):
        # today - start > days_valid (False: 10 - 5 = 5 > 5 is False)
        assert is_expired(10, 5, 5) is False

    def test_is_expired_well_within_validity(self):
        # today - start > days_valid (False: 7 - 5 = 2 > 5 is False)
        assert is_expired(7, 5, 5) is False
