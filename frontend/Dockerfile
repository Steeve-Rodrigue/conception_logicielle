# ---------- Builder ----------
FROM node:20-slim AS builder
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
RUN npm run build

# ---------- Runtime ----------
FROM nginx:alpine
COPY --from=builder /build/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]



