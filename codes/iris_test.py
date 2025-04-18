# lê o iris.csv
import pandas as pd
df = pd.read_csv('iris.csv')

# discretiza os dados numéricos (transforma números em categorias)
# divisão entre valores baixos, médios e altos
def discretize(coluna, n_bins=3):
    return pd.cut(coluna, bins=n_bins, labels=[f'bin{i}' for i in range(n_bins)])

for col in df.columns[:-1]:  # Ignora a última coluna (rótulo)
    df[col] = discretize(df[col])

#converter dataFram em para lista de listas
examples = df.values.tolist()
features = list(range(len(examples[0]) - 1))  # Índices das colunas, exceto a última

#treina a árvore
from decision_tree_builder import id3
tree = id3(examples, features)

#função para classificação de novos exemplos
def classify(tree, example):
    while not tree.is_leaf():
        feature_value = example[tree.feature]
        if feature_value in tree.children:
            tree = tree.children[feature_value]
        else:
            return None  # Valor desconhecido
    return tree.label

# avaliar árvore
# divide dados manualmente (70% treino / 30% teste)
# compara rótulo previsto com rótulo real, calcula acurácia
import random
random.shuffle(examples)
split_point = int(len(examples) * 0.7)
train_examples = examples[:split_point]
test_examples = examples[split_point:]

correct = 0
for e in test_examples:
    if classify(tree, e) == e[-1]:
        correct += 1
#cálculo acurácia
print("Acurácia:", correct / len(test_examples))