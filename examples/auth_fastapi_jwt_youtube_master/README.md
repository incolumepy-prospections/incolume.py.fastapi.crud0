# Autenticação no FastAPI com JWT

## Vídeos / commits
[**1. Introdução** [YouTube]](https://www.youtube.com/watch?v=l9pM5yYamPY&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=1)

---
[**2. Estrutura do Projeto** [YouTube]](https://www.youtube.com/watch?v=c1cwtNYsk1o&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=2)

--> [commit - 4f7ccca](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/4f7ccca04accfc607f6bc07357d1024e1aed4638)

----

[**3. Configurando Banco de Dados** [YouTube]](https://www.youtube.com/watch?v=J07qWfzSlUk&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=3)

--> [commit - baf5ce2](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/baf5ce255391524dad0790b192cbb2b215e2955c)

---

[**4. Migrations com Alembic** [YouTube]](https://www.youtube.com/watch?v=rDoaFASEpbY&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=4)

--> [commit - 565a7db](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/565a7db081b92ee0fe2e461175510093994ae962)

---

[**5. Cadastro de usuários** [YouTube]](https://www.youtube.com/watch?v=c1vTa6WIMTg&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=5)

--> [commit - 599a2ed](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/599a2eddc95d828d8f3bae7a55066fff3c1bb25c)

---

[**6. Login** [YouTube]](https://www.youtube.com/watch?v=-e8O1MAZZsQ&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=6)

--> [commit - 2166794](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/21667948670c6c519a0734d4073e1d200a823df9)

---

[**7. Validação de Token** [YouTube]](https://www.youtube.com/watch?v=0A5RtzoRQsA&list=PLyIsgi-C8ysKOAUEWI-Ehv37AiEKGtWj1&index=7)

--> [commit - 725bb48](https://github.com/diogoduartec/auth-fastapi-jwt-youtube/commit/725bb48ad26697d5ac355e362fd48b36bb3c31ad)


## Dependências
- Poetry
- Docker
- Docker compose

## Como rodar
1. Ative a virtual env
```bash
poetry shell
```

2. Instale as dependências
```bash
poetry install
```

3. Suba o banco de dados
```bash
docker-compose up postgresql -d
```

4. Rode as migrations
```bash
alembic upgrade head
```

5. Inicie a aplicação
```bash
uvicorn app.main:app --reload
```

