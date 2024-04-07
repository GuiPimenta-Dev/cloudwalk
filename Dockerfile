# Use the official Node.js image as base
FROM node:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY node/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY node/ ./

# Expose the port the app runs on
EXPOSE 3000

# Start the server
CMD ["node", "app.js"]
