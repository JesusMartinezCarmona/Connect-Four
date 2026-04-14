import numpy as np
import random
import pickle
import os

class QAgent:
    def __init__(self, epsilon=0.2, alpha=0.5, gamma=0.9):
        self.q_table = {}  # Memoria del agente: {estado: {accion: valor_q}}
        self.epsilon = epsilon  # Tasa de exploración
        self.alpha = alpha      # Tasa de aprendizaje
        self.gamma = gamma      # Factor de descuento
        
    def get_q(self, state, action):
        return self.q_table.get(state, {}).get(action, 0.0)

    def choose_action(self, state, valid_actions):
        # Exploración (aleatorio) vs Explotación (mejor jugada)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(valid_actions)
        
        # Buscar la acción con el valor Q más alto
        q_values = [self.get_q(state, a) for a in valid_actions]
        max_q = max(q_values)
        
        # Si hay varias acciones con el mismo valor máximo, elegir una al azar
        best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state, next_valid_actions):
        old_q = self.get_q(state, action)
        
        if not next_valid_actions:
            next_max_q = 0.0
        else:
            next_max_q = max([self.get_q(next_state, a) for a in next_valid_actions])
            
        # Ecuación de Bellman para Q-Learning
        new_q = old_q + self.alpha * (reward + self.gamma * next_max_q - old_q)
        
        if state not in self.q_table:
            self.q_table[state] = {}
        self.q_table[state][action] = new_q

    def save_q_table(self, filename="q_table.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename="q_table.pkl"):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)