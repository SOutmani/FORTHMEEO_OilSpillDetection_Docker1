#!/usr/bin/env python
'''
Authors: Sabrina Outmani, Noemi Fazzini
Application Package 1 takes as input the use case folder and some additional non-required parameters like bounding box and . The outputs is a list of the downloaded sentinel-1 images.
'''
import click
import click2cwl
from click2cwl import dump
import os
import sys
import logging
from datetime import datetime
from .module_log import logger
from .module_asf import asf_search

### input arguments
@click.command(
    short_help="This is Workflow class label",
    help="This is Workflow class doc",
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.option("--use-case-directory", "--dir", type=str, required=True, help="Name of use-case folder", metavar="dir_name")
@click.option("--bbox", "--aoi", type=str, required=False, help="Bounding Box", metavar="min_lon, min_lat, max_lon, max_lat")
@click.option("--start-date", "--start", type=str, required=False, help="Start date for data search", metavar="yyyy-mm-dd")
@click.option("--time-interval", "--days", type=int, required=False, help="Time interval (n of days) for data search", metavar="n_days")
@click.option("--end-date", "--end", type=int, required=False, help="End date for data search", metavar="yyyy-mm-dd")
@click.option("--verbose",              is_flag=True, default=False, help="Verbose mode")
@click.option("--debug",                is_flag=True, default=False, help="Debug mode")
@click.pass_context
def main(ctx, use_case_directory, verbose, debug, bbox=None, start_date=None, time_interval=None, end_date=None):
    """
    Usage:
        python3 main.py --bbox min_lon,min_lat,max_lon,max_lat --dir dir_name --debug
        python3 main.py --bbox 24.0779,35.7034,24.6972,36.2628 --dir crete --start 2023-06-27 --days 1 --debug
        oilspill001 --bbox 24.0779,35.7034,24.6972,36.2628 --dir crete --start 2023-06-27 --days 1 --debug
    """
    # Call dump to generate CWL information
    dump(ctx)

    if verbose:
        logger.setLevel(logging.INFO)
    if debug:
        logger.setLevel(logging.DEBUG)
    #Create use case folder
    #working_dir = os.path.join('data', use_case_directory)
    working_dir = use_case_directory
    if not os.path.exists(working_dir):
        os.makedirs(working_dir)
    
    #If no bounding box is given, then the default area of interest is Crete
    if not bbox:
        bbox='22.5,34.5,27.5,36' 
    
    '''
    HISTORIC SEARCH: IF START DATE IS GIVEN, SPECIFIC IMAGES ARE DOWNLOADED (CERULEAN API CAN BE USED TO RETURN BOUNDING BOXES CONTAINING DETECTIONS THAT CAN BE USED LATER (PROBABLY NOT).
    '''
    #If specific dates are given - historic search.
    if start_date:        
        if not time_interval and not end_date:
            raise click.UsageError("Either --time-interval or --end-date must be provided after --start-date.")
            sys.exit()
        if end_date:
            logger.info('Starting historic search.')
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Compute the time interval in days
            time_interval = (end_date - start_date).days

        #logger.info("Activating Cerulean API")
        #bounding_boxes = cerulean_date_and_bbox(start_date, time_interval, bbox) #tbf
        logger.info("Downloading Sentinel-1 Images. Approximaately 1 minute per product.")
        sentinel_paths,raw_sentinel_dir = asf_search(bbox, working_dir, start_date, time_interval) #tbf

    '''
    MONITORING: IF START DATE IS NOT GIVEN, WE USE TODAYS DATE, OR THE DATETIME OF THE LATEST CERULEAN DETECTION - but API needs some fixing. AGAIN WE CAN RETURN BOUNDING BOXES CONTAINING DETECTIONS THAT CAN BE USED LATER (PROBABLY NOT).
    '''
    logger.info('Starting AOI scan.')
    #logger.info("Alarm Activation via Cerulean API")
    #event_date = cerulean_datetime(bbox) #tbf
    #bounding_boxes = cerulean_bbox(bbox) #tbf
	
    logger.info("Downloading Sentinel-1 Images")
    #overriding the parameter above for illustration purposes
    #event_date = '2023-06-27' 
    #sentinel_paths, raw_sentinel_dir = asf_search(bbox, working_dir, event_date)

    # Define the file path where you want to save the list
    sentinel_list = os.path.join(raw_sentinel_dir,'sentinel_paths.txt')

    # Write each item from the list to the text file
    with open(sentinel_list, 'w') as file:
        for path in sentinel_paths:
            file.write(f"{path}\n")

    logger.info("Sentinel-1 images successfully downloaded.")
    
    return sentinel_paths, sentinel_list

if __name__ == "__main__":
    main()