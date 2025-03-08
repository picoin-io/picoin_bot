# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt requirements.txt
COPY picion_bot.py picion_bot.py

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "picion_bot.py"]
