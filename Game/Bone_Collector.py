
import arcade
import random
import os

SPRITE_SCALING = 0.1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Collect Bones"

# These numbers represent "states" that the game can be in.

GAME_RUNNING = 0
GAME_OVER = 1
GAME_OVER_TIMEOUT = 2
LEVEL_1 = 3

# Change the bone count and initial timer here
BONE_COUNT = 50
INITIAL_TIMER = 20


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, screen_width, screen_height, title):
        """ Constructor """
        # Call the parent constructor. Required and must be the first line.
        super().__init__(screen_width, screen_height, title)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Set the background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Start 'state' will be showing the first page of instructions.
        self.current_state = GAME_RUNNING

        self.player_list = None
        self.bone_list = None

        # Set up the player
        self.score = 0
        self.player_sprite = None
        self.level = 1


    def setup(self):
        """
        Set up the game.
        """
        # Sprite lists
        
        self.player_list = arcade.SpriteList()
        self.bone_list = arcade.SpriteList()
        self.timer = INITIAL_TIMER
        # Set up the player
        self.player_sprite = arcade.Sprite("images/dog2.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Specifying how bones are increasing according to the level
        num_bones = self.level * BONE_COUNT
        for i in range(num_bones):

            # Create the bone instance
            bone = arcade.Sprite("images/bone.png", SPRITE_SCALING / 1.5)

            # Position the bone
            bone.center_x = random.randrange(SCREEN_WIDTH)
            bone.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the bone to the lists
            self.bone_list.append(bone)

        # Don't show the mouse cursor
        self.set_mouse_visible(False)


    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Timeout!!! Game Over"
        arcade.draw_text(output, 140, 400, arcade.color.RED, 30)

        output = f"Final Score: {self.score}"
        arcade.draw_text(output, 140, 300, arcade.color.ROSE, 25)

        output = "Click to restart"
        arcade.draw_text(output, 140, 200, arcade.color.DARK_GREEN, 24)

    def draw_game_complete(self):
        output = "Congratulations!!! Game Completed"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2, arcade.color.DARK_ELECTRIC_BLUE, 25)

        output = f"Final Score: {self.score}"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2 - 50, arcade.color.ROSE, 25)

        output = "Click to restart"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2 - 100, arcade.color.DARK_GREEN, 18)


    def level_change(self):
        """
        Draw "Level Change" across the screen.
        """
        output = "Congratulations!!! Level Completed"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2, arcade.color.YELLOW, 25)

        output = f"Current Score: {self.score}"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2 - 50, arcade.color.ROSE, 25)

        output = "Goto Next Level"
        arcade.draw_text(output, 50, SCREEN_HEIGHT/2 - 100, arcade.color.DARK_GREEN, 18)


    def draw_game(self):
        """
        Draw all the sprites, along with the score.
        """
        # Draw all the sprites.
        self.player_list.draw()
        self.bone_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.DARK_GREEN, 14)

        output = f"Time Remaining: {self.timer:02.2f}"

        # Output the timer text.
        arcade.draw_text(output, SCREEN_WIDTH - (SCREEN_WIDTH/2 + 100), SCREEN_HEIGHT - 20, arcade.color.DARK_BLUE, 18, bold=True)
        output = f"Level: {self.level}"
        arcade.draw_text(output, 10, SCREEN_HEIGHT-20, arcade.color.PURPLE, 14)


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == GAME_RUNNING:
            self.draw_game()
        elif self.current_state == LEVEL_1:
            self.draw_game()
            self.level_change()
        elif self.current_state == GAME_OVER_TIMEOUT:
            self.draw_game()
            self.draw_game_over()
        elif self.current_state == GAME_OVER:
            self.draw_game()
            self.draw_game_complete()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        if self.current_state == GAME_RUNNING:
            self.current_state = GAME_RUNNING
        elif self.current_state == LEVEL_1:
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER or self.current_state == GAME_OVER_TIMEOUT:
            # Restart the game.
            self.level = 1
            self.score = 0
            self.setup()
            self.current_state = GAME_RUNNING

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        # Only move the user if the game is running.
        if self.current_state == GAME_RUNNING:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y


    def update(self, delta_time):
        """ Movement and game logic """
        if self.current_state == GAME_RUNNING:
            self.timer -= delta_time
            if self.timer <= 0:
                self.timer = 0
                self.current_state = GAME_OVER_TIMEOUT
        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.bone_list.update()
            self.player_list.update()

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.bone_list)

            # Loop through each colliding sprite, remove it, and add to the
            # score.
            for bone in hit_list:
                bone.kill()
                self.score += 1

            # If we've collected all the games, then move to a "GAME_OVER"
            # state.
            if len(self.bone_list) == 0:
                if self.level == 1:
                    self.level += 1
                    self.current_state = LEVEL_1
                else:
                    self.current_state = GAME_OVER
                    self.set_mouse_visible(True)


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()