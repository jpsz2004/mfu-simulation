import pygame
import sys
import random

pygame.init()

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MFU - Zelda Style")

# Fuente y colores
FONT = pygame.font.SysFont("PixelOperator", 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
GREEN = (30, 180, 60)

# Ruta de las imágenes
IMAGENES = {
    "Espada": "espada.png",
    "Escudo": "escudo.png",
    "Bomba": "bomba.png",
    "Arco": "arco.png",
    "Poción": "pocion.png"
}

# Redimensionar las imágenes a un tamaño adecuado
TAMANO_IMAGEN = (40, 40)  # Tamaño que le daremos a las imágenes

posiciones_animadas = {}
velocidad_animacion = 10  # Cuanto mayor, más rápida la animación


# Función para cargar las imágenes
def cargar_imagenes():
    cargadas = {}
    for item, path in IMAGENES.items():
        try:
            print(f"Cargando imagen: {path}")  # Depuración
            img = pygame.image.load(path)
            print(f"Tamaño original de {item}: {img.get_size()}")  # Verifica el tamaño original
            img = pygame.transform.scale(img, TAMANO_IMAGEN)
            print(f"Tamaño redimensionado de {item}: {img.get_size()}")  # Verifica el tamaño después de redimensionar
            cargadas[item] = img
            print(f"Imagen cargada: {item}")  # Depuración
        except pygame.error as e:
            print(f"Error al cargar la imagen {path}: {e}")
    return cargadas

# Cargar imágenes
IMAGENES_CARGADAS = cargar_imagenes()

# Clase de Inventario MFU
class InventarioMFU:
    def __init__(self, capacidad):
        self.capacidad = capacidad
        self.inventario = {}
        self.eliminado = None


    def usar(self, item, jugador_pos):
        if item == "Espada":
            print(f"Usando {item}. ¡Atacando a los enemigos!")
            self.inventario[item] += 1
            return "espada"
        elif item == "Bomba":
            print(f"Usando {item}. ¡Explosión!")
            self.inventario[item] += 1
            return "bomba"
        elif item == "Arco":
            print(f"Usando {item}. ¡Disparando una flecha!")
            self.inventario[item] += 1
            return "arco"
        elif item == "Escudo":
            print(f"Usando {item}. ¡Defendiéndose de un ataque!")
            self.inventario[item] += 1
            return "escudo"
        elif item == "Poción":
            print(f"Usando {item}. ¡Curando al personaje!")
            self.inventario[item] += 1
            return "pocion"
        else:
            return None


    def recoger(self, item):
        if item in self.inventario:
            print(f"{item} ya está en inventario.")
            return
        self.eliminado = None
        if len(self.inventario) >= self.capacidad:
            mfu = max(self.inventario, key=self.inventario.get)
            print(f"Inventario lleno. Eliminando '{mfu}' (MFU).")
            del self.inventario[mfu]
            self.eliminado = mfu
                
        self.inventario[item] = 0
        print(f"Recogiste {item}.")

def dibujar_inventario(inv):
    pygame.draw.rect(SCREEN, GRAY, (10, HEIGHT - 100, WIDTH - 20, 90))

    estado = "Lleno" if len(inv.inventario) >= inv.capacidad else "Disponible"
    estado_color = (255, 0, 0) if estado == "Lleno" else (0, 200, 0)
    SCREEN.blit(FONT.render(f"Inventario MFU - Estado: {estado}", True, estado_color), (20, HEIGHT - 90))

    items_ordenados = sorted(inv.inventario.items(), key=lambda x: -x[1])

    # Actualiza las posiciones destino
    for i, (item, usos) in enumerate(items_ordenados):
        destino_x = 40 + i * 150
        destino_y = HEIGHT - 60

        if item not in posiciones_animadas:
            posiciones_animadas[item] = [destino_x, destino_y]  # Inicialmente donde va

        actual_x, actual_y = posiciones_animadas[item]

        # Interpolación simple hacia destino
        dx = destino_x - actual_x
        dy = destino_y - actual_y
        if abs(dx) > 1:
            actual_x += dx // velocidad_animacion
        if abs(dy) > 1:
            actual_y += dy // velocidad_animacion

        posiciones_animadas[item] = [actual_x, actual_y]

        color = (255, 100, 100) if item == inv.eliminado else GRAY
        pygame.draw.rect(SCREEN, color, (actual_x, actual_y, 120, 50), border_radius=10)

        if item in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS[item], (actual_x + 5, actual_y + 5))
        SCREEN.blit(FONT.render(f"{item}", True, BLACK), (actual_x + 50, actual_y + 5))
        SCREEN.blit(FONT.render(f"Usos: {usos}", True, BLACK), (actual_x + 50, actual_y + 25))

    for item in list(posiciones_animadas.keys()):
        if item not in inv.inventario:
            posiciones_animadas.pop(item)
    
    return [item for item, usos in items_ordenados]



# Dibuja el mundo y los ítems
# Dibuja el mundo y los ítems
def dibujar_mundo(jugador_pos, accion_actual):
    SCREEN.fill(GREEN)
    pygame.draw.circle(SCREEN, (255, 220, 100), jugador_pos, 20)  # Héroe
    
    if accion_actual == "espada":
        if "Espada" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Espada"], (jugador_pos[0] + 30, jugador_pos[1] - 20))
    elif accion_actual == "bomba":
        if "Bomba" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Bomba"], (jugador_pos[0] + 40, jugador_pos[1] - 10))
    elif accion_actual == "arco":
        if "Arco" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Arco"], (jugador_pos[0] + 30, jugador_pos[1] - 20))
    elif accion_actual == "escudo":
        if "Escudo" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Escudo"], (jugador_pos[0] - 40, jugador_pos[1] - 20))
    elif accion_actual == "pocion":
        if "Poción" in IMAGENES_CARGADAS:
            SCREEN.blit(IMAGENES_CARGADAS["Poción"], (jugador_pos[0] - 40, jugador_pos[1] - 20))
    
    texto = FONT.render("Muévete con flechas o WASD | 1-5 para recoger | Click para usar", True, WHITE)
    SCREEN.blit(texto, (20, 20))


# Loop principal
def main():
    clock = pygame.time.Clock()
    inventario = InventarioMFU(3)
    jugador_x, jugador_y = WIDTH // 2, HEIGHT // 2
    velocidad = 5
    accion_actual = None
    eliminado_timer = 0  
    


    while True:
        clock.tick(30)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            jugador_x -= velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            jugador_x += velocidad
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            jugador_y -= velocidad
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            jugador_y += velocidad

        jugador_x = max(20, min(WIDTH - 20, jugador_x))
        jugador_y = max(20, min(HEIGHT - 120, jugador_y))  # Deja espacio para inventario

        dibujar_mundo((jugador_x, jugador_y), accion_actual)
        dibujar_inventario(inventario)
        orden_actual = dibujar_inventario(inventario)
        pygame.display.flip()

        # dentro del loop principal, después de flip()
        if inventario.eliminado:
            eliminado_timer += 1
            if eliminado_timer > 30:  # 1 segundo a 30 FPS
                inventario.eliminado = None
                eliminado_timer = 0


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    index = event.key - pygame.K_1
                    ITEMS = ["Espada", "Escudo", "Bomba", "Arco", "Poción"]
                    inventario.recoger(ITEMS[index])
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, item in enumerate(orden_actual):
                    x = 40 + i * 150
                    y = HEIGHT - 60
                    if x <= mx <= x + 120 and y <= my <= y + 50:
                        accion_actual = inventario.usar(item, (jugador_x, jugador_y))
        
if __name__ == "__main__":
    main()