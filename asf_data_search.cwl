#!/usr/bin/env cwl-runner

cwlVersion: v1.2
$graph:
- class: Workflow
  id: datasearch
  doc: Sentinel-1 image search
  requirements:
    - class: DockerRequirement
      dockerPull: oilspill001:1.0.0
    - class: InlineJavascriptRequirement

  inputs:
    use_case_directory:
      doc: directory where to find input files and where to store outputs
      type: Directory
      s:name: use case directory
      s:description: directory containing raw files, preprocessed files, and use case results
      s:keywords:
        - dir
        - Directory
    bbox:
      doc: bounding box for image search
      type: string?
      s:name: bounding box
      s:description: min_lon, min_lat, max_lon, max_lat
      s:keywords:
        - bbox
        - box
    start_date:
      doc: start date for data search
      type: string?
      s:name: start date
      s:description: yyyy-mm-dd
      s:keywords:
        - start
        - startdate
    time_interval:
      doc: time interval (n of days) for data search
      type: int?
      s:name: time interval
      s:description: n_days
      s:keywords:
        - time
        - interval
        - days
    end_date:
      doc: End date for data search
      type: string
      s:name: end date
      s:description: yyyy-mm-dd
      s:keywords:
        - end
        - enddate
    verbose:
      doc: verbose
      type: boolean? 
      s:name: verbose
      s:description: verbose
      s:keywords:
        - verbose
    debug:
      doc: debug
      type: boolean?  
      s:name: debug
      s:description: debug
      s:keywords:
        - debug

  outputs:
    datasearch_output:
      type: Directory
      outputSource: data_search/results

  steps:
    data_search:
      in:
        use_case_directory: use_case_directory
        bbox: bbox
        start_date: start_date
        time_interval: time_interval
        end_date: end_date
        verbose: verbose
        debug: debug
      run: '#datasearch'
      out:
        - results

- class: CommandLineTool
  id: datasearch_tool
  label: "Data Search Tool"
  requirements:
    - class: DockerRequirement
      dockerPull: oilspill001:1.0.0  # Use the same image for this tool if needed
  baseCommand: 
    - /srv/miniconda3/envs/oilspill001/bin/python  # Path to your Python executable
    - -m
    - oilspill001.main  # Path to your script
  inputs:
    bbox:
      type: string
      inputBinding:
        position: 1
        prefix: "--bbox"  
    use_case_directory:
      type: Directory
      inputBinding:
        position: 2
        prefix: "--dir"
    start_date:
      type: string
      inputBinding:
        position: 3
        prefix: "--start"
    time_interval:
      type: int? 
      inputBinding:
        position: 4
        prefix: "--days"
    end_date:
      type: string? 
      inputBinding:
        position: 5
        prefix: "--end"    
    verbose:
      type: boolean?  # Correctly formatted as boolean or null for optional
      inputBinding:
        position: 6
        prefix: "--verbose"
    debug:
      type: boolean? # Correctly formatted as boolean or null for optional
      inputBinding:
        position: 7
        prefix: "--debug"

  outputs:
    results:
      type: Directory
      outputBinding:
        glob: .

$namespaces:
  s: https://schema.org/

s:description: |-
  ASF search for SAR images from Sentinel-1
s:name: Sentinel-1 Oil Spill Detection Pipeline
s:softwareVersion: 1.0.0
s:programmingLanguage: python
s:sourceOrganization:
  - class: s:Organization
    s:name: MEEO SRL
    s:url: https://meeo.it/
s:author:
  - class: s:Person
    s:email: outmani@meeo.it
    s:name: Sabrina Outmani
  - class: s:Person
    s:email: fazzini@meeo.it
    s:name: Noemi Fazzini

