import json
import sys
import io
import os

from lxml import etree

import cairosvg

PUSH_TO_END_TAG = "%LAST_ALPHABETICALLY%"
PUSH_TO_END_STRING = "ZZZZZZZZZZZZ"
EMPTY_SKILL_TITLE = "________________"
NAMESPACES = {"base":"http://www.w3.org/2000/svg"}

def order_skill(skill_dict):
    title_parsed = skill_dict['title'].replace(PUSH_TO_END_TAG, PUSH_TO_END_STRING)
    subtitle_parsed = skill_dict['subtitle'].replace(PUSH_TO_END_TAG, PUSH_TO_END_STRING)
    if title_parsed:
        return "".join([c for c in title_parsed if c.isalpha()])
    elif subtitle_parsed:
        return "".join([c for c in subtitle_parsed if c.isalpha()])
    else:
        return PUSH_TO_END_STRING

def make_pdf(template_tree, sheet_data, output_filename=None):
    data = sheet_data
    # Sorts skills alphabetically by title (or subtitle) if requested
    if data["SORT_ALPHABETICAL"]:
        data['SKILLS'].sort(key=order_skill)

    # Substitutes keywords
    for keyword, value in data['KEYWORDS'].items():
        for match in template_tree.findall(f".//base:tspan[.='{keyword}']", NAMESPACES):
            match.text = value

    # Substitutes skill data
    for i in range(57):
        try:
            skill = data['SKILLS'][i]
            title_clean = skill['title'].replace(PUSH_TO_END_TAG, '')
            subtitle_clean = skill['subtitle'].replace(PUSH_TO_END_TAG, '')
            if skill['title']:
                skill_title = title_clean
            else:
                skill_title = EMPTY_SKILL_TITLE
            if skill['percentage']:
                skill_subtitle = f"{subtitle_clean} ({skill['percentage']})"
            else:
                skill_subtitle = f"{subtitle_clean}"
            skill_box = skill['checkbox']
            skill_font = skill.get("font", None)

        except IndexError:
            skill_title = EMPTY_SKILL_TITLE
            skill_subtitle = ""
            skill_box = True
            skill_font = None

        # Alters title and font
        title = template_tree.find(f".//base:tspan[.='%skill_{i}%']", NAMESPACES)
        title.text = skill_title
        if skill_font:
            title.find("..").set("style", title.find("..").attrib["style"].replace("Bookmania", skill_font))

        # Alters subtitle
        subtitle = template_tree.find(
            f".//base:tspan[.='%skill_{i}_subtitle%']",
            NAMESPACES
        )
        subtitle.text = skill_subtitle

        # Remove checkbox if needed
        checkbox = template_tree.find(
            f".//base:desc[.='%checkbox_skill_{i}%']/...",
            NAMESPACES
        )
        checkbox.set('visibility', 'visible' if skill_box else 'hidden')

    if output_filename:
        if not os.path.exists(os.path.dirname(output_filename)):
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        cairosvg.svg2pdf(
            bytestring=etree.tostring(template_tree, encoding="utf-8"),
            write_to=output_filename
        )
    else:
        # Create memory file to store conversion, then return bytestring
        in_memory_file = io.BytesIO()
        cairosvg.svg2pdf(
            bytestring=etree.tostring(template_tree, encoding="utf-8"),
            write_to=in_memory_file
        )
        return in_memory_file

if __name__=="__main__":
    # Loads template
    with open(sys.argv[1], 'r') as f_template:
        p = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(f_template.read().encode('utf-8'), parser=p)

    # Loads translation data
    with open(sys.argv[2], 'r') as f_data:
        data = json.load(f_data)

    make_pdf(root, data, sys.argv[3])