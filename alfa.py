from platform import platform
from random import randint
import arcade



UPDATES_PER_FRAME = 5

WIDTH = 1280
HEIGHT = 720
TITLE = 'GAME'
SCALE = .5

class Rocket(arcade.Sprite):

    def __init__(self):

        super().__init__()

        self.cur_texture = 0
        self.points = [[-22, -90], [22, -90], [20, 28], [-22, 28]]
        self.set_hit_box(self.points)
        
        self.idle_texture = arcade.load_texture('images/rocket.png')
        

        self.rocket_textures = []

        for i in range(4):

            texture = arcade.load_texture(f'images/rocket_{i+1}.png')

            self.rocket_textures.append(texture)
    
    def update_animation(self, delta_time : float):

        if self.change_y == -1 or self.change_y == 0:
            self.texture = self.idle_texture
            return

        self.cur_texture += 1

        if self.cur_texture > 3 * UPDATES_PER_FRAME:

            self.cur_texture = 0

        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.rocket_textures[frame]


class MyGame(arcade.Window):

    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        self.player_list = None

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player = Rocket()

        self.player.center_x = WIDTH / 2
        self.player.center_y =  HEIGHT / 2
        self.player.change_y = -1
        self.player.scale = SCALE
        print(self.player.position)

        self.player_list.append(self.player)

        self.rocket_sound = arcade.load_sound('sounds/rocket.wav')

        platform_loc = randint(0, 800)

        self.platfrom = arcade.Sprite('images/platform.png')
        self.platfrom.center_x = platform_loc
        self.platfrom.bottom = 0

        self.platfrom_pilar = arcade.Sprite('images/platform_pilar.png')
        self.platfrom_pilar.center_x = platform_loc + 80
        self.platfrom_pilar.center_y = 200

        self.back = arcade.Sprite('images/mountains.jpg')
        self.back.center_x = WIDTH / 2
        self.back.center_y = HEIGHT / 2
        self.back.scale = 2


        arcade.set_background_color(arcade.color.SKY_BLUE)

    def on_draw(self):
        
        self.clear()
        self.back.draw()
        self.player_list.draw()
        self.platfrom_pilar.draw()
        self.platfrom.draw()
        
    
    def on_update(self, delta_time: float):

        if self.player.collides_with_sprite(self.platfrom):
            self.player.change_y = 0
            self.player.change_angle = 0
        
        print(self.player.bottom)
        if self.player.bottom < 0:
            arcade.close_window()
            self.player.change_y = 0

        self.player_list.update()

        self.player_list.update_animation()

    def on_key_press(self, symbol, modifiers):
        
        
        if symbol == arcade.key.UP:
            self.player.change_y = 3
            
            self.sound = arcade.sound.play_sound(self.rocket_sound)
            

        if symbol == arcade.key.LEFT:
            self.player.change_x = -1.0
            self.player.change_angle = -.5
            
            
           

        if symbol == arcade.key.RIGHT:
            self.player.change_x = 1
            self.player.change_angle = .5
           
        




    def on_key_release(self, symbol: int, modifiers: int):

        if symbol == arcade.key.UP:
            self.player.change_y = -1
            arcade.stop_sound(self.sound)

            

        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT:
            self.player.change_x = 0   


def main():
    """ Main function """
    window = MyGame(WIDTH, HEIGHT, TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()