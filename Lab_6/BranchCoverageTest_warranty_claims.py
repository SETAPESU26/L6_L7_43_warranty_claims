
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status
)

# -----------------------------------------
# 1. OUT OF WARRANTY CHARGE TEST CASES
# -----------------------------------------

def test_unregistered_product_does_not_get_registration_extension():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_registered_non_premium_product_gets_registration_extension():
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0


def test_registered_premium_product_does_not_get_another_extension():
    assert out_of_warranty_charge("premium", 40, "defect", True) == 400


def test_exact_end_of_warranty_has_zero_charge():
    assert out_of_warranty_charge("basic", 12, "defect", False) == 0


def test_defect_claim_with_six_excess_months():
    assert out_of_warranty_charge("standard", 30, "defect", False) == 600


def test_accidental_claim_with_six_excess_months():
    assert out_of_warranty_charge("standard", 30, "accidental", False) == 1200


def test_defect_claim_with_more_than_twelve_excess_months():
    assert out_of_warranty_charge("basic", 25, "defect", False) == 1950


def test_accidental_claim_with_more_than_twelve_excess_months():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575


# -----------------------------------------
# 2. CLAIM ALLOWED TEST CASES
# -----------------------------------------

def test_recall_claim_at_limit_is_allowed():
    assert claim_allowed(0, 5, True) is True


def test_recall_claim_above_limit_is_not_allowed():
    assert claim_allowed(0, 6, True) is False


def test_non_recall_claim_before_thirty_days_is_not_allowed():
    assert claim_allowed(29, 1, False) is False


def test_non_recall_claim_after_thirty_days_at_limit_is_allowed():
    assert claim_allowed(30, 2, False) is True


def test_non_recall_claim_after_thirty_days_above_limit_is_not_allowed():
    assert claim_allowed(30, 3, False) is False


# -----------------------------------------
# 3. SLA STATUS TEST CASES
# -----------------------------------------

@pytest.mark.parametrize(
    "hours_left, is_hardware, is_priority, expected",
    [
        (72, True, True, "on_track"),
        (48, True, False, "on_track"),
        (36, True, False, "at_risk"),
        (35, True, False, "critical"),
        (24, False, False, "on_track"),
        (36, False, True, "at_risk"),
        (35, False, True, "critical"),
    ],
)
def test_sla_status_all_decision_outcomes(
    hours_left, is_hardware, is_priority, expected
):
    assert sla_status(
        hours_left, is_hardware, is_priority
    ) == expected
