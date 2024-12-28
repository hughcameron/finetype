use burn::tensor::backend::AutodiffBackend;
use clap::{Arg, Command};
use classifier::data::FineTypeDataset;
use serde_json::Value;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[cfg(not(feature = "f16"))]
#[allow(dead_code)]
type ElemType = f32;
#[cfg(feature = "f16")]
type ElemType = burn::tensor::f16;

pub fn launch<B: AutodiffBackend>(device: B::Device, input: Option<String>, file: Option<String>) {
    let inputs: Vec<String> = if let Some(input) = input {
        vec![input]
    } else if let Some(file) = file {
        let file = File::open(file).expect("Unable to open file");
        let reader = BufReader::new(file);
        reader
            .lines()
            .map(|line| line.expect("Unable to read line"))
            .collect()
    } else {
        let stdin = io::stdin();
        let handle = stdin.lock();
        handle
            .lines()
            .map(|line| line.expect("Unable to read line"))
            .collect()
    };

    for input in inputs {
        if input.trim().is_empty() {
            continue;
        }

        let predictions: Vec<String> = if let Ok(json_value) = serde_json::from_str::<Value>(&input)
        {
            match json_value {
                Value::String(s) => vec![s],
                Value::Array(arr) => arr
                    .into_iter()
                    .filter_map(|v| v.as_str().map(|s| s.to_string()))
                    .collect(),
                _ => vec![],
            }
        } else {
            vec![input]
        };

        for prediction in predictions {
            let result = classifier::inference::infer_single::<B, FineTypeDataset>(
                device.clone(),
                "/tmp/classifier-finetype",
                prediction.trim().to_string(),
            );

            println!("{}", result);
        }
    }
}

#[cfg(any(
    feature = "ndarray",
    feature = "ndarray-blas-netlib",
    feature = "ndarray-blas-openblas",
    feature = "ndarray-blas-accelerate",
))]
mod ndarray {
    use burn::backend::{
        ndarray::{NdArray, NdArrayDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(input: Option<String>, file: Option<String>) {
        launch::<Autodiff<NdArray<f32>>>(NdArrayDevice::Cpu, input, file);
    }
}

#[cfg(feature = "tch-gpu")]
mod tch_gpu {
    use burn::backend::{
        libtorch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(input: Option<String>, file: Option<String>) {
        #[cfg(not(target_os = "macos"))]
        let device = LibTorchDevice::Cuda(0);
        #[cfg(target_os = "macos")]
        let device = LibTorchDevice::Mps;

        launch::<Autodiff<LibTorch<f32>>>(device, input, file);
    }
}

#[cfg(feature = "tch-cpu")]
mod tch_cpu {
    use burn::backend::{
        tch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(input: Option<String>, file: Option<String>) {
        launch::<Autodiff<LibTorch<f32>>>(LibTorchDevice::Cpu, input, file);
    }
}

#[cfg(feature = "wgpu")]
mod wgpu {
    use burn::backend::{
        wgpu::{Wgpu, WgpuDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(input: Option<String>, file: Option<String>) {
        launch::<Autodiff<Wgpu<f32, i32>>>(WgpuDevice::default(), input, file);
    }
}

fn main() {
    let matches = Command::new("FineType")
        .version("1.0")
        .author("Hugh Cameron (https://github.com/hughcameron)")
        .about("Classifies text")
        .arg(
            Arg::new("input")
                .short('i')
                .long("input")
                .value_name("INPUT")
                .help("Single JSON string or JSON array of strings")
                .value_parser(clap::value_parser!(String)),
        )
        .arg(
            Arg::new("file")
                .short('f')
                .long("file")
                .value_name("FILE")
                .help("File containing text input")
                .value_parser(clap::value_parser!(String)),
        )
        .get_matches();

    let input = matches.get_one::<String>("input").cloned();
    let file = matches.get_one::<String>("file").cloned();

    #[cfg(any(
        feature = "ndarray",
        feature = "ndarray-blas-netlib",
        feature = "ndarray-blas-openblas",
        feature = "ndarray-blas-accelerate",
    ))]
    ndarray::run(input, file);
    #[cfg(feature = "tch-gpu")]
    tch_gpu::run(input, file);
    #[cfg(feature = "tch-cpu")]
    tch_cpu::run(input, file);
    #[cfg(feature = "wgpu")]
    wgpu::run(input, file);
}
