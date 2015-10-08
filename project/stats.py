from flask import Flask, render_template
from fixture import *
from django.db.models import Count
import pdb

app = Flask(__name__)

@app.route("/")
def stats():
  results = {}
  results["num_users"] = User.objects.count()
  results["num_petreports"] = PetReport.objects.count()
  results["num_lost_petreports"] = PetReport.objects.filter(status="Lost").count()
  results["num_found_petreports"] = PetReport.objects.filter(status="Found").count()
  results["num_petmatches"] = PetMatch.objects.count()
  top_5_reporters = UserProfile.objects.annotate(num_reports=Count("proposed_related")).order_by('-num_reports')[:5]
  results["top_5_reporters"] = top_5_reporters
  return render_template("stats.html", results=results)

if __name__ == "__main__":
    app.run()