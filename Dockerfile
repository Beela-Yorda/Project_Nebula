# Use Node.js LTS image as base
FROM node:lts AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Use Nginx image as base for serving the static files
FROM nginx:alpine AS final

# Copy built React app from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx serverll
CMD ["nginx", "-g", "daemon off;"]
