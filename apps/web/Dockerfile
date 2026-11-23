FROM node:20-alpine AS deps
WORKDIR /srv
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund || npm install --no-audit --no-fund --no-package-lock

FROM node:20-alpine AS builder
WORKDIR /srv
COPY --from=deps /srv/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /srv
ENV NODE_ENV=production
COPY --from=builder /srv/.next/standalone ./
COPY --from=builder /srv/.next/static ./.next/static
COPY --from=builder /srv/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
