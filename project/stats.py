from flask import Flask, render_template
from fixture import *
import pdb

app = Flask(__name__)

@app.route("/")
def status():
  return "UP"

@app.route("/stats/")
def stats():
  results = {}
  results["num_users"] = User.objects.count()
  results["num_petreports"] = PetReport.objects.count()
  results["num_lost_petreports"] = PetReport.objects.filter(status="Lost").count()
  results["num_found_petreports"] = PetReport.objects.filter(status="Found").count()
  results["num_petmatches"] = PetMatch.objects.count()
  return render_template("stats.html", results=results)

if __name__ == "__main__":
    app.run()