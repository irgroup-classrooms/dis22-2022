# tests to suppress exit code 5 in GitHub workflow for rai as long as no proper tests are implemented
import pytest


@pytest.mark.ut
def test_unit_suppression():
    return pytest.ExitCode(0)


@pytest.mark.it
def test_integration_suppression():
    return pytest.ExitCode(0)
