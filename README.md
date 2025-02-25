# Love Message Scheduler & Reminder App

## Overview

This app allows you to automatically send love messages to your wife via WhatsApp at scheduled times. You can customize the messages using an LLM (Large Language Model) like GPT, and the app includes a flexible scheduling system for sending messages at specific times of the day, on specific days of the week, or for special occasions (e.g., anniversaries, birthdays). Additionally, the app sends a reminder a day before a special occasion, ensuring you never forget an important event!

Features
	•	Automatic Love Messages: The app generates sweet messages using GPT and sends them to your wife’s WhatsApp.
	•	Customizable Schedules: You can schedule love messages for specific times of the day (e.g., every morning or at random times).
	•	Day-Specific Scheduling: Schedule messages only on weekdays, weekends, or specific days (e.g., only on Monday).
	•	Special Occasion Scheduling: Schedule messages for anniversaries, birthdays, and other important events.
	•	Reminders: Get reminders for upcoming special occasions one day before they happen.
	•	GUI Interface: An easy-to-use graphical interface to input prompts, manage schedules, and more.

Requirements
	1.	Python 3.7+
	2.	Libraries:
	•	openai
	•	twilio
	•	tkinter (for GUI)
	•	apscheduler

You can install the required libraries using pip:
pip install openai twilio tkinter apscheduler
<img width="659" alt="Screenshot 2025-02-25 at 13 50 13" src="https://github.com/user-attachments/assets/8a7baca1-1ce9-4930-be37-1ed16e50b27c" />
## Setup
	1.	Twilio Account:
	•	Sign up for a Twilio account at Twilio.
	•	Create a WhatsApp sandbox or purchase a WhatsApp-enabled Twilio number.
	•	Note down your Twilio Account SID, Auth Token, and the WhatsApp sandbox number.
	2.	OpenAI API Key:
	•	Sign up at OpenAI.
	•	Create a new API key and save it.
	3.	Configure the App:
	•	Replace your_openai_api_key with your OpenAI API key.
	•	Replace your_twilio_sid, your_twilio_auth_token, and the twilio_whatsapp_number in the code with your actual Twilio credentials and WhatsApp number.

Code Explanation

1. Generating Love Messages:

The app uses OpenAI’s GPT to generate love messages based on a user-provided prompt. The prompt can be anything like “Write a sweet love message for my wife.”

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

2. Sending Messages via Twilio:

Twilio’s API is used to send WhatsApp messages. Messages are sent using the twilio Python library.
def send_message(prompt="Write a sweet love message for my wife"):
    love_message = generate_love_message(prompt)
    client = Client(account_sid, auth_token)
    msg = client.messages.create(
        from_=twilio_whatsapp_number,
        body=love_message,
        to=wife_whatsapp_number
    )
<img width="660" alt="Screenshot 2025-02-25 at 13 52 15" src="https://github.com/user-attachments/assets/507f0a39-d4c5-4b7a-b86c-75c5893522c8" />
3. Scheduling Messages:

The app uses apscheduler to schedule messages at specific times. You can choose specific days of the week and times.

scheduler.add_job(send_scheduled_message, "cron", hour=time_obj.hour, minute=time_obj.minute, day_of_week=day)

4. Special Occasion Scheduling:

Users can also schedule messages for special occasions such as birthdays or anniversaries.

<img width="663" alt="Screenshot 2025-02-25 at 13 55 22" src="https://github.com/user-attachments/assets/06e43f62-83f4-4d4e-a349-5ac7df75abd0" />

5. Reminder Before Special Occasion:

A reminder is sent one day before the special occasion to ensure that the user is notified.

<img width="663" alt="Screenshot 2025-02-25 at 13 55 58" src="https://github.com/user-attachments/assets/93f72c96-9a79-45d6-85e4-7cb34a9dc408" />

## Use Cases
	1.	Daily Love Messages:
Schedule messages to be sent every morning or at random times during the day to surprise your wife with love.

	2.	Weekday/Weekend Specific Messages:
You can set messages to be sent only on weekdays or weekends, or any specific day of the week.

	3.	Special Occasion Messages:
Schedule love messages for special occasions like anniversaries, birthdays, and other important dates.

	4.	Reminders for Special Occasions:
Receive a reminder a day before any special occasion so that you can plan ahead.

## GUI

The app comes with a simple GUI built using Tkinter. You can use the GUI to:
	•	Enter prompts to generate love messages.
	•	Schedule messages at specific times.
	•	Manage and remove scheduled messages.
	•	View and manage special occasion messages.

## Example of Usage
	1.	Open the app.
	2.	Enter a custom prompt (e.g., “Write a romantic message for my wife”).
	3.	Press Generate & Send to send the message immediately.
	4.	Use the Schedule Messages section to set a time and choose specific days (e.g., every Monday, Wednesday, and Friday at 9 AM).
	5.	Use the Special Occasions section to schedule messages for important dates like anniversaries, birthdays, etc.
	6.	The app will automatically send the messages as per the schedule and send reminders a day before the occasion.

## Files
	•	main.py: The main script that runs the application.
	•	schedules.json: File that stores the schedules to persist them across app restarts.

## License

This project is open-source and available under the MIT License.
