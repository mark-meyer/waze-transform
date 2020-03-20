# xmls2pb 
Script to transform arcgis json to waze feed json format

### Requirements
Python 3.6 or greater

### Installing
Install dependencies:  
```
pip3 install -r requirements.txt
``` 

Copy configuration in `config-orig.py` to config.py and add customization.

### Running
Start the script with
```
python ./run.py
```
or for more logging information:
```
python ./run.py --log DEBUG 
```

### Running as a service on EC2
The included file `wazetrans.service` is a basic systemd service. Place it somewhere 
that systemd looks, such as `/etc/systemd/system` then reload, enable, and start:
```
sudo systemctl daemon-reload
sudo systemctl enable wazetrans.service
sudo systemctl start wazetrans.service
```
Check for status with:

```
sudo systemctl status wazetrans.service
```


### Authors
* **Mark Meyer** - *Initial work* - [Github](https://github.com/mark-meyer)
