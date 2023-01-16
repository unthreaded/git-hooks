import sys

EXPECTED_LABELS = ['Patch', 'Minor', 'Major']

if __name__ == "__main__":
    # Default to empty string
    all_labels = sys.argv[1] or ""

    all_labels = all_labels.split(',')

    version_labels = list(filter(lambda label: label.strip() in EXPECTED_LABELS, all_labels))

    if len(version_labels) > 1:
        print(f"ERROR, needed exactly 1 label in ({EXPECTED_LABELS}), got: {all_labels}")
        exit(1)
    else:
        print('Labels look good!')
