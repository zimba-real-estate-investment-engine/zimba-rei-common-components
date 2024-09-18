# Zimba Real Estate Engine Common Components
This repo will contain common components whose modules will be referenced by other repositories. In addition API endpoints are also going to be included in this repo.

## FastAPI and Containerization
Below are the current API endpoints that are currently available in this repo.
* deals-api
* investor-profiles-api
* listings-api
* mortgages-api
* underwriters-api

The development environment is containerized using docker-compose. The following commands can be run to start up the containers the development
environment.
```bash 
docker-compose up --build --force-recreate
```
#### TBD: CI/CD is yet to be done.

## Repository Structure with Multiple Modules
Typical structure
```text
project_root/
    ├── package_one/
    │   ├── setup.py
    │   ├── requirements.txt
    │   └── src/
    │       └── package_one/
    │           └── __init__.py
    ├── package_two/
    │   ├── setup.py
    │   ├── requirements.txt
    │   └── src/
    │       └── package_two/
    │           └── __init__.py
    └── common_package/
        ├── setup.py
        ├── requirements.txt
        └── src/
            └── common_package/
                └── __init__.py

```

These modules can be included in the **requirements.txt** as shown below:
```bash
package_one @ git+https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/zimba-real-estate-investment-engine/zimba-rei-common-components.git@main#egg=package_one
```