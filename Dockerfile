FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

# Make port 8040 available to the world outside this container
EXPOSE 8040

#Environment variables
ENV PINECONE_API_KEY = a8861bb3-e7fa-469d-aecf-0372fbed64ee

# Run main.py when the container launches
CMD ["python3", "main.py"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8040"]