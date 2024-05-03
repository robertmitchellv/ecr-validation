from pathlib import Path
from lxml import etree
from saxonche import PySaxonProcessor
from rich.console import Console


# define the base directory and file paths
base_dir = Path(__file__).parent
xslt_path = base_dir / "schema" / "CDAR2_IG_PHCASERPT_R2_STU1.1_SCHEMATRON.xsl"
xml_path = (
    base_dir / "sample-files" / "CDAR2_IG_PHCASERPT_R2_STU1.1_2019APR_SAMPLE_ZIKA.xml"
)
output_path = base_dir / "logs" / "svrl-output.xml"


def parse_svrl(svrl_result):
    # parse the SVRL result string
    svrl_doc = etree.fromstring(svrl_result.encode("utf-8"))

    # namespace map for finding elements
    ns = {
        "svrl": "http://purl.oclc.org/dsdl/svrl",
        "sch": "http://purl.oclc.org/dsdl/schematron",
    }

    # extract all fired-rule elements and associated failed assertions
    results = []
    fired_rules = svrl_doc.xpath("//svrl:fired-rule", namespaces=ns)

    for rule in fired_rules:
        role = rule.get("role")

        # iterate over all failed assertions following each fired rule
        for assertion in rule.xpath(
            "following-sibling::svrl:failed-assert", namespaces=ns
        ):
            text = (
                assertion.find("svrl:text", namespaces=ns).text
                if assertion.find("svrl:text", namespaces=ns)
                else "No message"
            )
            location = assertion.get("location")
            context = assertion.get("context")
            test_id = assertion.get("id")

            results.append(
                {
                    "context": context,
                    "location": location,
                    "message": text,
                    "severity": role,
                    "test_id": test_id,
                }
            )

    return results


def display_svrl(validation_results, console):
    for result in validation_results:
        console.print(f"Context: {result['context']}")
        console.print(f"Location: {result['location']}")
        console.print(f"Message: {result['message']}")
        console.print(f"Severity: {result['severity']}")
        console.print("-" * 40)


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
            compiled_stylesheet = None

        if compiled_stylesheet is None:
            console.print(
                "Failed to compile stylesheet. Check the file path and permissions."
            )
        else:
            try:
                result = compiled_stylesheet.transform_to_string(
                    source_file=str(xml_path)
                )
                if result:
                    console.print("Transformation successful.")
                    validation_results = parse_svrl(result)
                    display_svrl(validation_results, console)
                else:
                    console.print("No output was generated from the transformation.")
            except Exception as e:
                console.print(f"Error during transformation: {str(e)}")


validate_xml_with_schematron(xml_path=str(xml_path))
