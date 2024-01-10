# zupimages

Script to upload a file to [ZupImages](https://www.zupimages.net).

# Usage

```
python zupimages.py [file]
```

`file`: a valid image path. Accepted format: jpg, jpeg, gif, png, bmp, tiff, tif.

# Install
## Prerequisite
- Python 3.11+ (not tested with previous versions)

## Clone repository
```
git clone https://github.com/PhunkyBob/zupimages.git
cd zupimages
```

## (optional) Create virtual environment
```
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -U pip
```

## Install dependencies
```
python -m pip install -r requirements.txt
```

# Binary

You can try the [experimental binary for Windows](https://github.com/PhunkyBob/zupimages/releases/latest). 
Compilation with Nuitka for Windows: 
```
python -m nuitka --standalone --onefile --windows-icon-from-ico=favicon.ico zupimages.py
```
