FROM node:26.13.0-slim AS build

WORKDIR /app

RUN npm install --global corepack && corepack enable

COPY package.json yarn.lock .yarnrc.yml ./
COPY .yarn/ ./.yarn/
RUN yarn install --immutable

COPY . .
RUN yarn build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080
