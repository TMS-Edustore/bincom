from flask import Flask, render_template, request, redirect, url_for
from models import db, PollingUnit, AnnouncedPUResult, LGA

app = Flask(__name__)

# Configure connection to MariaDB (MySQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://bincom:bincom@localhost/bincom_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)


# ----------------------
# ROUTES
# ----------------------

@app.route('/')
def home():
    polling_units = PollingUnit.query.all()
    return render_template('index.html', polling_units=polling_units)
    # return render_template('index.html')


# @app.route('/polling_unit_results', methods=['GET', 'POST'])
# def select_polling_unit():
#     if request.method == 'POST':
#         polling_unit_id = request.form.get('polling_unit_id')
#         return redirect(url_for('polling_unit_results', polling_unit_id=polling_unit_id))
    
#     polling_units = PollingUnit.query.all()
#     return render_template('select_polling_unit.html', polling_units=polling_units)

@app.route('/polling_unit_results/<int:polling_unit_id>')
def polling_unit_results(polling_unit_id):
    print(f"Polling Unit ID: {polling_unit_id}")
    polling_unit = PollingUnit.query.filter_by(polling_unit_id=polling_unit_id).first()
    if not polling_unit:
        return f"Polling unit with ID {polling_unit_id} not found."

    results = AnnouncedPUResult.query.filter_by(polling_unit_uniqueid=polling_unit.uniqueid).all()
    return render_template('polling_unit_results.html', polling_unit=polling_unit, results=results)


@app.route('/lga-results', methods=['GET', 'POST'])
def lga_results():
    lgas = LGA.query.all()
    total_scores = {}

    if request.method == 'POST':
        lgas = LGA.query.all()
        total_scores = {}
        selected_lga_id = int(request.form['lga_id'])
        print(f"Selected LGA ID: {selected_lga_id}")
        polling_units = PollingUnit.query.filter_by(lga_id=selected_lga_id).all()
        # print(polling_units)

        all_results = []
        for pu in polling_units:
            print(f'polling unit unique_id {pu.uniqueid}')
            pu_results = AnnouncedPUResult.query.filter_by(polling_unit_uniqueid=pu.polling_unit_id).all()
            all_results.extend(pu_results)
            print(f"Polling Unit id: {pu.uniqueid}, polling unit Results: {pu_results}")

        # Sum total scores per party
        for result in all_results:
            party = result.party_abbreviation
            total_scores[party] = total_scores.get(party, 0) + result.party_score
            print(f"Party: {party}, Score: {result.party_score}, Total: {total_scores[party]}")

        # print(f"Selected LGA ID 2: {selected_lga_id}")
        selected_lga = LGA.query.filter_by(lga_id=selected_lga_id).first()
        print(f"Selected LGA data: {selected_lga.lga_id}")
        return render_template('lga_results.html', lgas=lgas, selected_lga=selected_lga, total_scores=total_scores)

    return render_template('lga_results.html', lgas=lgas)


@app.route('/add-result', methods=['GET', 'POST'])
def add_result():
    if request.method == 'POST':
        uniqueid = request.form['polling_unit_uniqueid']
        party = request.form['party_abbreviation']
        score = int(request.form['party_score'])

        new_result = AnnouncedPUResult(
            polling_unit_uniqueid=uniqueid,
            party_abbreviation=party,
            party_score=score,
            entered_by_user='admin',
            date_entered=db.func.now(),
            user_ip_address=request.remote_addr
        )
        db.session.add(new_result)
        db.session.commit()
        return redirect(url_for('home'))

    polling_units = PollingUnit.query.all()
    return render_template('add_result.html', polling_units=polling_units)



@app.route('/lga-polling-results', methods=['GET', 'POST'])
def lga_polling_results():
    lgas = LGA.query.all()
    
    # Fetch all distinct parties for dropdown
    parties = db.session.query(AnnouncedPUResult.party_abbreviation).distinct().all()
    parties = [p[0] for p in parties]  # Flatten to list

    selected_lga = None
    selected_party = None
    results_by_pu = []

    if request.method == 'POST':
        selected_lga_id = int(request.form['lga_id'])
        selected_party = request.form.get('party', '').strip()

        # Get selected LGA
        selected_lga = LGA.query.filter_by(lga_id=selected_lga_id).first()

        if selected_lga:
            polling_units = PollingUnit.query.filter_by(lga_id=selected_lga.lga_id).all()

            for pu in polling_units:
                # Get results per polling unit, with optional party filter
                query = AnnouncedPUResult.query.filter_by(polling_unit_uniqueid=pu.uniqueid)
                if selected_party:  # Filter by party if selected
                    query = query.filter_by(party_abbreviation=selected_party)

                results = query.all()

                results_by_pu.append({
                    'polling_unit': pu,
                    'results': results
                })

    return render_template(
        'lga_polling_results.html',
        lgas=lgas,
        parties=parties,
        selected_lga=selected_lga,
        selected_party=selected_party,
        results_by_pu=results_by_pu
    )

# ----------------------
# RUN THE APP
# ----------------------

if __name__ == '__main__':
    app.run(debug=True)
