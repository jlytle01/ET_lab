# ET_lab
Data acquisition code for evapotranspiration measurement
Roadmap as follows:
- acquire accurate data from sample sensor on demand over i2c
- acquire accurate data from network of sensors on demand over i2c
- program the RPi to collect data on a rolling basis, and export daily .csv
- interface with cloud-based service to upload daily files
- run python on cloud-based service to compile daily files into uniform database
- send notifications on successful data upload, DB entry, any errors or missing data. 
