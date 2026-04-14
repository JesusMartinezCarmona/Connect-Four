import tkinter as tk
from tkinter import messagebox
from game import Connect4
from q_agent import QAgent
import os

class Connect4QGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Conecta 4 IA - Q-Learning (Arturo Ed.)")
        self.root.resizable(False, False)
        
        self.score_human = 0
        self.score_ai = 0
        self.game = Connect4()
        
        # --- CARGAR EL AGENTE ENTRENADO ---
        # Epsilon = 0.0 significa EXPLOTACIÓN PURA. El agente ya no explorará al azar,
        # solo usará su memoria para intentar ganarte o bloquearte.
        self.bot = QAgent(epsilon=0.0) 
        
        if os.path.exists("q_table.pkl"):
            self.bot.load_q_table("q_table.pkl")
            print(f"Memoria cargada exitosamente con {len(self.bot.q_table)} estados.")
        else:
            messagebox.showwarning("Advertencia", "No se encontró 'q_table.pkl'. El agente jugará al azar.")

        self.circles = []
        self.turn = 0 
        self.game_over = False

        # --- INTERFAZ VISUAL ---
        self.score_frame = tk.Frame(self.root, bg="gray20", pady=10)
        self.score_frame.pack(fill="x")
        self.label_score = tk.Label(self.score_frame, text=f"Tú: 0 | Q-Agent: 0", font=("Arial", 18, "bold"), fg="white", bg="gray20")
        self.label_score.pack()

        self.canvas = tk.Canvas(self.root, width=700, height=600, bg="blue", highlightthickness=0)
        self.canvas.pack()

        self.btn_frame = tk.Frame(self.root, width=700)
        self.btn_frame.pack()
        
        self.buttons = []
        for i in range(7):
            self.btn_frame.columnconfigure(i, minsize=100)
            btn = tk.Button(self.btn_frame, text="Tirar ↓", command=lambda c=i: self.human_move(c), font=("Arial", 9, "bold"), bg="#f0f0f0")
            btn.grid(row=0, column=i, sticky="ew", padx=2, pady=5)
            self.buttons.append(btn)

        self.btn_reset = tk.Button(self.root, text="🔄 Reiniciar Tablero", command=self.reset_game, font=("Arial", 10, "bold"), bg="orange", fg="white", pady=5)
        self.btn_reset.pack(pady=10)

        self.draw_empty_board()

    def draw_empty_board(self):
        self.circles = []
        self.canvas.delete("all")
        for r in range(6):
            row_circles = []
            for c in range(7):
                circle = self.canvas.create_oval(c*100+10, r*100+10, (c+1)*100-10, (r+1)*100-10, fill="white", outline="black")
                row_circles.append(circle)
            self.circles.append(row_circles)

    def update_board(self):
        for r in range(6):
            for c in range(7):
                p = self.game.board[r][c]
                color = "white"
                if p == 1: color = "red"
                elif p == 2: color = "yellow"
                self.canvas.itemconfig(self.circles[r][c], fill=color)
        self.label_score.config(text=f"Tú: {self.score_human} | Q-Agent: {self.score_ai}")

    def reset_game(self):
        self.game = Connect4()
        self.game_over = False
        self.turn = 0
        self.update_board()
        for b in self.buttons: b.config(state="normal")

    def human_move(self, col):
        if not self.game_over and self.turn == 0 and self.game.is_valid_location(col):
            self.game.drop_piece(col, 1)
            self.update_board()
            
            if self.game.check_win(1):
                self.score_human += 1
                self.end_round("¡Le ganaste a la máquina!")
                return
            
            if len(self.game.get_valid_locations()) == 0:
                self.end_round("¡Empate!")
                return

            self.turn = 1
            for b in self.buttons: b.config(state="disabled")
            self.root.after(400, self.bot_move) # Pequeña pausa visual

    def bot_move(self):
        if self.game_over: return
        
        # El agente lee el estado actual del tablero y busca en su memoria
        state = self.game.get_state()
        valid_locations = self.game.get_valid_locations()
        
        # El agente elige la mejor acción basada en su entrenamiento
        col = self.bot.choose_action(state, valid_locations)
        
        if col is not None:
            self.game.drop_piece(col, 2)
            self.update_board()
            
            if self.game.check_win(2):
                self.score_ai += 1
                self.end_round("El Q-Agent te ha ganado.")
                return
                
            if len(self.game.get_valid_locations()) == 0:
                self.end_round("¡Empate!")
                return
            
            self.turn = 0
            for b in self.buttons: b.config(state="normal")

    def end_round(self, msg):
        self.game_over = True
        self.update_board()
        for b in self.buttons: b.config(state="disabled")
        messagebox.showinfo("Fin de la Partida", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = Connect4QGUI(root)
    root.mainloop()