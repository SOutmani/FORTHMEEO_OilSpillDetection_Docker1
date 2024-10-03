$graph:
- baseCommand: oilspill001
  class: CommandLineTool
  id: clt
  inputs:
    use_case_directory:
      inputBinding:
        position: 1
        prefix: --use-case-directory
      type: string
    bbox:
      inputBinding:
        position: 2
        prefix: --bbox
      type: string?
    start_date:
      inputBinding:
        position: 3
        prefix: --start-date
      type: string?
    time_interval:
      inputBinding:
        position: 4
        prefix: --time-interval
      type: None?
    end_date:
      inputBinding:
        position: 5
        prefix: --end-date
      type: None?
    verbose:
      inputBinding:
        position: 6
        prefix: --verbose
      type: boolean?
    debug:
      inputBinding:
        position: 7
        prefix: --debug
      type: boolean?
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /srv/miniconda3/envs/oilspill001/bin:/srv/miniconda3/condabin:/srv/miniconda3/bin:/srv/miniconda3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    ResourceRequirement: {}
  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: This is Workflow class doc
  id: oilspill001
  inputs:
    use_case_directory:
      doc: Name of use-case folder
      label: Name of use-case folder
      type: string
    bbox:
      doc: Bounding Box
      label: Bounding Box
      type: string?
    start_date:
      doc: Start date for data search
      label: Start date for data search
      type: string?
    time_interval:
      doc: Time interval (n of days) for data search
      label: Time interval (n of days) for data search
      type: None?
    end_date:
      doc: End date for data search
      label: End date for data search
      type: None?
    verbose:
      default: false
      doc: Verbose mode
      label: Verbose mode
      type: boolean?
    debug:
      default: false
      doc: Debug mode
      label: Debug mode
      type: boolean?
  label: This is Workflow class label
  outputs:
  - id: wf_outputs
    outputSource:
    - step_1/results
    type: Directory
  steps:
    step_1:
      in:
        use_case_directory: use_case_directory
        bbox: bbox
        start_date: start_date
        time_interval: time_interval
        end_date: end_date
        verbose: verbose
        debug: debug
      out:
      - results
      run: '#clt'
$namespaces:
  s: https://schema.org/
cwlVersion: v1.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
