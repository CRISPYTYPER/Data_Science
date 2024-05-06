import math
from collections import Counter, defaultdict


# Load data from a file
def load_data(filename):
    """
        Read the data from the given filename.

        Parameters:
            filename (str): File name to read.
                ex. "dt_train.txt"
        Return:
            examples (dict): A list of dictionaries of each training data.
                ex. [{'age': '<=30', 'income': 'high', 'student': 'no', 'credit_rating': 'fair', 'Class:buys_computer': 'no'},...]
            feature_attributes (list): A list of feature names (except target).
                ex. ['age', 'income', 'student', 'credit_rating']
            target_attribute (str): A name of target attribute.
                ex. "Class:buys_computer"
    """
    with open(filename, 'r') as file:
        attribute_names = file.readline().strip().split('\t')
        examples = list(dict(zip(attribute_names, line.strip().split('\t'))) for line in file)
        feature_attribute_names = attribute_names[:-1]
        target_attribute_name = attribute_names[-1]
        return examples, feature_attribute_names, target_attribute_name


# Calculate entropy
def entropy(examples, target_attribute_name):
    target_val_counts = Counter(example[target_attribute_name] for example in examples)
    examples_len = len(examples)
    return -sum((count / examples_len) * math.log2(count / examples_len) for count in target_val_counts.values())


# Calculate information gain
def information_gain(examples, attribute_name, target_attribute_name):
    original_entropy = entropy(examples, target_attribute_name)
    branches = defaultdict(list)
    for example in examples:
        branches[example[attribute_name]].append(example)
    after_entropy = sum((len(examples_in_branch) / len(examples)) * entropy(examples_in_branch, target_attribute_name) for examples_in_branch in branches.values())
    return original_entropy - after_entropy


# Calculate split information
def split_information(examples, attribute_name):
    counts = Counter(example[attribute_name] for example in examples)
    examples_len = len(examples)
    return -sum((count / examples_len) * math.log2(count / examples_len) for count in counts.values())


# Calculate gain ratio
def gain_ratio(examples, attribute_name, target_attribute_name):
    info_gain = information_gain(examples, attribute_name, target_attribute_name)
    split_info = split_information(examples, attribute_name)
    if split_info:
        return info_gain / split_info
    else:
        return 0


# Build the decision tree
def build_tree(examples, feature_attribute_names, target_attribute_name):
    distinct_targets = set(example[target_attribute_name] for example in examples)
    if len(distinct_targets) == 1:
        return distinct_targets.pop()
    elif len(feature_attribute_names) == 0:  # no more attributes to compare
        return Counter(example[target_attribute_name] for example in examples).most_common(1)[0][0]  # Return most common target attribute
    best_attribute = max(feature_attribute_names, key=lambda attr: gain_ratio(examples, attr, target_attribute_name))
    tree = {best_attribute: {}}
    remaining_attributes = [attr for attr in feature_attribute_names if attr != best_attribute]
    grouped_examples = defaultdict(list)
    for x in examples:
        grouped_examples[x[best_attribute]].append(x)
    for value, subset in grouped_examples.items():
        tree[best_attribute][value] = build_tree(subset, remaining_attributes, target_attribute_name)
    return tree


# Function to use the tree for prediction
def classify(tree, example):
    if type(tree) is not dict:
        return tree
        # leaf nodes are represented by their class label
        # instead of further dictionary structures

    attribute = next(iter(tree))
    attribute_value = example.get(attribute)
    if attribute_value in tree[attribute]:
        return classify(tree[attribute][attribute_value], example)
    return None  # Handle case where attribute value is not in the tree


# Main function to execute the workflow
def main(train_file, test_file, result_file):
    # Load training data
    train_data, feature_attribute_names, target_attribute_name = load_data(train_file)
    # Build a decision tree
    decision_tree = build_tree(train_data, feature_attribute_names, target_attribute_name)
    # Load test data
    test_data, _, _ = load_data(test_file)
    # Classify test data and write results
    with open(result_file, 'w') as file:
        for attribute in feature_attribute_names:
            file.write(f"{attribute}\t")
        file.write(f"{target_attribute_name}\n")

        for example in test_data:
            classification = classify(decision_tree, example)
            for feature_val in example.values():
                file.write(f"{feature_val}\t")
            file.write(f"{classification}\n")


if __name__ == '__main__':
    import sys

    main(*sys.argv[1:])
