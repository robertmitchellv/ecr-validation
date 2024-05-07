from pathlib import Path
from lxml import etree
from saxonche import PySaxonProcessor
from rich.console import Console
from rich.table import Table

# Define the base directory and file paths
base_dir = Path(__file__).parent
xslt_path = base_dir / "schema" / "CDAR2_IG_PHCASERPT_R2_STU1.1_SCHEMATRON.xsl"
xml_path = (
    base_dir / "sample-files" / "CDAR2_IG_PHCASERPT_R2_STU1.1_2019APR_SAMPLE_ZIKA.xml"
)


def parse_svrl(svrl_result):
    # Parse the SVRL result string
    svrl_doc = etree.fromstring(svrl_result.encode("utf-8"))

    # Namespace map for finding elements
    ns = {
        "svrl": "http://purl.oclc.org/dsdl/svrl",
        "sch": "http://purl.oclc.org/dsdl/schematron",
    }

    # Extract all failed assertions
    results = []
    for assertion in svrl_doc.findall(".//svrl:failed-assert", namespaces=ns):
        text_element = assertion.find("svrl:text", namespaces=ns)
        text = text_element.text.strip() if text_element is not None else "No message"
        context = assertion.get("location", "No context provided").strip()
        test = assertion.get("test", "No test provided").strip()
        results.append({"message": text, "context": context, "test": test})
    return results


def display_svrl(validation_results, console):
    # Create a Rich table with the specified format
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Message", style="dim", width=50)
    table.add_column("Context", style="dim", width=50)
    table.add_column("Test", style="dim", width=50)

    # Add rows to the table
    for result in validation_results:
        table.add_row(result["message"], result["context"], result["test"])

    # Display the table
    console.print(table)


def validate_xml_with_schematron(xml_path):
    console = Console()
    with PySaxonProcessor(license=False) as processor:
        xslt_processor = processor.new_xslt30_processor()
        try:
            compiled_stylesheet = xslt_processor.compile_stylesheet(
                stylesheet_file=str(xslt_path)
            )
            console.print("Stylesheet compiled successfully.")
        except Exception as e:
            console.print(f"Error during stylesheet compilation: {str(e)}")
            return

        try:
            result = compiled_stylesheet.transform_to_string(source_file=str(xml_path))
            if result:
                console.print("Transformation successful.")
                validation_results = parse_svrl(result)
                display_svrl(validation_results, console)
            else:
                console.print("No output was generated from the transformation.")
        except Exception as e:
            console.print(f"Error during transformation: {str(e)}")


validate_xml_with_schematron(xml_path=str(xml_path))
