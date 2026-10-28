
import hashlib
import json
import time


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.mine()

    def calculate_hash(self):
        data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine(self):
        while True:
            h = self.calculate_hash()
            if h.startswith("0000"):
                return h
            self.nonce += 1


class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending = []
        self.chain.append(Block(0, ["Genesis Block"], "0"))

    def add_transaction(self, sender, receiver, amount):
        if sender and receiver and amount > 0:
            self.pending.append({
                "sender": sender,
                "receiver": receiver,
                "amount": amount
            })

    def add_block(self):
        if self.pending:
            block = Block(
                len(self.chain), self.pending.copy(),
                self.chain[-1].hash
            )
            self.chain.append(block)
            self.pending = []

    def validate(self):
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False
            if not block.hash.startswith("0000"):
                return False
            if i > 0 and block.previous_hash != self.chain[i-1].hash:
                return False
        return True


if __name__ == "__main__":
    bc = Blockchain()
    bc.add_transaction("Alice", "Bob", 50)
    bc.add_block()
    bc.add_transaction("Charlie", "David", 20)
    bc.add_block()

    for b in bc.chain:
        print("Block:", b.index)
        print("Transactions:", b.transactions)
        print("Hash:", b.hash)
        print("Nonce:", b.nonce)
        print()

    print("Blockchain valid:", bc.validate())
