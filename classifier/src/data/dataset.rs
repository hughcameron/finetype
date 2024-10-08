// The FineTypeDataset struct is an examples of specific text
// classification datasets. The dataset struct has a field for the underlying
// SQLite dataset and implements methods for accessing and processing the data.
// The dataset is also provided with specific information about its classes via
// the TextClassificationDataset trait. These implementations are designed to be used
// with a machine learning framework for tasks such as training a text classification model.
use burn::data::dataset::{source::huggingface::HuggingfaceDatasetLoader, Dataset, SqliteDataset};
use derive_new::new;

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
    pub title: String,   // The title of the item
    pub content: String, // The content of the item
    pub label: usize,    // The label of the item (classification category)
}

/// Struct for the FineType dataset
pub struct FineTypeDataset {
    dataset: SqliteDataset<FineTypeItem>, // Underlying SQLite dataset
}

/// Implements the Dataset trait for the FineType dataset
impl Dataset<TextClassificationItem> for FineTypeDataset {
    /// Returns a specific item from the dataset
    fn get(&self, index: usize) -> Option<TextClassificationItem> {
        self.dataset.get(index).map(|item| {
            TextClassificationItem::new(
                format!("Title: {} - Content: {}", item.title, item.content),
                item.label,
            )
        })
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
        let dataset: SqliteDataset<FineTypeItem> = HuggingfaceDatasetLoader::new("FineType_01")
            .dataset(split)
            .unwrap();
        Self { dataset }
    }
}

/// Implement the TextClassificationDataset trait for the FineType dataset
impl TextClassificationDataset for FineTypeDataset {
    /// Returns the number of unique classes in the dataset
    fn num_classes() -> usize {
        14
    }

    /// Returns the name of a class given its label
    fn class_name(label: usize) -> String {
        match label {
            0 => "Company",
            1 => "EducationalInstitution",
            2 => "Artist",
            3 => "Athlete",
            4 => "OfficeHolder",
            5 => "MeanOfTransportation",
            6 => "Building",
            7 => "NaturalPlace",
            8 => "Village",
            9 => "Animal",
            10 => "Plant",
            11 => "Album",
            12 => "Film",
            13 => "WrittenWork",
            _ => panic!("invalid class"),
        }
        .to_string()
    }
}
