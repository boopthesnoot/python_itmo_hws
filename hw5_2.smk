import os
import collections


IDS = [id for id in os.listdir("./input") if not id.startswith('.')]


rule all:
    input: expand("output/{ids}", ids=IDS)


rule counter:
    input: "input/{file}"
    output: "output/{file}"
    run:
        with open("{}".format(input)) as inp:
            alltext = "".join([i.strip() for i in inp.readlines()]).lower()
            od = collections.OrderedDict(sorted(collections.Counter(alltext).items()))
            with open("{}".format(output), "a") as out:
                for i in od:
                    out.write("{}: {}\n".format(i, od[i]))

