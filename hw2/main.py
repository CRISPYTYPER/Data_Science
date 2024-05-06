import sys
import math
from collections import Counter, defaultdict


def load_data(filename):
    """
        Read the data from the given filename.

        Parameters:
            filename (str): File name to read.
                ex. "dt_train.txt"
        Return:
            examples (dict): A list of dictionaries of each training data.
                ex. [{'age': '<=30', 'income': 'high', 'student': 'no', 'credit_rating': 'fair', 'Class:buys_computer': 'no'},...]
            feature_attribute_names (list): A list of feature names (except target).
                ex. ['age', 'income', 'student', 'credit_rating']
            target_attribute_name (str): A name of target attribute.
                ex. "Class:buys_computer"
    """
    with open(filename, 'r') as file:
        attribute_names = file.readline().strip().split('\t')
        examples = list(dict(zip(attribute_names, line.strip().split('\t'))) for line in file)
        feature_attribute_names = attribute_names[:-1]
        target_attribute_name = attribute_names[-1]
        return examples, feature_attribute_names, target_attribute_name


def entropy(examples, target_attribute_name):
    target_val_counts = Counter(example[target_attribute_name] for example in examples)
    examples_len = len(examples)
    return -sum((count / examples_len) * math.log2(count / examples_len) for count in target_val_counts.values())


def information_gain(examples, attribute_name, target_attribute_name):
    original_entropy = entropy(examples, target_attribute_name)
    branches = defaultdict(list)
    for example in examples:
        branches[example[attribute_name]].append(example)
    after_entropy = sum((len(examples_in_branch) / len(examples)) * entropy(examples_in_branch, target_attribute_name) for examples_in_branch in branches.values())
    return original_entropy - after_entropy


def split_information(examples, attribute_name):
    counts = Counter(example[attribute_name] for example in examples)
    examples_len = len(examples)
    return -sum((count / examples_len) * math.log2(count / examples_len) for count in counts.values())


def gain_ratio(examples, attribute_name, target_attribute_name):
    info_gain = information_gain(examples, attribute_name, target_attribute_name)
    split_info = split_information(examples, attribute_name)
    if split_info != 0:
        return info_gain / split_info
    else:
        return 0


def build_tree(examples, feature_attribute_names, target_attribute_name):
    distinct_targets = set(example[target_attribute_name] for example in examples)
    if len(distinct_targets) == 1:
        return distinct_targets.pop()
    elif len(feature_attribute_names) == 0:  # no more attributes to compare
        return Counter(example[target_attribute_name] for example in examples).most_common(1)[0][0]  # Return most common target attribute
    best_attribute_name = max(feature_attribute_names, key=lambda attribute: gain_ratio(examples, attribute, target_attribute_name))
    tree = {best_attribute_name: {}}
    remaining_attribute_names = [attr for attr in feature_attribute_names if attr != best_attribute_name]
    branched_examples = defaultdict(list)  # list of branched examples separated by "best_attribute_name"
    for example in examples:
        branched_examples[example[best_attribute_name]].append(example)
    for best_attribute_value, examples_in_one_branch in branched_examples.items():
        tree[best_attribute_name][best_attribute_value] = build_tree(examples_in_one_branch, remaining_attribute_names, target_attribute_name)
    return tree


def classify(tree, example):
    if type(tree) is not dict:
        return tree
        # leaf nodes are represented by their class label
        # instead of further dictionary structures

    branching_attribute_name = list(tree.keys())[0]
    attribute_value = example[branching_attribute_name]
    if attribute_value in tree[branching_attribute_name]:
        return classify(tree[branching_attribute_name][attribute_value], example)
    return None  # If attribute value of training example is not in the tree


# Main function
def main(train_file, test_file, result_file):
    # Load training data
    train_examples, feature_attribute_names, target_attribute_name = load_data(train_file)
    # Build a decision tree
    decision_tree = build_tree(train_examples, feature_attribute_names, target_attribute_name)
    # Load test data
    test_examples, _, _ = load_data(test_file)
    # Classify test data and write results
    with open(result_file, 'w') as file:
        for attribute in feature_attribute_names:
            file.write(f"{attribute}\t")
        file.write(f"{target_attribute_name}\n")

        for example in test_examples:
            classification = classify(decision_tree, example)
            for feature_val in example.values():
                file.write(f"{feature_val}\t")
            file.write(f"{classification}\n")


if __name__ == '__main__':
    main(*sys.argv[1:])
