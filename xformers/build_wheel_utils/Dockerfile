    FROM nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04

RUN apt-get update && apt-get -y install build-essential git \
    python3 python3-dev python3-pip

RUN pip3 install wheel ninja numpy && \
    pip install torch --extra-index-url https://download.pytorch.org/whl/cu116

# link cuda to make pkg-config --cflags cuda works
# RUN ln -s /usr/lib/pkgconfig/cuda-11.7.pc /usr/lib/pkgconfig/cuda.pc

RUN mkdir /workspace

# entrypoint script does switches u/g ID's and `chown`s everything
COPY compile.sh /bin/entrypoint.sh
CMD ["/bin/entrypoint.sh"]
