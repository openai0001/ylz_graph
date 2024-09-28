FROM langchain/langgraph-api:3.11

RUN apt-get update
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
RUN pip install poetry
ADD ./pyproject.toml /deps/ylz_graph/
# 禁止poetry自动创建虚拟环境
RUN poetry config virtualenvs.create false
# 安装依赖包
RUN POETRY_HTTP_TIMEOUT=120 poetry install -C /deps/ylz_graph --no-root
ADD ./ylz_graph/config.yaml /root/.ylz_graph/

ADD . /deps/ylz_graph

#RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -c /api/constraints.txt -e /deps/*

#ENV LANGSERVE_GRAPHS='{"graph1": "/deps/ylz_graph/graph_cloud.py:graph1","graph2": "/deps/ylz_graph/graph_cloud.py:graph2","graph3": "/deps/ylz_graph/graph_cloud.py:graph3"}'
ENV LANGSERVE_GRAPHS='{"graph": "/deps/ylz_graph/graph_cloud.py:graphTest"}'

WORKDIR /deps/ylz_graph
