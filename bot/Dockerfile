FROM python:3.8-slim

# pythonのuオプションと等しい
ENV PYTHONUNBUFFERED 1

# poetryのインストール
RUN python -m pip install -U pip
RUN pip install poetry
RUN poetry config virtualenvs.in-project true

# poetryパッケージのインストール
WORKDIR /code
COPY pyproject.toml /code/
COPY poetry.lock /code/
RUN poetry install --no-dev --no-root

COPY . /code/
CMD ["poetry", "run", "python", "main.py"]
