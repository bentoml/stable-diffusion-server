# Build xformers wheels using docker

First clone and checkout the repository (assuming in `~/tmp`):

```bash
cd ~/tmp/
git clone https://github.com/facebookresearch/xformers.git
git checkout v0.0.13
git submodule update --init --recursive
```

Then go back to this directory, build the docker image and compile a wheel.
You can edit `TORCH_CUDA_ARCH_LIST` in `run.sh` to the card you want to support.

```
cd path_of_this_directory
./build.sh && ./run.sh
```

After some heavy compiling works, there will be a wheel at `~/tmp/xformers/dist/xformers-0.0.14.dev0-cp38-cp38-linux_x86_64.whl`.
You can just copy this file to `../wheels/`

