# FineType

FineType is a project aimed at building a comprehensive taxonomy of variable characters (varchars) and profiling unseen data beyond primitive types. The primary goals of FineType include data profiling, modelling, and validation, as well as data generation for testing and training purposes.

## Installation

FineType can be installed as a binary. The installation process is straightforward and ensures that all necessary dependencies are included.

## Usage

FineType can be used via a command line interface (CLI). The CLI provides various flags to customise the behaviour of the tool according to the user's needs. Below is an explanation of the command line flags available in `infer.rs`.

### Command Line Flags

- `--input` or `-i`: This flag allows the user to provide a single JSON string or a JSON array of strings as input. The input is processed by the classifier to generate predictions.

- `--file` or `-f`: This flag specifies a file containing text input. The file is read, and each line is processed as a separate input for classification.

- `--value` or `-v`: When this flag is set, the input value is included in the output. This is useful for tracing back the predictions to their corresponding inputs.

- `--logit` or `-l`: This flag includes the logit value of the prediction in the output. The logit value provides additional information about the confidence of the prediction.

### Example Usage

To classify a single input string:
```sh
./classifier/target/release/infer -i "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90"
```

To classify multiple input strings from a file:
```sh
./classifier/target/release/infer -f data.json
```

To include the input value and logit in the output:
```sh
./classifier/target/release/infer -i "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90" -v -l
```

## Development Dependencies

FineType relies on several development dependencies to ensure robust functionality and performance. The primary dependencies include:

- Rust: The core language used for developing FineType, providing performance and safety.
- Burn: A deep learning framework in Rust, used for model training and inference.
- Python: Utilised for data generation and preprocessing tasks.
- Mimesis: A Python library for generating synthetic data, aiding in the creation of training and validation datasets.

## FineType Goals

The overarching goals of FineType are to build a detailed taxonomy of varchars and to profile unseen data beyond primitive types. This enables more accurate data profiling, modelling, and validation, as well as the generation of high-quality data for testing and training purposes.

## FineType Use Cases

FineType is designed to be versatile and applicable in various scenarios, including:

- Data profiling: Analysing and categorising data to understand its structure and content.
- Data modelling: Creating models that accurately represent the data for various applications.
- Data validation: Ensuring that data conforms to expected formats and standards.
- Data generation: Producing synthetic data for testing and training machine learning models.

By leveraging FineType, users can gain deeper insights into their data and improve the quality and reliability of their data-driven applications.
