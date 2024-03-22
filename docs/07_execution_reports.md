## Execute pytest tests
> command example

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s
```

> if only want execute 1 test 

```shell
 python -m pytest todo_api/sections/test_sections.py::TestSection::test_get_section -v -s
```

## Pytest - Grouping the Tests

> Use markers in tests

```python
@pytest.mark.<markername>
```
> Example

```python
@pytest.mark.smoke
```

Those markers should be added in pytest.ini file

```ini
[pytest]
markers =
    update: test for update project
    smoke: test for smoke suite for project endpoint
    create: test for create project
```

After that you can run your tests with command:

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s -m smoke
```

## Reports

### junitxml
> package junitxml is included in pytest

then execute command 

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s --junitxml=report.xml
```


### html
> Install package pytest-html

```shell
pip install pytest-html
```

then execute command 

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s --html=pytest_html_report.html

```

### excel
> Install package pytest-excel
```shell
pip install pytest-excel
```

then execute command 

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s --excelreport=report.xlsx
```

### markdown
> Install package pytest-md-report
```shell
pip install pytest-md-report
```

then execute command 

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s --md-report --md-report-output md_report.md
```

### allure
> Install package allure-pytest

```shell
pip install allure-pytest
```

> then execute command 

```shell
 python -m pytest todo_api/sections/test_sections.py -v -s --alluredir allure-results

```
> Once reports is generated you can see with command:
 
```shell
allure serve allure_results
```

### Send Automated results by teams
You need to install package pymsteams

```shell
pip install pymsteams
```

## References

> Pytest junitxml: https://www.browserstack.com/docs/test-management/upload-reports-cli/frameworks/pytest

> Pytest html: https://pypi.python.org/pypi/pytest-html 

> Pytest excel: https://pypi.python.org/pypi/pytest-excel 

> Pytest Markdown: https://pypi.org/project/pytest-md-report/

> allure pytest: https://allurereport.org/docs/pytest/ , https://allurereport.org/docs/, https://installati.one/install-allure-ubuntu-22-04/

> Teams and weebooks: https://www.datacamp.com/tutorial/how-to-send-microsoft-teams-messages-with-python 