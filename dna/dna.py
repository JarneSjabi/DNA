import csv
import sys

def main():
    # Check arg length
    if len(sys.argv) != 3:
        print("Usage: python dna.py <database.csv> <dna_sequence.txt>")
        sys.exit(1)

    db_filename = sys.argv[1]
    dna_filename = sys.argv[2]

    db = load_database(db_filename)

    # Sequences #
    sequence = load_dna_sequence(dna_filename)

    # STR-counting
    str_counts = {}
    for str_name in db[0].keys():
        if str_name != 'name':
            str_counts[str_name] = longest_match(sequence, str_name)

    # STR-Compare
    match = check_for_match(db, str_counts)
    
    if match:
        print(f"Match found: {match}")
    else:
        print("No match found")


def load_database(filename):
    db = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            db.append(row)
    return db


def load_dna_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def longest_match(sequence, subsequence):
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run


def check_for_match(db, str_counts):
    for person in db:
        match = True
        for str_name, count in str_counts.items():
            if int(person[str_name]) != count:
                match = False
                break
        if match:
            return person['name']
    return None


if __name__ == "__main__":
    main()
