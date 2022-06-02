from streamlit_vtkjs import st_vtkjs
from pathlib import Path

vtkjs_path = Path('daylight_factor.vtkjs')
st_vtkjs(content=vtkjs_path.read_bytes(), key='df')
