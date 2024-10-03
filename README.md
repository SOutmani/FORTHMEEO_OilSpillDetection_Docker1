# FORTHMEEO_OilSpillDetection_Docker1
Docker 1 consists in Sentinel-1 data search and download.

# ILIAD - Oil Spill Pilot
#### MEEO, FORTH

## Application Package 1: oilspill001 
### Data Download
This is the first application package of the oil spill detection workflow and allows to search and download SAR data from Sentinel-1 data globally.

### Getting Started 
If you haven't yet, build the miniconda docker.
```bash
docker build -t my_miniconda:latest -f Dockerfile.miniconda . 
```
Then build the application package docker file by mounting a volume i.e. "/home/ubuntu/volume"
```bash
docker build -t oilspill001:1.0.0 -f Dockerfile1 .
docker run -v /home/ubuntu/volume:/oil_spill_directory -it oilspill001:1.0.0
```
### Example Commands
Once inside the docker you can display the help message and then start searching for relevant data.
```bash
oilspill001 --help
oilspill001 --bbox 24.07,35.70,24.69,36.26 --dir crete --start 2023-06-27 --days 1 --debug
```