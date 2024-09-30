# 1. Use an official Python runtime as a parent image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file to the working directory
COPY requirements.txt /app/

# 4. Install any required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the entire project into the container
COPY . /app/

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Define the environment variable for Django to run
ENV DJANGO_ENV=production

# 8. Run migrations and start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
