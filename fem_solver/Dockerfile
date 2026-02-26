
FROM dealii/dealii:v9.5.1-jammy

USER root
WORKDIR /app


RUN apt-get update && apt-get install -y \
    cmake \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/src /app/build /app/data

CMD ["/bin/bash"]