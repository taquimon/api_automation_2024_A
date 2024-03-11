## Components of Automation Framework
* Test Data management
* Testing libraries
* Unit Testing
* Integration Testing
* End to End Testing 
* BDD

<img height="500" src="img/test-automation-components.png" width="500"/>

## API Testing Process
![](img/api+process.webp)

## Secrets

1. using env variables
```shell
$ export variable_name=value
$ export API_KEY_TEST=dummykey
```

```python
import os

# Get the secret key from the environment
secret_key = os.environ.get('api_key_test')
print(secret_key)
```
2. Using dotenv
first install python-dotenv
```shell
pip install python-dotenv
```
create .env file

```shell
API_KEY=test-key
API_SECRET=test-secret
```
then load the content of file like this example
```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

print("API_KEY: ", api_key)
print("API_SECRET: ", api_secret)
```

3. Using third party lib

```python
import hvac
def get_token():
    client = hvac.Client(
        url='http://127.0.0.1:8200',
        token='xxxxxx',
    )    

    read_response = client.secrets.kv.read_secret_version(path='')
    
    token = read_response['data']['data']['']
    print(token)
    return token

get_token()
```

## Task 2:

Create basic CRUD like projects example using a different API:
- Authentication
- Create (POST)
- Rad (GET)
- Delete (DELETE)
- Update
- Cleanup

