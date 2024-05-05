import math
from collections import Counter, defaultdict


# Helper function to load data from a file
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
        attributes = file.readline().strip().split('\t')
        examples = [dict(zip(attributes, line.strip().split('\t'))) for line in file]
        feature_attributes = attributes[:-1]
        target_attribute = attributes[-1]
        return examples, feature_attributes, target_attribute

# Calculate entropy
def entropy(examples, target_attribute):
    counts = Counter(x[target_attribute] for x in examples)
    total = len(examples)
    return -sum((count / total) * math.log2(count / total) for count in counts.values() if count)

# Calculate information gain
def information_gain(examples, attribute, target_attribute):
    total_entropy = entropy(examples, target_attribute)
    subsets = defaultdict(list)
    for example in examples:
        subsets[example[attribute]].append(example)
    subset_entropy = sum((len(subset) / len(examples)) * entropy(subset, target_attribute) for subset in subsets.values())
    return total_entropy - subset_entropy

# Calculate split information
def split_information(examples, attribute):
    counts = Counter(x[attribute] for x in examples)
    total = len(examples)
    return -sum((count / total) * math.log2(count / total) for count in counts.values() if count)

# Calculate gain ratio
def gain_ratio(examples, attribute, target_attribute):
    info_gain = information_gain(examples, attribute, target_attribute)
    split_info = split_information(examples, attribute)
    return info_gain / split_info if split_info else 0

# Build the decision tree
def build_tree(examples, attributes, target_attribute):
    if len(set(x[target_attribute] for x in examples)) == 1:
        return examples[0][target_attribute]
    if not attributes:  # no more attributes to compare
        return Counter(x[target_attribute] for x in examples).most_common(1)[0][0]  # Return most common target attribute
    best_attribute = max(attributes, key=lambda attr: gain_ratio(examples, attr, target_attribute))
    tree = {best_attribute: {}}
    remaining_attributes = [attr for attr in attributes if attr != best_attribute]
    grouped_examples = defaultdict(list)
    for x in examples:
        grouped_examples[x[best_attribute]].append(x)
    for value, subset in grouped_examples.items():
        tree[best_attribute][value] = build_tree(subset, remaining_attributes, target_attribute)
    return tree

# Function to use the tree for prediction
def classify(tree, example):
    if type(tree) is not dict:
        return tree
        # leaf nodes are typically represented by their class label
        # instead of further dictionary structures

    attribute = next(iter(tree))
    attribute_value = example.get(attribute)
    if attribute_value in tree[attribute]:
        return classify(tree[attribute][attribute_value], example)
    return None # Handle case where attribute value is not in the tree


# Main function to execute the workflow
def main(train_file, test_file, result_file):
    # Load training data
    train_data, feature_attributes, target_attribute = load_data(train_file)
    # Build a decision tree
    decision_tree = build_tree(train_data, feature_attributes, target_attribute)
    # Load test data
    test_data, _, _ = load_data(test_file)
    # Classify test data and write results
    with open(result_file, 'w') as file:
        for attribute in feature_attributes:
            file.write(f"{attribute}\t")
        file.write(f"{target_attribute}\n")

        for example in test_data:
            classification = classify(decision_tree, example)
            for feature_val in example.values():
                file.write(f"{feature_val}\t")
            file.write(f"{classification}\n")

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])




