# showntell - `chemistry`

This build includes a range of packages that support the production of rich materials relating to chenostry topics, including the rendering of chemical formulae and 3D molecular models.

[![Binder](http://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/psychemedia/showntell/chemistry)

## Notebooks

Notebooks included:

- `index_chemistry.ipynb`: demo of a wide range of packages - `pybel`, `moldesign`, `pubchempy`, `chembl_webresource_client`, `pypdb`, `rdkit`, `nglview`.

### Local build

```python
pip3 install jupyter-repo2docker

jupyter-repo2docker --image-name psychemedia/binder_chemistry --no-run https://github.com/psychemedia/showntell/tree/chemistry


docker push psychemedia/binder_chemistry
```