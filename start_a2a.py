import subprocess

# 构建命令
command = [
    "python", "train_a2a.py",
    "--OUTPUT_DIR", "output/a2a/HB02",
    "--trainsubject", "HB02",
    "--testsubject", "HB02",
    "--param_file", "configs/a2a_production.yaml",
    "--batch_size", "4",
    "--reshape", "1",
    "--DENSITY", "HB",
    "--wavebased", "1",
    "--n_filter_samples", "80",
    "--n_fft", "256",
    "--formant_supervision", "1",
    "--intensity_thres", "-1",
    "--epoch_num", "60"
]

# 运行命令
subprocess.run(command)
