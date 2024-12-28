// This module defines the inference process for a text classification model.
// It loads a model and its configuration from a directory, and uses a tokenizer
// and a batcher to prepare the input data. The model is then used to make predictions
// on the input samples, and the results are printed out for each sample.
// Import required modules and types

use crate::{
    data::{BertCasedTokenizer, TextClassificationBatcher, TextClassificationDataset, Tokenizer},
    model::TextClassificationModelConfig,
    training::ExperimentConfig,
};
use burn::{
    data::dataloader::batcher::Batcher,
    prelude::*,
    record::{CompactRecorder, Recorder},
};
use std::sync::Arc;

pub fn infer_single<B: Backend, D: TextClassificationDataset + 'static>(
    device: B::Device,
    artifact_dir: &str,
    sample: String,
) -> String {
    // Load experiment configuration
    let config = ExperimentConfig::load(format!("{artifact_dir}/config.json").as_str())
        .expect("Config file present");

    // Initialize tokenizer
    let tokenizer = Arc::new(BertCasedTokenizer::default());

    // Get number of classes from dataset
    let n_classes = D::num_classes();

    // Initialize batcher for batching samples
    let batcher = Arc::new(TextClassificationBatcher::<B>::new(
        tokenizer.clone(),
        device.clone(),
        config.max_seq_length,
    ));

    // Load pre-trained model weights
    let record = CompactRecorder::new()
        .load(format!("{artifact_dir}/model").into(), &device)
        .expect("Trained model weights");

    // Create model using loaded weights
    let model = TextClassificationModelConfig::new(
        config.transformer,
        n_classes,
        tokenizer.vocab_size(),
        config.max_seq_length,
    )
    .init(&device)
    .load_record(record);

    // Run inference on the given text sample
    let item = batcher.batch(vec![sample.clone()]); // Batch the single sample
    let predictions = model.infer(item);

    let prediction = predictions.slice([0..1]); // Get prediction for the sample
    let class_index = prediction.argmax(1).squeeze::<1>(1).into_scalar(); // Get class index
    D::class_name(class_index.elem::<i32>() as usize) // Return the class name
}
