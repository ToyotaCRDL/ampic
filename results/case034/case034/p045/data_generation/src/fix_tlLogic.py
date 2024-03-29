from absl import app, flags

import xml.etree.ElementTree as ET
import subprocess
import yaml

FLAGS = flags.FLAGS

flags.DEFINE_string('prefix', "tokyo",
                    'prefix of input and output file names', short_name="o")


def fix_tlLogic(prefix="tokyo", out_prefix="tokyo_fixed"):

    tree = ET.parse(prefix + '.tmp.net.xml')

    root = tree.getroot()
    with open(prefix + ".priority_3way.yaml", "r") as f:
        priority = yaml.safe_load(f)

    for tl in root.findall('tlLogic'):
        n = tl.attrib["id"]

        connections = root.findall(f".//connection[@tl=\"{n}\"]")
        fr_list = [""] * len(connections)
        dir_list = [""] * len(connections)
        for con in connections:
            fr, dr, li = con.attrib["from"], con.attrib["dir"], con.attrib["linkIndex"]
            fr_list[int(li)] = fr
            dir_list[int(li)] = dr

        phases = tl.findall("phase")

        if "3way" in n:
            p = priority[n] + "to" + n
            print(n, p, ":", fr_list, ":", dir_list)
            if dir_list[1] == "s" and dir_list[2] == "s":
                p = fr_list[5]
            if dir_list[3] == "s" and dir_list[4] == "s":
                p = fr_list[1]
            if dir_list[5] == "s" and dir_list[0] == "s":
                p = fr_list[3]
            state0 = ["r" if fr == p else "G" for fr in fr_list]
            state1 = ["G" if fr == p else "r" for fr in fr_list]
            state0y = ["r" if fr == "r" else "y" for fr in state0]
            state1y = ["r" if fr == "r" else "y" for fr in state1]
            state2 = ["r" for fr in fr_list]
            t0 = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state0)})
            t1 = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state1)})
            t2 = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state2)})
            t0y = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state0y)})
            t1y = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state1y)})
            for ph in phases:
                tl.remove(ph)
            tl.append(t0)
            tl.append(t1)
            tl.append(t2)
            tl.append(t0y)
            tl.append(t1y)
        elif "4way" in n:
            assert(fr_list[0] == fr_list[1])
            assert(fr_list[0] == fr_list[2])
            state0 = "GGgrrrGGgrrr"
            state1 = "rrrGGgrrrGGg"
            state2 = "rrrrrrrrrrrr"
            state0y = "yyyrrryyyrrr"
            state1y = "rrryyyrrryyy"
            t0 = ET.Element("phase", attrib={
                            "duration": "30", "state": state0})
            t1 = ET.Element("phase", attrib={
                            "duration": "30", "state": state1})
            t2 = ET.Element("phase", attrib={
                            "duration": "30", "state": state2})
            t0y = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state0y)})
            t1y = ET.Element("phase", attrib={
                            "duration": "30", "state": "".join(state1y)})
            for ph in phases:
                tl.remove(ph)
            tl.append(t0)
            tl.append(t1)
            tl.append(t2)
            tl.append(t0y)
            tl.append(t1y)
        else:
            pass

    tree.write(out_prefix+'.net.xml')


def main(argv):
    prefix = FLAGS.prefix
    fix_tlLogic(prefix=f"{prefix}", out_prefix=prefix)


if __name__ == '__main__':
    app.run(main)
