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

## Clone sub-modules
If you're not using the latest version of git, you might need to use: `git clone --recurse-submodules`
