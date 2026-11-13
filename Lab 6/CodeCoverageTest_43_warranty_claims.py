
import pytest

from warranty_claims import (
    out_of_warranty_charge,
    claim_allowed,
    sla_status
)


# --------------------------------------------------
# 1. OUT OF WARRANTY CHARGE TESTS
# --------------------------------------------------

def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 20, "defect", False)


def test_negative_product_age():
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_registered_basic_plan():
    # Basic: 12 months + 6 registration months
    assert out_of_warranty_charge(
        "basic", 19, "defect", True
    ) == 100


def test_registered_premium_plan():
    # Premium does not receive the additional 6 months
    assert out_of_warranty_charge(
        "premium", 37, "defect", True
    ) == 100


def test_unregistered_standard_plan():
    assert out_of_warranty_charge(
        "standard", 25, "defect", False
    ) == 100


def test_within_warranty():
    assert out_of_warranty_charge(
        "standard", 20, "defect", False
    ) == 0


def test_accidental_claim_with_excess_under_12_months():
    assert out_of_warranty_charge(
        "basic", 13, "accidental", False
    ) == 200


def test_non_accidental_claim_with_excess_over_12_months():
    # 13 excess months × (100 + 50)
    assert out_of_warranty_charge(
        "basic", 25, "defect", False
    ) == 1950


def test_accidental_claim_with_excess_over_12_months():
    # 13 excess months × (200 + 50 + 25)
    assert out_of_warranty_charge(
        "basic", 25, "accidental", False
    ) == 3575


# --------------------------------------------------
# 2. CLAIM ALLOWED TESTS
# --------------------------------------------------

def test_recall_claim_within_limit():
    assert claim_allowed(10, 5, True) is True


def test_recall_claim_exceeds_limit():
    assert claim_allowed(10, 6, True) is False


def test_non_recall_claim_within_30_days():
    assert claim_allowed(29, 1, False) is False


def test_non_recall_claim_allowed():
    assert claim_allowed(30, 2, False) is True


def test_non_recall_claim_exceeds_limit():
    assert claim_allowed(30, 3, False) is False


# --------------------------------------------------
# 3. SLA STATUS TESTS
# --------------------------------------------------

def test_hardware_non_priority_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_non_hardware_non_priority_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_hardware_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_non_hardware_priority_on_track():
    assert sla_status(48, False, True) == "on_track"


def test_sla_at_risk():
    assert sla_status(36, True, False) == "at_risk"


def test_sla_critical():
    assert sla_status(35, True, False) == "critical"
