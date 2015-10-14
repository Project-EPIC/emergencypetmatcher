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

  #Top 5 Users who have reported the most Pet Reports
  results["top_5_reporters"] = UserProfile.objects.annotate(num_reports=Count("proposed_related")).order_by('-num_reports')[:5]

  #Top 5 Users who have matched the most pets
  results["top_5_matchers"] = UserProfile.objects.annotate(num_matches=Count("proposed_by_related")).order_by('-num_matches')[:5]

  #Number of Upvotes
  results["num_upvotes"] = PetMatch.objects.aggregate(Count("up_votes"))
  #Number of Downvotes
  results["num_downvotes"] = PetMatch.objects.aggregate(Count("down_votes"))
  #Number of PetMatches voted on (at least once).

  return render_template("stats.html", results=results)

if __name__ == "__main__":
    app.run()