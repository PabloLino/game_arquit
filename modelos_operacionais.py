import turtle
import random
import time
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

screen = turtle.Screen()
screen.title("Modelos Operacionais - Colete os Prós e Evite os Contras")
screen.bgcolor("lightblue")
screen.setup(width=800, height=600)
screen.tracer(0)

gif_path = resource_path("empresa_icon.gif")
screen.register_shape(gif_path)

empresa = turtle.Turtle()
empresa.shape(gif_path)
empresa.penup()
empresa.goto(0, 0)

empresa.direction = "stop"

pros_list = [
    "Alta Padronização", "Alta Integração", "Cooperação", "Centralização",
    "Sinergia entre Unidades", "Otimização de Processos", "Eficiência Operacional", "Inovação"
]

contras_list = [
    "Baixa Padronização", "Falta de Sinergia", "Processos Desconectados", "Fragmentação",
    "Burocracia", "Alto Custo de Implementação", "Falhas de Comunicação", "Desalinhamento Estratégico"
]

def gerar_coordenadas_validas(existing_positions, min_dist=50):
    while True:
        x = random.randint(-390, 390)
        y = random.randint(-290, 290)
        if all(((x - ex_x) ** 2 + (y - ex_y) ** 2) ** 0.5 > min_dist for ex_x, ex_y in existing_positions):
            return x, y

pro_label = turtle.Turtle()
pro_label.speed(0)
pro_label.color("green")
pro_label.penup()
pro_label.hideturtle()
pro_text = random.choice(pros_list)
pro_label.goto(gerar_coordenadas_validas([]))
pro_label.write(pro_text, align="center", font=("Courier", 16, "bold"))

contra_labels = []
contra_positions = []

for _ in range(5):
    contra_label = turtle.Turtle()
    contra_label.speed(0)
    contra_label.color("red")
    contra_label.penup()
    contra_label.hideturtle()
    contra_text = random.choice(contras_list)
    contra_position = gerar_coordenadas_validas([pro_label.pos()])
    contra_label.goto(contra_position)
    contra_label.write(contra_text, align="center", font=("Courier", 16, "bold"))
    contra_labels.append(contra_label)
    contra_positions.append(contra_position)

score = 0
high_score = 0

def draw_score():
    score_label.clear()
    score_label.goto(0, 240)
    score_label.write(f"Score: {score}  High Score: {high_score}", align="center", font=("Arial", 24, "bold"))

score_label = turtle.Turtle()
score_label.speed(0)
score_label.color("black")
score_label.penup()
score_label.hideturtle()

draw_score()

def move_up():
    if empresa.direction != "down":
        empresa.direction = "up"

def move_down():
    if empresa.direction != "up":
        empresa.direction = "down"

def move_left():
    if empresa.direction != "right":
        empresa.direction = "left"

def move_right():
    if empresa.direction != "left":
        empresa.direction = "right"

def move():
    if empresa.direction == "up":
        y = empresa.ycor()
        empresa.sety(y + 10)

    if empresa.direction == "down":
        y = empresa.ycor()
        empresa.sety(y - 10)

    if empresa.direction == "left":
        x = empresa.xcor()
        empresa.setx(x - 10)

    if empresa.direction == "right":
        x = empresa.xcor()
        empresa.setx(x + 10)

screen.listen()
screen.onkey(move_up, "w")
screen.onkey(move_down, "s")
screen.onkey(move_left, "a")
screen.onkey(move_right, "d")
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

def game_loop():
    global score, high_score, pro_text

    move()

    width = screen.window_width() // 2
    height = screen.window_height() // 2

    if empresa.distance(pro_label) < 20:
        score += 1
        if score > high_score:
            high_score = score

        pro_label.clear()
        pro_text = random.choice(pros_list)
        pro_label.goto(gerar_coordenadas_validas(contra_positions))
        pro_label.write(pro_text, align="center", font=("Courier", 16, "bold"))

        for i, contra_label in enumerate(contra_labels):
            contra_label.clear()
            contra_text = random.choice(contras_list)
            contra_position = gerar_coordenadas_validas([pro_label.pos()] + contra_positions[:i])
            contra_label.goto(contra_position)
            contra_label.write(contra_text, align="center", font=("Courier", 16, "bold"))
            contra_positions[i] = contra_position

        draw_score()

    for contra_label in contra_labels:
        if empresa.distance(contra_label) < 20:
            empresa.goto(0, 0)
            empresa.direction = "stop"
            score = 0

            draw_score()
            break

    if abs(empresa.xcor()) > width or abs(empresa.ycor()) > height:
        empresa.goto(0, 0)
        empresa.direction = "stop"
        score = 0

        draw_score()

    screen.update()
    time.sleep(0.05)
    screen.ontimer(game_loop, 50)

game_loop()
screen.mainloop()
