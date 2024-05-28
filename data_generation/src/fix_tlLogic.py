from absl import app, flags

import xml.etree.ElementTree as ET
import subprocess
import yaml

FLAGS = flags.FLAGS

flags.DEFINE_string('prefix', "tokyo",
                    'prefix of input and output file names', short_name="o")


def fix_tlLogic(prefix="tokyo", out_prefix="tokyo_fixed"):
    # tmp.net.xml を読み込む
    tree = ET.parse(prefix + '.tmp.net.xml')
    root = tree.getroot()

    # priority_3way.yaml を読み込む
    with open(prefix + ".priority_3way.yaml", "r") as f:
        priority = yaml.safe_load(f)

    # tlLogic (信号機) をそれぞれ編集する。
    for tl in root.findall('tlLogic'):
        n = tl.attrib["id"]

        # 信号機の名前 ("id") を指定して connection を列挙
        connections = root.findall(f".//connection[@tl=\"{n}\"]")
        # リンク番号 (linkIndex) によって "from", "dir" を整理
        fr_list = [""] * len(connections)
        dir_list = [""] * len(connections)
        for con in connections:
            fr, dr, li = con.attrib["from"], con.attrib["dir"], con.attrib["linkIndex"]
            fr_list[int(li)] = fr
            dir_list[int(li)] = dr

        # 信号機の名前 ("id") によって3差路か4差路か判別する
        if "3way" in n:
            # 3差路の場合
            # `from` ごとに linkIndex が振られていると仮定する
            assert(len(connections) == 6)
            fr0, fr1, fr2 = fr_list[0], fr_list[2], fr_list[4]
            assert (fr_list[1] == fr0)
            assert (fr_list[3] == fr1)
            assert (fr_list[5] == fr2)

            # p を非優先道路とする
            # 直進路がない場合、3way_priority.yaml から設定を持ってくる
            p = priority[n] + "to" + n
            # 直進路が2つあればそれらを優先道路にする
            is_straight_0 = (dir_list[0] == "s" or dir_list[1] == "s")
            is_straight_1 = (dir_list[2] == "s" or dir_list[3] == "s")
            is_straight_2 = (dir_list[4] == "s" or dir_list[5] == "s")
            if is_straight_0 and is_straight_1:
                p = fr_list[5]
            if is_straight_1 and is_straight_2:
                p = fr_list[1]
            if is_straight_2 and is_straight_0:
                p = fr_list[3]

            # 信号パターンの生成
            state0 = ["r" if fr == p else "G" for fr in fr_list] # 青赤パターン0: 優先路が青
            state1 = ["G" if fr == p else "r" for fr in fr_list] # 青赤パターン1: 非優先路が青
            state2 = ["r" for fr in fr_list] # 全赤
            state0y = ["r" if fr == "r" else "y" for fr in state0] # 黄赤パターン0: 優先路が黄
            state1y = ["r" if fr == "r" else "y" for fr in state1] # 黄赤パターン1: 非優先路が黄

            # 適当な duration を付けて <phase> の生成
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

            # 生成した <phase> を元のものと置換
            phases = tl.findall("phase")
            for ph in phases:
                tl.remove(ph)
            for ph in [t0, t1, t2, t0y, t1y]:
                tl.append(ph)
        elif "4way" in n:
            # 4差路の場合
            # `from` ごとに linkIndex が振られていると仮定する
            assert(len(connections) == 12)
            fr0, fr1, fr2, fr3 = fr_list[0], fr_list[3], fr_list[6], fr_list[9]
            assert (fr_list[1] == fr0)
            assert (fr_list[2] == fr0)
            assert (fr_list[4] == fr1)
            assert (fr_list[5] == fr1)
            assert (fr_list[7] == fr2)
            assert (fr_list[8] == fr2)
            assert (fr_list[10] == fr3)
            assert (fr_list[11] == fr3)

            # 信号パターンの生成
            state0 = "GGgrrrGGgrrr" # 青赤パターン0
            state1 = "rrrGGgrrrGGg" # 青赤パターン1
            state2 = "rrrrrrrrrrrr" # 全赤
            state0y = "yyyrrryyyrrr" # 黄赤パターン0
            state1y = "rrryyyrrryyy" # 黄赤パターン1

            # 適当な duration を付けて <phase> の生成
            t0 = ET.Element("phase", attrib={"duration": "30", 
                                             "state": state0})
            t1 = ET.Element("phase", attrib={"duration": "30", 
                                             "state": state1})
            t2 = ET.Element("phase", attrib={"duration": "30", 
                                             "state": state2})
            t0y = ET.Element("phase", attrib={"duration": "30", 
                                              "state": "".join(state0y)})
            t1y = ET.Element("phase", attrib={"duration": "30", 
                                              "state": "".join(state1y)})

            # 生成した <phase> を元のものと置換
            phases = tl.findall("phase")
            for ph in phases:
                tl.remove(ph)
            for ph in [t0, t1, t2, t0y, t1y]:
                tl.append(ph)
        else:
            pass

    # net.xml として xml を出力
    tree.write(out_prefix+'.net.xml')


def main(argv):
    prefix = FLAGS.prefix
    fix_tlLogic(prefix=f"{prefix}", out_prefix=prefix)


if __name__ == '__main__':
    app.run(main)
