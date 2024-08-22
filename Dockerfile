FROM ghcr.io/ad-sdl/wei:v0.6.1

LABEL org.opencontainers.image.source=https://github.com/AD-SDL/a4s_sealer_module.git
LABEL org.opencontainers.image.description="Drivers and REST API's for the A4S Sealer"
LABEL org.opencontainers.image.licenses=MIT

#########################################
# Module specific logic goes below here #
#########################################

RUN mkdir -p a4s_sealer_module

COPY ./src a4s_sealer_module/src
COPY ./README.md a4s_sealer_module/README.md
COPY ./pyproject.toml a4s_sealer_module/pyproject.toml
COPY ./tests a4s_sealer_module/tests

RUN --mount=type=cache,target=/root/.cache \
    pip install -e ./a4s_sealer_module

CMD ["python", "a4s_sealer_module/scripts/a4s_sealer_rest_node.py"]

RUN usermod -aG dialout app
#########################################
