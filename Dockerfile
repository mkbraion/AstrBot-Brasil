FROM node:24-slim AS dashboard-build
WORKDIR /dashboard
RUN npm install --global pnpm@10.32.1
COPY dashboard/package.json dashboard/pnpm-lock.yaml dashboard/pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY dashboard/ ./
COPY astrbot/core/utils/t2i/template/shiki_runtime.iife.js /astrbot/core/utils/t2i/template/shiki_runtime.iife.js
RUN pnpm run i18n:check && pnpm run i18n:check:ptbr && pnpm run build

FROM python:3.12-slim
WORKDIR /AstrBot

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    libssl-dev \
    ca-certificates \
    bash \
    ffmpeg \
    libavcodec-extra \
    fonts-noto-cjk \
    curl \
    gnupg \
    git \
    ripgrep \
    && curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /AstrBot/
COPY --from=dashboard-build /dashboard/dist /AstrBot/astrbot/dashboard/dist
RUN python -c "from pathlib import Path; from astrbot import __version__; Path('astrbot/dashboard/dist/assets/version').write_text('v' + __version__, encoding='utf-8')"

RUN python -m pip install uv \
    && echo "3.12" > .python-version \
    && uv lock \
    && uv export --format requirements.txt --output-file requirements.txt --frozen \
    && uv pip install -r requirements.txt --no-cache-dir --system \
    && uv pip install socksio uv pilk --no-cache-dir --system \
    && uv pip install -e . --no-deps --system \
    && touch /AstrBot/.astrbot

EXPOSE 6185

CMD ["python", "main.py", "--webui-dir", "/AstrBot/astrbot/dashboard/dist"]
