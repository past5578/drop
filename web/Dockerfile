FROM node:lts-alpine

WORKDIR /app

COPY . .

RUN npm install

RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=4321

CMD ["node", "./dist/server/entry.mjs"]