# Neural Speech Decoding

By Xupeng Chen, Ran Wang, Amirhossein Khalilian-Gourtani, Leyao Yu, Patricia Dugan, Daniel Friedman, Werner Doyle, Orrin Devinsky, Yao Wang, Adeen Flinker

## Our Paper is Online!
[Paper Published in Nature Machine Intelligence](https://www.nature.com/articles/s42256-024-00824-8)

[![DOI - 10.1038/s42256-024-00824-8](https://img.shields.io/badge/DOI-10.1038%2Fs42256--024--00824--8-blue)](https://www.nature.com/articles/s42256-024-00824-8)


## Software (this repo)
[![Software DOI](https://zenodo.org/badge/762555618.svg)](https://zenodo.org/doi/10.5281/zenodo.10719427)

## DEMO

Check our [Demo Page](https://xc1490.github.io/nsd/)

## Introduction
Our ECoG to Speech decoding framework is initially described in [A Neural Speech Decoding Framework Leveraging Deep Learning and Speech Synthesis](https://www.biorxiv.org/content/10.1101/2023.09.16.558028v1). We present a novel deep learning-based neural speech decoding framework that includes an ECoG Decoder that translates electrocorticographic (ECoG) signals from the cortex into interpretable speech parameters and a novel differentiable Speech Synthesizer that maps speech parameters to spectrograms. We develop a companion audio-to-audio auto-encoder consisting of a Speech Encoder and the same Speech Synthesizer to generate reference speech parameters to facilitate the training of the ECoG Decoder. This framework generates natural-sounding speech and is highly reproducible across a large cohort of participants (N = 48). We provide two-stage training **pipeline** with visualization tools.

<div align="center">
    <img src="fig/fig1.png" />
</div>

## Getting Started

### Installation

- Install `CUDA 11.0` with `cuDNN 8` following the official installation guide of [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) and [cuDNN](https://developer.nvidia.com/rdp/cudnn-archive).

- Setup conda environment:
```bash
conda create -n Neural_Speech python=3.7 -y
conda activate Neural_Speech

# Install requirements
conda install pytorch torchvision torchaudio cudatoolkit=11 -c pytorch -y

# Clone NSD
git clone https://github.com/flinkerlab/neural_speech_decoding
cd neural_speech_decoding

# Install other requirements
pip install -r requirements.txt
```

## Data

Prepare the data in HDF5 format, refer to the [prepare_data](notebooks/prepare_data.ipynb)

Optionally, if you want to provide extra supervision for pitch and formant, please refer to the [formant_pitch_label_extraction](notebooks/formant_pitch_label_extraction.ipynb)

Example Data is available [HERE](example_data/README.md), you could download and put it in the `example_data` folder.

## Training
Fill in the config files including `configs/a2a_production.yaml,configs/e2a_production.yaml,configs/AllSubjectInfo.json,configs/train_param_production.json` following the example of participants `HB02`

## Speech to Speech 

```shell
usage: train_a2a.py [-h] [-c FILE] [--DENSITY DENSITY] [--wavebased WAVEBASED]
[--bgnoise_fromdata BGNOISE_FROMDATA] [--ignore_loading IGNORE_LOADING] 
[--finetune FINETUNE] [--learnedmask LEARNEDMASK]
[--dynamicfiltershape DYNAMICFILTERSHAPE] [--formant_supervision FORMANT_SUPERVISION]
[--pitch_supervision PITCH_SUPERVISION] [--intensity_supervision INTENSITY_SUPERVISION]
[--n_filter_samples N_FILTER_SAMPLES] [--n_fft N_FFT] [--reverse_order REVERSE_ORDER]
[--lar_cap LAR_CAP] [--intensity_thres INTENSITY_THRES]
[--RNN_COMPUTE_DB_LOUDNESS RNN_COMPUTE_DB_LOUDNESS] 
[--BIDIRECTION BIDIRECTION][--MAPPING_FROM_ECOG MAPPING_FROM_ECOG] [--OUTPUT_DIR OUTPUT_DIR]
[--COMPONENTKEY COMPONENTKEY][--trainsubject TRAINSUBJECT] [--testsubject TESTSUBJECT]
[--reshape RESHAPE][--ld_loss_weight LD_LOSS_WEIGHT] [--alpha_loss_weight ALPHA_LOSS_WEIGHT]
[--consonant_loss_weight CONSONANT_LOSS_WEIGHT] [--batch_size BATCH_SIZE] 
[--param_file PARAM_FILE][--pretrained_model_dir PRETRAINED_MODEL_DIR] [--causal CAUSAL]
[--anticausal ANTICAUSAL][--rdropout RDROPOUT] [--epoch_num EPOCH_NUM] [--use_stoi USE_STOI]
[--use_denoise USE_DENOISE][--noise_db NOISE_DB]
```

Example usage:

```shell
python train_a2a.py --OUTPUT_DIR output/a2a/HB02 --trainsubject HB02 --testsubject HB02 \
--param_file configs/a2a_production.yaml --batch_size 16 --reshape 1 --DENSITY "HB" \
--wavebased 1 --n_filter_samples 80 --n_fft 256 --formant_supervision 1 \
--intensity_thres -1 --epoch_num 60
```

## ECoG to Speech

Same arguments as `train_a2a.py`

Example usage:

```
python train_e2a.py --OUTPUT_DIR output/e2a/resnet_HB02 --trainsubject HB02 \
--testsubject HB02 --param_file configs/e2a_production.yaml --batch_size 16 \
--MAPPING_FROM_ECOG ECoGMapping_ResNet --reshape 1 --DENSITY "HB" --wavebased 1 \
--dynamicfiltershape 0 --n_filter_samples 80 --n_fft 256 --formant_supervision 1 \
--intensity_thres -1 --epoch_num 60 --pretrained_model_dir output/a2a/HB02 --causal 0
```


## Running time
We train 60 epochs for Speech to Speech and ECoG to Speech. Running on one A100 GPU usually take 6 hours for Speech to Speech and 10 hours for ECoG to Speech

## Contamination analysis
Based on [Observation and assessment of acoustic contamination of electrophysiological brain signals during speech production and sound perception](https://iopscience.iop.org/article/10.1088/1741-2552/abb25e). We did contamination analysis in [contamination_analysis](contamination_analysis)

## Some modules explanation

In `model.py`

- GHMR (`class`): Gradient Harmonized Single-stage Detector, used for balance data distributions
- spectrogram_loss (`func`): given ground truth and decoded spectrogram, calculate difference loss in multi scales
- run_a2a_loss (`func`): loss function for Speech to Speech decoding
- run_components_loss (`func`): loss function for ECoG to Speech decoding

In `networks.py`

- FormantEncoder (`class` registered as EncoderFormant): the Speech Encoder
- FormantSysth (`class` registered as GeneratorFormant): the Speech Synthesizer
- ECoGMapping_Bottleneck (`class` registered as ECoGMapping_ResNet): the ECoG Decoder using ResNet as backbone
- ECoGMappingRNN (`class` registered as ECoGMapping_RNN): the ECoG Decoder using RNN as backbone
- ECoGMapping_3D_SWIN (`class` registered as ECoGMapping_3D_SWIN): the ECoG Decoder using 3D SWIN as backbone


## Citing Our Work
```dotnetcli
@article{chen2023neural,
  title={A Neural Speech Decoding Framework Leveraging Deep Learning and Speech Synthesis},
  author={Chen, Xupeng and Wang, Ran and Khalilian-Gourtani, Amirhossein and Yu, Leyao and Dugan, Patricia and Friedman, Daniel and Doyle, Werner and Devinsky, Orrin and Wang, Yao and Flinker, Adeen},
  journal={Nature Machine Intelligence},
  year={2024},
  publisher={Nature Publishing Group UK London}
}
```