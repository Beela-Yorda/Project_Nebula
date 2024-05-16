# Use Node.js LTS image as base
FROM node:lts AS build

# Set the working directory in the Docker image
WORKDIR /app

# Copy the package.json file from the frontend directory to the Docker image
COPY ./frontend/package.json /app/packages/package.json

# Install dependencies using npm
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Nginx stage to serve the static files
FROM nginx:alpine AS final

# Copy built React app from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]



# Set the working directory in the Docker image
WORKDIR /app

# Copy the package.json file from the frontend directory to the Docker image
COPY ./frontend/packages/package.json /app/packages/package.json

# Install dependencies using npm
RUN npm install
