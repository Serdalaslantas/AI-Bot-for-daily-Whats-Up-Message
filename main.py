from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
import tkinter as tk
from tkinter import messagebox, ttk
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import json
import os
import dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Twilio credentials
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
twilio_whatsapp_number = "whatsapp:+14155238886"
persons_whatsapp_number = "whatsapp:+123456789"

# Scheduler
scheduler = BackgroundScheduler()

# File to store schedules
schedule_file = "schedules.json"


# Load saved schedules
def load_schedules():
    if os.path.exists(schedule_file):
        try:
            with open(schedule_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []


# Save schedules to file
def save_schedules():
    with open(schedule_file, "w") as f:
        json.dump(scheduled_times, f)


# Load scheduled times from file
scheduled_times = load_schedules()


# Function to generate a love message using GPT
def generate_love_message(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# Function to send a WhatsApp message
def send_message(prompt="Write romantic messages to my fiance. add hearts and mention my name in the end."):
    love_message = generate_love_message(prompt)
    try:
        clients = Client(account_sid, auth_token)
        msg = clients.messages.create(
            from_=twilio_whatsapp_number,
            body=love_message,
            to=persons_whatsapp_number
        )
        print(f"Message sent: {love_message}")
    except Exception as e:
        print(f"Failed to send message: {e}")


# Function to add a scheduled time with selected days
def add_schedule():
    time_str = time_entry.get()
    selected_days = [day for day, var in day_vars.items() if var.get()]

    if not selected_days:
        messagebox.showerror("Error", "Please select at least one day.")
        return

    try:
        time_obj = datetime.datetime.strptime(time_str, "%H:%M")
        schedule_entry = {"time": time_str, "days": selected_days}

        if schedule_entry not in scheduled_times:
            scheduled_times.append(schedule_entry)
            update_schedule_list()
            save_schedules()

            for day in selected_days:
                scheduler.add_job(send_scheduled_message, "cron", hour=time_obj.hour, minute=time_obj.minute,
                                  day_of_week=day)
            scheduler.start()
            messagebox.showinfo("Success", f"Message scheduled at {time_str} on {', '.join(selected_days)}")
        else:
            messagebox.showwarning("Warning", "This schedule already exists.")
    except ValueError:
        messagebox.showerror("Error", "Enter time in HH:MM format (24-hour clock)")


# Function to remove a selected schedule
def remove_schedule():
    selected_index = schedule_listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Please select a schedule to remove.")
        return

    selected_entry = scheduled_times[selected_index[0]]
    scheduled_times.remove(selected_entry)
    update_schedule_list()
    save_schedules()

    scheduler.remove_all_jobs()  # Clear all jobs
    for schedule in scheduled_times:
        time_obj = datetime.datetime.strptime(schedule["time"], "%H:%M")
        for day in schedule["days"]:
            scheduler.add_job(send_scheduled_message, "cron", hour=time_obj.hour, minute=time_obj.minute,
                              day_of_week=day)

    messagebox.showinfo("Success", "Schedule removed successfully.")


# Function to update the schedule list in GUI
def update_schedule_list():
    schedule_listbox.delete(0, tk.END)
    for schedule in scheduled_times:
        schedule_listbox.insert(tk.END, f"{schedule['time']} - {', '.join(schedule['days'])}")


# Function to send scheduled messages
def send_scheduled_message():
    send_message()


# Restore scheduled messages on startup
for schedule in scheduled_times:
    time_obj = datetime.datetime.strptime(schedule["time"], "%H:%M")
    for day in schedule["days"]:
        scheduler.add_job(send_scheduled_message, "cron", hour=time_obj.hour, minute=time_obj.minute, day_of_week=day)
scheduler.start()

# Create GUI using Tkinter
root = tk.Tk()
root.title("Love Message Scheduler")

tk.Label(root, text="Enter Your Love Message Prompt:").pack(pady=5)
prompt_entry = tk.Entry(root, width=50)
prompt_entry.pack(pady=5)

send_button = tk.Button(root, text="Generate & Send", command=send_message)
send_button.pack(pady=5)

tk.Label(root, text="Schedule Messages (HH:MM):").pack(pady=5)
time_entry = tk.Entry(root, width=10)
time_entry.pack(pady=5)

tk.Label(root, text="Select Days:").pack(pady=5)
day_frame = tk.Frame(root)
day_frame.pack(pady=5)

day_vars = {
    "mon": tk.IntVar(),
    "tue": tk.IntVar(),
    "wed": tk.IntVar(),
    "thu": tk.IntVar(),
    "fri": tk.IntVar(),
    "sat": tk.IntVar(),
    "sun": tk.IntVar()
}

for day, var in day_vars.items():
    tk.Checkbutton(day_frame, text=day.capitalize(), variable=var).pack(side=tk.LEFT)

add_schedule_button = tk.Button(root, text="Add Schedule", command=add_schedule)
add_schedule_button.pack(pady=5)

tk.Label(root, text="Scheduled Messages:").pack(pady=5)
schedule_listbox = tk.Listbox(root, width=40, height=6)
schedule_listbox.pack(pady=5)

remove_schedule_button = tk.Button(root, text="Remove Selected", command=remove_schedule)
remove_schedule_button.pack(pady=5)

update_schedule_list()  # Populate the list with saved schedules

root.mainloop()
