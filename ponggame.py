import tkinter as tk
import requests
import random

# ================= LOGIN =================
def entrar():
    global usuario
    usuario = entrada_user.get()
    login.destroy()
    iniciar_jogo()

login = tk.Tk()
login.title("Login")
login.configure(bg="black")

tk.Label(login, text="Usuário", fg="cyan", bg="black").pack()
entrada_user = tk.Entry(login)
entrada_user.pack()

tk.Label(login, text="Senha", fg="cyan", bg="black").pack()
entrada_senha = tk.Entry(login, show="*")
entrada_senha.pack()

tk.Button(login, text="Entrar", command=entrar, bg="purple", fg="white").pack(pady=10)

# ================= API =================
def enviar_pontos(p1, p2):
    try:
        requests.post("https://httpbin.org/post", json={
            "usuario": usuario,
            "pontos_esq": p1,
            "pontos_dir": p2
        })
    except:
        print("Erro API")

# ================= JOGO =================
def iniciar_jogo():
    global canvas, barra_esq, barra_dir, bola
    global vel_bola_x, vel_bola_y, vel_esq, vel_dir
    global pontos_esq, pontos_dir, texto

    janela = tk.Tk()
    janela.title("Pong Neon 80s")

    canvas = tk.Canvas(janela, width=800, height=600, bg="black")
    canvas.pack()

    # Linha central estilo retrô
    for i in range(0, 600, 20):
        canvas.create_line(400, i, 400, i+10, fill="purple")

    # Barras
    barra_esq = canvas.create_rectangle(30, 250, 40, 350, fill="cyan")
    barra_dir = canvas.create_rectangle(760, 250, 770, 350, fill="magenta")

    # Bola
    bola = canvas.create_oval(390, 290, 410, 310, fill="white")

    vel_bola_x = 5
    vel_bola_y = 5
    vel_esq = 0
    vel_dir = 0

    pontos_esq = 0
    pontos_dir = 0

    texto = canvas.create_text(400, 30, fill="cyan",
                               font=("Courier", 20, "bold"),
                               text="0 x 0")

    # CONTROLES
    def tecla_pressionada(e):
        global vel_esq, vel_dir
        if e.keysym == "w": vel_esq = -8
        if e.keysym == "s": vel_esq = 8
        if e.keysym == "Up": vel_dir = -8
        if e.keysym == "Down": vel_dir = 8

    def tecla_solta(e):
        global vel_esq, vel_dir
        if e.keysym in ("w", "s"): vel_esq = 0
        if e.keysym in ("Up", "Down"): vel_dir = 0

    janela.bind("<KeyPress>", tecla_pressionada)
    janela.bind("<KeyRelease>", tecla_solta)

    # LOOP
    def jogo():
        global vel_bola_x, vel_bola_y, pontos_esq, pontos_dir

        # Movimento
        canvas.move(barra_esq, 0, vel_esq)
        canvas.move(barra_dir, 0, vel_dir)
        canvas.move(bola, vel_bola_x, vel_bola_y)

        pos = canvas.coords(bola)

        # Colisão topo
        if pos[1] <= 0 or pos[3] >= 600:
            vel_bola_y *= -1

        # Colisão barras
        if canvas.coords(barra_esq)[0] < pos[0] < canvas.coords(barra_esq)[2] and \
           canvas.coords(barra_esq)[1] < pos[1] < canvas.coords(barra_esq)[3]:
            vel_bola_x *= -1.1

        if canvas.coords(barra_dir)[0] < pos[2] < canvas.coords(barra_dir)[2] and \
           canvas.coords(barra_dir)[1] < pos[3] < canvas.coords(barra_dir)[3]:
            vel_bola_x *= -1.1

        # 🟢 Gol direita (corrigido)
        if pos[2] >= 800:
            pontos_esq += 1
            enviar_pontos(pontos_esq, pontos_dir)
            canvas.coords(bola, 390, 290, 410, 310)

            vel_bola_x = random.choice([-5, 5])
            vel_bola_y = random.choice([-5, 5])

        # 🟢 Gol esquerda (corrigido)
        if pos[0] <= 0:
            pontos_dir += 1
            enviar_pontos(pontos_esq, pontos_dir)
            canvas.coords(bola, 390, 290, 410, 310)

            vel_bola_x = random.choice([-5, 5])
            vel_bola_y = random.choice([-5, 5])

        # Atualiza placar
        canvas.itemconfig(texto, text=f"{pontos_esq} x {pontos_dir}")

        janela.after(16, jogo)

    jogo()
    janela.mainloop()

login.mainloop()
