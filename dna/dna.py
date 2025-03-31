import csv
import sys

def main():
    ## CLI ##
    # Check arg length
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <dna_sequence.txt>")
        sys.exit(1)

    cli = sys.argv
    db_path = cli[1]
    sequence_path = cli[2]

    ## Database ##
    db = load_database(db_path)

    ## Sequences ##
    sequence = load_dna_sequence(sequence_path)

    ## STR ##
    # Counting
    str_counts = {}
    for str_name in db[0].keys():
        if str_name != 'name': # Prevent CSV header mismatch
            str_counts[str_name] = longest_match(sequence, str_name)

    # Comparing and showing result
    profile_matching = compare(db, str_counts)
    
    if profile_matching:
        print(f"DNA Profile match found: {profile_matching}")
    else:
        print("No DNA Profile match found")

def load_database(filename):
    """Load database by filename"""
    db = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            db.append(row)
    return db

def load_dna_sequence(filename):
    """Load DNA sequence file"""
    with open(filename, "r") as f:
        return f.read().strip()

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1
            
            # If there is no match in the substring
            else:
                break
        
        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run

def compare(db, str_counts):
    for person in db:
        is_profile_match = True
        for str_name, count in str_counts.items():
            if int(person[str_name]) != count:
                is_profile_match = False
                break
        if is_profile_match:
            return person['name']
    return None


if __name__ == "__main__":
    main()
