import os
import sys
import logging
import asf_search as asf
from dotenv import load_dotenv
from shapely.geometry import Polygon
from datetime import datetime, timedelta
from .module_log import logger

def asf_search(aoi, use_case_directory, event_date, time_interval=None):	
	xmin, ymin, xmax, ymax = [float(coord) for coord in aoi.split(',')]
	vertices = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]
	polygon = Polygon(vertices)
	aoi = polygon.wkt

    # Handle credentials
	if os.path.isfile('.env'):
		load_dotenv('.env')
		username = os.environ.get('asf_login')
		password = os.environ.get('asf_pwd')
	else:
		logger.error('No ASF credentials found.')
		sys.exit()

	if time_interval:
		days = time_interval
	else:
		days = 1

	end_date = (datetime.strptime(event_date, "%Y-%m-%d") + timedelta(days)).strftime("%Y-%m-%d")
	logger.debug(f"Searching images between: {event_date} - {end_date} in the area of interest")
	logger.info("Starting Data Search")		
	products = asf.search(platform=[asf.PLATFORM.SENTINEL1],
			     processingLevel=[asf.PRODUCT_TYPE.GRD_HD],
			     intersectsWith=aoi,
			     start=event_date,
			     end=end_date,		
			     maxResults=100)
	
	n_results = len(products)
	logger.debug(f"Found {n_results} images.")
	if n_results == 0:
		logger.debug("No images found. Change parameters.")
		sys.exit()
		
	# Initialize the directory to store downloaded products
	raw_dir = 'raw_sentinel'
	tmp_dir = os.path.join(use_case_directory, raw_dir)
	if not os.path.exists(tmp_dir):
		os.mkdir(tmp_dir)

	filenames_to_download = []
	filepaths = []
	for feature in products:
		filename = feature.properties['fileName']
		filenames_to_download.append(filename.split('.')[0])
		path = os.path.join(tmp_dir, filename)
		filepath = os.path.abspath(path)
		filepaths.append(filepath)
	
	#Download products
	#logger.info(f"Downloading Sentinel-1 images to {tmp_dir}.")
	session = asf.ASFSession().auth_with_creds(username, password)
	download_products = asf.granule_search(filenames_to_download)
	for feature in download_products:
		feature.download(path=tmp_dir, session=session)
	
	return filepaths, tmp_dir