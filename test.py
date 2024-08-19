import torch
import torchaudio
import numpy as np

def compute_spectrogram(wave, n_fft, power, device):
    try:
        # 创建Spectrogram对象并将其移动到相同的设备
        spectrogram_transform = torchaudio.transforms.Spectrogram(
            n_fft=n_fft * 2 - 1,
            win_length=n_fft * 2 - 1,
            hop_length=int(wave_fr / spec_fr),
            power=power
        ).to(device)  # 将Spectrogram对象移动到GPU

        # 计算频谱
        spectrogram = spectrogram_transform(wave)
        return spectrogram
    except Exception as e:
        print(f"Error: {e}")
        return None

# 读取.npy文件
input_path = r"F:\sjwlab\chenyinda\eegandsound\neural_speech_decoding\example_data\wave.npy"  # 替换为你的.np文件路径
wave_data = np.load(input_path)
device = "cuda" if torch.cuda.is_available() else "cpu"

# 将numpy数组转换为torch张量并移动到设备
wave_tensor = torch.tensor(wave_data).to(device)

# 测试参数
n_fft = 256
wave_fr = 16000
spec_fr = 125
power = 2

# 计算频谱
spectrogram = compute_spectrogram(wave_tensor, n_fft, power, device)
print(spectrogram)
