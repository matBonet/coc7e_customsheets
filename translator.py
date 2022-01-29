import json
import sys

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

if __name__=="__main__":
    template = sys.argv[1]
    parameters = sys.argv[2]
    output = sys.argv[3]

    # Loads configuration
    with open(parameters, 'r') as f_json:
        data = json.load(f_json)

    # Sorts skills alphabetically by title (or subtitle) if requested
    if data["SORT_ALPHABETICAL"]:
        data['SKILLS'].sort(key=order_skill)

    import pprint
    pprint.pprint(data['SKILLS'])

    # Loads template
    with open(template, 'r') as f_template:
        p = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
        root = etree.fromstring(f_template.read().encode('utf-8'), parser=p)

    # Substitutes keywords
    for keyword, value in data['KEYWORDS'].items():
        for match in root.findall(f".//base:tspan[.='{keyword}']", NAMESPACES):
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
        except IndexError:
            skill_title = EMPTY_SKILL_TITLE
            skill_subtitle = ""
            skill_box = True

        # Alters title
        title = root.find(f".//base:tspan[.='%skill_{i}%']", NAMESPACES)
        title.text = skill_title

        # Alters subtitle
        subtitle = root.find(
            f".//base:tspan[.='%skill_{i}_subtitle%']",
            NAMESPACES
        )
        subtitle.text = skill_subtitle

        # Remove checkbox if needed
        checkbox = root.find(
            f".//base:desc[.='%checkbox_skill_{i}%']/...",
            NAMESPACES
        )
        checkbox.set('visibility', 'visible' if skill_box else 'hidden')

    cairosvg.svg2pdf(
        bytestring=etree.tostring(root, encoding="utf-8"),
        write_to=output
    )