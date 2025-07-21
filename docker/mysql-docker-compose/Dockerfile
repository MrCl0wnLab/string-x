version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: strx-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: Str1ngX_r00t!
      MYSQL_DATABASE: strx_db
      MYSQL_USER: strx_user
      MYSQL_PASSWORD: Str1ngX_p4ss!
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
      - ./init:/docker-entrypoint-initdb.d
    command:
      - --default-authentication-plugin=mysql_native_password
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --innodb_buffer_pool_size=512M
    networks:
      - strx-net

  # Interface web opcional para administração do MySQL
  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: strx-phpmyadmin
    depends_on:
      - mysql
    ports:
      - "8080:80"
    environment:
      PMA_HOST: mysql
      PMA_PORT: 3306
      MYSQL_ROOT_PASSWORD: Str1ngX_r00t!
    networks:
      - strx-net

volumes:
  mysql-data:

networks:
  strx-net:
    driver: bridge
