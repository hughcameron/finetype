# Training the model:
cargo run --bin train --release --features wgpu

# Inference binary release:
cargo build --release --bin infer --features wgpu

# STDIN inference:
echo "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90" | ./classifier/target/release/infer

# Inference from input:
./target/release/infer -i "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90"
./target/release/infer -i '["bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90", "00:16:3e:1c:0c:8c"]'

# Inference from file:
echo '["bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90", "00:16:3e:1c:0c:8c"]' > data.json
./target/release/infer -f data.json
