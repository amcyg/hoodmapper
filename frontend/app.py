import os
import json
from flask import Flask, render_template, request

RECOMMENDATIONS_FILE = os.path.join(os.path.dirname(__file__),
                                    'data/recommendations.json')

print RECOMMENDATIONS_FILE


# neighborhood data encapsulator
class NeighborhoodRecs(object):
    def __init__(self):
        with open(RECOMMENDATIONS_FILE, 'rb') as recfile:
            self._recommendations = json.load(recfile)

    def recommend_hoods(self, input_hood):
        items_unsorted = self._recommendations.get(input_hood).items()
        return sorted(items_unsorted, key=lambda x: x[1], reverse=True)


app = Flask(__name__)
app.debug = True

recs = NeighborhoodRecs()


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/recommend')
def recommend():
    source_hood = request.args.get('neighborhood')
    source_city = request.args.get('city')

    recommended_hoods = recs.recommend_hoods(source_hood)

    return render_template('recommend.html', original_hood=source_hood,
                           recommendations=recommended_hoods,
                           recommendations_json=json.dumps(recommended_hoods),
                           )

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
