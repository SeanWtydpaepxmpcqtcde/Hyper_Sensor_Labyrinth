def on_forever():
    pass
basic.forever(on_forever)
from microbit import *
import ssd1306

# 1. Initialize I2C and OLED Screen
# SDA is Pin 20, SCL is Pin 19
i2c.init(freq=400000, sda=pin20, scl=pin19)
oled = ssd1306.initialize()

# 2. Physics Variables
ball_x = 64.0        # Starting X position (center)
ball_y = 32.0        # Starting Y position (center)
vel_x = 0.0         # Velocity X
vel_y = 0.0         # Velocity Y
friction = 0.92      # Air resistance (0 to 1)
sensitivity = 200    # Lower is more sensitive

# 3. Main Game Loop
while True:
    # --- Input Processing ---
    # Get tilt data from the built-in accelerometer
    acc_x = accelerometer.get_x()
    acc_y = accelerometer.get_y()
    
    # --- Physics Engine ---
    # Convert tilt to acceleration
    vel_x += acc_x / sensitivity
    vel_y += acc_y / sensitivity
    
    # Apply friction (prevents the ball from sliding forever)
    vel_x *= friction
    vel_y *= friction
    
    # Update position
    ball_x += vel_x
    ball_y += vel_y
    
    # --- Collision Detection (Screen Borders) ---
    # OLED size is 128x64. Keeping the ball within 0-127 and 0-63.
    if ball_x < 2:
        ball_x = 2
        vel_x = 0
    elif ball_x > 125:
        ball_x = 125
        vel_x = 0
        
    if ball_y < 2:
        ball_y = 2
        vel_y = 0
    elif ball_y > 61:
        ball_y = 61
        vel_y = 0

    # --- Rendering (Graphics) ---
    oled.clear()
    
    # Draw the "Ball" as a 4x4 filled rectangle
    oled.fill_rect(int(ball_x - 2), int(ball_y - 2), 4, 4, 1)
    
    # Optional: Draw UI or Walls here
    # oled.text("Score: 0", 0, 0)
    
    oled.show()
    
    # Control the frame rate (approx. 50 FPS)
    sleep(20)
