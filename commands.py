from weather import get_weather
from reminder import add_reminder


def process_command(command):
    command = command.lower().strip()

    # Greeting
    if "hello" in command or "hi" in command:
        return {
            "type": "text",
            "message": "Hello! How can I help you today?"
        }

    # Weather Command
    elif "weather in" in command:

        city = command.split("weather in")[-1].strip()

        weather = get_weather(city)

        if weather:

            message = (
                f"The weather in {weather['city']} is "
                f"{weather['temperature']} degree Celsius "
                f"with {weather['description']}."
            )

            return {
                "type": "weather",
                "message": message,
                "data": weather
            }

        else:

            return {
                "type": "text",
                "message": "Sorry, I couldn't fetch the weather."
            }

    # Reminder Command
    elif "remind me to" in command:

        reminder = command.replace("remind me to", "").strip()

        add_reminder(reminder)

        return {
            "type": "text",
            "message": f"Reminder added: {reminder}"
        }

    # Unknown Command
    else:

        return {
            "type": "text",
            "message": "Sorry, I didn't understand that command."
        }