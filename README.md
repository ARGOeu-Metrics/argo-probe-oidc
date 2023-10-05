# argo-probe-oidc

The package contains probe to handle OIDC tokens. There are two probes:

* `fetch-access-token`
* `check-refresh-token-expiration`

`fetch-access-token` probe is used for fetching of OIDC access token. `check-refresh-token-expiration` probe is used to check the validity of refresh token needed for fetching the access token.

## Synopsis

### fetch-access-token

The probe `fetch-access-token` has several arguments. `<CLIENT_ID>`, `<CLIENT_SECRET>`, and `<REFRESH_TOKEN>` arguments are mandatory, and the rest have default values (which can be overridden).

```
# /usr/libexec/argo/probes/oidc/fetch-access-token --help
usage: fetch-access-token [-h] [-u URL] --client_id CLIENT_ID --client_secret
                          CLIENT_SECRET --refresh_token REFRESH_TOKEN
                          [--token_file TOKEN_FILE] [-U USER] [-t TIMEOUT]

ARGO probe for fetching OIDC tokens.

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL from which the token is fetched (default:
                        https://aai.egi.eu/oidc/token)
  --client_id CLIENT_ID
                        identifier of client
  --client_secret CLIENT_SECRET
                        secret value of client
  --refresh_token REFRESH_TOKEN
                        refresh token
  --token_file TOKEN_FILE
                        file for storing obtained token (default:
                        /etc/nagios/globus/oidc)
  -U USER, --user USER  username of user executing the probe (default: nagios)
  -t TIMEOUT, --timeout TIMEOUT
                        timeout in seconds (default: 60)
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

ARGO probe for checking refresh token expiration

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
