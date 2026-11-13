# def parse_claim(text):
#     plan, months = text.split(':')
#     return plan.strip().title(), float(months)

# def age_average(ages_csv):
#     values = [int(r) for r in ages_csv.split(',')]
#     return sum(values) // len(values)

# def payable_charge(text):
#     charge, discount = text.split('|')
#     total = float(charge) * 1.18 - float(discount)
#     return max(total, 0)

# def main():
#     print("==== Running parse_claim ====")
#     user_input = input("Enter plan:age in months (e.g. standard:30): ")
#     result = parse_claim(user_input)
#     print("Plan and Age:", result)

#     print("\n==== Running age_average ====")
#     user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
#     result = age_average(user_input)
#     print("Average Age:", result)

#     print("\n==== Running payable_charge ====")
#     user_input = input("Enter charge|discount (e.g. 1500|200): ")
#     result = payable_charge(user_input)
#     print("Payable Charge:", result)

# if __name__ == "__main__":
#     main()


import math


def parse_claim(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if text.count(':') != 1:
        raise ValueError("Invalid format. Use plan:months")

    plan, months = text.split(':')

    plan = plan.strip()

    if not plan:
        raise ValueError("Plan name cannot be empty")

    try:
        months = float(months.strip())
    except ValueError:
        raise ValueError("Months must be a valid number")

    if not math.isfinite(months) or months < 0:
        raise ValueError("Months must be non-negative")

    return plan.title(), months


def age_average(ages_csv):
    if not isinstance(ages_csv, str):
        raise ValueError("Input must be a string")

    if not ages_csv.strip():
        raise ValueError("Age list cannot be empty")

    try:
        values = [int(r.strip()) for r in ages_csv.split(',')]
    except ValueError:
        raise ValueError("Ages must be valid integers")

    if any(age < 0 for age in values):
        raise ValueError("Ages cannot be negative")

    return sum(values) // len(values)


def payable_charge(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    if text.count('|') != 1:
        raise ValueError("Invalid format. Use charge|discount")

    charge, discount = text.split('|')

    try:
        charge = float(charge.strip())
        discount = float(discount.strip())
    except ValueError:
        raise ValueError("Charge and discount must be numbers")

    if not math.isfinite(charge) or not math.isfinite(discount):
        raise ValueError("Amounts must be finite numbers")

    if charge < 0 or discount < 0:
        raise ValueError("Amounts cannot be negative")

    total = charge * 1.18 - discount

    if not math.isfinite(total):
        raise ValueError("Calculated amount is too large")

    return max(total, 0)


def main():
    print("==== Running parse_claim ====")

    try:
        user_input = input(
            "Enter plan:age in months (e.g. standard:30): "
        )
        result = parse_claim(user_input)
        print("Plan and Age:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running age_average ====")

    try:
        user_input = input(
            "Enter product ages as CSV (e.g. 12,24,36): "
        )
        result = age_average(user_input)
        print("Average Age:", result)
    except ValueError as e:
        print("Invalid input:", e)

    print("\n==== Running payable_charge ====")

    try:
        user_input = input(
            "Enter charge|discount (e.g. 1500|200): "
        )
        result = payable_charge(user_input)
        print("Payable Charge:", result)
    except ValueError as e:
        print("Invalid input:", e)


if __name__ == "__main__":
    main()
