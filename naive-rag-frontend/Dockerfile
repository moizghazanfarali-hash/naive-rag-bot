# Base image
FROM node:20-slim AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy frontend code and build
COPY . .
RUN npm run build

# Production server to serve static files
FROM node:20-slim

WORKDIR /app
RUN npm install -g serve

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

EXPOSE 5173

# Serve the build files on port 5173
CMD ["serve", "-s", "dist", "-l", "5173"]