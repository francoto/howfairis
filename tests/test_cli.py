import re
from click.testing import CliRunner
from requests_mock import Mocker
from howfairis.cli.cli import cli


runner = CliRunner()


def test_invalid_url():
    runner = CliRunner()
    response = runner.invoke(cli, [""])
    expected_message = "url should start with https://"
    assert response.exception.args[0] == expected_message


def test_url_not_git():
    runner = CliRunner()
    response = runner.invoke(cli, ["https://www.esciencecenter.nl"])
    expected_message = "Repository should be on github.com or on gitlab.com."
    assert response.exception.args[0] == expected_message


def test_url_not_repository():
    runner = CliRunner()
    response = runner.invoke(cli, ["https://github.com/fair-software"])
    expected_message = "url is not a repository"
    assert response.exception.args[0] == expected_message


def test_matching_badge(requests_mock: Mocker):
    owner = "fair-software"
    repo_string = "howfairis"
    filename = "README.rst"
    url = "https://github.com/{0}/{1}".format(owner, repo_string)
    api = "https://api.github.com/repos/{0}/{1}".format(owner, repo_string)
    raw = "https://raw.githubusercontent.com/{0}/{1}/master".format(owner, repo_string)
    howfairis_badge = "https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green"
    pypi_badge = "https://img.shields.io/pypi/v/howfairis.svg?colorB=blue"
    cii_badge = "https://bestpractices.coreinfrastructure.org/projects/4630/badge"
    requests_mock.get(url, status_code=200)
    requests_mock.get(api, json={"default_branch": "master"}, status_code=200)
    requests_mock.get(api + "/license", status_code=200)
    requests_mock.get(raw + "/.howfairis.yml", status_code=200)
    requests_mock.get(raw + "/CITATION", status_code=200)
    requests_mock.get(raw + "/CITATION.cff", status_code=200)
    requests_mock.get(raw + "/codemeta.json", status_code=200)
    requests_mock.get(raw + "/" + filename, text=howfairis_badge+pypi_badge+cii_badge, status_code=200)
    requests_mock.get(raw + "/.zenodo.json", status_code=200)
    requests_mock.get(api + "/commits", status_code=200)
    runner = CliRunner()
    response = runner.invoke(cli, [url])
    assert response.exit_code == 0 and re.search("all good", response.output)


def test_upgraded_badge(requests_mock: Mocker):
    owner = "fair-software"
    repo_string = "howfairis"
    filename = "README.rst"
    url = "https://github.com/{0}/{1}".format(owner, repo_string)
    api = "https://api.github.com/repos/{0}/{1}".format(owner, repo_string)
    raw = "https://raw.githubusercontent.com/{0}/{1}/master".format(owner, repo_string)
    howfairis_badge = "https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow"
    pypi_badge = "https://img.shields.io/pypi/v/howfairis.svg?colorB=blue"
    cii_badge = "https://bestpractices.coreinfrastructure.org/projects/4630/badge"
    requests_mock.get(url, status_code=200)
    requests_mock.get(api, json={"default_branch": "master"}, status_code=200)
    requests_mock.get(api + "/license", status_code=200)
    requests_mock.get(raw + "/.howfairis.yml", status_code=200)
    requests_mock.get(raw + "/CITATION", status_code=200)
    requests_mock.get(raw + "/CITATION.cff", status_code=200)
    requests_mock.get(raw + "/codemeta.json", status_code=200)
    requests_mock.get(raw + "/" + filename, text=howfairis_badge+pypi_badge+cii_badge, status_code=200)
    requests_mock.get(raw + "/.zenodo.json", status_code=200)
    requests_mock.get(api + "/commits", status_code=200)
    runner = CliRunner()
    response = runner.invoke(cli, [url])
    assert response.exit_code == 1 and re.search("Congratulations", response.output)


def test_mismatching_badge(requests_mock: Mocker):
    owner = "fair-software"
    repo_string = "howfairis"
    filename = "README.rst"
    url = "https://github.com/{0}/{1}".format(owner, repo_string)
    api = "https://api.github.com/repos/{0}/{1}".format(owner, repo_string)
    raw = "https://raw.githubusercontent.com/{0}/{1}/master".format(owner, repo_string)
    howfairis_badge = "https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green"
    requests_mock.get(url, status_code=200)
    requests_mock.get(api, json={"default_branch": "master"}, status_code=200)
    requests_mock.get(api + "/license", status_code=200)
    requests_mock.get(raw + "/.howfairis.yml", status_code=200)
    requests_mock.get(raw + "/CITATION", status_code=200)
    requests_mock.get(raw + "/CITATION.cff", status_code=200)
    requests_mock.get(raw + "/codemeta.json", status_code=200)
    requests_mock.get(raw + "/" + filename, text=howfairis_badge, status_code=200)
    requests_mock.get(raw + "/.zenodo.json", status_code=200)
    requests_mock.get(api + "/commits", status_code=200)
    runner = CliRunner()
    response = runner.invoke(cli, [url])
    assert response.exit_code == 1 and re.search("different from", response.output)


def test_missing_badge(requests_mock: Mocker):
    owner = "fair-software"
    repo_string = "howfairis"
    filename = "README.rst"
    url = "https://github.com/{0}/{1}".format(owner, repo_string)
    api = "https://api.github.com/repos/{0}/{1}".format(owner, repo_string)
    raw = "https://raw.githubusercontent.com/{0}/{1}/master".format(owner, repo_string)
    requests_mock.get(url, status_code=200)
    requests_mock.get(api, json={"default_branch": "master"}, status_code=200)
    requests_mock.get(api + "/license", status_code=200)
    requests_mock.get(raw + "/.howfairis.yml", status_code=200)
    requests_mock.get(raw + "/CITATION", status_code=200)
    requests_mock.get(raw + "/CITATION.cff", status_code=200)
    requests_mock.get(raw + "/codemeta.json", status_code=200)
    requests_mock.get(raw + "/" + filename, text="", status_code=200)
    requests_mock.get(raw + "/.zenodo.json", status_code=200)
    requests_mock.get(api + "/commits", status_code=200)
    runner = CliRunner()
    response = runner.invoke(cli, [url])
    assert response.exit_code == 1 and re.search("It seems", response.output)
