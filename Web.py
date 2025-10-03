from flask import Flask, render_template, request, send_from_directory
import subprocess
import os
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt

# setting variables for directory paths
html_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Front_End"))
style_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Styles"))
bash_dir = os.path.abspath(os.path.dirname(__file__))
web = Flask(__name__, template_folder = html_dir, static_folder = style_dir)

# returns a list where each position is 1 iff the item at the position in items(a list) is present in list(a list)
def search(list, items) :
    result=[]
    for i in items :
        if i in list :
            result.append("1")
        else :
            result.append("0")
    return result

# renders the upload page
@web.route("/", methods=["GET", "POST"])
def upload() :
    if request.method=="GET" :
        return render_template("Upload.html", err="")

@web.route("/display", methods=["POST", "GET"])
def display() :

    if request.method == "GET" :
        return render_template("Display.html")

    # csv generation

    # if the file is uploaded (initialising the csv's for the first time)
    if len(request.files)!=0 :
        file=request.files["upload"]
        filepath=os.path.abspath(os.path.join(bash_dir, file.filename))
        convertpath=os.path.abspath(os.path.join(os.path.dirname(filepath), "Convert.sh"))
        filterpath=os.path.abspath(os.path.join(os.path.dirname(filepath), "Filter.sh"))
        file.save(filepath)
        try :
            subprocess.run(["bash", convertpath, filepath], check=True, text=True)
        except :
            return render_template("Upload.html", err="File contents do not match to a log file.")
        subprocess.run(["bash", filterpath, os.path.abspath(os.path.join(os.path.dirname(__file__),"Table.csv"))], check=True, text=True)

    # if filter is entered by the user
    else :
        from_time=""
        to_time=""
        levels=request.form.getlist("level") if len(request.form.getlist("level"))!=0 and "all" not in request.form.getlist("level") else ["notice", "error"]
        events=request.form.getlist("event") if len(request.form.getlist("event"))!=0 and "all" not in request.form.getlist("event") else ["E1", "E2", "E3", "E4", "E5", "E6"]
        lev_bool=search(levels, ["notice", "error"])
        eve_bool=search(events, ["E1", "E2", "E3", "E4", "E5", "E6"])
        with open(f"{os.path.join(bash_dir, "Summary.csv")}", "r") as file :
            lines=file.readlines()
            from_time=lines[1].strip().split(",")[1] if len(request.form["from"])==0 else request.form["from"]
            to_time=lines[-1].strip().split(",")[1] if len(request.form["to"])==0 else request.form["to"]
        try :
            subprocess.run(["bash", os.path.abspath(os.path.join(os.path.dirname(__file__),"Filter.sh")), os.path.abspath(os.path.join(os.path.dirname(__file__),"Table.csv")), from_time, to_time]+lev_bool+eve_bool, check=True, text=True)
        except :
            return render_template("Display.html", table_msg="Invalid date format.")

    # table making

    with open(f"{os.path.join(html_dir, "Template.html")}", "r") as html :
        paras=html.readlines()
        with open(f"{os.path.join(bash_dir, "Table.csv")}", "r") as csv :
            lines=csv.readlines()
            count=0
            for para in paras :
                if "<thead>" in para :
                    count=paras.index(para)+9
                    break
            for line in lines :
                fields=(line.strip()).split(",")
                if lines.index(line)==0 :
                    for field in fields :
                        paras.insert(count-8+fields.index(field), f"<th>{field}</th>\n")
                else :
                    for field in fields :
                        paras.insert(count, f"<td>{field}</td>\n")
                        count+=1
                    count+=1
                    paras.insert(count, "<tr>\n")
                    count+=1
                    paras.insert(count, "</tr>\n")
        with open(f"{os.path.join(html_dir, "Display.html")}", "w") as output :
            output.seek(0)
            output.writelines(paras)

    return render_template("Display.html")

@web.route("/plots", methods=["POST", "GET"])
def plot() :
    from_time=""
    to_time=""
    levels=["notice", "error"]
    events=["E1", "E2", "E3", "E4", "E5", "E6"]
    lev_bool=search(levels, ["notice", "error"])
    eve_bool=search(events, ["E1", "E2", "E3", "E4", "E5", "E6"])
    pie={"notice": 0, "error": 0}
    bar={"E1": 0, "E2": 0, "E3": 0, "E4": 0, "E5": 0, "E6": 0}
    plot={}
    with open(f"{os.path.join(bash_dir, "Summary.csv")}", "r") as file :
        lines=file.readlines()
        from_time=lines[1].strip().split(",")[1] if len(request.form["from"])==0 else request.form["from"]
        to_time=lines[-1].strip().split(",")[1] if len(request.form["to"])==0 else request.form["to"]
    try :
        subprocess.run(["bash", os.path.abspath(os.path.join(os.path.dirname(__file__),"Filter.sh")), os.path.abspath(os.path.join(os.path.dirname(__file__),"Filtered.csv")), from_time, to_time]+lev_bool+eve_bool, check=True, text=True)
    except :
        return render_template("Display.html", plot_msg="Invalid date format.")
    with open(f"{os.path.join(bash_dir, "Filtered.csv")}", "r") as file :
        lines=file.readlines()
        for line in lines :
            fields=line.strip().split(",")
            if lines.index(line)!=0 :
                pie[fields[2]]+=1
                bar[fields[4]]+=1
                if fields[1] in plot : plot[fields[1]]+=1
                else : plot[fields[1]]=1     
    plt.figure()
    plt.plot([x for x in plot], [plot[x] for x in plot], "b-")
    plt.title("No. of logs vs Time")
    plt.xticks([list(plot.keys())[0], list(plot.keys())[-1]])
    # plt.xticks([plot[x] for x in list(plot) if list(plot).index(x)%100==0])
    plt.savefig(f"{os.path.join(style_dir, 'Line')}")
    plt.close()
    plt.figure()
    plt.pie([(pie["error"]*100)/(pie["notice"]+pie["error"]), (pie["notice"]*100)/(pie["notice"]+pie["error"])], labels=["error", "notice"], autopct='%1.1f%%')
    plt.title("Distribution of notice and errors")
    plt.savefig(f"{os.path.join(style_dir, 'Pie')}")
    plt.close()
    plt.figure()
    plt.bar([x for x in bar], [bar[x] for x in bar], color='r', width=0.5)
    plt.title("Distribution of events")
    plt.savefig(f"{os.path.join(style_dir, 'Bar')}")
    plt.close()
    return render_template("Plots.html")

# downloads a file from styles directory
@web.route("/download/<filename>")
def download(filename) :
    return send_from_directory(style_dir, filename, as_attachment=True)

# downloads a file from back end directory
@web.route("/bash/<filename>")
def bash(filename) :
    return send_from_directory(bash_dir, filename, as_attachment=True)

# generate a filtered csv
@web.route("/generate", methods=["POST", "GET"])
def generate() :
    from_time=""
    to_time=""
    levels=["notice", "error"]
    events=["E1", "E2", "E3", "E4", "E5", "E6"]
    lev_bool=search(levels, ["notice", "error"])
    eve_bool=search(events, ["E1", "E2", "E3", "E4", "E5", "E6"])
    with open(f"{os.path.join(bash_dir, "Summary.csv")}", "r") as file :
        lines=file.readlines()
        from_time=lines[1].strip().split(",")[1] if len(request.form["from"])==0 else request.form["from"]
        to_time=lines[-1].strip().split(",")[1] if len(request.form["to"])==0 else request.form["to"]
    try :
        subprocess.run(["bash", os.path.abspath(os.path.join(os.path.dirname(__file__),"Filter.sh")), os.path.abspath(os.path.join(os.path.dirname(__file__),"Filtered.csv")), from_time, to_time]+lev_bool+eve_bool, check=True, text=True)
    except :
        return render_template("Display.html", download_msg="Invalid date format.")
    return send_from_directory(bash_dir, "Filtered.csv", as_attachment=True)

if(__name__=="__main__") :
    web.run(debug=True)