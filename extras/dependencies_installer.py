import os

requirements_path = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ), '..', 'requirements.txt'
)

os.system(f'pip install -r {requirements_path}')
