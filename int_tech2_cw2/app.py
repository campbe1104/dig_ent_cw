import os
from flask import Flask, render_template, request
from back import *
import geocoder
from datetime import datetime
from models import db, Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///searches.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def is_valid_country_code(country_code):
    valid_country_codes = [
        "AF", "AX", "AL", "DZ", "AS", "AD", "AO", "AI", "AQ", "AG",
        "AR", "AM", "AW", "AU", "AT", "AZ", "BH", "BS", "BD", "BB",
        "BY", "BE", "BZ", "BJ", "BM", "BT", "BO", "BQ", "BA", "BW",
        "BV", "BR", "IO", "BN", "BG", "BF", "BI", "KH", "CM", "CA",
        "CV", "KY", "CF", "TD", "CL", "CN", "CX", "CC", "CO", "KM",
        "CG", "CD", "CK", "CR", "CI", "HR", "CU", "CW", "CY", "CZ",
        "DK", "DJ", "DM", "DO", "EC", "EG", "SV", "GQ", "ER", "EE",
        "ET", "FK", "FO", "FJ", "FI", "FR", "GF", "PF", "TF", "GA",
        "GM", "GE", "DE", "GH", "GI", "GR", "GL", "GD", "GP", "GU",
        "GT", "GG", "GN", "GW", "GY", "HT", "HM", "VA", "HN", "HK",
        "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IM", "IL", "IT",
        "JM", "JP", "JE", "JO", "KZ", "KE", "KI", "KP", "KR", "KW",
        "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU",
        "MO", "MK", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MQ",
        "MR", "MU", "YT", "MX", "FM", "MD", "MC", "MN", "ME", "MS",
        "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NC", "NZ", "NI",
        "NE", "NG", "NU", "NF", "MP", "NO", "OM", "PK", "PW", "PS",
        "PA", "PG", "PY", "PE", "PH", "PN", "PL", "PT", "PR", "QA",
        "RE", "RO", "RU", "RW", "BL", "SH", "KN", "LC", "MF", "PM",
        "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG",
        "SX", "SK", "SI", "SB", "SO", "ZA", "GS", "SS", "ES", "LK",
        "SD", "SR", "SJ", "SZ", "SE", "CH", "SY", "TW", "TJ", "TZ",
        "TH", "TL", "TG", "TK", "TO", "TT", "TN", "TR", "TM", "TC",
        "TV", "UG", "UA", "AE", "GB", "US", "UM", "UY", "UZ", "VU",
        "VE", "VN", "VG", "VI", "WF", "EH", "YE", "ZM", "ZW"
    ]
    return country_code.upper() in valid_country_codes

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    detected_region = None
    show_info = request.args.get('show_info') == 'True'

    if request.method == 'POST':
        input1 = request.form.get('input1')
        input2 = request.form.get('input2')
        show_info = request.form.get('show_info') == 'on'

        if not input1:
            error_message = "Please enter an artist name."
        else:
            if not input2:
                g = geocoder.ip('me')
                input2 = g.country
                detected_region = f"Detected country: {input2}"
            else:
                if not is_valid_country_code(input2):
                    error_message = "Invalid country code. Please enter a valid ISO 3166-1 alpha-2 code."
                else:
                    detected_region = None

            if not error_message:
                songs = song_list(input2, input1)
                action_url = f"/?show_info={'True' if show_info else 'False'}"


                new_search = Search(artist=input1, country=input2, timestamp=datetime.now())
                db.session.add(new_search)
                db.session.commit()

                return render_template('index.html', songs=songs, detected_region=detected_region,
                                       show_info=show_info, action_url=action_url)

    return render_template('index.html', error_message=error_message, show_info=show_info)

@app.route('/history')
def history():
    searches = Search.query.order_by(Search.timestamp.desc()).all()
    return render_template('history.html', searches=searches)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
