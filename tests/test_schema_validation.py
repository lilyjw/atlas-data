import pytest
from schema import SchemaError, SchemaWrongKeyError

"""
Validates ATLAS data objects against schemas defined in conftest.py.
"""

def test_validate_tactics(tactic_schema, tactics):
    """Validates each tactic dictionary.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        tactic_schema.validate(tactics)
    except SchemaError as e:
        pytest.fail(e.code)

def test_validate_techniques(technique_schema, subtechnique_schema, techniques):
    """Validates each technique dictionary, both top-level and subtechniques.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        # Check if dictionary is a top-level technique
        technique_schema.validate(techniques)
    except SchemaWrongKeyError as wke:
        # Could be a subtechnique
        if wke.code.startswith("Wrong key 'subtechnique-of'"):
            try:
                # Validate the subtechnique
                subtechnique_schema.validate(techniques)
            except SchemaError as se:
                # Fail with any errors
                pytest.fail(se.code)
        else:
            # Otherwise is another key error
            pytest.fail(wke.code)
    except SchemaError as e:
        # Fail with any other technique errors
        pytest.fail(e.code)

def test_validate_case_studies(case_study_schema, case_studies):
    """Validates each case study dictionary.
    Explicitly fails with message to capture more in pytest short test info.
    """
    try:
        case_study_schema.validate(case_studies)
    except SchemaError as e:
        pytest.fail(e.code)