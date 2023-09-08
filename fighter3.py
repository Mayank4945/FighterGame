import pygame
import random

class Fighter():
    def __init__(user,player,x,y, flip, data, animation_sheet, animation_steps):
        user.player = player
        user.size = data[0]
        user.image_scale = data[1]
        user.offset=data[2]
        user.flip = flip
        user.animation_list = user.load_images(animation_sheet, animation_steps)
        user.animation_list23 = user.load_images23(animation_sheet, animation_steps)
        user.action = 0#0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        user.frame_index=0
        user.image = user.animation_list[user.action][user.frame_index]
        user.update_time = pygame.time.get_ticks()
        user.rect = pygame.Rect((x, y, 80, 100))
        user.vel_y = 0
        user.running=False
        user.jump = False
        user.attacking = False
        user.attack_type = 0
        user.attack_cooldown = 0
        user.hit = False
        user.health = 100
        user.alive = True
    
    def load_images(user, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for i in range(animation):
                temp_img = sprite_sheet.subsurface(i * user.size,y * user.size, user.size, user.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (user.size * user.image_scale,user.size*user.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def load_images23(user, sprite_sheet, animation_steps):
        #extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for i in range(animation):
                temp_img = sprite_sheet.subsurface(i * 160,y * user.size, user.size, user.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (user.size * user.image_scale,user.size*user.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list



    def move(user,WIDTH,HEIGHT,surface,target,round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        user.running = False     
        user.attack_type = 0   

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if user.attacking == False and user.alive == True and round_over == False:
            #check player 1 controls
            if user.player ==1:
            #movement 
                if key[pygame.K_a]:
                    dx = -SPEED
                    user.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    user.running = True
                #jump
                if key[pygame.K_SPACE] and user.jump == False:
                    user.vel_y = -25
                    user.jump = True
                #attack
                if key[pygame.K_KP_ENTER] or key[pygame.K_RETURN]:
                    user.attack(target)
                    #determine which attack is used
                    if key[pygame.K_KP_ENTER]:
                        user.attack_type = 2
                    if key[pygame.K_RETURN]:
                        user.attack_type = 1

        ai=random.randint(1,75)
        #check player 2 controls
        if user.player ==2 and user.alive==True:
        #movement 
            if ai == 1:
                dx = -(SPEED*8)
                user.running = True
            if ai == 2:
                dx = SPEED*5
                user.running = True
            #jump
            if ai == 3 and user.jump == False:
                user.vel_y = -25
                user.jump = True
            #attack
            if ai == 4 or ai == 5:
                user.attack(target)
                #determine which attack is used
                if ai == 4:
                    user.attack_type = 2
                if ai == 5:
                    user.attack_type = 1
            else:
                pass
        
        #apply gravity
        user.vel_y += GRAVITY
        dy += user.vel_y
        
        dy += user.vel_y
 
        #ensure player stays on screen
        if user.rect.left + dx <0:
            dx = - user.rect.left
        if user.rect.right + dx > WIDTH:
            dx=WIDTH - user.rect.right
        if user.rect.bottom + dy > HEIGHT - 110:
            user.vel_y = 0
            user.jump = False
            dy = HEIGHT - 110 - user.rect.bottom
        
        #ensure players face each other
        if target.rect.centerx > user.rect.centerx:
            user.flip = False
        else:
            user.flip = True

        #apply attack collision
        if user.attack_cooldown >0:
            user.attack_cooldown -= 1

        #update player position
        user.rect.x += dx
        user.rect.y += dy
    
    #handle animation updates
    def update(user):
        #check what action the player is performing
        if user.health <= 0:
            user.health = 0
            user.alive = False
            user.update_action(6)#6:death
        elif user.hit == True:
            user.update_action(5) #5 hit
        elif user.attacking == True:
            if user.attack_type ==1:
                user.update_action(3)  #3 : attack1
            elif user.attack_type==2:
                user.update_action(4)  #4 : attack2
        elif user.jump == True:
            user.update_action(2)  #2 : jump
        elif user.running ==True:
            user.update_action(1)  #1 : run
        else: 
            user.update_action(0)  #0 : idle

        animation_cooldown = 40
        #update image
        user.image = user.animation_list[user.action][user.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - user.update_time > animation_cooldown:
            user.frame_index+=1
            user.update_time=pygame.time.get_ticks()
        #check if the animation is finished
        if user.frame_index>=len(user.animation_list[user.action]):
            #if the player is dead then end the animation
            if user.alive == False:
                user.frame_index = len(user.animation_list[user.action]) - 1
            else:
                user.frame_index=0
                #check if an attack was executed
                if user.action == 3 or user.action == 4:
                    user.attacking = False
                    user.attack_cooldown = 20
                #check if damage was taken
                if user.action == 5:
                    user.hit = False
                    #if the player was in the middle of an attack, then the attack is stopped
                    user.attacking=False
                    user.attack_cooldown = 20

    #handle animation updates
    def update23(user):
        #check what action the player is performing
        if user.health <= 0:
            user.health = 0
            user.alive = False
            user.update_action(6)#6:death
        elif user.hit == True:
            user.update_action(5) #5 hit
        elif user.attacking == True:
            if user.attack_type ==1:
                user.update_action(3)  #3 : attack1
            elif user.attack_type==2:
                user.update_action(4)  #4 : attack2
        elif user.jump == True:
            user.update_action(2)  #2 : jump
        elif user.running ==True:
            user.update_action(1)  #1 : run
        else: 
            user.update_action(0)  #0 : idle

        animation_cooldown = 40
        #update image
        user.image = user.animation_list23[user.action][user.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - user.update_time > animation_cooldown:
            user.frame_index+=1
            user.update_time=pygame.time.get_ticks()
        #check if the animation is finished
        if user.frame_index>=len(user.animation_list23[user.action]):
            #if the player is dead then end the animation
            if user.alive == False:
                user.frame_index = len(user.animation_list23[user.action]) - 1
            else:
                user.frame_index=0
                #check if an attack was executed
                if user.action == 3 or user.action == 4:
                    user.attacking = False
                    user.attack_cooldown = 20
                #check if damage was taken
                if user.action == 5:
                    user.hit = False
                    #if the player was in the middle of an attack, then the attack is stopped
                    user.attacking=False
                    user.attack_cooldown = 20



    def attack(user,target):
        if user.attack_cooldown == 0:
            user.attacking = True
            attacking_rect = pygame.Rect(user.rect.centerx - (2 * user.rect.width * user.flip), user.rect.y, 2* user.rect.width, user.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def update_action(user,new_action):
        #check if the new action is different to the previous one 
        if new_action != user.action:
            user.action = new_action
            #update the animation settings
            user.frame_index = 0
            user.update_time = pygame.time.get_ticks()


    def draw(user,surface):
        img=pygame.transform.flip(user.image,user.flip,False)
        surface.blit(img,(user.rect.x-(user.offset[0]*user.image_scale),user.rect.y-(user.offset[1]*user.image_scale)))