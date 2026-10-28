
import hashlib
import json
import time


class VoteBlock:
    def __init__(self, voter, candidate, previous_hash):
        self.voter = voter
        self.candidate = candidate
        self.timestamp = time.time()
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


class VotingBlockchain:
    def __init__(self):
        self.chain = []
        self.voters = set()
        self.chain.append(VoteBlock("0", "Genesis", "0" * 64))

    def add_vote(self, voter, candidate):
        if voter in self.voters:
            print("Duplicate vote blocked:", voter)
            return

        block = VoteBlock(voter, candidate, self.chain[-1].hash)
        self.chain.append(block)
        self.voters.add(voter)
        print("Vote added:", voter, "->", candidate)

    def tally(self):
        result = {}
        for block in self.chain[1:]:
            result[block.candidate] = result.get(block.candidate, 0) + 1
        return result

    def validate(self):
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            if block.hash != block.calculate_hash():
                return False
            if block.previous_hash != self.chain[i - 1].hash:
                return False
        return True


if __name__ == "__main__":
    vb = VotingBlockchain()
    vb.add_vote("V001", "Alice")
    vb.add_vote("V002", "Bob")
    vb.add_vote("V003", "Alice")
    vb.add_vote("V001", "Alice")

    print("\nVote Tally:")
    for candidate, count in vb.tally().items():
        print(candidate, ":", count, "votes")

    print("Blockchain Length:", len(vb.chain))
    print("Blockchain Valid:", vb.validate())
