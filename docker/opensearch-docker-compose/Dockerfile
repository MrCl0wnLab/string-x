version: '3.8'

services:
  opensearch-node1:
    image: opensearchproject/opensearch:latest
    container_name: opensearch-node1
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node1
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=${OPENSEARCH_JAVA_OPTS:--Xms1g -Xmx1g}"
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_ADMIN_PASSWORD:-Str1ngX_p4ss!}
      - "DISABLE_INSTALL_DEMO_CONFIG=true"
      - "DISABLE_SECURITY_PLUGIN=${OPENSEARCH_DISABLE_SECURITY:-false}"
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data1:/usr/share/opensearch/data
    ports:
      - "${OPENSEARCH_PORT:-9200}:9200"
      - "${OPENSEARCH_PERF_PORT:-9600}:9600"
    healthcheck:
      test: ["CMD-SHELL", "curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD:-Str1ngX_p4ss!} https://localhost:9200"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - opensearch-net

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    container_name: opensearch-dashboards
    ports:
      - "${OPENSEARCH_DASHBOARD_PORT:-5601}:5601"
    environment:
      - OPENSEARCH_HOSTS=["https://opensearch-node1:9200"]
      - DISABLE_SECURITY_DASHBOARDS_PLUGIN=${OPENSEARCH_DISABLE_SECURITY:-false}
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:5601/api/status"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - opensearch-net
    depends_on:
      opensearch-node1:
        condition: service_healthy

volumes:
  opensearch-data1:
    driver: local

networks:
  opensearch-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/16
