# Setting up the screen
import turtle
import keyboard
import math
import random
import winsound
import pygame as pg
import sys

WIDTH = 800
HEIGHT = 600

def turtles():
    global player, score_pen, gm, enemy, bullet, scr
    scr = turtle.Screen()
    turtle.setup(WIDTH, HEIGHT)
    scr.bgcolor("black")
    
    scr.title("Space Project")
    scr.bgpic("backg.gif")
    # Set up scenes
    turtle.register_shape("ene.gif")
    turtle.register_shape("spaceship.gif")

    # Create the player
    player = turtle.Turtle()
    player.color("blue")
    player.shape("spaceship.gif")
    player.penup()
    player.speed(0)
    player.setposition(0, -200)
    player.setheading(90)

    # Draw score
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color("white")
    score_pen.penup()
    score_pen.setposition(-200, 250)
    scorestring = "Score: %s" % score
    score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
    score_pen.hideturtle()

    # Gameover text
    gm = turtle.Turtle()
    gm.speed(0)
    gm.color("white")
    gm.penup()
    gm.setposition(-250, 0)
    gm.hideturtle()

    scorestring = "Score: %s" % score
    score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
    score_pen.hideturtle()

    # Add enemies to the list
    for i in range(number_of_enemies):
        # Creates enemy
        enemies.append(turtle.Turtle())

    for enemy in enemies:
        enemy.color("red")
        enemy.shape("ene.gif")
        enemy.penup()
        enemy.speed(0)
        x = random.randint(-300, 300)
        y = random.randint(100, 400)
        enemy.setposition(x, y)

    # Create the player's bullet
    bullet = turtle.Turtle()
    bullet.color("yellow")
    bullet.shape("triangle")
    bullet.penup()
    bullet.speed(0)
    bullet.setheading(90)
    bullet.shapesize(0.5, 0.5)
    bullet.hideturtle()


# Player movement
playerspeed = 15

scoremult = 10


def speed_up():
    playerspeed = 30


# Chose number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []

# Set the score to 0
score = 0

enemyspeed = 2

bulletspeed = 40

turtles()


# Left and right
def move_left():
    if keyboard.is_pressed('shift'):
        playerspeed = 35
    else:
        playerspeed = 15
    # player.setposition(player.xcor()-playerspeed,-350)
    x = player.xcor()
    x -= playerspeed
    if x < -350:
        x = -350
    player.setx(x)


def move_right():
    if keyboard.is_pressed('shift'):
        playerspeed = 35
    else:
        playerspeed = 15

    x = player.xcor()
    x += playerspeed
    if x > 350:
        x = 350
    player.setx(x)


def fire_bullet():
    # Globally declare bulletstate in order to modify
    global bulletstate
    if not bullet.isvisible():
        winsound.PlaySound("laser", winsound.SND_ASYNC)
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() - 10
        bullet.setposition(x, y)
        bullet.showturtle()
        


def isCollision(t1, t2):
    # Pytagorean theorem that calculates the distance between 2 points , if the distance is less than a certain amount we can say that the 2 objects collided.
    return t1.distance(t2) < 25


def close_game():
    scr.bye()
    winsound.PlaySound(None, winsound.SND_ALIAS)
    pg.mixer.stop()
    sys.exit("Game closed")


# Create keyboard bindings

turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(fire_bullet, "space")

turtle.listen()
run = True
# Main game loop
while run:
    
    for enemy in enemies:
        if player.isvisible():
            # Move the enemy
            x = enemy.xcor()
            x += enemyspeed
            enemy.setx(x)

            # Move enemy back and down
            if enemy.xcor() > 350:
                # Nested loop to move all enemies at the same time
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                enemyspeed *= -1

            if enemy.xcor() < -350:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                enemyspeed *= -1
            # Check for collision between bullet and enemy
            if isCollision(bullet, enemy):

                winsound.PlaySound("explosion", winsound.SND_ASYNC)
                
                # Reset bullet
                bullet.hideturtle()
                bullet.setposition(0, -400)
                # Reset enemy
                x = random.randint(-300, 300)
                y = random.randint(100, 400)
                enemy.setposition(x, y)
                # update score
                score += scoremult
                scoremult += 10
                scorestring = "Score: %s" % score
                score_pen.clear()
                score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
                # update speed
                if enemyspeed > 0:
                    enemyspeed += 1
                else:
                    enemyspeed -= 1

            # Check collision between player and enemy
            if isCollision(player, enemy):
                player.hideturtle()
                enemy.hideturtle()
                print("Game Over!")
                gm.showturtle()
                gmstring = "Game Over! Final Score:%s" % score + "\nPress Escape to exit"
                gm.write(gmstring, False, align="left", font=("Arial", 24, "normal"))
                turtle.onkey(close_game, "Escape")
                run = False
                break
            if enemy.ycor() < -390:
                player.hideturtle()
                enemy.hideturtle()
                print("Game Over!")
                gm.showturtle()
                gmstring = "Game Over! Final Score:%s" % score + "\nPress Escape to exit"
                gm.write(gmstring, False, align="left", font=("Arial", 24, "normal"))
                turtle.onkey(close_game, "Escape")
                run = False
                break
        else:
            print("Your score is: %s" % score)
            gm.showturtle()
            gmstring = "Game Over! Final Score:%s" % score + "\nPress Escape to exit"
            gm.write(gmstring, False, align="left", font=("Arial", 24, "normal"))
            turtle.onkey(close_game, "Escape")
            break

    # Move the bullet
    if bullet.isvisible():
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Bullet checker for top
    if bullet.ycor() > 450:
        bullet.hideturtle()
        

