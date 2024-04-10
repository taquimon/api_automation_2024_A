# Deployment

## jenkins
* freestyle
* pipeline

env variables

1. global properties

2. using Envinject plugin
- Properties Content


3. environment (pipeline)
- Use json pipeline config

## Build Steps
### Execute Shell

```shell
python3.11 -V
python3.11 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python3.11 -m pytest todo_api/ -v -s --alluredir reports/allure/allure-results

```

```json
pipeline {
    agent any

    stages {
        stage('python version') {
            steps {
              sh 'python3 --version'
            }
        }
        stage('Run Python Scripts') {
            steps {
                withPythonEnv('python3') {
                    sh 'pip install -r requirements.txt'
                    sh 'python3 -m behave -f allure_behave.formatter:AllureFormatter -o allure-results'
                }
            }
        }
        stage('reports') {
            steps {
                script {
                    allure ([
                        includeProperties: false,
                        jdk:'',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                 }
            }
        }
    }
}

```

### Post build actions
- Allure Reports



## docker

> docker example

```yaml
# imagen con python
FROM python:3

# label del maintainer
LABEL maintainer="edwin.taquichiri@jalasoft.com"

# copy the code to /opt/app folder
COPY . /opt/app
WORKDIR /opt/app

# update system
RUN apt-get update

# install java always add -y option
RUN apt-get install -y default-jre
RUN java -version

# install allure
RUN wget https://github.com/allure-framework/allure2/releases/download/2.18.1/allure_2.18.1-1_all.deb
RUN dpkg -i allure_2.18.1-1_all.deb

# install/upgrade pip
RUN python3 -m pip install --upgrade pip

# install virtualenv librarary/package
RUN python3 -m pip install --user virtualenv

# create virtualenv for the framework
RUN python3 -m venv env

# activate virtual environment
RUN . env/bin/activate

# install requirements
RUN python3 -m pip install -r requirements.txt
```

## GitLab

```yaml
stages:          # List of stages for jobs, and their order of execution
  - test
  - test_pytest

# python version image
image: python:3.11.4

before_script:
  - apt-get update
  - echo "*** install requirements ***"
  - python3 --version
  - echo "Upgrade pip"
  - pip install --upgrade pip
  - pip install pipenv
  - echo "Clean cache pipenv"
  - pipenv run pipenv-resolver --clear
  - echo "Install requirements"
  - pipenv install
  - echo "Set PYTHONPATH"
  - export PYTHONPATH=$PWD
  - echo "*** finish install requirements ***"
  - echo "*** installing java ***"
  - apt-get install default-jre default-jdk -y
  - java -version

unit-test:   # This job runs in the test stage.
  stage: test    # It only starts when the job in the build stage completes successfully.
  script:
    - echo "Running unit tests... This will take about 60 seconds."
    - pipenv run pytest unittests/ --junitxml=logs/report_pytest.xml

linterns:   # This job also runs in the test stage.
  stage: test    # It can run at the same time as unit-test-job (in parallel).
  script:
    - echo "Linting code... This will take about 10 seconds."
    - pipenv run pylint ./folder_tests --rcfile=.pylintrc --report=no

test_pytest:      # This job runs in the deploy stage.
   stage: test_pytest  # It only runs when *both* jobs in the test stage complete successfully.
   script:
     - echo "Deploying application..."
     - pipenv run robot --exclude DEPRECATED -d logs test_cases
     - echo "Application successfully deployed."
```
