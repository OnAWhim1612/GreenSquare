from flask import Flask, render_template, request, redirect, session, jsonify
import openai
from PIL import Image
import pytesseract

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Replace with a secret key for session management


@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route('/domestic_result', methods=['GET', 'POST'])
def domestic_result():
    if request.method == 'POST':
        # Handle form submission and session data storage here
        session['name'] = request.form['fullName']
        session['fullName'] = request.form['fullName']
        session['email'] = request.form['email']
        session['location'] = request.form['location']
        session['area'] = float(request.form['area'])
        session['electricityBill'] = float(request.form['electricityBill'])
        session['residents'] = float(request.form['residents'])
        session['eci'] = session['electricityBill'] / (session['residents'] * session['area'])
        session['weeklyWaste'] = float(request.form['weeklyWaste'])/session['residents']
        if  session['eci']>1.5:
            session['cons'] = "Your Energy Consumption is above the reccomended threshold"
        elif session['eci']<1.5 and session['eci']>=0.8:
            session['cons'] = "Your Energy consumption is at the avverage level"
        else:
            session['cons'] = "Your Energy Consumption is below average :)"
        if session['weeklyWaste']>4:
            session['wfeed'] = "Your waste production is above the average"
        elif  session['weeklyWaste']<4 and session['weeklyWaste']>2:
            session['wfeed'] = "Your waste production is at the average"
        else:
            session['wfeed'] = "Your waste production is below the average"
        session['dwellingType'] =   request.form['dwellingType']
        session['indoorPlants'] = request.form['indoorPlants']
        if session['indoorPlants'] == "yes":
            session['pmess'] = "It's awesome that you have indoor plants. Click the button below for more plant suggestions!"
        else:
            session['pmess'] = "Indoor Plants are a great way to bring Fresh Air into your home! Click the button below for suggestions tailored to your needs."

        # Redirect to a confirmation page or perform other actions

    # If the request method is GET, display the form data (if available)
    name = session.get('name', '')
    fullName = session.get('fullName', '')
    email = session.get('email', '')
    location = session.get('location', '')
    area = session.get('area', '')
    electricityBill = session.get('electricityBill', '')
    residents = session.get('residents', '')
    eci = session.get('eci', '')
    weeklyWaste = session.get('weeklyWaste', '')
    cons = session.get('cons', '')
    wfeed = session.get('wfeed', '')
    dwellingType= session.get('dwellingType', '')
    indoorPlants = session.get('indoorPlants', '')
    pmess =  session.get('pmess', '')


    # Retrieve other fields from session as needed

    return render_template('domestic_result.html', name=name, fullName=fullName, email=email, location=location, eci=eci, weeklyWaste = weeklyWaste, cons=cons, wfeed=wfeed, residents = residents, area=area, dwellingType=dwellingType, indoorPlants=indoorPlants, pmess=pmess)


@app.route('/corporate')
def corporate():
    return render_template('corporate.html')

@app.route('/public')
def public():
    return render_template('public.html')

@app.route('/domestic', methods=['GET', 'POST'])
def domestic():
    if request.method == 'POST':
        session['name'] = request.form['fullName']
        session['fullName'] = request.form['fullName']
        session['email'] = request.form['email']
        session['location'] = request.form['location']
        session['area'] = float(request.form['area'])
        session['electricityBill'] = float(request.form['electricityBill'])
        session['residents'] = float(request.form['residents'])
        session['eci'] = session['electricityBill'] / (session['residents'] * session['area'])
        session['weeklyWaste'] = float(request.form['weeklyWaste'])/session['residents']
        if  session['eci']>1.5:
            session['cons'] = "Your Energy Consumption is above the reccomended threshold"
        elif session['eci']<1.5 and session['eci']>=0.8:
            session['cons'] = "Your Energy consumption is at the avverage level"
        else:
            session['cons'] = "Your Energy Consumption is below average :)"
        if session['weeklyWaste']>4:
            session['wfeed'] = "Your waste production is above the average"
        elif  session['weeklyWaste']<4 and session['weeklyWaste']>2:
            session['wfeed'] = "Your waste production is at the average"
        else:
            session['wfeed'] = "Your waste production is below the average"


        return redirect('/domestic_result')
    return render_template('domestic.html')

@app.route('/plant')
def plant():
    return render_template('plant.html')


@app.route('/corporate_result', methods=['GET', 'POST'])
def corporate_result():

    if request.method == 'POST':
        # Handle form submission and session data storage here
        session['companyName'] = request.form['companyName']
        session['contactName'] = request.form['contactName']
        session['email'] = request.form['email']
        session['location'] = request.form['location']
        session['buildingType'] = request.form['buildingType']
        session['floorArea'] = request.form['floorArea']
        session['employees'] = request.form['employees']
        session['wastePractices'] = request.form['wastePractices']
        session['weeklyWaste'] = request.form['weeklyWaste']
        session['greenBuildingCertification'] = request.form['greenBuildingCertification']
        session['commuteOptions'] = request.form['commuteOptions']

    companyName = session.get('companyName', '')
    contactName = session.get('contactName', '')
    email = session.get('email', '')
    location = session.get('location', '')
    buildingType = session.get('buildingType', '')
    floorArea = session.get('floorArea', '')
    employees = session.get('employees', '')
    wastePractices = session.get('wastePractices', '')
    weeklyWaste = session.get('weeklyWaste', '')
    greenBuildingCertification = session.get('greenBuildingCertification', '')
    commuteOptions = session.get('commuteOptions', '')
    return render_template('corporate_result.html', employees=employees, companyName=companyName, contactName=contactName, email=email, location=location, buildingType=buildingType, floorArea=floorArea, wastePractices=wastePractices, weeklyWaste=weeklyWaste, greenBuildingCertification=greenBuildingCertification, commuteOptions=commuteOptions)

@app.route('/audit')
def audit():
    return render_template('energy Audit.html')

@app.route('/ai')
def ai():
    return render_template('ai.html')



@app.route('/placebin', methods=['GET', 'POST'])
def placebin():
    return render_template('placebin.html')


@app.route('/public_result', methods=['POST'])
def public_result():
    if request.method == 'POST':
        # Handle form submission and session data storage here
        session['spaceName'] = request.form['spaceName']
        session['location'] = request.form['location']
        session['spaceType'] = request.form['spaceType']
        session['area'] = request.form['area']
        session['electricityUsage'] = request.form['electricityUsage']
        session['wastePractices'] = request.form['wastePractices']
        session['weeklyWaste'] = request.form['weeklyWaste']
        session['greenFeatures'] = request.form['greenFeatures']
        session['transportationAccess'] = request.form['transportationAccess']

    # Retrieve data from session
    spaceName = session.get('spaceName', '')
    location = session.get('location', '')
    spaceType = session.get('spaceType', '')
    area = session.get('area', '')
    electricityUsage = session.get('electricityUsage', '')
    wastePractices = session.get('wastePractices', '')
    weeklyWaste = session.get('weeklyWaste', '')
    greenFeatures = session.get('greenFeatures', '')
    transportationAccess = session.get('transportationAccess', '')

    return render_template('public_result.html', spaceName=spaceName, location=location, spaceType=spaceType, area=area, electricityUsage=electricityUsage, wastePractices=wastePractices, weeklyWaste=weeklyWaste, greenFeatures=greenFeatures, transportationAccess=transportationAccess)


if __name__ == '__main__':
    app.run(debug=True)
