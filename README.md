# argo-probe-oidc

The package contains metrics to handle OIDC tokens. There are two metrics:

* `fetch-access-token`
* `check-refresh-token-expiration`

The former is used for fetching the OIDC access token, and the latter is used to check the validity of the refresh token which is needed for fetching of the access token.

## Synopsis

### fetch-access-token

The probe `fetch-access-token` has several arguments.

```
# /usr/libexec/argo/probes/oidc/fetch-access-token --help
usage: fetch-access-token [-h] [-u URL] --client_id CLIENT_ID --client_secret
                          CLIENT_SECRET --refresh_token REFRESH_TOKEN
                          [--token_file TOKEN_FILE] [-t TIMEOUT]

Nagios probe for fetching OIDC tokens.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL from which the token is fetched
  --client_id CLIENT_ID
                        The identifier of the client
  --client_secret CLIENT_SECRET
                        The secret value of the client
  --refresh_token REFRESH_TOKEN
                        The value of the refresh token
  --token_file TOKEN_FILE
                        File for storing obtained token
  -t TIMEOUT, --timeout TIMEOUT
                        timeout
```

Example execution of the probe:

```
/usr/libexec/argo/probes/oidc/fetch-access-token -u https://aai.egi.eu/auth/realms/egi/protocol/openid-connect/token --client_id <client_id> --client_secret <client_secret> --refresh_token <refresh_token> --token_file /path/to/oidc_token_file -t 60
OK - Access token fetched successfully.
```

### check-refresh-token-expiration

The probe `check-refresh-token-expiration` has two arguments.

```
# /usr/libexec/argo/probes/oidc/check-refresh-token-expiration --help
usage: check-refresh-token-expiration [-h] --token TOKEN [-t TIMEOUT]

Nagios probe for checking refresh token expiration

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Refresh token
  -t TIMEOUT, --timeout TIMEOUT
                        timeout
```

Example execution of the probe:

```
# /usr/libexec/argo/probes/oidc/check-refresh-token-expiration --token <refresh_token> -t 30
OK - Refresh token valid.
```
