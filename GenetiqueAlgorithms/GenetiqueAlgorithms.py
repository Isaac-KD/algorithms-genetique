import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

from SnakeGame.Game import Game

def create_model(input_size, hidden_size, output_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(hidden_size, activation='relu', input_shape=(input_size,)),
        tf.keras.layers.Dense(hidden_size, activation='relu'),
        tf.keras.layers.Dense(output_size, activation='softmax')
    ])
    return model

def initialize_population(population_size, input_size, hidden_size, output_size):
    population = []
    for _ in range(population_size):
        model = create_model(input_size, hidden_size, output_size)
        population.append(model)
    return population

def evaluate_individual(model):
    game = Game()
    return game.run_model(model) # return the fitness of the model

def select_population(population, fitnesses, num_parent):
    sorted_indices = np.argsort(fitnesses)[::-1]
    selected_population = [population[i] for i in sorted_indices[:num_parent]]
    return selected_population

def crossover(parent1, parent2, input_size, hidden_size, output_size):
    child1, child2 = create_model(input_size, hidden_size, output_size), create_model(input_size, hidden_size, output_size)
    for i in range(len(parent1.layers)):
        if isinstance(parent1.layers[i], tf.keras.layers.Dense) and isinstance(parent2.layers[i], tf.keras.layers.Dense):
            w1, b1 = parent1.layers[i].get_weights()
            w2, b2 = parent2.layers[i].get_weights()
            midpoint = np.random.randint(w1.shape[1])
            new_w1 = np.concatenate([w1[:, :midpoint], w2[:, midpoint:]], axis=1)
            new_w2 = np.concatenate([w2[:, :midpoint], w1[:, midpoint:]], axis=1)
            child1.layers[i].set_weights([new_w1, b1])
            child2.layers[i].set_weights([new_w2, b2])
    return child1, child2

def mutate(model, mutation_rate=0.01):
    mutated_model = tf.keras.models.clone_model(model)  # Clonez le modèle d'origine
    for layer in mutated_model.layers:
        if isinstance(layer, tf.keras.layers.Dense):
            weights = layer.get_weights()  # Obtenez les poids du modèle
            mutated_weights = []  # Stockez les nouveaux poids mutés
            for w in weights:
                shape = w.shape
                mutation_mask = np.random.choice([0, 1], size=shape, p=[1 - mutation_rate, mutation_rate])
                mutation_values = np.random.normal(loc=0, scale=0.1, size=shape)  # Ajoutez un petit bruit gaussien
                mutated_weights.append(w + mutation_values * mutation_mask)
            layer.set_weights(mutated_weights)  # Appliquez les nouveaux poids mutés à la couche
    return mutated_model

def genetique_algo(population_size,input_size,hidden_size,output_size,num_generations,num_parents,name_fichier):
    population = initialize_population(population_size, input_size, hidden_size, output_size)
    print(" Starting genetique")
    for generation in range(num_generations):
        fitnesses = [evaluate_individual(model) for model in population]
        selected_population = select_population(population, fitnesses, num_parents)

        new_population = []
        for _ in range(len(population)-num_parents):
            parent1, parent2 = np.random.choice(selected_population, 2, replace=False)
            child1, child2 = crossover(parent1, parent2,input_size, hidden_size, output_size)
            new_population.extend([mutate(child1), mutate(child2)])
        
        population = new_population 
        
        #Affichage   
        best_fitness = max(fitnesses)
        # Ouvrir le fichier en mode ajout (append)
    with open("exemple.txt", "a") as fichier:
        fichier.write(f"Generation {generation}: Best Fitness = {best_fitness} \n")
        
    best_model_index = np.argmax(fitnesses)
    best_model = population[best_model_index]
    best_model.save(name_fichier+".h5")
    print("Best model saved as '"+name_fichier+".h5'")