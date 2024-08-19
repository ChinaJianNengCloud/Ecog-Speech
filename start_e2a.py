import subprocess


def main():
    # 定义命令行参数
    command = [
        "python", "train_e2a.py",
        "--OUTPUT_DIR", "output/e2a/resnet_HB02",
        "--trainsubject", "HB02",
        "--testsubject", "HB02",
        "--param_file", "configs/e2a_production.yaml",
        "--batch_size", "16",
        "--MAPPING_FROM_ECOG", "ECoGMapping_ResNet",
        "--reshape", "1",
        "--DENSITY", "HB",
        "--wavebased", "1",
        "--dynamicfiltershape", "0",
        "--n_filter_samples", "80",
        "--n_fft", "256",
        "--formant_supervision", "1",
        "--intensity_thres", "-1",
        "--epoch_num", "60",
        "--pretrained_model_dir", "output/a2a/HB02",
        "--causal", "0"
    ]

    # 运行命令
    subprocess.run(command)


if __name__ == "__main__":
    main()
