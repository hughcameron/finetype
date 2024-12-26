// The FineTypeDataset struct is an examples of specific text
// classification datasets. The dataset struct has a field for the underlying
// SQLite dataset and implements methods for accessing and processing the data.
// The dataset is also provided with specific information about its classes via
// the TextClassificationDataset trait. These implementations are designed to be used
// with a machine learning framework for tasks such as training a text classification model.
use burn::data::dataset::{source::huggingface::HuggingfaceDatasetLoader, Dataset, SqliteDataset};
use derive_new::new;
use std::collections::HashMap;

// Define a struct for text classification items
#[derive(new, Clone, Debug)]
pub struct TextClassificationItem {
    pub text: String, // The text for classification
    pub label: usize, // The label of the text (classification category)
}

// Trait for text classification datasets
pub trait TextClassificationDataset: Dataset<TextClassificationItem> {
    fn num_classes(&self) -> usize;
    fn class_name(&self, label: usize) -> String;
}

/// Struct for items in the FineType dataset
#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct FineTypeItem {
    pub class: String,
    pub text: String,
    pub label: usize,
}

/// Struct for the FineType dataset
pub struct FineTypeDataset {
    dataset: SqliteDataset<FineTypeItem>,
    labels: HashMap<usize, String>,
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
        let labels = Self::load_labels(&dataset.db_file()).unwrap_or_default();
        Self { dataset, labels }
    }

    fn load_labels(
        db_path: &std::path::PathBuf,
    ) -> Result<HashMap<usize, String>, rusqlite::Error> {
        let conn = rusqlite::Connection::open(db_path)?;
        let mut stmt = conn.prepare("SELECT label, class FROM labels")?;

        let label_iter = stmt.query_map([], |row| {
            let label: usize = row.get(0)?;
            let class: String = row.get(1)?;
            Ok((label, class))
        })?;

        let mut labels = HashMap::new();
        for label in label_iter {
            let (key, value) = label?;
            labels.insert(key, value);
        }

        Ok(labels)
    }
}

/// Implement the TextClassificationDataset trait for the FineType dataset
impl TextClassificationDataset for FineTypeDataset {
    fn num_classes(&self) -> usize {
        self.labels.len()
    }

    fn class_name(&self, label: usize) -> String {
        self.labels
            .get(&label)
            .cloned()
            .unwrap_or_else(|| "Unknown class".to_string())
    }
}
