
import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status

def test_product_within_standard_warranty_has_no_charge():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_registered_basic_plan_gets_six_extra_months():
    # Basic coverage is 12 months, extended to 18 when registered.
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0


def test_defect_claim_within_first_twelve_excess_months():
    # Standard coverage is 24 months; 30 months means 6 excess months at 100/month.
    assert out_of_warranty_charge("standard", 30, "defect", False) == 600


def test_accidental_claim_within_first_twelve_excess_months():
    # Accidental claims use a rate of 200 per excess month.
    assert out_of_warranty_charge("standard", 30, "accidental", False) == 1200


def test_accidental_claim_more_than_twelve_months_out_of_warranty():
    # Basic coverage is 12 months; 25 months means 13 excess months.
    # Rate = 200 + 50 + 25 = 275; charge = 13 * 275.
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575




@pytest.mark.parametrize(
    "hours_left, is_hardware, is_priority, expected",
    [
        (72, True, True, "on_track"),
        (40, False, True, "at_risk"),
        (20, False, True, "critical"),
    ],
)
def test_sla_status_outcomes_for_priority_claims(
    hours_left, is_hardware, is_priority, expected
):
    assert sla_status(hours_left, is_hardware, is_priority) == expected