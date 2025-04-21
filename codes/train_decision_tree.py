#ler mcts_dataset.csv
import csv

def load_dataset(filename):
    dataset = []
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)
        dataset = [list(map(int, row)) for row in reader]
    return dataset


data = load_dataset('mcts_dataset.csv')
features = list(range(42)) # atributos s0 a s41

# dividir teste (30%) e treino (70%)
import random
random.shuffle(data)
split_point = int(0.7*len(data))
train_data = data[:split_point]
test_data = data[split_point:]

# treinar árvore
from decision_tree_builder import id3

tree = id3(train_data, features)

# testar e calcular acurácia
from decision_tree_builder import DecisionNode

def classify(tree, example):
    while not tree.is_leaf():
        feature_value = example[tree.feature]
        if feature_value in tree.children:
            tree = tree.children[feature_value]
        else:
            return tree.label
    return tree.label

# calcular acurácia
correct = 0
for example in test_data:
    predicted = classify(tree, example)
    actual = example[-1]
    if predicted == actual:
        correct += 1
accuracy = correct / len(test_data)
print(f"Acurácia da árvore de decisão: {accuracy:.2%}")


#função predict_move(state, tree) para jogar
def predict_move(state, tree):
    board_flat = [cell for row in state.board for cell in row]
    return classify(tree, board_flat)

# guardar árvore
import pickle
with open('decision_tree.pkl', 'wb') as f:
    pickle.dump(tree, f)

# carregar depois
# with open("decision_tree_connect4.pkl", "rb") as f:
#     tree = pickle.load(f)