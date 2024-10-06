# FineType Classification

This project provides an example implementation for training and inferencing text classification
models on the FineType Label dataset using the Rust-based Burn Deep Learning Library.

# Usage

## Torch GPU backend

```bash
git clone https://github.com/tracel-ai/burn.git
cd burn

# Use the --release flag to really speed up training.
# Use the f16 feature if your CUDA device supports FP16 (half precision) operations. May not work well on every device.

export TORCH_CUDA_VERSION=cu121  # Set the cuda version (CUDA users)

cargo run --example finetype-train --release --features tch-gpu  # Train on the finetype dataset
cargo run --example finetype-infer --release --features tch-gpu  # Run inference finetype dataset
```

## Torch CPU backend

```bash
git clone https://github.com/tracel-ai/burn.git
cd burn

# Use the --release flag to really speed up training.

cargo run --example finetype-train --release --features tch-cpu  # Train on the finetype dataset
cargo run --example finetype-infer --release --features tch-cpu  # Run inference finetype dataset
```

## ndarray backend

```bash
git clone https://github.com/tracel-ai/burn.git
cd burn

# Use the --release flag to really speed up training.

# Replace ndarray by ndarray-blas-netlib, ndarray-blas-openblas or ndarray-blas-accelerate for different matmul techniques

cargo run --example finetype-train --release --features ndarray  # Train on the finetype dataset
cargo run --example finetype-infer --release --features ndarray  # Run inference finetype dataset
```

## WGPU backend

```bash
git clone https://github.com/tracel-ai/burn.git
cd burn

# Use the --release flag to really speed up training.

cargo run --example finetype-train --release --features wgpu  # Train on the finetype dataset
cargo run --example finetype-infer --release --features wgpu  # Run inference finetype dataset
```

## CUDA backend

```bash
git clone https://github.com/tracel-ai/burn.git
cd burn

# Use the --release flag to really speed up training.
```
