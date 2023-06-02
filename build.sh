VERSION='v1'
docker build --no-cache -t aws-exporter-app:${VERSION} .
sed -i "s/VERSION/${VERSION}/" docker-compose.yaml
