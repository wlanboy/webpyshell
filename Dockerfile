# Use the official Python image as the base
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the container
COPY main.py /app/
COPY templates/ /app/templates/
COPY static/ /app/static/

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 2100

# Command to run the Flask app
#CMD ["python", "main.py"]
#./.venv/bin/gunicorn -k gevent -w 1 --bind 0.0.0.0:2100 --log-level info main:app --reload
CMD ["gunicorn", "-k", "gevent", "-w", "1", "--bind", "0.0.0.0:2100", "--log-level", "info", "main:app", "--reload"]