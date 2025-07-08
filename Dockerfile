#https://hub.docker.com/layers/library/python/3-alpine3.21/images/sha256-4ca5d46491194916d97e5d13b01ed571391f735814595e2c83b44091043b1631
FROM python:3-alpine3.21

# Adicionar metadados como labels
LABEL maintainer="MrCl0wn <mrcl0wnlab[@]gmail.com>"
LABEL version="0.1.0"
LABEL description="Ferramenta de Automatização e Manipulação de Strings"
LABEL org.opencontainers.image.source="https://github.com/MrCl0wnLab/string-x"

# Copiar arquivos para /app
COPY . /app

# Va até o diretorio /app
WORKDIR /app

# Clonar o repositório diretamente do GitHub
RUN git clone https://github.com/MrCl0wnLab/string-x.git . && \
    rm -rf .git

# Instalar requirements.txt
RUN pip install -r requirements.txt

# Criar link simbólico dentro do container para acesso global ao comando
RUN chmod +x /app/strx && \
    ln -sf /app/strx /usr/local/bin/strx

# Inicie o strx
ENTRYPOINT ["python3", "strx"]

# Caso não passe argumentos use o -exemples
CMD ["-examples"]

# Nota: Para criar um link simbólico no sistema host (fora do Docker), use:
# 
# # Verificar o link atual
# ls -la /usr/local/bin/strx
# 
# # Se necessário, recriar o link
# sudo rm /usr/local/bin/strx
# sudo ln -sf $HOME/Documentos/string-x/strx /usr/local/bin/strx