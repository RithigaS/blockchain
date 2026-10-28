
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

        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith("000"):
                break
            self.nonce += 1

    def calculate_hash(self):
        data = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        self.chain.append(Block(0, ["Genesis Block"], "0" * 64))

    def add_block(self, transactions):
        block = Block(
            len(self.chain), transactions, self.chain[-1].hash
        )
        self.chain.append(block)

    def is_valid(self):
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False
            if not block.hash.startswith("000"):
                return False
            if i > 0 and block.previous_hash != self.chain[i - 1].hash:
                return False
        return True


def consensus(nodes):
    valid_nodes = [n for n in nodes if n.is_valid()]
    if not valid_nodes:
        return

    longest = max(valid_nodes, key=lambda n: len(n.chain)).chain
    for node in nodes:
        if not node.is_valid() or len(node.chain) < len(longest):
            node.chain = longest.copy()


if __name__ == "__main__":
    node1, node2, node3 = Blockchain(), Blockchain(), Blockchain()

    node1.add_block(["A pays B 5"])
    node1.add_block(["C pays D 7"])
    node2.add_block(["X pays Y 10"])
    node3.add_block(["M pays N 2"])

    nodes = [node1, node2, node3]

    print("Before consensus:")
    for i, node in enumerate(nodes, 1):
        print(f"Node {i}: {len(node.chain)} blocks")

    consensus(nodes)

    print("\nAfter consensus:")
    for i, node in enumerate(nodes, 1):
        print(f"Node {i}: {len(node.chain)} blocks")

    print("Consensus achieved:", all(
        n.chain[-1].hash == nodes[0].chain[-1].hash
        for n in nodes
    ))

