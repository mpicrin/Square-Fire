import time
import pygame
import random

pygame.init()

ANCHO = 480
ALTO = 640

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SQUARE FIRE")

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
GRIS = (100, 100, 100)
MORADO = (200, 0 ,255)
AMARILLO = (255, 255, 0)

fuente = pygame.font.SysFont(None, 32)
grande = pygame.font.SysFont(None, 64)

reloj = pygame.time.Clock()
FPS = 60

nave = pygame.Rect(ANCHO // 2 - 20, ALTO - 60, 40 ,40)
jefe = pygame.Rect(ANCHO // 2 - 20, 60, 80 ,50)
balas = []
retardo_disparo = 500
ultimo_disparo = 0
meteoritos = []
intervalo_meteorito = 1000
ultimo_meteorito = 0
max_meteoritos = 10000
meteoritos_generados = 0
puntos = 0
vidas = 3
meteorito_vel = 4
vel_nave = 7
n = random.randint(5 , 20)
n1 = random.randint(30 , 40)
n2 = random.randint(50, 60)
n3 = random.randint(90 , 100)
n4 = random.randint(140, 149)
tiempo_total = 30
duracion_poder = 5
contador_inicio = time.time()
modo_poder = False
inicio_poder = 0
activar_poder = False
auto_disparo = False
boss = False
vida_jefe = random.randint(50, 70)
vida_jefe_max = vida_jefe
vel_jefe = 4
balas_jefe = []
retardo_jefe = 1500 
ultimo_disparo_jefe = 0

def dibujar():
    global tiempo_restante, auto_disparo
    pantalla.fill(NEGRO)
    pygame.draw.rect(pantalla, BLANCO, nave)
    if puntos > 10:
        pygame.draw.rect(pantalla, ROJO, jefe)
        if not boss:
            boss = True
            dibujar_vida_jefe()

    for bala in balas:
        if bala.width > 10:
            color_bala = MORADO
        else:
            color_bala = AMARILLO if auto_disparo else ROJO
        pygame.draw.rect(pantalla, color_bala, bala)

    for m in meteoritos:
        pygame.draw.rect(pantalla, GRIS, m)
        
    color_jefe = ROJO if vida_jefe > vida_jefe_max // 2 else (150, 0, 0)
    pygame.draw.rect(pantalla, color_jefe, jefe)

    text_vidas = fuente.render(f"HP: {vidas}", True, BLANCO)
    if vidas == 2:
        text_vidas = fuente.render(f"HP: {vidas}", True, AMARILLO)
    if vidas == 1:
        text_vidas = fuente.render(f"HP: {vidas}", True, ROJO)
    texto_puntos = fuente.render(f"SCORE: {puntos}/150", True, BLANCO)
    pantalla.blit(text_vidas, (10, 10))
    pantalla.blit(texto_puntos, (10, 40))

    if tiempo_restante == 0 and not modo_poder:
        texto = fuente.render(f"PowerUP Ready", True, ROJO)
    else:
        texto = fuente.render(f"{tiempo_restante}", True, BLANCO)
    pantalla.blit(texto, (480 - texto.get_width() - 20, 20))
    pygame.display.flip()

def mostrar_game_over():
    pantalla.fill(NEGRO)
    mensaje = grande.render("GAME OVER", True, ROJO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 - 40))
    texto = fuente.render(f"              SCORE: {puntos}", True, BLANCO)
    pantalla.blit(texto, (ANCHO//2 - mensaje.get_width()//2, ALTO//2))
    pygame.display.flip()
    pygame.time.delay(3000)

def mostar_ganador():
    pantalla.fill(NEGRO)
    mensaje = grande.render("You Win!", True, BLANCO)
    pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2,ALTO//2 - 40))
    pygame.display.flip()
    pygame.time.delay(3000)

def dibujar_vida_jefe():
    ancho_max = 200
    alto_barra = 15
    x_barra = ANCHO // 2 - ancho_max // 2
    y_barra = 20

    porcentaje = max(0, vida_jefe) / vida_jefe_max
    ancho_actual = int(porcentaje * ancho_max)

    fondo = pygame.Rect(x_barra, y_barra, ancho_max, alto_barra)
    barra = pygame.Rect(x_barra, y_barra, ancho_actual, alto_barra)

    pygame.draw.rect(pantalla, (100, 0, 0), fondo)     
    if porcentaje > 0.5:
        color_barra = (0, 255, 0)    
    elif porcentaje > 0.2:
        color_barra = (255, 255, 0)  
    else:
        color_barra = (255, 0, 0)    
    pygame.draw.rect(pantalla, color_barra, barra) 
    borde = pygame.Rect(x_barra, y_barra, ancho_max, alto_barra)
    pygame.draw.rect(pantalla, BLANCO, borde, 2)   
    
def dano():
    mensaje = fuente.render("-1", True, ROJO)
    pantalla.blit(mensaje, (nave.x + 10, nave.y + 10))
    pygame.display.flip()
    pygame.time.delay(350)

def mostrar_instrucciones():
    fondo = pygame.image.load("SQUAREFIRE.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    esperando = True
    while esperando:
        pantalla.blit(fondo, (0, 0))
        texto = fuente.render("Press any key for continue", True, BLANCO)
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO - 80))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def powerup():
    global activar_poder, contador_inicio, modo_poder, inicio_poder, retardo_disparo, tiempo_total, auto_disparo
    tiempo_actual = time.time()
    tiempo_restante = tiempo_total - (tiempo_actual - contador_inicio)

    if not modo_poder and tiempo_restante <= 0 and activar_poder:
        modo_poder = True
        inicio_poder = time.time()
        retardo_disparo = 100
        activar_poder = False
        auto_disparo = True

    if modo_poder and (time.time() - inicio_poder) >= duracion_poder:
        modo_poder = False
        contador_inicio = time.time()
        retardo_disparo = 500
        auto_disparo = False

    return max(0, int(tiempo_restante))

def pedir_nombre():
    nombre = ""
    escribiendo = True
    input_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2, 200, 40)
    color_activo = (255, 255, 255)
    color_inactivo = (180, 180, 180)
    color_borde = color_inactivo

    while escribiendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif len(nombre) < 15 and evento.unicode.isprintable():
                    nombre += evento.unicode

        pantalla.fill((0, 0, 0))
        mensaje = grande.render("Your Name", True, BLANCO)
        pantalla.blit(mensaje, (ANCHO//2 - mensaje.get_width()//2, ALTO//2 - 60))

        pygame.draw.rect(pantalla, color_borde, input_rect, 2)
        texto_nombre = fuente.render(nombre, True, color_activo)
        pantalla.blit(texto_nombre, (input_rect.x + 10, input_rect.y + 5))

        pygame.display.flip()
        reloj.tick(30)

    return nombre

def guardar_resultado(nombre, resultado, inicio, puntos, vidas):
    fin = time.time()
    duracion = int(fin - inicio)
    minutos = duracion // 60
    segundos = duracion % 60
    registro = f"Player: {nombre} | Result: {resultado} | HP: {vidas} | Score: {puntos} | Time: {minutos:02}:{segundos:02}\n"

    with open("Ranking.txt", "a") as f:
        f.write(registro)

mostrar_instrucciones()
inicio_juego = time.time()
exe = True
while exe:
    reloj.tick(FPS)
    ahora = pygame.time.get_ticks()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            exe = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_x and tiempo_restante <= 0:
                activar_poder = True
            if evento.key == pygame.K_c and tiempo_restante <= 0:
                bala = pygame.Rect(nave.centerx - 25, nave.y - 25, 50,50)
                balas.append(bala)
                modo_poder = True

    tc = pygame.key.get_pressed()
    tiempo_restante = powerup()

    if tc[pygame.K_a] and nave.left > 0:
        nave.x -= vel_nave
    if tc[pygame.K_d] and nave.right < ANCHO:
        nave.x += vel_nave
    if tc[pygame.K_SPACE] and ahora -ultimo_disparo >= retardo_disparo:
        bala = pygame.Rect(nave.centerx - 2, nave.y - 10, 4, 10)
        balas.append(bala)
        ultimo_disparo = ahora
    if auto_disparo and ahora -ultimo_disparo >= retardo_disparo:
        bala = pygame.Rect(nave.centerx - 2, nave.y - 10, 4, 10)
        balas.append(bala)
        ultimo_disparo = ahora
    if meteoritos_generados < max_meteoritos and ahora - ultimo_meteorito >= intervalo_meteorito and boss == False:
        x = random.randint(0, ANCHO - 30)
        m = pygame.Rect(x, -30, 30, 30)
        meteoritos.append(m)
        meteoritos_generados += 1
        ultimo_meteorito = ahora

    if vida_jefe <= vida_jefe_max // 2:
        retardo_jefe = 700
    else:
        retardo_jefe = 1500
        
    if boss:
        meteoritos_generados = 10000 

        if vida_jefe <= vida_jefe_max // 2:
            vel_jefe = 7 
        else:
            vel_jefe = 4 
    
        jefe.x += vel_jefe
        if jefe.right >= ANCHO or jefe.left <= 0:
            vel_jefe *= -1 
            
        for bala_j in balas_jefe[:]:
            bala_j["rect"].x += bala_j["vx"]
            bala_j["rect"].y += bala_j["vy"]
            pygame.draw.rect(pantalla, MORADO, bala_j["rect"])
            if bala_j["rect"].colliderect(nave):
                dano()
                vidas -= 1
                balas_jefe.remove(bala_j)
            elif bala_j["rect"].top > ALTO or bala_j["rect"].left < 0 or bala_j["rect"].right > ANCHO:
                balas_jefe.remove(bala_j)
        
        if ahora - ultimo_disparo_jefe >= retardo_jefe:
            dx = nave.centerx - jefe.centerx
            dy = nave.centery - jefe.bottom
            distancia = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            vel_x = dx / distancia * 5
            vel_y = dy / distancia * 5
            bala_j = {"rect": pygame.Rect(jefe.centerx - 4, jefe.bottom, 8, 8), "vx": vel_x, "vy": vel_y}
            balas_jefe.append(bala_j)
            ultimo_disparo_jefe = ahora
    
        for bala in balas[:]:
            bala.y -= 8 if bala.width <= 10 else 4
            if bala.bottom < 0:
                balas.remove(bala)
            elif jefe.colliderect(bala):
                vida_jefe -= 1
                balas.remove(bala)
        

    else:
        for bala in balas[:]:
            if bala.width > 10:
                bala.y -= 4
            else:
                bala.y -= 8
            if bala.bottom <0:
                balas.remove(bala)

        if puntos == 10:
            meteorito_vel = 8
            intervalo_meteorito = 500
        elif puntos == 40:
            meteorito_vel = 10
            intervalo_meteorito = 250
        elif puntos == 100:
            meteorito_vel = 12
            intervalo_meteorito = 100

        if puntos == n or puntos == n1 or puntos == n2 or puntos == n3 or puntos == n4:
            vel_nave = 0
        else:
            vel_nave = 7

        for m in meteoritos[:]:
            m.y += meteorito_vel

            if m.colliderect(nave):
                meteoritos.remove(m)
                dano()
                vidas -= 1
            elif m.top > ALTO:
                meteoritos.remove(m)
            else:
                for bala in balas[:]:
                    if m.colliderect(bala):
                        if bala.width > 10:
                            if m in meteoritos:
                                meteoritos.remove(m)
                            puntos +=1
                        else:
                            if m in meteoritos:
                                meteoritos.remove(m)
                            if bala in balas:
                                balas.remove(bala)
                            puntos += 1
                        break

    dibujar()
    if vidas <= 0:
        mostrar_game_over()
        nombre = pedir_nombre()
        guardar_resultado(nombre,"Loss", inicio_juego, puntos, vidas)
        exe = False
    elif puntos >= 150:
        mostar_ganador()
        nombre = pedir_nombre()
        guardar_resultado(nombre,"Win", inicio_juego, puntos, vidas)
        exe = False
    pygame.display.flip()
pygame.quit() 
