import argparse
import datetime
import signal
import sys

import jwt
from argo_probe_oidc.NagiosResponse import NagiosResponse

nagios = NagiosResponse()


class TimeoutError(Exception):
    pass


class timeout:
    def __init__(self, seconds=1, error_message="Timeout"):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


def validate_token(args):
    date_format = "%b %d %Y %H:%M:%S"
    try:
        unix_time = jwt.decode(args.token, verify=False)["exp"]
        expiration_time = datetime.datetime.fromtimestamp(unix_time)
        timedelta = expiration_time - datetime.datetime.today()

        if timedelta.total_seconds() > 0:
            if 15 <= timedelta.days < 30:
                nagios.writeWarningMessage(
                    "Refresh token will expire in %d days on %s" % (
                        timedelta.days, expiration_time.strftime(date_format)
                    )
                )
                nagios.setCode(nagios.WARNING)

            elif 0 <= timedelta.days < 15:
                nagios.writeCriticalMessage(
                    "Refresh token will expire in %d days on %s" % (
                        timedelta.days, expiration_time.strftime(date_format)
                    )
                )
                nagios.setCode(nagios.CRITICAL)

            else:
                nagios.writeOkMessage(
                    "Refresh token valid until %s" % (
                        expiration_time.strftime(date_format)
                    )
                )

        else:
            nagios.writeCriticalMessage(
                "Refresh token is expired (was valid until %s)" %
                expiration_time.strftime(date_format)
            )
            nagios.setCode(nagios.CRITICAL)

        print(nagios.getMsg())

    except jwt.exceptions.DecodeError as e:
        print("UNKNOWN - Token is malformed: %s" % str(e))

    except Exception as e:
        print("UNKNOWN - %s" % str(e))

        nagios.setCode(nagios.UNKNOWN)

    sys.exit(nagios.getCode())


def main():
    parser = argparse.ArgumentParser(
        description="ARGO probe for checking refresh token expiration"
    )
    parser.add_argument(
        "--token", dest="token", type=str, required=True, help="Refresh token"
    )
    parser.add_argument(
        "-t", "--timeout", dest="timeout", type=int, default=5, help="timeout"
    )
    args = parser.parse_args()

    with timeout(seconds=args.timeout):
        validate_token(args)


if __name__ == "__main__":
    main()
