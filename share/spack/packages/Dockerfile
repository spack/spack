FROM ubuntu:18.04 AS build-env
WORKDIR /build
RUN apt-get update && apt-get install -y jq
COPY packages.json ./
COPY split.sh ./
RUN /build/split.sh

FROM nginx:mainline-alpine
COPY --from=build-env --chown=nginx:nginx /build/packages /build/packages.json /usr/share/nginx/html/api/

CMD ["nginx", "-g", "daemon off;"]
