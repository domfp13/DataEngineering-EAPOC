# DataEngineering-EAPOC
DataEngineering-EAPOC is a POC (proof of concept) of an Enterprise Architecture Framework that allow to find the relationship between different core business definitions:
* Experience Services: IT channels which enable access to functional services used by the support areas or customers directly. In general terms, IT tools which are part of the customer journey
* Functional Services: These IT services provide business functions and should be aligned to the capabilities centers need.
* Core Services: Tools used by IT to support business functional systems, experience systems, perform system integration, data governance and management, analytics, automation  and finally CI/CD

### Local Testing

```sh
$ cd DataEngineering-EAPOC
$ docker image build -t webapp .
$ docker container run -d -p 8080:80 --name my_app -e PORT=80 webapp
$ docker container run -d -p 8080:80 --name my_app -e PORT=80 -v "%cd%":/webapp webapp
$ curl http://localhost:8080/
```
### Python env
```sh
$ C:/Users/lf188653/AppData/Local/Continuum/anaconda3/Scripts/activate
$ conda activate EAPOC
```
