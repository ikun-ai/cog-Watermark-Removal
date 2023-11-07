# cog-Watermark-Removal

## Introduction

cog-Watermark-Removal is a powerful tool that uses cog to remove watermarks from images on rep. 

Use tensorflow architecture to run on cpu

## Installation

To install cog-Watermark-Removal, please follow these steps:

1. Clone the repository from GitHub:

```
git clone https://github.com/ikun-ai/cog-Watermark-Removal
```

2. Navigate into the cloned repository:

```
cd cog-Watermark-Removal
```

3. Download the model dirs using this [link](https://drive.google.com/drive/folders/1xRV4EdjJuAfsX9pQme6XeoFznKXG0ptJ) and put it under model/ (rename checkpoint.txt to checkpoint because sometimes google drive automatically adds .txt after download)

4. Make sure cog and docker are installed


## Usage

To use cog-Watermark-Removal, follow these steps:

1. Open your terminal and navigate to the directory where you have cloned the repository.

2. Run the following command:

```
cog predict -i image=@/path/to/input/image
```

Replace `/path/to/input/image` with the path to the image file you want to remove the watermark from. 

3. Wait for the process to complete. The tool will automatically identify and remove the watermark from the image. The processed image will be saved to the specified output path.

## Note

- The effectiveness of watermark removal may vary depending on the complexity and opacity of the watermark. 
- Please respect copyright laws and use this tool responsibly.