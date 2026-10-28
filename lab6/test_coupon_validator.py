import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ==============================================================================
# Code and Branch Coverage Test Cases for coupon_validator
# ==============================================================================

# --- Tests for coupon_discount ---

def test_welcome_coupon_new_user():
    """Validates WELCOME10 coupon for a new user (10% discount)."""
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20.0


def test_welcome_coupon_existing_user():
    """Validates WELCOME10 coupon for an existing user (0 discount)."""
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_empty_cart_error():
    """Validates that cart total <= 0 raises ValueError('empty cart')."""
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", -50, True, "mon")


def test_weekend_coupon_sat_large_cart():
    """Validates WEEKEND20 on Saturday with cart total >= 500 (20% discount)."""
    assert coupon_discount("WEEKEND20", 600, False, "sat") == 120.0
    assert coupon_discount("WEEKEND20", 500, False, "sat") == 100.0


def test_weekend_coupon_sat_small_cart():
    """Validates WEEKEND20 on Saturday with cart total < 500 (flat 50 discount)."""
    assert coupon_discount("WEEKEND20", 400, False, "sat") == 50


def test_weekend_coupon_sun_large_cart():
    """Validates WEEKEND20 on Sunday with cart total >= 500 (20% discount)."""
    assert coupon_discount("WEEKEND20", 1000, False, "sun") == 200.0


def test_weekend_coupon_sun_small_cart():
    """Validates WEEKEND20 on Sunday with cart total < 500 (flat 50 discount)."""
    assert coupon_discount("WEEKEND20", 350, False, "sun") == 50


def test_weekend_coupon_weekday():
    """Validates WEEKEND20 on a weekday (0 discount)."""
    assert coupon_discount("WEEKEND20", 700, False, "tue") == 0


def test_flat100_above_threshold():
    """Validates FLAT100 with cart total > 300 (100 discount)."""
    assert coupon_discount("FLAT100", 350, False, "mon") == 100


def test_flat100_exact_and_below_threshold():
    """Validates FLAT100 with cart total <= 300 (0 discount)."""
    assert coupon_discount("FLAT100", 300, False, "mon") == 0
    assert coupon_discount("FLAT100", 200, False, "mon") == 0


def test_unknown_coupon_code():
    """Validates fallback for unrecognized coupon codes."""
    assert coupon_discount("SPECIAL50", 1000, True, "sat") == 0


# --- Tests for best_discount ---

def test_best_discount_empty_list():
    """Validates best_discount when no coupon codes are provided."""
    assert best_discount([], 500, True, "sat") == 0


def test_best_discount_picks_highest():
    """Validates best_discount picks the best coupon among multiple options."""
    # On Sunday with cart 600:
    # WEEKEND20 gives 120
    # FLAT100 gives 100
    # WELCOME10 with is_new_user=False gives 0
    # Cap = 600 * 0.4 = 240. 120 <= 240 -> returns 120
    assert best_discount(["WEEKEND20", "FLAT100", "WELCOME10"], 600, False, "sun") == 120.0


def test_best_discount_exceeds_cap():
    """Validates that discount is capped at 40% of the cart total."""
    # Cart total = 100, Cap = 100 * 0.4 = 40.
    # WEEKEND20 on Saturday with cart 100 gives 50.
    # 50 > 40, so discount is capped at 40.
    assert best_discount(["WEEKEND20"], 100, False, "sat") == 40.0


def test_best_discount_at_boundary_cap():
    """Validates best_discount when best discount is within or at cap."""
    # Cart total = 250, Cap = 100. WELCOME10 gives 25. 25 <= 100 -> returns 25.
    assert best_discount(["WELCOME10"], 250, True, "mon") == 25.0


# --- Tests for is_expired ---

def test_zero_validity_expired():
    """Validates coupon is expired when days_valid is 0."""
    assert is_expired(10, 5, 0) is True


def test_negative_validity_expired():
    """Validates coupon is expired when days_valid is negative."""
    assert is_expired(10, 5, -1) is True


def test_validity_exceeded():
    """Validates coupon is expired when elapsed days exceed validity."""
    assert is_expired(10, 5, 3) is True


def test_validity_boundary_not_expired():
    """Validates coupon is still valid on the exact expiry day (today - start == days_valid)."""
    assert is_expired(10, 5, 5) is False


def test_validity_not_expired():
    """Validates coupon is valid when well within validity period."""
    assert is_expired(8, 5, 10) is False
