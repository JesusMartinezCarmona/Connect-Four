from game import Connect4
from q_agent import QAgent
import time

def train_agent(episodes, epsilon):
    agent = QAgent(epsilon=epsilon)
    agent.load_q_table("q_table.pkl") # Cargar memoria si existe
    
    wins = 0
    losses = 0
    draws = 0

    print(f"\n--- Iniciando entrenamiento: {episodes} juegos | Epsilon: {epsilon} ---")
    start_time = time.time()

    for i in range(episodes):
        game = Connect4()
        game_over = False
        turn = 1 # 1: Agente (Aprende), 2: Random (Oponente)
        
        state = game.get_state()

        while not game_over:
            valid_locations = game.get_valid_locations()
            
            if turn == 1:
                action = agent.choose_action(state, valid_locations)
                game.drop_piece(action, 1)
                
                next_state = game.get_state()
                next_valid = game.get_valid_locations()
                reward = 0
                
                if game.check_win(1):
                    reward = 100  # Recompensa por ganar
                    wins += 1
                    game_over = True
                elif len(next_valid) == 0:
                    reward = 10   # Recompensa ligera por empatar
                    draws += 1
                    game_over = True
                else:
                    reward = -0.1 # Castigo ligero por cada paso (para ganar rápido)

                agent.learn(state, action, reward, next_state, next_valid)
                state = next_state
                turn = 2
            else:
                # Turno del Oponente Aleatorio
                action = random.choice(valid_locations)
                game.drop_piece(action, 2)
                
                if game.check_win(2):
                    # El agente perdió en el turno del oponente. Castigamos la última acción.
                    agent.learn(state, action, -100, game.get_state(), [])
                    losses += 1
                    game_over = True
                elif len(game.get_valid_locations()) == 0:
                    draws += 1
                    game_over = True
                
                state = game.get_state() # Actualizar estado para el agente
                turn = 1

    agent.save_q_table("q_table.pkl")
    
    print(f"Entrenamiento Finalizado en {round(time.time() - start_time, 2)}s")
    print(f"Victorias: {wins} | Derrotas: {losses} | Empates: {draws}")
    print(f"Estados aprendidos en Q-Table: {len(agent.q_table)}")

if __name__ == "__main__":
    import random 
    train_agent(episodes=10, epsilon=1.0) 
    # train_agent(episodes=1000, epsilon=0.5)
    # train_agent(episodes=10000, epsilon=0.1)