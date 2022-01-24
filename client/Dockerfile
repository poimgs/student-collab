FROM node:16-alpine3.14 AS builder
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm install
COPY ./ /app/
RUN npm run build

FROM nginx:1.20.2-alpine
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/build /usr/share/nginx/html