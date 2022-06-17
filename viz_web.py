from pollination_streamlit_viewer import viewer
from pathlib import Path

vtkjs_path = Path('daylight_factor.vtkjs')
viewer(content=vtkjs_path.read_bytes(), key='df')
