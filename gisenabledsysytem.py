from flask import Flask, render_template, request, session
import folium
from geopy.geocoders import Nominatim
from templates.DBConnection import Db


app = Flask(__name__)
app.secret_key = "444"


@app.route('/')
def tourist_login():
    return render_template('tourist/tourist_login.html')


@app.route('/tourist_login_post', methods=['post'])
def tourist_login_post():
    user_name = request.form['mail']
    password = request.form['pass']
    db = Db()
    login_qry = "SELECT * FROM `tourist` WHERE `mail` = '" + user_name + "' AND `password` = '" + password + "'"
    tourist_id = db.selectOne(login_qry)
    print(tourist_id)
    session['lid'] = tourist_id['id']
    if tourist_id is not None:
        return '''<script>alert("login Successfully");window.location='/home'</script>'''
    else:
        return '''<script>alert("Invalid password or username");window.location='/'</script>'''


@app.route('/tourist_signup')
def tourist_signup():
    return render_template('tourist/tourist_signup.html')


@app.route('/tourist_signup_post', methods=['post'])
def tourist_signup_post():
    name = request.form['name']
    mail = request.form['mail']
    password = request.form['pass']
    confirm_pass = request.form['confirm_pass']

    db = Db()

    if name == '' or mail == '' or password == '' or confirm_pass == '':
        return '''<script>alert("fill up all the data");window.location='/tourist_signup'</script>'''
    else:
        if password == confirm_pass:
            signup_query = "INSERT INTO `tourist`(`name`, `password`, `mail`) VALUES ('" + name + "', '" + password + "', '" + mail + "')"
            db.insert(signup_query)
            return '''<script>alert("Inserted Successfully");window.location='/'</script>'''
        else:
            return '''<script>alert("Invalid password or mismatch");window.location='/tourist_signup'</script>'''


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/home')
def home():
    return render_template('tourist/home.html')


# @app.route('/home_post', methods=['post'])
# def home_post():


@app.route('/search_by_place')
def search_by_place():
    return render_template('tourist/search_page.html')


@app.route('/search_by_place_post', methods=['post'])
def search_by_place_post():
    db = Db()
    search = request.form['search']
    geolocator = Nominatim(user_agent="MyApp")

    location = geolocator.geocode(search)
    lat = location.latitude
    lon = location.longitude

    geolocator.reverse("{}, {}".format(lat, lon))
    m = folium.Map(location=[lat, lon], tiles='OpenStreetMap', zoom_start=11)
    folium.Marker(location=[lat, lon], icon=folium.Icon(
        color='red', prefix='fa-solid', icon='fa-utensils')).add_to(m)

    distance = "SELECT *, SQRT(POW(69.1 * (`latitude` - '" + str(lat) + "'), 2) + POW(69.1 * ('" + str(lon) +\
               "' - `longitude`) * COS(`latitude` / 57.3), 2)) AS distance FROM `resorts` HAVING distance < 2500"

    qry = db.select(distance)
    print(qry)
    for i in qry:
        lat = i['latitude']
        lon = i['longitude']

        folium.Marker(location=[lat, lon]).add_to(m)

    return m.get_root().render()


@app.route('/view_packages')
def view_packages():
    return render_template('destination/packages.html')


@app.route('/view_arjunCottage')
def view_arjunCottage():
    return render_template('destination/arjuncottage.html')


@app.route('/view_orion')
def view_orion():
    return render_template('destination/orion.html')


@app.route('/view_hamuse')
def view_hamuse():
    return render_template('destination/hamuse.html')


@app.route('/view_florra')
def view_florra():
    return render_template('destination/florra.html')


@app.route('/agra_details')
def agra_details():
    # db = Db()
    # qry = "SELECT `places`.*, `feedback`.*, `tourist`.* FROM `places` INNER JOIN `feedback` INNER JOIN `tourist` WHERE `places`.`id`=`feedback`.`place_id` AND `places`.`place_name`='Agra'"
    # res = db.select(qry)
    return render_template('destination/agra.html')


@app.route('/munnar_details')
def munnar_details():
    return render_template('destination/munnar.html')


@app.route('/koda_details')
def koda_details():
    return render_template('destination/kodaikkanal.html')


@app.route('/kuttanad_details')
def kuttanad_details():
    return render_template('destination/kuttanad.html')


@app.route('/kashmir_details')
def kashmir_details():
    return render_template('destination/kashmir.html')


@app.route('/write_feedback')
def write_feedback():

    # db = Db()
    # feedback = request.form['feedback']
    # qry = "INSERT INTO `feedback`(`place_id`, `tourist_id`, `feedback`) VALUES ('" + val + "', '" + str(session['lid']) + "', '" + feedback + "')"
    # db.insert(qry)
    return render_template('tourist/feedback.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

