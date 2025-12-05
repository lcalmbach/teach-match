import argparse
import csv
import os
import xml.etree.ElementTree as ET


def get_local_name(tag: str) -> str:
    """
    Entfernt XML-Namespace aus Tags: '{ns}tag' -> 'tag'
    """
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def collect_fieldnames(entities):
    """
    Sammelt alle möglichen Spaltennamen aus einer Liste von Entity-Elementen.
    - Attribute des Elements selbst
    - Text der direkten Kind-Elemente
    - Attribute der direkten Kind-Elemente (Name: <childtag>_<attrname>)
    """
    fieldnames = set()

    for entity in entities:
        # Attribute des Entity-Elements
        for attr_name in entity.attrib.keys():
            fieldnames.add(attr_name)

        # direkte Kind-Elemente
        for child in entity:
            lname = get_local_name(child.tag)
            text = (child.text or "").strip()

            if text:
                fieldnames.add(lname)

            for attr_name in child.attrib.keys():
                fieldnames.add(f"{lname}_{attr_name}")

    return sorted(fieldnames)


def entity_to_row(entity, fieldnames):
    """
    Wandelt ein Entity-Element in ein Dict für csv.DictWriter um.
    Falls ein Feld mehrfach vorkommt, werden die Werte mit '|' verkettet.
    """
    row = {fn: "" for fn in fieldnames}

    # Attribute des Entity-Elements
    for attr_name, attr_value in entity.attrib.items():
        if attr_name in row:
            row[attr_name] = attr_value

    # direkte Kind-Elemente
    for child in entity:
        lname = get_local_name(child.tag)
        text = (child.text or "").strip()

        if text:
            if lname in row:
                if row[lname]:
                    row[lname] = row[lname] + "|" + text
                else:
                    row[lname] = text

        for attr_name, attr_value in child.attrib.items():
            key = f"{lname}_{attr_name}"
            if key in row:
                if row[key]:
                    row[key] = row[key] + "|" + attr_value
                else:
                    row[key] = attr_value

    return row


def export_collection_to_csv(collection_element, output_dir):
    """
    Nimmt ein Top-Level-Collection-Element (z.B. <teachers>)
    und schreibt eine CSV-Datei, eine Zeile pro Kind (z.B. <teacher>).
    """
    entities = list(collection_element)
    if not entities:
        return  # nichts zu exportieren

    collection_name = get_local_name(collection_element.tag)
    csv_filename = os.path.join(output_dir, f"{collection_name}.csv")

    fieldnames = collect_fieldnames(entities)
    if not fieldnames:
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entity in entities:
            row = entity_to_row(entity, fieldnames)
            writer.writerow(row)

    print(f"Wrote {csv_filename} ({len(entities)} rows)")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Untis XML export into one CSV per entity collection."
    )
    parser.add_argument(
        "xml_path",
        help="Path to untis.xml (e.g. C:\\Users\\...\\untis.xml)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default="csv_output",
        help="Directory to write CSV files into (default: csv_output)",
    )

    args = parser.parse_args()

    tree = ET.parse(args.xml_path)
    root = tree.getroot()

    # alle direkten Kinder von <document> durchgehen:
    # <general>, <timeperiods>, <holidays>, <departments>, <rooms>, <subjects>, <teachers>, <classes>, ...
    for collection in root:
        export_collection_to_csv(collection, args.output_dir)


if __name__ == "__main__":
    main()
