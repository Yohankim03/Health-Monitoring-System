FROM node:14-buster

# Set the working directory in the Docker container
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json (or yarn.lock) files for the React app
COPY web/package*.json ./web/

# Install dependencies for the React app
RUN cd web && npm install

# Copy the React application files into the container
COPY web/ ./web/

# Python is already installed in the Buster images, install pip
RUN apt-get update && apt-get install -y python3-pip

# Copy the Flask application files and requirements into the container
COPY requirements.txt .
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the ports that your Flask and React apps run on
EXPOSE 3000 5000

# Run the development servers using the 'dev' script in package.json
CMD ["npm", "run", "dev", "--prefix", "web"]
