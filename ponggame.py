import tkinter as tk
import requests
import random

# ================= CONFIG =================
LARGURA = 800
ALTURA = 600

# ================= APP =================
class PongGame:
    def __init__(self):
        self.usuario = ""
        self.criar_login()

    # ================= LOGIN =================
    def criar_login(self):
        self.login = tk.Tk()
        self.login.title("Login")
        self.login.configure(bg="black")

        tk.Label(self.login, text="Usuário", fg="cyan", bg="black").pack()
        self.entrada_user = tk.Entry(self.login)
        self.entrada_user.pack()

        tk.Label(self.login, text="Senha", fg="cyan", bg="black").pack()
        self.entrada_senha = tk.Entry(self.login, show="*")
        self.entrada_senha.pack()

        tk.Button(self.login, text="Entrar", command=self.validar_login,
                  bg="purple", fg="white").pack(pady=10)

        self.msg = tk.Label(self.login, text="", fg="red", bg="black")
        self.msg.pack()

        self.login.mainloop()

    def validar_login(self):
        user = self.entrada_user.get()
        senha = self.entrada_senha.get()

        if user == "" or senha == "":
            self.msg.config(text="Preencha tudo!")
        else:
            self.usuario = user
            self.login.destroy()
            self.criar_menu()

    # ================= MENU =================
    def criar_menu(self):
        self.menu = tk.Tk()
        self.menu.title("Menu")
        self.menu.configure(bg="black")

        tk.Label(self.menu, text=f"Bem-vindo, {self.usuario}",
                 fg="cyan", bg="black", font=("Courier", 16)).pack(pady=20)

        tk.Button(self.menu, text="Jogar", command=self.iniciar_jogo,
                  bg="purple", fg="white", width=20).pack(pady=10)

        tk.Button(self.menu, text="Sair", command=self.menu.destroy,
                  bg="red", fg="white", width=20).pack(pady=10)

        self.menu.mainloop()

    # ================= API =================
    def enviar_pontos(self):
        try:
            requests.post("https://httpbin.org/post", json={
                "usuario": self.usuario,
                "pontos_esq": self.pontos_esq,
                "pontos_dir": self.pontos_dir
            })
        except:
            print("Erro API")

    # ================= JOGO =================
    def iniciar_jogo(self):
        self.menu.destroy()

        self.janela = tk.Tk()
        self.janela.title("Pong Neon 80s")

        self.canvas = tk.Canvas(self.janela, width=LARGURA, height=ALTURA, bg="black")
        self.canvas.pack()

        # Linha central
        for i in range(0, ALTURA, 20):
            self.canvas.create_line(400, i, 400, i+10, fill="purple")

        # Objetos
        self.barra_esq = self.canvas.create_rectangle(30, 250, 40, 350, fill="cyan")
        self.barra_dir = self.canvas.create_rectangle(760, 250, 770, 350, fill="magenta")
        self.bola = self.canvas.create_oval(390, 290, 410, 310, fill="white")

        # Velocidade
        self.vel_bola_x = random.choice([-5, 5])
        self.vel_bola_y = random.choice([-5, 5])
        self.vel_esq = 0
        self.vel_dir = 0

        # Pontos
        self.pontos_esq = 0
        self.pontos_dir = 0

        self.texto = self.canvas.create_text(
            400, 30, fill="cyan",
            font=("Courier", 20, "bold"),
            text="0 x 0"
        )

        # BOTÃO REINICIAR
        tk.Button(self.janela, text="Reiniciar", command=self.resetar_jogo,
                  bg="purple", fg="white").pack()

        # Controles
        self.janela.bind("<KeyPress>", self.tecla_press)
        self.janela.bind("<KeyRelease>", self.tecla_solta)

        self.loop()
        self.janela.mainloop()

    def tecla_press(self, e):
        if e.keysym == "w": self.vel_esq = -8
        if e.keysym == "s": self.vel_esq = 8
        if e.keysym == "Up": self.vel_dir = -8
        if e.keysym == "Down": self.vel_dir = 8

    def tecla_solta(self, e):
        if e.keysym in ("w", "s"): self.vel_esq = 0
        if e.keysym in ("Up", "Down"): self.vel_dir = 0

    def resetar_jogo(self):
        self.pontos_esq = 0
        self.pontos_dir = 0
        self.canvas.coords(self.bola, 390, 290, 410, 310)

    def limitar_barra(self, barra):
        x1, y1, x2, y2 = self.canvas.coords(barra)

        if y1 < 0:
            self.canvas.move(barra, 0, -y1)
        if y2 > ALTURA:
            self.canvas.move(barra, 0, ALTURA - y2)

    def loop(self):
        # Movimento
        self.canvas.move(self.barra_esq, 0, self.vel_esq)
        self.canvas.move(self.barra_dir, 0, self.vel_dir)
        self.canvas.move(self.bola, self.vel_bola_x, self.vel_bola_y)

        # Limites das barras
        self.limitar_barra(self.barra_esq)
        self.limitar_barra(self.barra_dir)

        pos = self.canvas.coords(self.bola)

        # Topo/baixo
        if pos[1] <= 0 or pos[3] >= ALTURA:
            self.vel_bola_y *= -1

        # Colisão com barras
        if self.canvas.coords(self.barra_esq)[2] >= pos[0] and \
           self.canvas.coords(self.barra_esq)[1] <= pos[1] <= self.canvas.coords(self.barra_esq)[3]:
            self.vel_bola_x = abs(self.vel_bola_x) + 0.5

        if self.canvas.coords(self.barra_dir)[0] <= pos[2] and \
           self.canvas.coords(self.barra_dir)[1] <= pos[3] <= self.canvas.coords(self.barra_dir)[3]:
            self.vel_bola_x = -abs(self.vel_bola_x) - 0.5

        # Gol
        if pos[2] >= LARGURA:
            self.pontos_esq += 1
            self.enviar_pontos()
            self.reset_bola()

        if pos[0] <= 0:
            self.pontos_dir += 1
            self.enviar_pontos()
            self.reset_bola()

        # Atualiza placar
        self.canvas.itemconfig(self.texto,
                               text=f"{self.pontos_esq} x {self.pontos_dir}")

        self.janela.after(16, self.loop)

    def reset_bola(self):
        self.canvas.coords(self.bola, 390, 290, 410, 310)
        self.vel_bola_x = random.choice([-5, 5])
        self.vel_bola_y = random.choice([-5, 5])


# ================= EXECUTAR =================
PongGame()
