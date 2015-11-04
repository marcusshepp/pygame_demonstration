""" Pong in pygame. """
import os

import pygame
from pygame import sprite
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


class BaseSprite(sprite.Sprite):
    """ Base class for sprite classes with a bitmap image. """
    bitmap_filename = None
    image = None
    groups = None

    @classmethod
    def load_image(cls):
        """ Load the image used for all instances of a sprite class. """
        # Can't set this to a converted image until post display initialization
        # so resorting to class method for a one-time load.
        path = os.path.join('resources', cls.bitmap_filename)
        cls.image = pygame.image.load(path)
        cls.image.convert()

    def __init__(self, start_pos):
        # Old-style base class, so can't use super().
        sprite.Sprite.__init__(self, self.groups)
        self.pos = start_pos
        self.image = self.image
        self.rect = self.image.get_rect()


    def update(self):
        """ Set the new top-left position of the sprite. """
        self.rect.topleft = self.pos


class Paddle(BaseSprite):
    bitmap_filename = 'paddle.bmp'
    UP = -1
    DOWN = 1
    STATIONARY = 0

    def __init__(self, start_pos, boundary,
                    speed=5, direction=STATIONARY):
        """ Create a new Paddle.

        * start_pos - A 2-tuple of position (x, y).
        * speed - The number of pixels per update to move the paddle.
        * direction - Can be Paddle.UP, Paddle.DOWN or Paddle.STATIONARY.
        """
        BaseSprite.__init__(self, start_pos)
        self.boundary = boundary
        self.direction = direction
        self.speed = speed

    def update(self):
        """ Change the position of the paddle. """
        vertical_delta = self.speed * self.direction
        self.pos = (self.pos[0], self.pos[1] + vertical_delta)

        # Keep the paddle within the boudary.
        if self.pos[1] < self.boundary.top:
            self.pos = (self.pos[0], self.boundary.top)

        elif self.pos[1] > self.boundary.bottom:
            self.pos = (self.pos[0], self.boundary.bottom)

        self.rect.topleft = self.pos


class Player(object):
    """ An AI that controls a paddle. """
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

    def play(self):
        """ Position the paddle based on the ball's position. """
        if self.ball.rect.top < self.paddle.rect.top:
            self.paddle.direction = self.paddle.UP
        elif self.ball.rect.bottom > self.paddle.rect.bottom:
            self.paddle.direction = self.paddle.DOWN


class Ball(BaseSprite):
    bitmap_filename = 'ball.bmp'

    def __init__(self, start_pos, 
                    speed=1, horizontal_direction=1,
                    vertical_direction=1):
        """ Create a new Ball.

        * start_pos - A 2-tuple of position (x, y).
        * speed - The number of pixels per update to move the ball.
        * horizontal_direction - Can be -1 for West or 1 for East.
        * vertical_direction - Can be -1 for North or 1 for South
        """
        BaseSprite.__init__(self, start_pos)
        self.vertical_direction = vertical_direction
        self.horizontal_direction = horizontal_direction
        self.speed = speed
        self.in_collision = False

    def update(self):
        """ Change the position of the ball. """
        vertical_delta = self.speed * self.vertical_direction
        horizontal_delta = self.speed * self.horizontal_direction
        self.pos = (self.pos[0] + horizontal_delta ,
                    self.pos[1] + vertical_delta)
        self.rect.topleft = self.pos

    def toggle_horizontal_direction(self):
        self.horizontal_direction = -1 * self.horizontal_direction

    def toggle_vertical_direction(self):
        self.vertical_direction = -1 * self.vertical_direction


def bounce_ball_off_boundary(ball, boundary):
    """ Change the ball's direction if it touches the boundary. """
    if ball.rect.top < boundary.top or ball.rect.bottom > boundary.bottom: 
        if not ball.in_collision:
            ball.in_collision = True
            ball.toggle_vertical_direction()
    elif ball.rect.left < boundary.left or ball.rect.right > boundary.right:
        if not ball.in_collision:
            ball.in_collision = True
            ball.toggle_horizontal_direction()
    elif ball.in_collision:
        ball.in_collision = False



def bounce_ball_off_paddles(ball, left_paddle, right_paddle):
    """ Change the ball's direction if it touches the paddles. """
    if pygame.sprite.collide_rect(ball, left_paddle):
        if not ball.in_collision:
            ball.in_collision = True
            ball.toggle_horizontal_direction()
    elif pygame.sprite.collide_rect(ball, right_paddle):
        if not ball.in_collision:
            ball.in_collision = True
            ball.toggle_horizontal_direction()
    elif ball.in_collision:
        ball.in_collision = False


def main():
    """ Runs the game.

    Press ESC to exit.
    """
    screen_width = 640
    screen_height = 480
    paddle_width = 10
    paddle_height = 100
    padding = 20 

    # Black screen with hidden mouse.
    pygame.init()
    pygame.mouse.set_visible(0)
    screen = pygame.display.set_mode((screen_width, screen_height))
    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # The range of movement for the paddles
    paddle_range = screen.get_rect().copy()
    # paddle_range.rect.top -= padding
    # paddle_range.rect.left -= padding
    paddle_range.width -= 2 * padding 
    paddle_range.height -= 2 * padding
    paddle_range.height -= paddle_height
    paddle_range.left += padding
    paddle_range.top += padding


    # Sprites - two paddles and a ball.
    sprites = sprite.Group()
    Paddle.groups = sprites
    Ball.groups = sprites

    Paddle.load_image()
    left_paddle = Paddle((paddle_range.left, paddle_range.top), paddle_range)
    right_paddle = Paddle((paddle_range.right - paddle_width, paddle_range.top), paddle_range)

    Ball.load_image()
    ball = Ball((100, 100))

    left_player = Player(left_paddle, ball)
    right_player = Player(right_paddle, ball)
    
    going = True
    while going:
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

        sprites.clear(screen, background)
        bounce_ball_off_paddles(ball, left_paddle, right_paddle)
        bounce_ball_off_boundary(ball, screen.get_rect())
        left_player.play()
        right_player.play()
        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()