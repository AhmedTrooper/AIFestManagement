FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* .npmrc* ./
RUN npm install --omit=dev || true

FROM node:20-alpine AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build || true

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app .
EXPOSE 3000
CMD ["npm", "run", "start"]
