use classifier::data::FineTypeDataset;

use burn::tensor::backend::AutodiffBackend;

#[cfg(not(feature = "f16"))]
#[allow(dead_code)]
type ElemType = f32;
#[cfg(feature = "f16")]
type ElemType = burn::tensor::f16;

pub fn launch<B: AutodiffBackend>(device: B::Device) {
    classifier::inference::infer::<B, FineTypeDataset>(
        device,
        "/tmp/classifier-finetype",
        // Samples from the test dataset, but you are free to test with your own text.
        vec![
            "9f143a4f-1be7-4d88-b9c4-0098edf36e82".to_string(),
            "bf23468d-efab-42a4-b0a3-be9161709ad7".to_string(),
            "1706048114".to_string(),
            "1732431937".to_string(),
            "America/Argentina/Catamarca".to_string(),
            "Asia/Jakarta".to_string(),
            "AS2746317214".to_string(),
            "AS478163328".to_string(),
            "163.177.121.157".to_string(),
            "70.104.82.87".to_string(),
            "163.177.121.157:1640".to_string(),
            "189.214.64.251:16050".to_string(),
            "bdd6:40fb:667:1ad1:1c80:317f:a3b1:799d".to_string(),
            "bc89:60a9:23b8:c1e9:3924:56de:3eb1:3b90".to_string(),
            "00:16:3e:1c:0c:8c".to_string(),
            "00:16:3e:3e:72:47".to_string(),
            "8.8.8.8".to_string(),
            "1.1.1.1".to_string(),
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2".to_string(),
            "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36".to_string(),
            "1brnTP3fAbnFbmOHnKYaXRvj7uff0LYTH8".to_string(),
            "3esM2wleOV911xCZkwPRQeNHpCq5QnuVdY".to_string(),
            "3404 332181 96006".to_string(),
            "4223 3890 8386 3795".to_string(),
            "0x46685257bdd640fb06671ad11c80317fa3b1799d".to_string(),
            "0x1a3d1fa7bc8960a923b8c1e9392456de3eb13b90".to_string(),
            "GTCTGGATCT".to_string(),
            "TGTTGGTGAT".to_string(),
            "GUCUGGAUCU".to_string(),
            "UGUUGGUGAU".to_string(),
            "#390062".to_string(),
            "#0cce35".to_string()
        ],
    );
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

    use crate::{launch, ElemType};

    pub fn run() {
        launch::<Autodiff<NdArray<ElemType>>>(NdArrayDevice::Cpu);
    }
}

#[cfg(feature = "tch-gpu")]
mod tch_gpu {
    use burn::backend::{
        libtorch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::{launch, ElemType};

    pub fn run() {
        #[cfg(not(target_os = "macos"))]
        let device = LibTorchDevice::Cuda(0);
        #[cfg(target_os = "macos")]
        let device = LibTorchDevice::Mps;

        launch::<Autodiff<LibTorch<ElemType>>>(device);
    }
}

#[cfg(feature = "tch-cpu")]
mod tch_cpu {
    use burn::backend::{
        tch::{LibTorch, LibTorchDevice},
        Autodiff,
    };

    use crate::{launch, ElemType};

    pub fn run() {
        launch::<Autodiff<LibTorch<ElemType>>>(LibTorchDevice::Cpu);
    }
}

#[cfg(feature = "wgpu")]
mod wgpu {
    use burn::backend::{
        wgpu::{Wgpu, WgpuDevice},
        Autodiff,
    };

    use crate::{launch, ElemType};

    pub fn run() {
        launch::<Autodiff<Wgpu<ElemType, i32>>>(WgpuDevice::default());
    }
}

fn main() {
    #[cfg(any(
        feature = "ndarray",
        feature = "ndarray-blas-netlib",
        feature = "ndarray-blas-openblas",
        feature = "ndarray-blas-accelerate",
    ))]
    ndarray::run();
    #[cfg(feature = "tch-gpu")]
    tch_gpu::run();
    #[cfg(feature = "tch-cpu")]
    tch_cpu::run();
    #[cfg(feature = "wgpu")]
    wgpu::run();
}
