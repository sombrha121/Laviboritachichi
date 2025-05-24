import turtle
import time
import random
from abc import ABC, abstractmethod

# ----- Configuración inicial -----
WIDTH, HEIGHT = 600, 600
DELAY = 0.1

# ----- Interfaz y Fábricas de Comida -----
# ------------------------------
# Sección que implementa los 4 tipos de comida con efectos distintos,
# utilizando clases que heredan de una interfaz abstracta (Comida).
# Cada clase tiene color y efecto único sobre la serpiente.
# ------------------------------

class Comida(ABC):
    def __init__(self, color):
        self.t = turtle.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.goto(random.randint(-280, 280), random.randint(-280, 280))

    @abstractmethod
    def efecto(self, snake):
        pass

# 🟢 Comida Fit: +1 punto y crecer
class ComidaFit(Comida):
    def __init__(self):
        super().__init__("green")

    def efecto(self, snake):
        snake.crecer()
        snake.puntaje += 1

# 🟣 Comida Venenosa: -1 punto y reducir tamañ
class ComidaVenenosa(Comida): 
    def __init__(self):
        super().__init__("purple")

    def efecto(self, snake):
        snake.reducir()
        snake.puntaje = max(0, snake.puntaje - 1)

# 🟡 Comida Alta en Grasas: +3 puntos y más lent
class ComidaGrasa(Comida): 
    def __init__(self):
        super().__init__("yellow")

    def efecto(self, snake):
        snake.crecer()
        snake.puntaje += 3
        snake.retraso += 0.05

 # 🟠 Comida para Reyes: +5 puntos y más rápida
class ComidaRey(Comida):
    def __init__(self):
        super().__init__("orange")

    def efecto(self, snake):
        snake.crecer()
        snake.puntaje += 5
        snake.retraso = max(0.05, snake.retraso - 0.03)
# ------------------------------
# Aplicación del Patrón Abstract Factory.
# Se define la interfaz FabricaComida y luego 4 implementaciones
# que retornan una instancia de su tipo específico de comida.
# ------------------------------

class FabricaComida(ABC):
    @abstractmethod
    def crear_comida(self):
        pass

class FabricaFit(FabricaComida):
    def crear_comida(self):
        return ComidaFit()

class FabricaVenenosa(FabricaComida):
    def crear_comida(self):
        return ComidaVenenosa()

class FabricaGrasa(FabricaComida):
    def crear_comida(self):
        return ComidaGrasa()

class FabricaRey(FabricaComida):
    def crear_comida(self):
        return ComidaRey()

# ----- Clase Snake -----
class Snake:
    def __init__(self):
        self.segments = []
        self.direccion = "stop"
        self.retraso = DELAY
        self.puntaje = 0
        self.crear_cabeza()

    def crear_cabeza(self):
        cabeza = turtle.Turtle()
        cabeza.shape("square")
        cabeza.color("black")
        cabeza.penup()
        cabeza.goto(0, 0)
        self.segments.append(cabeza)

    def mover(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        cabeza = self.segments[0]
        if self.direccion == "up":
            cabeza.sety(cabeza.ycor() + 20)
        if self.direccion == "down":
            cabeza.sety(cabeza.ycor() - 20)
        if self.direccion == "left":
            cabeza.setx(cabeza.xcor() - 20)
        if self.direccion == "right":
            cabeza.setx(cabeza.xcor() + 20)

    def crecer(self):
        nuevo = turtle.Turtle()
        nuevo.shape("square")
        nuevo.color("gray")
        nuevo.penup()
        self.segments.append(nuevo)

    def reducir(self):
        if len(self.segments) > 1:
            self.segments[-1].hideturtle()
            self.segments.pop()

    def colision_borde(self):
        cabeza = self.segments[0]
        return not (-290 < cabeza.xcor() < 290 and -290 < cabeza.ycor() < 290)

    def colision_cuerpo(self):
        cabeza = self.segments[0]
        return any(seg.distance(cabeza) < 10 for seg in self.segments[1:])

    def reset(self):
        for seg in self.segments:
            seg.hideturtle()
        self.segments.clear()
        self.puntaje = 0
        self.retraso = DELAY
        self.direccion = "stop"
        self.crear_cabeza()

# ----- Controlador del juego -----
class JuegoSnake:
    def __init__(self):
        self.ventana = turtle.Screen()
        self.ventana.title("Snake con Abstract Factory")
        self.ventana.bgcolor("pink")
        self.ventana.setup(width=WIDTH, height=HEIGHT)
        self.ventana.tracer(0)

        self.snake = Snake()
        self.label = turtle.Turtle()
        self.label.hideturtle()
        self.label.color("black")
        self.label.penup()
        self.label.goto(0, 260)
        self.label.write("Puntaje: 0", align="center", font=("Courier", 18, "normal"))

        self.comida = self.generar_comida()

        self.ventana.listen()
        self.ventana.onkey(lambda: self.cambiar_direccion("up"), "Up")
        self.ventana.onkey(lambda: self.cambiar_direccion("down"), "Down")
        self.ventana.onkey(lambda: self.cambiar_direccion("left"), "Left")
        self.ventana.onkey(lambda: self.cambiar_direccion("right"), "Right")

        # Soporte para teclas WASD
        self.ventana.onkey(lambda: self.cambiar_direccion("up"), "w")
        self.ventana.onkey(lambda: self.cambiar_direccion("down"), "s")
        self.ventana.onkey(lambda: self.cambiar_direccion("left"), "a")
        self.ventana.onkey(lambda: self.cambiar_direccion("right"), "d")


    def cambiar_direccion(self, direccion):
        if (direccion == "up" and self.snake.direccion != "down") or \
           (direccion == "down" and self.snake.direccion != "up") or \
           (direccion == "left" and self.snake.direccion != "right") or \
           (direccion == "right" and self.snake.direccion != "left"):
            self.snake.direccion = direccion

    def generar_comida(self):
          # ------------------------------
        # Aquí se aplica el patrón Abstract Factory en tiempo de ejecución.
        # Se elige aleatoriamente una fábrica concreta y se genera una comida.
        # ------------------------------
        fabrica = random.choice([
            FabricaFit(),
            FabricaVenenosa(),
            FabricaGrasa(),
            FabricaRey()
        ])
        return fabrica.crear_comida()

    def actualizar_puntaje(self):
        self.label.clear()
        self.label.write(f"Puntaje: {self.snake.puntaje}", align="center", font=("Courier", 18, "normal"))

    def ejecutar(self):
        while True:
            self.ventana.update()

            if self.snake.direccion != "stop":
                self.snake.mover()

                # Colisión con comida
                if self.snake.segments[0].distance(self.comida.t) < 20:
                      # ------------------------------
                    # La serpiente colisiona con la comida:
                    # - Se oculta la comida,
                    # - Se aplica su efecto con el método abstracto `efecto`,
                    # - Se actualiza el puntaje y se genera una nueva comida.
                    # ------------------------------
                    self.comida.t.hideturtle()
                    self.comida.efecto(self.snake)
                    self.actualizar_puntaje()
                    self.comida = self.generar_comida()

                # Colisión con borde
                # Colisión con borde o cuerpo
                if self.snake.colision_borde() or self.snake.colision_cuerpo():
                    self.label.clear()
                    self.label.write("¡Perdiste! Reiniciando...", align="center", font=("Courier", 18, "bold"))
                    self.ventana.update()  # <<--- Esto fuerza a mostrar el mensaje
                    time.sleep(2)

                    self.label.clear()
                    self.snake.reset()
                    self.comida.t.hideturtle()
                    self.comida = self.generar_comida()
                    self.actualizar_puntaje()

            time.sleep(self.snake.retraso)

# ----- Ejecutar juego -----
if __name__ == "__main__":
    juego = JuegoSnake()
    juego.ejecutar()
