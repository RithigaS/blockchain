
# Experiment 1: Merkle Tree-Based Verification System
# Using SHA-256 to verify file integrity

# Import required Python modules
import os
import json
import hashlib

# Folder containing the sample text files
FOLDER = "sample_files"

# File used to store the original Merkle Root and metadata
METADATA_FILE = "merkle_metadata.json"


# Function to calculate the SHA-256 hash of data
def sha256_hex(data: bytes) -> str:
    # Generate the hash and return it in hexadecimal format
    return hashlib.sha256(data).hexdigest()


# Function to read a file and calculate its hash
def file_hash(path: str) -> str:
    # Open the file in binary read mode
    with open(path, "rb") as f:
        # Read the file contents and calculate its hash
        return sha256_hex(f.read())


# Function to create the next layer of the Merkle Tree
def merkle_layer(hashes):

    # If the number of hashes is odd, duplicate the last hash
    if len(hashes) % 2 == 1:
        hashes = hashes + [hashes[-1]]

    # Store the parent hashes in this list
    parent = []

    # Process two hashes at a time
    for i in range(0, len(hashes), 2):

        # Convert hexadecimal hashes into bytes and combine them
        combined = (
            bytes.fromhex(hashes[i])
            + bytes.fromhex(hashes[i + 1])
        )

        # Hash the combined data and store the parent hash
        parent.append(sha256_hex(combined))

    # Return the new layer of parent hashes
    return parent


# Function to build the complete Merkle Tree
def build_merkle_tree(file_paths):

    # Calculate the hash of every file (leaf hashes)
    leaves = [file_hash(path) for path in file_paths]

    # Check whether any files were found
    if not leaves:
        raise ValueError("No text files found in sample_files!")

    # Store all layers, starting with the leaf hashes
    tree = [leaves]

    # Start building from the leaf layer
    layer = leaves

    # Continue until only one hash remains
    while len(layer) > 1:

        # Generate the next parent layer
        layer = merkle_layer(layer)

        # Add the new layer to the tree
        tree.append(layer)

    # Return the complete tree; the last hash is the root
    return tree


# Function to generate the Merkle Proof for a selected leaf
def merkle_proof(tree, index):

    # Store sibling hashes needed for verification
    proof = []

    # Start with the selected leaf's index
    idx = index

    # Visit every layer except the root layer
    for layer in tree[:-1]:

        # If the index is even, its sibling is on the right
        if idx % 2 == 0:

            # If no right sibling exists, use the same hash
            sibling = idx + 1 if idx + 1 < len(layer) else idx

        # If the index is odd, its sibling is on the left
        else:
            sibling = idx - 1

        # Add the sibling hash to the proof
        proof.append(layer[sibling])

        # Move to the parent's index
        idx //= 2

    # Return the list of sibling hashes
    return proof


# Function to verify a Merkle Proof
def verify_proof(leaf_hash, proof, root, index):

    # Start with the selected file's hash
    computed = leaf_hash

    # Store the current node's index
    idx = index

    # Reconstruct the root using the proof
    for sibling in proof:

        # If the current node is on the left, hash it first
        if idx % 2 == 0:
            combined = (
                bytes.fromhex(computed)
                + bytes.fromhex(sibling)
            )

        # If the current node is on the right, hash its sibling first
        else:
            combined = (
                bytes.fromhex(sibling)
                + bytes.fromhex(computed)
            )

        # Calculate the parent hash
        computed = sha256_hex(combined)

        # Move to the parent's index
        idx //= 2

    # Return True if the calculated root matches the stored root
    return computed == root


# Main program starts here
if __name__ == "__main__":

    # Find all text files inside the sample_files folder
    # Sort them so that file ordering remains consistent
    files = sorted(
        os.path.join(FOLDER, name)
        for name in os.listdir(FOLDER)
        if name.endswith(".txt")
    )

    # Build the Merkle Tree using the sample files
    tree = build_merkle_tree(files)

    # Get the root hash from the last layer
    current_root = tree[-1][0]

    # Check whether the original metadata file already exists
    if os.path.exists(METADATA_FILE):

        # Read the previously saved metadata
        with open(METADATA_FILE, "r") as f:
            metadata = json.load(f)

        # Retrieve the original Merkle Root
        stored_root = metadata["root"]

        print("Original stored root:", stored_root)

    else:
        # On the first run, save the current root as the original root
        stored_root = current_root

        # Prepare the metadata containing filenames and leaf hashes
        metadata = {
            "files": [os.path.basename(p) for p in files],
            "leaf_hashes": tree[0],
            "root": stored_root
        }

        # Save the metadata in JSON format
        with open(METADATA_FILE, "w") as f:
            json.dump(metadata, f, indent=4)

        print("Original root saved to metadata.")

    # Display every file and its leaf hash
    print("\nFiles and leaf hashes:")

    for path, h in zip(files, tree[0]):
        print(f"{path} -> {h}")

    # Display the newly calculated Merkle Root
    print("\nCurrent Merkle Root:", current_root)

    # Compare the current root with the original stored root
    print("Matches stored root:", current_root == stored_root)

    # Generate a proof for the second file (index 1)
    if len(files) >= 2:

        # Select the second file
        index = 1

        # Generate its Merkle Proof
        proof = merkle_proof(tree, index)

        # Display the proof
        print("\nProof for:", files[index])
        print(proof)

        # Verify the selected file using its leaf hash and proof
        valid = verify_proof(
            tree[0][index],
            proof,
            stored_root,
            index
        )

        # Display the verification result
        print("\nVerification result:", valid)
