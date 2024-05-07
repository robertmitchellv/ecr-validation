from lxml import etree
from rich.console import Console
from rich.table import Table

# Load the SVRL file
svrl_path = "svrl-output.xml"
with open(svrl_path, "rb") as file:  # Open as binary to avoid encoding issues
    svrl_content = file.read()

# Parse the SVRL content
svrl_doc = etree.fromstring(svrl_content)

# Namespace map for finding elements
ns = {
    "svrl": "http://purl.oclc.org/dsdl/svrl",
    "sch": "http://purl.oclc.org/dsdl/schematron",
}

# Extract failed assertions
errors = []
for assertion in svrl_doc.findall(".//svrl:failed-assert", namespaces=ns):
    message = assertion.find("svrl:text", namespaces=ns).text.strip()
    context = assertion.get("location", "No context provided").strip()
    test = assertion.get("test").strip()
    errors.append({"message": message, "context": context, "test": test})

# Create a Rich console
console = Console()

# Create a Rich table with lines between rows
table = Table(show_header=True, header_style="bold magenta", show_lines=True)
table.add_column("Message", style="dim", width=50)
table.add_column("Context", style="dim", width=50)
table.add_column("Test", style="dim", width=50)

# Add rows to the table
for error in errors:
    table.add_row(error["message"], error["context"], error["test"])

# Display the table
console.print(table)
