# Step 1: Build stage
FROM node:24-slim AS build-stage

WORKDIR /workspace

# Copy dependency manifests and install packages
COPY package*.json ./
RUN npm ci

# Copy source code and compile project
COPY . .

# Declare build arguments for Vite compilation
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Step 2: Serve stage
FROM nginx:alpine

# Copy built static files to nginx serving folder
COPY --from=build-stage /workspace/dist /usr/share/nginx/html

# Copy custom nginx routing config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
