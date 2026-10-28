
import secrets
import hashlib

ledger = {}
wallet_keys = {}


def create_wallet():
    private_key = secrets.token_hex(32)
    address = hashlib.sha256(private_key.encode()).hexdigest()
    wallet_keys[address] = private_key
    return private_key, address


def get_balance(address):
    return ledger.get(address, 0)


def send_funds(sender, receiver, amount, private_key):
    if wallet_keys.get(sender) != private_key:
        print("Invalid private key!")
        return False

    if amount <= 0 or get_balance(sender) < amount:
        print("Invalid amount or insufficient balance!")
        return False

    ledger[sender] -= amount
    ledger[receiver] = ledger.get(receiver, 0) + amount
    print("Transaction successful!")
    return True


if __name__ == "__main__":
    privA, addrA = create_wallet()
    privB, addrB = create_wallet()

    ledger[addrA] = 100

    print("Wallet A:", addrA)
    print("Wallet B:", addrB)
    print("Initial balances:", get_balance(addrA), get_balance(addrB))

    send_funds(addrA, addrB, 40, privA)

    print("Updated balances:", get_balance(addrA), get_balance(addrB))
