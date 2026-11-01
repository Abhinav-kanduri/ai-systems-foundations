"""Educational example: mathematical conservation is weaker than banking correctness."""

def transfer(balance_a: int, balance_b: int, amount: int):
    return balance_a - amount, balance_b + amount


def guarded_transfer(balance_a: int, balance_b: int, amount: int, authorized: bool):
    if not authorized:
        raise PermissionError("Unauthorized transfer")
    if amount < 0:
        raise ValueError("Amount must be nonnegative")
    if amount > balance_a:
        raise ValueError("Insufficient funds")
    return transfer(balance_a, balance_b, amount)


if __name__ == "__main__":
    for amount in [200, -100, 1200]:
        a, b = transfer(1000, 500, amount)
        print(f"amount={amount:5}, balances=({a}, {b}), conserved={a+b==1500}")
    print("Conservation holds even when business rules are violated.")
