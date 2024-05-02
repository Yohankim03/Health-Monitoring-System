# Use a base image with both Python and Node.js
FROM nikolaik/python-nodejs:python3.10-nodejs16

# Set the working directory to the project root
WORKDIR /usr/src/app

# Copy the Flask application files
COPY app.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set up the React application
WORKDIR /usr/src/app/web
COPY web/package*.json ./
RUN npm install
COPY web/ .

# Expose the ports (React typically runs on 3000, Flask on 5000)
EXPOSE 3000 5000

# Set the working directory to the web directory to run npm scripts
WORKDIR /usr/src/app/web

# Command to start the application
CMD ["npm", "run", "dev"]
