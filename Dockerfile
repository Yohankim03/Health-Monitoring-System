# Use a base image with both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs16

# Set the working directory to the project root
WORKDIR /usr/src/app

# Set the Python path to include the root directory (and any other necessary directories)
ENV PYTHONPATH=/usr/src/app

# Copy the Flask application files
COPY database.db app.py requirements.txt queue_manager.py tasks.py test_queue.py extensions.py ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the api directory if it is a package
COPY api/ ./api/

# Set up the React application
COPY web/package*.json ./web/
WORKDIR /usr/src/app/web
RUN npm install
COPY web/ .

# Move back to the project root
WORKDIR /usr/src/app

# Expose the ports (React typically runs on 3000, Flask on 5000)
EXPOSE 3000 5000

# Run the command to start both the Flask and React servers from the web directory
CMD ["npm", "run", "dev", "--prefix", "web"]
