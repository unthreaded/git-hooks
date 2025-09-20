"""
    Ensure a pull request has exactly one version label
"""
import os
import sys
import json

VALID_LABELS = {'Patch', 'Minor', 'Major', "no-release"}

def extract_labels_from_event(event_file: str) -> set[str]:
    """Extract label names from a GitHub event JSON file.

    Args:
        event_file: Path to the JSON event file produced by GitHub Actions.

    Returns:
        A set of label names (strings) found on the pull request.
    """
    with open(event_file, 'r', encoding='utf-8') as f:
        payload = json.load(f)
    labels = payload.get('pull_request', {}).get('labels', [])
    return {str(lbl.get('name', '')).strip() for lbl in labels}


def are_labels_valid(labels_on_pr: set[str]) -> bool:
    """Check whether the PR has exactly one allowed version label.

    Args:
        labels_on_pr: Set of label names present on the pull request.

    Returns:
        True if exactly one label from VALID_LABELS is present; otherwise False.
    """
    print(f"Found labels on pull request: {labels_on_pr}")
    overlap = VALID_LABELS.intersection(labels_on_pr)
    return len(overlap) == 1


if __name__ == "__main__":
    print("Checking pull request labels")
    event_path = sys.argv[1]
    success: bool = False
    if event_path and os.path.isfile(event_path):
        all_labels = extract_labels_from_event(event_path)
        success = are_labels_valid(all_labels)
    else:
        print("No labels found")

    if not success:
        print(f"Did not find exactly one of the following labels: {VALID_LABELS}")

    sys.exit(0 if success else 1)
