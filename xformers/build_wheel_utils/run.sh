docker run -e FORCE_CUDA="1" \
       -e TORCH_CUDA_ARCH_LIST="6.0;6.1;6.2;7.0;7.2;8.0;8.6" \
       -v ~/tmp/xformers:/workspace/xformers xformer-compiler:latest \
       -it --rm
