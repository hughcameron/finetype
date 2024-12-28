use burn::tensor::backend::AutodiffBackend;
use clap::{Arg, ArgAction, Command};
use classifier::data::FineTypeDataset;
use serde_json::{json, Map, Value};
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[cfg(not(feature = "f16"))]
#[allow(dead_code)]
type ElemType = f32;
#[cfg(feature = "f16")]
type ElemType = burn::tensor::f16;

pub fn launch<B: AutodiffBackend<FloatElem = f32>>(
    device: B::Device,
    input: Option<String>,
    file: Option<String>,
    return_value: bool,
    return_logit: bool,
) {
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
            let (class_name, logit) = classifier::inference::infer_single::<B, FineTypeDataset>(
                device.clone(),
                "/tmp/classifier-finetype",
                prediction.trim().to_string(),
            );

            let mut result = Map::new();
            result.insert("class".to_string(), json!(class_name));

            if return_value {
                result.insert("input".to_string(), json!(prediction.trim()));
            }

            if return_logit {
                result.insert("logit".to_string(), json!(logit));
            }

            println!("{}", Value::Object(result));
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

    pub fn run(
        input: Option<String>,
        file: Option<String>,
        return_value: bool,
        return_logit: bool,
    ) {
        launch::<Autodiff<NdArray<f32>>>(
            NdArrayDevice::Cpu,
            input,
            file,
            return_value,
            return_logit,
        );
    }
}

#[cfg(feature = "tch-gpu")]
mod tch_gpu {
    use burn::backend::{
        libtorch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(
        input: Option<String>,
        file: Option<String>,
        return_value: bool,
        return_logit: bool,
    ) {
        #[cfg(not(target_os = "macos"))]
        let device = LibTorchDevice::Cuda(0);
        #[cfg(target_os = "macos")]
        let device = LibTorchDevice::Mps;

        launch::<Autodiff<LibTorch<f32>>>(device, input, file, return_value, return_logit);
    }
}

#[cfg(feature = "tch-cpu")]
mod tch_cpu {
    use burn::backend::{
        tch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(
        input: Option<String>,
        file: Option<String>,
        return_value: bool,
        return_logit: bool,
    ) {
        launch::<Autodiff<LibTorch<f32>>>(
            LibTorchDevice::Cpu,
            input,
            file,
            return_value,
            return_logit,
        );
    }
}

#[cfg(feature = "wgpu")]
mod wgpu {
    use burn::backend::{
        wgpu::{Wgpu, WgpuDevice},
        Autodiff,
    };

    use crate::launch;

    pub fn run(
        input: Option<String>,
        file: Option<String>,
        return_value: bool,
        return_logit: bool,
    ) {
        launch::<Autodiff<Wgpu<f32, i32>>>(
            WgpuDevice::default(),
            input,
            file,
            return_value,
            return_logit,
        );
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
                .value_parser(clap::value_parser!(String))
                .help("Single JSON string or JSON array of strings"),
        )
        .arg(
            Arg::new("file")
                .short('f')
                .long("file")
                .value_name("FILE")
                .value_parser(clap::value_parser!(String))
                .help("File containing text input"),
        )
        .arg(
            Arg::new("value")
                .short('v')
                .long("value")
                .action(ArgAction::SetTrue)
                .help("Return the input value in the output"),
        )
        .arg(
            Arg::new("logit")
                .short('l')
                .long("logit")
                .action(ArgAction::SetTrue)
                .help("Return the logit value of the prediction in the output"),
        )
        .get_matches();

    let input = matches.get_one::<String>("input").cloned();
    let file = matches.get_one::<String>("file").cloned();
    let return_value = matches.get_one::<bool>("value").unwrap_or(&false);
    let return_logit = matches.get_one::<bool>("logit").unwrap_or(&false);

    #[cfg(any(
        feature = "ndarray",
        feature = "ndarray-blas-netlib",
        feature = "ndarray-blas-openblas",
        feature = "ndarray-blas-accelerate",
    ))]
    ndarray::run(input, file, *return_value, *return_logit);
    #[cfg(feature = "tch-gpu")]
    tch_gpu::run(input, file, *return_value, *return_logit);
    #[cfg(feature = "tch-cpu")]
    tch_cpu::run(input, file, *return_value, *return_logit);
    #[cfg(feature = "wgpu")]
    wgpu::run(input, file, *return_value, *return_logit);
}
