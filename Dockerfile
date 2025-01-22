# docker build . -t specimen-builder
# docker run --rm -v `pwd`/src:/app/src -v `pwd`/out:/out specimen-builder
FROM node:14

COPY package.json yarn.lock /app/
RUN cd /app \
    && yarn install --pure-lockfile

COPY . /app/
RUN find /app -exec chown node:node \{\} +
EXPOSE 3001
USER node
RUN patch -p2 /app/node_modules/fontkit/index.js < /app/fontkit.diff
CMD cp /app/node_modules/fontkit/index.js /out/index.js; cd /app && yarn fontdata && yarn build && cp -pr _site /out/
