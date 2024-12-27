// The FineTypeDataset struct is an examples of specific text
// classification datasets. The dataset struct has a field for the underlying
// SQLite dataset and implements methods for accessing and processing the data.
// The dataset is also provided with specific information about its classes via
// the TextClassificationDataset trait. These implementations are designed to be used
// with a machine learning framework for tasks such as training a text classification model.
use burn::data::dataset::{source::huggingface::HuggingfaceDatasetLoader, Dataset, SqliteDataset};
use derive_new::new;
use rusqlite::Connection;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

// Define a struct for text classification items
#[derive(new, Clone, Debug)]
pub struct TextClassificationItem {
    pub text: String, // The text for classification
    pub label: usize, // The label of the text (classification category)
}

// Trait for text classification datasets
pub trait TextClassificationDataset: Dataset<TextClassificationItem> {
    fn num_classes() -> usize; // Returns the number of unique classes in the dataset
    fn class_name(label: usize) -> String; // Returns the name of the class given its label
}

/// Struct for items in the FineType dataset
#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct FineTypeItem {
    pub class: String, // The class of the item
    pub text: String,  // The text of the item
    pub label: usize,  // The label of the item (classification category)
}

/// Struct for the FineType dataset
pub struct FineTypeDataset {
    dataset: SqliteDataset<FineTypeItem>, // Underlying SQLite dataset
    labels: Arc<RwLock<HashMap<usize, String>>>, // Cache for labels
}

/// Implements the Dataset trait for the FineType dataset
impl Dataset<TextClassificationItem> for FineTypeDataset {
    /// Returns a specific item from the dataset
    fn get(&self, index: usize) -> Option<TextClassificationItem> {
        self.dataset
            .get(index)
            .map(|item| TextClassificationItem::new(item.text, item.label))
    }

    /// Returns the length of the dataset
    fn len(&self) -> usize {
        self.dataset.len()
    }
}

/// Implement methods for constructing the FineType dataset
impl FineTypeDataset {
    /// Returns the training portion of the dataset
    pub fn train() -> Self {
        Self::new("train")
    }

    /// Returns the testing portion of the dataset
    pub fn test() -> Self {
        Self::new("test")
    }

    /// Constructs the dataset from a split (either "train" or "test")
    pub fn new(split: &str) -> Self {
        let dataset: SqliteDataset<FineTypeItem> =
            HuggingfaceDatasetLoader::new("hughcameron/finetype_01")
                .dataset(split)
                .unwrap();
        let labels = Self::fetch_labels(&dataset);
        Self {
            dataset,
            labels: Arc::new(RwLock::new(labels)),
        }
    }

    /// Fetches the labels from the SQLite table and returns a HashMap
    fn fetch_labels(dataset: &SqliteDataset<FineTypeItem>) -> HashMap<usize, String> {
        let conn = Connection::open(dataset.db_file()).unwrap();
        let mut stmt = conn.prepare("SELECT label, class FROM labels").unwrap();
        let mut rows = stmt.query([]).unwrap();

        let mut labels = HashMap::new();
        while let Some(row) = rows.next().unwrap() {
            let label: usize = row.get(0).unwrap();
            let class: String = row.get(1).unwrap();
            labels.insert(label, class);
        }
        labels
    }

    /// Returns the number of unique classes in the dataset
    pub fn num_classes(&self) -> usize {
        self.labels.read().unwrap().len()
    }

    /// Returns the name of a class given its label
    pub fn class_name(&self, label: usize) -> String {
        self.labels
            .read()
            .unwrap()
            .get(&label)
            .cloned()
            .unwrap_or_else(|| "invalid class".to_string())
    }
}

/// Implement the TextClassificationDataset trait for the FineType dataset
impl TextClassificationDataset for FineTypeDataset {
    /// Returns the number of unique classes in the dataset
    fn num_classes() -> usize {
        FineTypeDataset::train().num_classes()
    }

    /// Returns the name of a class given its label
    fn class_name(label: usize) -> String {
        FineTypeDataset::train().class_name(label)
    }
}
