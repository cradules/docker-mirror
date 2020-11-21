import logging
import sys
import dockermirror
import ecrlogin
# Log information to stdout. Change log level from "root.setLevel"
root = logging.getLogger()
root.setLevel(logging.INFO)  # Here you can change the log level

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# Login to ecr
ecrlogin.login_docker_client_to_aws_ecr()
# # Run mirroring
dockermirror.run('config.ini')










