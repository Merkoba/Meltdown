#!/usr/bin/env bash

root="$(dirname "$(readlink -f "$0")")"
parent="$(dirname "$root")"
cd "$parent"

# 1. Safety Check
if [ ! -f "/opt/rocm/llvm/bin/clang" ]; then
    echo "Error: ROCm LLVM compilers not found at /opt/rocm/llvm/bin/clang"
    echo "Arch Linux users: Please run 'sudo pacman -S rocm-llvm' first."
    exit 1
fi

# 2. Dynamic Multi-Architecture Detection
# Grabs all GPUs, removes duplicates, and formats them as "gfx1010;gfx1032"
TARGET_ARCH=$(/opt/rocm/llvm/bin/amdgpu-arch 2>/dev/null | sort -u | tr '\n' ';' | sed 's/;$//')

CMAKE_OPTS="-DGGML_HIPBLAS=ON -DGGML_HIP=ON -DCMAKE_C_COMPILER=/opt/rocm/llvm/bin/clang -DCMAKE_CXX_COMPILER=/opt/rocm/llvm/bin/clang++ -DCMAKE_PREFIX_PATH=/opt/rocm"

if [ -n "$TARGET_ARCH" ]; then
    echo "Detected AMD GPU architectures: $TARGET_ARCH"
    CMAKE_OPTS="$CMAKE_OPTS -DAMDGPU_TARGETS=$TARGET_ARCH"
else
    echo "Warning: Could not dynamically detect GPU architecture. Attempting generic ROCm build."
fi

echo "Compiling llama-cpp-python with ROCm support..."

# 3. Execution
env CMAKE_ARGS="$CMAKE_OPTS" FORCE_CMAKE=1 venv/bin/pip install -v --upgrade --force-reinstall --no-cache-dir --no-binary llama-cpp-python -r llama_reqs.txt