FROM node:16-alpine3.14

COPY package.json yarn.lock /spa/

WORKDIR /spa

RUN yarn install --frozen-lockfile

COPY tsconfig.json webpack.config.ts /spa/

ENTRYPOINT ["yarn"]

CMD ["build"]
