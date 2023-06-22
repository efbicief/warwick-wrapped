# warwick-wrapped
Warwick Wrapped, a site which summarises your tabula data.

## Getting started
Use `pipenv run flask run` to start the app. Python 3.10 is required.
Make sure to create your own `config.yaml` by modifying `config/example_config.yaml`. Put it in `config/config.yaml`.
This config contains a number of fields:
```
config:
  consumer_secret: "<some b64-encoded secret>"
  consumer_key: "<some url>"
  base_url: "<For local testing, use localhost:5000>"
```

Warwick ITS should give you the `consumer_secret` and `consumer_key` when signing up for OAuth.

## Docker
We use Github actions to create Docker images for Wrapped. You can find the latest package release [here](https://github.com/efbicief/warwick-wrapped/pkgs/container/warwick-wrapped). Note that you should use your favourite container management software to map a config file to `app/config/config.yaml`.

## Docs
This software is deployed using UWCS services. Any documentation is on their Tech Team wiki [here](https://techteam.uwcs.co.uk/en/services/Wrapped).
