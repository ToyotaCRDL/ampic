import os
import subprocess
from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_string('prefix', "tokyo",
                    'prefix of input and output file names', short_name="o")
flags.DEFINE_float('period', "0.7",
                   'period parameter', short_name="p")


def main(argv):
    command = [
        "python",
        os.environ["SUMO_HOME"] + "/tools/randomTrips.py",
        "-n", f"{prefix}.net.xml",
        "-e", "7200",
        "--fringe-factor", "100",
        "--period", str(FLAGS.period),
        "--route-file", f"{prefix}.rou.xml"
    ]
    subprocess.call(command)


if __name__ == '__main__':
    app.run(main)
