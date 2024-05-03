from lxml import etree

# load the SVRL file
svrl_path = "svrl-output.xml"
with open(svrl_path, "r") as file:
    svrl_content = file.read()

# parse the SVRL content
svrl_doc = etree.fromstring(svrl_content.encode("utf-8"))

# namespace map for finding elements
ns = {
    "svrl": "http://purl.oclc.org/dsdl/svrl",
    "sch": "http://purl.oclc.org/dsdl/schematron",
}

# extract all failed assertions and their roles
results = []
fired_rules = svrl_doc.xpath("//svrl:fired-rule", namespaces=ns)

for rule in fired_rules:
    role = rule.get("role")
    # finding the nearest following failed-asserts
    failed_asserts = rule.xpath("following-sibling::svrl:failed-assert", namespaces=ns)
    for fa in failed_asserts:
        text = (
            fa.find("svrl:text", namespaces=ns).text
            if fa.find("svrl:text", namespaces=ns) is not None
            else "No message"
        )
        location = fa.get("location")
        test_id = fa.get("id")
        results.append(
            {"role": role, "message": text, "location": location, "test_id": test_id}
        )

# printing out results for verification
for result in results:
    print(
        f"Role: {result['role']}, Message: {result['message']}, Location: {result['location']}, Test ID: {result['test_id']}"
    )
