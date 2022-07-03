import random
import arcade



UPDATES_PER_FRAME = 5

WIDTH = 1000
HEIGHT = 780
TITLE = 'GAME'
SCALE = .5


class Rocket(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.cur_texture = 0
        self.points = [[-22, -90], [22, -90], [20, 28], [-22, 28]]
        self.set_hit_box(self.points)
        
        self.idle_texture = arcade.load_texture('images/spaceship.png')
        

        self.rocket_textures = []

        for i in range(4):

            texture = arcade.load_texture(f'images/spaceship_{i+1}.png')

            self.rocket_textures.append(texture)
    
    def update_animation(self, delta_time : float):

        # if self.change_y == -1 or self.change_y == 0:
        #     self.texture = self.idle_texture
        #     return

        self.cur_texture += 1

        if self.cur_texture > 3 * UPDATES_PER_FRAME:

            self.cur_texture = 0

        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.rocket_textures[frame]



class MyGame(arcade.Window):
    

    def __init__(self, width, height, title, resizable):

        super().__init__(width, height, title, resizable)

        self.player_list = None

        self.score = 0

    def setup(self):

        

        self.player_list = arcade.SpriteList()
        self.star_list = arcade.SpriteList()
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Rocket()

        self.player.center_x = WIDTH / 2
        self.player.center_y =  HEIGHT / 2
        self.player.change_y = 0
        self.player.scale = 1
        print(self.player.position)

        self.player_list.append(self.player)

        self.rocket_sound = arcade.load_sound('sounds/rocket.wav')
        self.sound = arcade.sound.play_sound(self.rocket_sound, looping=True, volume=.2)


        self.background_music = arcade.load_sound('sounds/background.wav')
        arcade.sound.play_sound(self.background_music, looping=True)

        arcade.schedule(self.add_star, .5)
        arcade.schedule(self.add_asteroid, 2)
        

        
        arcade.set_background_color(arcade.color.BLACK)

    def add_asteroid(self, delta_time:float):

        asteroid = arcade.Sprite('./images/asteroid.png', scale=.3)
        asteroid.top = HEIGHT + 80
        asteroid.center_x = random.randint(0, self.width)
        vel = random.randint(1,3)

        if vel == 1:
            asteroid.velocity = (0, -.3)
            asteroid.change_angle = -1
        elif vel == 2:
            asteroid.velocity = (0, -.4)
            asteroid.change_angle = 1
        elif vel == 3:
            asteroid.velocity = (0, -.5)
            asteroid.change_angle = .5

        self.asteroid_list.append(asteroid)

    def add_star(self, delta_time:float):

        star = arcade.Sprite('images/star.png')
        star.top =  self.height + 10
        star.center_x = random.randint(0, self.width)
        vel = random.randint(1,3)
        if vel == 1:            
            star.velocity = (0, -.3)
        elif vel == 2:
            star.velocity = (0,-.4)
        elif vel == 3:
            star.velocity = (0,-.5)

        self.star_list.append(star)

        star1 = arcade.Sprite('images/star.png')
        star1.top =  self.height + 10
        star1.center_x = random.randint(0, self.width)
        vel = random.randint(1,3)
        if vel == 1:            
            star1.velocity = (0, -.3)
        elif vel == 2:
            star1.velocity = (0,-.4)
        elif vel == 3:
            star1.velocity = (0,-.5)

        self.star_list.append(star1)

    # Function to draw everything on the screen
    def on_draw(self):
        
        self.clear()
        self.star_list.draw()
        self.player_list.draw()
        self.asteroid_list.draw()
        self.bullet_list.draw()

        output = f'Score: {self.score}'
        arcade.draw_text(text=output, start_x=10, start_y=20,
                            color=arcade.color.WHITE, font_size=14)
    
        
    
    def on_update(self, delta_time: float):


        self.player_list.update()

        self.player_list.update_animation()
        self.star_list.update()
        self.asteroid_list.update()

        self.bullet_list.update()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.asteroid_list)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for asteroid in hit_list:
                asteroid.remove_from_sprite_lists()
                self.score+=1
            
            if bullet.bottom > HEIGHT:
                bullet.remove_from_sprite_lists()
        

        for start in self.star_list:
            if start.top < 0:
                start.remove_from_sprite_lists()
        
        for asteroid in self.asteroid_list:
            if asteroid.top < 0:
                asteroid.remove_from_sprite_lists()




    def on_key_press(self, symbol, modifiers):
        
        
        if symbol == arcade.key.UP:
            self.player.change_y = 5
            
            
            
        if symbol == arcade.key.DOWN:
            self.player.change_y = -5


        if symbol == arcade.key.LEFT:
            self.player.change_x = -5
             
           

        if symbol == arcade.key.RIGHT:
            self.player.change_x = 5
        
        if symbol == arcade.key.SPACE:

            bullet = arcade.Sprite('./images/bullet.png')

            bullet.change_y = 5.5

            bullet.center_x = self.player.center_x
            bullet.bottom = self.player.top

            self.bullet_list.append(bullet)
           
        




    def on_key_release(self, symbol: int, modifiers: int):

        if symbol == arcade.key.UP:
            self.player.change_y = 0
            

        if symbol == arcade.key.DOWN:
            self.player.change_y = 0

            

        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player.change_x = 0   


def main():
    """ Main function """
    window = MyGame(WIDTH, HEIGHT, TITLE, resizable=False)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()