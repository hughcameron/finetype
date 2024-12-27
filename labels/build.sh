va eda

python generate_data.py --priority 5

python generate_data.py --texts 2 --output "learning_data/validation.ndjson"

huggingface-cli upload hughcameron/FineType_Labels_01 labels/learning_data/test.parquet --repo-type dataset
huggingface-cli upload hughcameron/FineType_Labels_01 labels/learning_data/train.parquet --repo-type dataset

duckdb < split_data.sql
