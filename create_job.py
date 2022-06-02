import streamlit as st
from pathlib import Path
from pollination_streamlit.api.client import ApiClient
from pollination_streamlit.interactors import NewJob, Recipe


def add_recipe_to_job(job, arguments, artifacts) -> NewJob:

    for artifact in artifacts:
        item = job.upload_artifact(
            artifact['file_path'], artifact['pollination_target_path'])
        arguments[artifact.key] = item

    job.arguments = [arguments]

    return job


def create_job(
        api_client: ApiClient,
        owner: str,
        project: str,
        name: str,
        description: str,
        cpu_count: int,
        grid_filter: str,
        min_sensor_count: int,
        hbjson: Path,
        radiance_parameters: str) -> str:
    """Create a job to run the daylight-factor recipe on Pollination.

    args:
        api_client: An ApiClient object.
        owner: The owner of the Pollination account.
        project: The name of the project inside which this job will be created.
        name: The name of the job.
        description: A description of the job.
        cpu_count: The number of CPUs to use for the job.
        grid_filter: A regex pattern as a string to filter grids.
        min_sensor_count: The minimum number of sensors to use per CPU.
        hbjson: The path to the HBJSON file.
        radiance_parameters: A string of radiance parameters.

    returns:
        The id of the created job.
    """

    recipe = Recipe('ladybug-tools', 'daylight-factor',
                    'latest', api_client)

    new_job = NewJob(owner, project, recipe, name=name,
                     description=description, client=api_client)
    arguments = {}

    model = new_job.upload_artifact(hbjson, '.')

    arguments['cpu-count'] = cpu_count
    arguments['grid-filter'] = grid_filter
    arguments['min-sensor-count'] = min_sensor_count
    arguments['model'] = model
    arguments['radiance-parameters'] = radiance_parameters

    new_job.arguments = [arguments]

    job = new_job.create()

    return job.id


with st.form('daylight-factor-job'):
    api_key = st.text_input(
        'Enter Pollination API key', type='password')
    owner = st.text_input('Project Owner')
    project = st.text_input('Project Name')

    st.markdown('---')

    cpu_count = st.number_input('CPU Count', value=50)
    grid_filter = st.text_input('Grid Filter', value='*')
    min_sensor_count = st.number_input('Min Sensor Count', value=200)
    hbjson_data = st.file_uploader('Upload HBJSON')
    rad_parameters = st.text_input('Rad Parameters',
                                   value='-ab 2 -aa 0.1 -ad 2048 -ar 64')

    submit_button = st.form_submit_button(
        label='Submit')

    if submit_button:
        # create HBJSON file path
        hbjson_file = Path('.', 'model.hbjson')
        # write HBJSON file
        hbjson_file.write_bytes(hbjson_data.read())

        # recipe inputs
        arguments = {
            'cpu_count': cpu_count,
            'grid_filter': grid_filter,
            'min_sensor_count': min_sensor_count,
            'radiance_parameters': rad_parameters,
        }

        # recipe inputs where a file needs to be uploaded
        arguments = {
            'model': {
                'file_path': hbjson_file,
                'pollination_target_path': '.'}
        }

        api_client = ApiClient(api_token=api_key)
        job_id = create_job(api_client, owner, project,
                            'test', 'Daylight-factor job for Pollination docs',
                            cpu_count, grid_filter, min_sensor_count, hbjson_file,
                            rad_parameters)
