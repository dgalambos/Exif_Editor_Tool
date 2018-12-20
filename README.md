# EXIF Editor Tool

>Exif Editor Tool is a command-line script based off of Python 2.7 to assist and automate EXIF metadata modification for images via an auto-generated CSV file.
# Features
The tool has multiple features:
- Modify:
    - Date/Time
    - GPS (latitude/longitude)
- Append tags/keywords
    - Tags are alphabetically ordered
- Wipe all EXIF data
- Watermark photos

# Getting EXIF Editor Tool
The source code can be checked out from the github repository with
```sh
git clone https://github.com/dgalambos/Exif_Editor_Tool.git
```

### Installation

* Pre-requisites
    * EXIF Editor Tool requires [Python 2.7](https://www.python.org/download/releases/2.7/), [Pip](https://pip.pypa.io/en/stable/installing/), as well as [PyExifTool](https://github.com/smarnach/pyexiftool) to run install the pre-requisites.

*Once `Python 2.7`, `Pip` and `PyExifTool` are installed:*

Install the dependencies via Pip and the requirements.txt:

```sh
$ cd path/to/repository
$ pip install -r requirements.txt
```

Current requirements are:

```sh
tqdm==4.28.1
Pillow==5.3.0
```

# Examples

| Command | Description | Example |
| ------ | ------ | ------ |
| `--csv` | Generates CSV file in user-designated folder | ```$ python exif_editor.py --csv true```  |
| `--wipe` | Wipes all EXIF data | ```$ python exif_editor.py --wipe true``` |
| `--gps` | Updates GPS locations EXIF, if given in CSV file | ```$ python exif_editor.py --gps true``` |
| `--time` | Updates Date/Time (all) EXIF, if given in CSV file | ```$ python exif_editor.py --time true``` |
| `--watermark` | Adds watermark to photos (EXIF data copied over) to new folder. New images will be appended '_watermark' after filename | ```$ python exif_editor.py --watermark true``` |
| `--tags` | Adds tags/keywords to the image. New keywords get appended to old list and alphabetically ordered | ```$ python exif_editor.py --tags true``` |


Commands can be stacked, too:

| Command | Description | Example |
| ------ | ------ | ------ |
| `--tags --watermark` | Adds tags/keywords and also watermarks the images | ```$ python exif_editor.py --tags true --watermark true``` |
| `--gps --time` | Updates the GPS coordinates and Date/Time (all) of the images | ```$ python exif_editor.py --gps true --time true``` |

### Todos
 - Make the code more efficient!

### Acknowledgements
> This tool was created thanks to [ExifTool by Steve Harvey](https://www.sno.phy.queensu.ca/~phil/exiftool/) as well as its Python wrapper [PyExifTool by Sven Marnach](https://github.com/smarnach/pyexiftool)
