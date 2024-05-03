# Validating eCR Messages

This repository is a WIP to conduct validation of eICR messages in Python leveraging a couple of open source tools. The tools are:

- [Saxonc-HE](https://pypi.org/project/saxonche/)
- [SchXslt](https://github.com/schxslt/schxslt)

## [Saxonc-HE](https://github.com/Saxonica/Saxon-HE)

The documentation for the Python API can be found [here](https://www.saxonica.com/saxon-c/doc12/html/saxonc.html). Saxon-HE is an open-source product available under the Mozilla Public License version 2.0.

## SchXslt

SchXslt is copyright (c) by David Maus <dmaus@dmaus.name> and released under the terms of the MIT license.

## Structure

```
.
├── logs
│   ├── check-svrl-results.py
│   └── svrl-output.xml
├── README.md
├── sample-files
│   ├── CDAR2_IG_PHCASERPT_R2_STU1.1_2019APR_SAMPLE_ZIKA.xml
│   ├── CDAR2_IG_PHCASERPT_R2_STU1.1_SAMPLE_MANUAL.xml
│   ├── CDAR2_IG_PHCASERPT_R2_STU1.1_Sample.xml
│   ├── eICR-TC-COVID-DX_20210412_eicr.xml
│   ├── eICR-TC-COVID-LabNeg_20210412_eicr.xml
│   ├── eICR-TC-COVID-Lab-Order_20210412_eicr.xml
│   ├── eICR-TC-COVID-LabPos_20210412_eicr.xml
│   ├── eICR-TC-COVID-Problem_20210412_eicr.xml
│   └── README.md
├── schema
│   ├── CDAR2_IG_PHCASERPT_R2_STU1.1_SCHEMATRON.sch
│   ├── CDAR2_IG_PHCASERPT_R2_STU1.1_SCHEMATRON.xsl
│   ├── convert-sch-to-xslt.py
│   ├── schxslt
│   │   ├── compile
│   │   │   ├── api-2.0.xsl
│   │   │   ├── compile-2.0.xsl
│   │   │   ├── functions.xsl
│   │   │   └── templates.xsl
│   │   ├── compile-for-svrl.xsl
│   │   ├── expand.xsl
│   │   ├── include.xsl
│   │   ├── pipeline-for-svrl.xsl
│   │   ├── pipeline.xsl
│   │   ├── svrl.xsl
│   │   ├── util
│   │   │   └── normalize-svrl.xsl
│   │   └── version.xsl
│   └── voc.xml
└── validate_ecr.py
```

In order to use the Schematron (`.sch`) file, it must first be converted via XSLT to an `.xsl` file. The `convert-sch-to-xslt.py` script does this for you. The `validate_ecr.py` script uses `saxonche` to validate the eICR messages by parsing through the `svrl` output from the validation. In the `logs` directory you'll see the `svrl` output for the file that is selected in the `validate_ecr.py` file. The `check-svrl-results.py` file is an attempt to better structure the results and is still a WIP. This code will be leveraged by the `parse_svrl` function in `validate_ecr.py` when completed.

## Goals

The goal here is to produce `svrl` results that are 1:1 comparable to the [AIMS Validator's](https://validator.aimsplatform.org/) output. Having validation that can be run in a dev or prod environment without needing to de-identify data to send to an online validator would be a boon for many developers working with eICR.
