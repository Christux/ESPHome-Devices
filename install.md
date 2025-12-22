# ESPHOME Devices

## Installation

### 1. Create a virtual environment
```bash
python3.12 -m venv .venv
```
### 2. Activate the environment
```bash
source .venv/bin/activate
```
### 3. Install ESPHOME
```bash
pip install esphome
```

## Usage

### Activate environment
```
source .venv/bin/activate
```
### Compile and upload firmware in device
```
esphome run minimonitor.yaml --device OTA
```
### Clean compiles files
```
esphome clean minimonitor.yaml
```
### Generate folder tree
```
tree -a -I "__pycache__|.git|.esphome|.venv"
```


