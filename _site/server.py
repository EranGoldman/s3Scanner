from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    page = ""
    images = ""
    other = ""
    imagesCounter = 0
    otherCounter = 0
    other += "<ul>"
    images += "<ul>"
    with open("interesting_file.txt","r") as f:
        for line in f:
            if ".jpg" in line.lower() or ".gif" in line.lower():
                images += "<li>"
                images += "<a href='" + line+ "'>"
                images += line
                images += "</a></li>"
                imagesCounter += 1
            else:
                other += "<li>"
                other += "<a href='" + line + "'>"
                other += line
                other += "</a></li>"
                otherCounter += 1
    other += "</ul>"
    images += "</ul>"

    page += "<table><tr><td>Images</td><td>other</td></tr>"
    page += "<tr><td>"
    page += str(imagesCounter)
    page += "</td><td>"
    page += str(otherCounter)
    page += "</td></tr>"
    page += "<tr><td>"
    page += images
    page += "</td><td style='vertical-align: top;'>"
    page += other
    page += "</td></tr></table>"

    return page
