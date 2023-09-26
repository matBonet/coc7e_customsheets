Simple script to make fully customizabble Call of Cthulhu 7th Edition Character Sheets. To use, an svg template must be provided, as well as a json file containing the content to be filled. This allows translations into any language and/or customization of the skills.

# How to use
```python3 translator.py {template_path} {parameter_path} {output_path}```

Example:

```python3 translator.py templates/coc7eanniversary_firstpage.svg translations/CoC-en.json "CoC 7e Custom Sheet (en)"```