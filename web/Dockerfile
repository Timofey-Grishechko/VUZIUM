# === Стадия 1: сборка ===
FROM node:20-alpine AS builder

WORKDIR /app

# Копируем только манифесты — кэш node_modules сохранится между сборками
COPY package.json package-lock.json ./
RUN npm ci

# Копируем исходники и собираем
COPY . .
RUN npm run build

# === Стадия 2: рантайм ===
FROM nginx:1.27-alpine

# Копируем собранную статику
COPY --from=builder /app/dist /usr/share/nginx/html

# Конфиг nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
