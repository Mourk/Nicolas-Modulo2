import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD

DUCK_IMG = { DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
JUMP_IMG = { DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
RUN_IMG = { DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}
X_POS = 80
Y_POS = 310
Y_POS_DUCK = 340
JUMP_VEL = 8.5

class Dinosaur(Sprite):
    def __init__ (self):
       self.type = DEFAULT_TYPE
       self.image = RUN_IMG[self.type][0]
       self.dino_rect = self.image.get_rect()
       self.dino_rect.x = X_POS
       self.dino_rect.y = Y_POS
       self.step_index = 0
       self.dino_run = True
       self.dino_jump = False
       self.dino_duck = False
       self.jump_vel = JUMP_VEL
       self.fast_run = False #não aumentará a velocidade
       self.run_speed = 1 # a velocidade vai ser 1, padrão
       self.fast_run_speed = 2 #se apertar a tecla SPACE vai correr mais rápido
       self.revived = False
       self.blink_count = 0 #Define que o número de piscadas é igual a 0
       self.setup_state()

    def revive(self):
        self.revived = True
        self.blink_count = 0

    def setup_state(self):
        self.has_power_up = False
        self.shield = False
        self.show_text = False
        self.shield_time_up = 0

    def update(self, user_input):
        if self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = True
            self.dino_duck = False

        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_jump = False
            self.dino_duck = True

        elif not self.dino_jump and not self.dino_duck:
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
        if self.step_index >= 9:
            self.step_index = 0

        if user_input[pygame.K_SPACE]: #APÓS APERTAR A TECLA SPACE, O DINOSSAURO CORRERÁ MAIS RÁPIDO
            self.fast_run = True
            self.run_speed = self.fast_run_speed
        else:
            self.fast_run = False
            self.run_speed = 1

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += self.run_speed ### controla qual imagem da animação de corrida é exibida. 
                                    #######Ele aumenta com base na self.run_speed, ou seja, quando o dinossauro está correndo ele passará correndo pelos obstáculos
    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -JUMP_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_vel = JUMP_VEL

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS_DUCK
        self.step_index += 1
        self.dino_duck = False

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        if not (self.revived and self.blink_count % 2 == 0): #verificar se o número de vezes que piscar é igual a par.
            screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        
        if self.revived: #se o número de vezes que piscar for maior que 10, o dinossauro para de piscar e renasce.
            self.blink_count += 1
            if self.blink_count > 10:
                self.revived = False