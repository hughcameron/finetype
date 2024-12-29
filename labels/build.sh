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
