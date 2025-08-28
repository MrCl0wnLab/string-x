version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: strx-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-Str1ngX_r00t!}
      MYSQL_DATABASE: strx_db
      MYSQL_USER: strx_user
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-Str1ngX_p4ss!}
    ports:
      - "${MYSQL_PORT:-3306}:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init:/docker-entrypoint-initdb.d
    command:
      - --default-authentication-plugin=mysql_native_password
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --innodb_buffer_pool_size=${MYSQL_BUFFER_POOL_SIZE:-512M}
      - --max_connections=${MYSQL_MAX_CONNECTIONS:-100}
      - --innodb_log_file_size=256M
      - --innodb_flush_log_at_trx_commit=2
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10
    networks:
      - strx-net

  # Interface web opcional para administração do MySQL
  phpmyadmin:
    image: phpmyadmin/phpmyadmin:latest
    container_name: strx-phpmyadmin
    depends_on:
      mysql:
        condition: service_healthy
    ports:
      - "${PHPMYADMIN_PORT:-8080}:80"
    environment:
      PMA_HOST: mysql
      PMA_PORT: 3306
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:-Str1ngX_r00t!}
      PMA_ARBITRARY: 1
      UPLOAD_LIMIT: 256M
    networks:
      - strx-net

volumes:
  mysql-data:
    driver: local

networks:
  strx-net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
