# Load python environment:
va eda

# Generate training data:
python generate_data.py --priority 5

# Generate validation data:
python generate_data.py --texts 2 --output "learning_data/validation.ndjson"

# Split and release the data:
duckdb < split_data.sql

# Upload the data:
huggingface-cli upload hughcameron/FineType_Labels_01 labels/learning_data/test.parquet --repo-type dataset
huggingface-cli upload hughcameron/FineType_Labels_01 labels/learning_data/train.parquet --repo-type dataset

# Training the model:
cargo run --bin train --release --features wgpu

# Inference binary release:
cargo build --release --bin infer --features wgpu

# STDIN inference:
echo "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90" | ./classifier/target/release/infer

# Inference from input:
./classifier/target/release/infer -i "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90"
./classifier/target/release/infer -i '["bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90", "00:16:3e:1c:0c:8c"]'

# Inference from file:
echo '["bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90", "00:16:3e:1c:0c:8c"]' > data.json
./classifier/target/release/infer -f data.json
