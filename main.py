import os
from flask import Flask, render_template, request, jsonify
from collections import Counter
app = Flask(__name__)


namelist = []
namepointer = -1
optionslist = []
counter = 0
t_titlestr = ""
t_voteoptions = ""
t_typestr = ""


def readstudents():
    with open("./stu", encoding="utf-8") as fp:
        datalist = [x.strip() for x in fp.readlines()]
        datalist = [x for x in datalist if len(x) > 0]
    return datalist


@app.route("/")
def index():
    global namelist
    global namepointer
    global counter
    global t_titlestr
    global t_voteoptions
    global t_typestr
    global optionslist
    namelist = readstudents()
    namepointer = -1
    optionslist = []
    counter = 0
    t_titlestr = ""
    t_voteoptions = ""
    t_typestr = ""
    if os.path.exists("./result.txt"):
        os.remove("./result.txt")
    return render_template("index.html")


@app.route("/vote")
def withname():
    global namelist
    global namepointer
    global counter
    global t_titlestr
    global t_voteoptions
    global t_typestr
    global optionslist
    t_titlestr = request.args.get("titlestr")
    t_voteoptions = request.args.get("voteoptions")
    t_typestr = request.args.get("typestr")
    optionslist = t_voteoptions.split(",")
    if int(t_typestr) == 0:
        # 有记名投票
        namepointer = namepointer + 1
        return render_template("vote.html", pname=namelist[namepointer],
                               t_titlestr=t_titlestr, t_voteoptions=t_voteoptions, t_typestr=t_typestr,
                               optionslist=optionslist)
    else:
        # 无记名投票
        counter = counter + 1
        return render_template("vote.html", pname=counter,
                               t_titlestr=t_titlestr, t_voteoptions=t_voteoptions, t_typestr=t_typestr,
                               optionslist=optionslist)


def writetofile(pname, optionstr):
    with open("./result.txt", "a", encoding="utf-8") as fp:
        fp.writelines(pname + "###" + str(optionstr) + "\n")


def readfromfile():
    with open("./result.txt", "r", encoding="utf-8") as fp:
        datalist = [x.strip() for x in fp.readlines()]
        datalist = [x.split("###")[1] for x in datalist if len(x) > 0]
    counter1 = Counter(datalist)
    resultlist = []
    for k,v in counter1.items():
        resultlist.append((k, v))
    resultlist.sort(key=lambda x: x[1], reverse=True)
    return resultlist


@app.route("/nextperson")
def nextperson():
    global namelist
    global namepointer
    global counter
    global t_titlestr
    global t_voteoptions
    global t_typestr
    global optionslist
    optionstr = request.args.get("optionstr")
    pname = request.args.get("pname")
    writetofile(pname, optionstr)
    if int(t_typestr) == 0:
        # 有记名投票
        namepointer = namepointer + 1
        if namepointer < len(namelist):
            return render_template("vote.html", pname=namelist[namepointer],
                                   t_titlestr=t_titlestr, t_voteoptions=t_voteoptions, t_typestr=t_typestr,
                                   optionslist=optionslist)
        else:
            oplist = readfromfile()
            return render_template("summary.html", oplist=oplist)

    else:
        # 无记名投票
        counter = counter + 1
        if counter <= len(namelist):
            return render_template("vote.html", pname=counter,
                                   t_titlestr=t_titlestr, t_voteoptions=t_voteoptions, t_typestr=t_typestr,
                                   optionslist=optionslist)
        else:
            oplist = readfromfile()
            return render_template("summary.html", oplist=oplist)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8888, debug=True)
