# Custom Call of Cthulhu 7th Edition Character Sheets

Simple script to make fully customizable Call of Cthulhu 7th Edition Character Sheets. To use, an svg template must be provided, as well as a json file containing the content to be filled. This allows translations into any language and/or customization of the skills.

## Setup

```pip install -r requirements.txt```
```sudo apt install libcairo2```

Remember to install the required fonts, listed in the ```templates/font_dependencies.yaml``` file.

## How to use

```python translator.py {template_path} {parameter_path} {output_path}```

Example:

```python translator.py templates/coc7eanniversary_firstpage.svg translations/CoC-en.json "CoC 7e Custom Sheet (en)"```
