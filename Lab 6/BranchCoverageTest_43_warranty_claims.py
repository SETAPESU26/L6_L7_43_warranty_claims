
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status
)


# ==================================================
# 1. OUT OF WARRANTY CHARGE - BRANCH TESTS
# ==================================================

def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 20, "defect", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_registered_non_premium():
    # Registered basic gets 6 additional months.
    assert out_of_warranty_charge(
        "basic", 19, "defect", True
    ) == 100


def test_registered_premium():
    # Premium does not get additional registration months.
    assert out_of_warranty_charge(
        "premium", 37, "defect", True
    ) == 100


def test_unregistered_customer():
    # Registration condition is false.
    assert out_of_warranty_charge(
        "standard", 25, "defect", False
    ) == 100


def test_within_warranty():
    # excess <= 0 is true.
    assert out_of_warranty_charge(
        "standard", 20, "defect", False
    ) == 0


def test_defect_claim_with_small_excess():
    # Non-accidental claim, excess <= 12.
    assert out_of_warranty_charge(
        "basic", 13, "defect", False
    ) == 100


def test_accidental_claim_with_small_excess():
    # Accidental claim, excess <= 12.
    assert out_of_warranty_charge(
        "basic", 13, "accidental", False
    ) == 200


def test_defect_claim_with_large_excess():
    # excess > 12, non-accidental claim.
    assert out_of_warranty_charge(
        "basic", 25, "defect", False
    ) == 1950


def test_accidental_claim_with_large_excess():
    # excess > 12, accidental claim.
    assert out_of_warranty_charge(
        "basic", 25, "accidental", False
    ) == 3575


# ==================================================
# 2. CLAIM ALLOWED - BRANCH TESTS
# ==================================================

def test_recall_claim_allowed():
    # Recall = True, claims <= 5.
    assert claim_allowed(10, 5, True) is True


def test_recall_claim_not_allowed():
    # Recall = True, claims > 5.
    assert claim_allowed(10, 6, True) is False


def test_non_recall_within_30_days():
    # Recall = False, days < 30.
    assert claim_allowed(29, 1, False) is False


def test_non_recall_after_30_days_allowed():
    # Recall = False, days >= 30, claims <= 2.
    assert claim_allowed(30, 2, False) is True


def test_non_recall_exceeds_claim_limit():
    # Recall = False, days >= 30, claims > 2.
    assert claim_allowed(30, 3, False) is False


# ==================================================
# 3. SLA STATUS - BRANCH TESTS
# ==================================================

def test_hardware_non_priority_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_non_hardware_non_priority_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_hardware_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_non_hardware_priority_on_track():
    assert sla_status(48, False, True) == "on_track"


def test_sla_at_risk():
    # Hardware cutoff = 48, at-risk boundary = 36.
    assert sla_status(36, True, False) == "at_risk"


def test_sla_critical():
    # Below the at-risk boundary.
    assert sla_status(35, True, False) == "critical"
