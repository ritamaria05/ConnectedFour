import math
from collections import Counter, defaultdict

class DecisionNode:
    def __init__(self, feature=None, value=None, children=None, label=None):
        self.feature = feature      # Feature index (e.g., column number)
        self.value = value          # Value to split on (for printing/tree tracing)
        self.children = children or {}  # Dict: value -> DecisionNode
        self.label = label          # If leaf node, the class label

    def is_leaf(self):
        return self.label is not None


def entropy(examples):
    label_counts = Counter(example[-1] for example in examples)
    total = len(examples)
    return -sum((count / total) * math.log2(count / total) for count in label_counts.values())


def information_gain(examples, feature_index):
    total_entropy = entropy(examples)
    subsets = defaultdict(list)
    
    for example in examples:
        subsets[example[feature_index]].append(example)

    weighted_entropy = sum(
        (len(subset) / len(examples)) * entropy(subset)
        for subset in subsets.values()
    )
    
    return total_entropy - weighted_entropy


def majority_class(examples):
    labels = [example[-1] for example in examples]
    return Counter(labels).most_common(1)[0][0]


def id3(examples, features):
    labels = [example[-1] for example in examples]
    
    # Base case 1: all examples have same label
    if labels.count(labels[0]) == len(labels):
        return DecisionNode(label=labels[0])
    
    # Base case 2: no more features to split
    if not features:
        return DecisionNode(label=majority_class(examples))
    
    # Choose best feature
    gains = [(f, information_gain(examples, f)) for f in features]
    best_feature, best_gain = max(gains, key=lambda x: x[1])

    # If no gain, make it a leaf
    if best_gain == 0:
        return DecisionNode(label=majority_class(examples))

    node = DecisionNode(feature=best_feature)

    # Partition on best feature
    feature_values = set(example[best_feature] for example in examples)
    for value in feature_values:
        subset = [ex for ex in examples if ex[best_feature] == value]
        if not subset:
            node.children[value] = DecisionNode(label=majority_class(examples))
        else:
            remaining_features = [f for f in features if f != best_feature]
            child = id3(subset, remaining_features)
            child.value = value
            node.children[value] = child

    return node
