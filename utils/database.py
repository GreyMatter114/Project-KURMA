import sqlite3
import time
import threading
# Create or connect to the SQLite database
conn = sqlite3.connect('./utils/robot_state.db')
cursor = conn.cursor()

# Create a table to store robot state
cursor.execute('''
    CREATE TABLE IF NOT EXISTS robot_state (
        timestamp TEXT,
        motor_direction INTEGER,
        servo_angle INTEGER,
        vacuum_pump_state INTEGER
    )
''')

# Function to update and store robot state
def update_robot_state():
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    motor_direction = 1  # Replace with actual motor direction value
    servo_angle = 90  # Replace with actual servo angle value
    vacuum_pump_state = 0  # Replace with actual vacuum pump state

    cursor.execute('INSERT INTO robot_state VALUES (?, ?, ?, ?)', (timestamp, motor_direction, servo_angle, vacuum_pump_state))
    conn.commit()

# Periodically update and store robot state
try:
    while True:
        update_robot_state()
        time.sleep(60)  # Update every 60 seconds (adjust as needed)
except :
    conn.close()
