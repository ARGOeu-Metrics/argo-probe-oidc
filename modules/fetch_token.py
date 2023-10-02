import argparse
import grp
import os
import pwd
import sys

import requests
from argo_probe_oidc.NagiosResponse import NagiosResponse


def main():
    parser = argparse.ArgumentParser(
        description="ARGO probe for fetching OIDC tokens.",
    )
    parser.add_argument(
        "-u", "--url", dest="url", type=str,
        default="https://aai.egi.eu/oidc/token",
        help="URL from which the token is fetched "
             "(default: https://aai.egi.eu/oidc/token)"
    )
    parser.add_argument(
        "--client_id", dest="client_id", type=str, required=True,
        help="identifier of client"
    )
    parser.add_argument(
        "--client_secret", dest="client_secret", type=str, required=True,
        help="secret value of client"
    )
    parser.add_argument(
        "--refresh_token", dest="refresh_token", type=str, required=True,
        help="refresh token"
    )
    parser.add_argument(
        "--token_file", dest="token_file", type=str,
        default="/etc/nagios/globus/oidc",
        help="file for storing obtained token "
             "(default: /etc/nagios/globus/oidc)"
    )
    parser.add_argument(
        "-U", "--user", dest="user", type=str, default="nagios",
        help="username of user executing the probe (default: nagios)"
    )
    parser.add_argument(
        "-t", "--timeout", dest="timeout", type=int, default=60,
        help="timeout in seconds (default: 60)"
    )
    args = parser.parse_args()

    nagios = NagiosResponse("Access token fetched successfully.")

    try:
        response = requests.post(
            args.url,
            auth=(args.client_id, args.client_secret),
            data={
                "client_id": args.client_id,
                "client_secret": args.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": args.refresh_token,
                "scope": "openid email profile eduperson_entitlement"
            },
            timeout=args.timeout
        )
        response.raise_for_status()

        access_token = response.json()["access_token"]

        with open(args.token_file, "w") as f:
            f.write(access_token)

        try:
            uid = pwd.getpwnam(args.user).pw_uid

        except KeyError:
            nagios.writeCriticalMessage(f"No user named '{args.user}'")
            nagios.setCode(nagios.CRITICAL)
            print(nagios.getMsg())
            sys.exit(nagios.getCode())

        try:
            gid = grp.getgrnam(args.user).gr_gid

        except KeyError:
            nagios.writeCriticalMessage(f"No group named '{args.user}'")
            nagios.setCode(nagios.CRITICAL)
            print(nagios.getMsg())
            sys.exit(nagios.getCode())

        os.chown(args.token_file, uid, gid)

        print(nagios.getMsg())
        sys.exit(nagios.getCode())

    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException,
            ValueError,
            KeyError
    ) as e:
        nagios.writeCriticalMessage(str(e))
        nagios.setCode(nagios.CRITICAL)
        print(nagios.getMsg())
        sys.exit(nagios.getCode())

    except IOError as e:
        nagios.writeCriticalMessage("Error creating file: " + str(e))
        nagios.setCode(nagios.CRITICAL)
        print(nagios.getMsg())
        sys.exit(nagios.getCode())

    except Exception as e:
        nagios.writeCriticalMessage(str(e))
        nagios.setCode(nagios.CRITICAL)
        print(nagios.getMsg())
        sys.exit(nagios.getCode())


if __name__ == "__main__":
    main()
