import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from plyer import notification
import time
import threading
from PIL import Image, ImageTk

# Function to send a notification
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10  # Notification will be shown for 10 seconds
    )

# Function to remind to drink water
def remind_water():
    send_notification("Water Reminder", "Time to drink a glass of water!")

# Function to remind to exercise
def remind_exercise():
    send_notification("Exercise Reminder", "It's time to exercise! Let's move your body.")

# Function that runs reminders with custom intervals
def run_reminders(water_interval, exercise_interval):
    while True:
        remind_water()  # Send water reminder
        time.sleep(water_interval * 60)  # Wait for user-defined interval in minutes (convert to seconds)

        remind_exercise()  # Send exercise reminder
        time.sleep(exercise_interval * 60)  # Wait for user-defined interval in minutes (convert to seconds)

# Start reminders in a separate thread
def start_reminders():
    try:
        # Get the intervals from the user input (convert to integers)
        water_interval = int(water_interval_entry.get())
        exercise_interval = int(exercise_interval_entry.get())

        # Start reminders in a background thread
        thread = threading.Thread(target=run_reminders, args=(water_interval, exercise_interval))
        thread.daemon = True  # This ensures the thread ends when the main program exits
        thread.start()

        # Update status
        status_label.config(text="Reminders are ON", fg="green")
    except ValueError:
        # If the user enters something that is not a number, show an error message
        status_label.config(text="Please enter valid numbers", fg="red")

# Function to start the journey (Go to the main page)
def start_journey():
    home_frame.pack_forget()  # Hide the home page
    main_frame.pack()  # Show the main page

# Function to generate health plan based on user input
def generate_health_plan():
    try:
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        goal = goal_var.get()

        # Calculate BMI (Body Mass Index)
        bmi = weight / (height ** 2)

        # Health Plan Recommendations
        if goal == "Weight Loss":
            if bmi >= 25:
                health_plan = f"To lose weight, aim for a calorie deficit of 500-1000 kcal/day.\n\nTry to consume 1200-1500 calories a day.\nExercise 4-5 days a week."
            else:
                health_plan = f"Focus on maintaining your weight with a balanced diet.\n\nConsume around 1800-2000 calories a day.\nExercise 3 times a week."
        elif goal == "Fitness":
            health_plan = f"Maintain a balanced diet with good protein intake.\n\nAim for 1500-2000 calories/day.\nFocus on strength training 3-4 days/week."
        else:
            health_plan = "It's important to have a balanced, healthy diet and regular exercise to maintain health."

        # Display the health plan to the user
        show_health_plan_page(health_plan)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid values for age, weight, and height.")

# Function to show health plan page after generating the plan
def show_health_plan_page(health_plan):
    # Hide the main page and show the health plan page
    main_frame.pack_forget()
    health_plan_frame.pack()

    # Display the health plan text
    health_plan_label.config(text=health_plan)

# Function to go back to the main page
def go_back():
    health_plan_frame.pack_forget()  # Hide health plan page
    main_frame.pack()  # Show the main page again

# Set up the main window using Tkinter
window = tk.Tk()
window.title("Healthy Tracker")
window.geometry("600x700")
window.config(bg='#2ecc71')

# ---- Home Page Frame ----
home_frame = tk.Frame(window, bg='#2ecc71')

# Health Tracker Label on the Home Page
welcome_label = tk.Label(home_frame, text="Welcome to Health Tracker", font=("Arial", 22, 'bold'), fg='white', bg='#2ecc71')
welcome_label.pack(pady=60)

# Start Journey Button on the Home Page
start_button = tk.Button(home_frame, text="Start the Journey", font=("Arial", 14, 'bold'), command=start_journey, bg='#3498db', fg='white', relief="raised", bd=4, padx=15, pady=10)
start_button.pack(pady=20)

home_frame.pack()  # Show the home page initially

# ---- Main Page Frame ----
main_frame = tk.Frame(window, bg='#2ecc71')

# Load and display the virtual coach image
coach_image = Image.open("coach_image.png")  # Make sure to place the image in the same directory as the code
coach_image = coach_image.resize((150, 150))  # Resize the image if needed
coach_photo = ImageTk.PhotoImage(coach_image)

coach_label = tk.Label(main_frame, image=coach_photo, bg='#2ecc71')
coach_label.pack(pady=20)

# Ask user for their details to generate a health plan
age_label = tk.Label(main_frame, text="Enter your age:", font=("Arial", 14), fg='white', bg='#2ecc71')
age_label.pack(pady=10)
age_entry = tk.Entry(main_frame, font=("Arial", 14), bd=2, relief="sunken")
age_entry.pack(pady=5)

weight_label = tk.Label(main_frame, text="Enter your weight (kg):", font=("Arial", 14), fg='white', bg='#2ecc71')
weight_label.pack(pady=10)
weight_entry = tk.Entry(main_frame, font=("Arial", 14), bd=2, relief="sunken")
weight_entry.pack(pady=5)

height_label = tk.Label(main_frame, text="Enter your height (m):", font=("Arial", 14), fg='white', bg='#2ecc71')
height_label.pack(pady=10)
height_entry = tk.Entry(main_frame, font=("Arial", 14), bd=2, relief="sunken")
height_entry.pack(pady=5)

goal_label = tk.Label(main_frame, text="What is your goal?", font=("Arial", 14), fg='white', bg='#2ecc71')
goal_label.pack(pady=10)

goal_var = ttk.Combobox(main_frame, values=["Weight Loss", "Fitness", "Health Maintenance"], state="readonly", font=("Arial", 14))
goal_var.pack(pady=5)

# Button to generate health plan
generate_button = tk.Button(main_frame, text="Generate Health Plan", font=("Arial", 14, 'bold'), command=generate_health_plan, bg='#9b59b6', fg='white', relief="raised", bd=4, padx=15, pady=10)
generate_button.pack(pady=20)

# Reminder Inputs and Buttons
reminder_label = tk.Label(main_frame, text="Set your reminders:", font=("Arial", 14, 'bold'), fg='white', bg='#2ecc71')
reminder_label.pack(pady=20)

water_interval_label = tk.Label(main_frame, text="Water reminder interval (min):", font=("Arial", 12), fg='white', bg='#2ecc71')
water_interval_label.pack(pady=5)
water_interval_entry = tk.Entry(main_frame, font=("Arial", 12), bd=2, relief="sunken")
water_interval_entry.pack(pady=5)

exercise_interval_label = tk.Label(main_frame, text="Exercise reminder interval (min):", font=("Arial", 12), fg='white', bg='#2ecc71')
exercise_interval_label.pack(pady=5)
exercise_interval_entry = tk.Entry(main_frame, font=("Arial", 12), bd=2, relief="sunken")
exercise_interval_entry.pack(pady=5)

status_label = tk.Label(main_frame, text="Set reminders and start!", font=("Arial", 12, 'italic'), fg='white', bg='#2ecc71')
status_label.pack(pady=5)

start_reminders_button = tk.Button(main_frame, text="Start Reminders", font=("Arial", 14, 'bold'), command=start_reminders, bg='#e67e22', fg='white', relief="raised", bd=4, padx=15, pady=10)
start_reminders_button.pack(pady=20)

# ---- Health Plan Page ----
health_plan_frame = tk.Frame(window, bg='#2ecc71')

# Display the generated health plan
health_plan_label = tk.Label(health_plan_frame, text="", font=("Arial", 14), fg='white', bg='#2ecc71', justify="left")
health_plan_label.pack(pady=20)

# Button to go back to the main page
back_button = tk.Button(health_plan_frame, text="Back to Main", font=("Arial", 14), command=go_back, bg='#3498db', fg='white', relief="raised", bd=4, padx=15, pady=10)
back_button.pack(pady=20)

# Pack the home frame initially
main_frame.pack_forget()
health_plan_frame.pack_forget()

# Run the Tkinter event loop
window.mainloop()








