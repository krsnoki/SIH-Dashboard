
from apps.home import blueprint
from flask import render_template, request, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound

states_data = {
    'Andhra Pradesh': ['Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Kadapa', 'Krishna', 'Kurnool', 'Nellore', 'Prakasam', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari'],
    'Arunachal Pradesh': ['Tawang', 'West Kameng', 'East Kameng', 'Papum Pare', 'Kurung Kumey', 'Kra Daadi', 'Lower Subansiri', 'Upper Subansiri', 'West Siang', 'East Siang', 'Siang', 'Upper Siang', 'Lower Siang'],
    'Assam': ['Dhubri', 'Kokrajhar', 'Bongaigaon', 'Barpeta', 'Darrang', 'Goalpara', 'Morigaon', 'Nagaon', 'Kamrup', 'Kamrup Metropolitan', 'Dhemaji', 'Lakhimpur', 'Dibrugarh', 'Tinsukia', 'Jorhat', 'Golaghat'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Purnia', 'Darbhanga', 'Bihar Sharif', 'Arrah', 'Begusarai', 'Katihar', 'Munger', 'Chhapra', 'Danapur', 'Saharsa', 'Hajipur', 'Gopalganj'],
    'Chhattisgarh': ['Raipur', 'Bilaspur', 'Durg', 'Raigarh', 'Korba', 'Jagdalpur', 'Ambikapur', 'Dhamtari', 'Mahasamund', 'Dalli-Rajhara', 'Tilda Newra', 'Manendragarh', 'Rajnandgaon', 'Kanker', 'Kawardha', 'Bhatapara'],
    'Goa': ['North Goa', 'South Goa'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar', 'Junagadh', 'Gandhinagar', 'Nadiad', 'Mehsana', 'Morbi', 'Surendranagar', 'Bharuch', 'Anand', 'Porbandar', 'Godhra'],
    'Haryana': ['Faridabad', 'Gurgaon', 'Rohtak', 'Hisar', 'Panipat', 'Ambala', 'Karnal', 'Sonipat', 'Yamunanagar', 'Panchkula', 'Bhiwani', 'Jind', 'Sirsa', 'Thanesar', 'Kaithal', 'Rewari'],
    'Himachal Pradesh': ['Shimla', 'Kullu', 'Manali', 'Dharamshala', 'Chamba', 'Mandi', 'Solan', 'Nahan', 'Sundarnagar', 'Paonta Sahib', 'Nurpur', 'Palampur', 'Kangra', 'Bilaspur', 'Una'],
    'Jharkhand': ['Ranchi', 'Jamshedpur', 'Dhanbad', 'Bokaro', 'Hazaribagh', 'Deoghar', 'Giridih', 'Ramgarh', 'Dumka', 'Chaibasa', 'Phusro', 'Madhupur', 'Chirkunda', 'Saunda', 'Khunti', 'Rajmahal'],
    'Karnataka': ['Bangalore', 'Mysuru', 'Hubballi', 'Mangaluru', 'Belagavi', 'Shivamogga', 'Ballari', 'Gulbarga', 'Davanagere', 'Vijayapura', 'Raichur', 'Kalaburagi', 'Hassan', 'Bidar', 'Dharwad', 'Udupi'],
    'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Kollam', 'Thrissur', 'Alappuzha', 'Kannur', 'Kottayam', 'Palakkad', 'Malappuram', 'Pathanamthitta', 'Idukki', 'Ernakulam', 'Wayanad', 'Kasaragod'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior', 'Ujjain', 'Sagar', 'Dewas', 'Satna', 'Ratlam', 'Rewa', 'Murwara', 'Singrauli', 'Burhanpur', 'Khandwa', 'Bhind', 'Chhindwara'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad', 'Solapur', 'Thane', 'Amravati', 'Kolhapur', 'Nanded', 'Sangli', 'Jalgaon', 'Akola', 'Latur', 'Dhule', 'Ahmednagar'],
    'Manipur': ['Imphal East', 'Imphal West', 'Thoubal', 'Bishnupur', 'Churachandpur', 'Senapati', 'Ukhrul', 'Tamenglong', 'Jiribam', 'Kakching', 'Chandel', 'Tengnoupal', 'Noney', 'Kamjong', 'Pherzawl'],
    'Meghalaya': ['East Khasi Hills', 'West Khasi Hills', 'East Garo Hills', 'West Garo Hills', 'Jaintia Hills', 'Ri-Bhoi', 'South Garo Hills', 'South West Garo Hills', 'West Jaintia Hills', 'East Jaintia Hills', 'North Garo Hills', 'West Khasi Hills'],
    'Mizoram': ['Aizawl', 'Lunglei', 'Saiha', 'Champhai', 'Serchhip', 'Kolasib', 'Lawngtlai', ' Mamit', 'Hnahthial', 'Khawzawl', 'Saitual'],
    'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung', 'Tuensang', 'Zunheboto', 'Wokha', 'Mon', 'Phek', 'Kiphire', 'Longleng', 'Peren'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Berhampur', 'Sambalpur', 'Puri', 'Balasore', 'Bhadrak', 'Baripada', 'Jharsuguda', 'Bargarh', 'Rayagada', 'Jeypore', 'Angul', 'Dhenkanal'],
    'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda', 'Hoshiarpur', 'Mohali', 'Batala', 'Pathankot', 'Moga', 'Abohar', 'Mansa', 'Firozpur', 'Kapurthala', 'Khanna'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Ajmer', 'Kota', 'Bikaner', 'Sikar', 'Alwar', 'Bharatpur', 'Pali', 'Sirohi', 'Ganganagar', 'Bhilwara', 'Tonk', 'Jhunjhunu', 'Churu'],
    'Sikkim': ['East Sikkim', 'West Sikkim', 'North Sikkim', 'South Sikkim'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Tiruppur', 'Ambattur', 'Madurai', 'Erode', 'Salem', 'Tiruppur', 'Chengalpattu', 'Tiruvallur', 'Kancheepuram', 'Vellore'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Khammam', 'Karimnagar', 'Ramagundam', 'Mahbubnagar', 'Nalgonda', 'Adilabad', 'Suryapet', 'Miryalaguda', 'Jagtial', 'Nirmal', 'Khammam', 'Sangareddy', 'Bodhan'],
    'Tripura': ['West Tripura', 'South Tripura', 'North Tripura', 'Dhalai', 'Khowai', 'Unakoti', 'Gomati', 'Sipahijala', 'Sepahijala', 'Dharmanagar', 'Pratapgarh', 'Ambassa', 'Udaipur', 'Bishalgarh', 'Kailasahar'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Ghaziabad', 'Agra', 'Varanasi', 'Allahabad', 'Meerut', 'Bareilly', 'Aligarh', 'Moradabad', 'Saharanpur', 'Gorakhpur', 'Faizabad', 'Jhansi', 'Muzaffarnagar', 'Mathura'],
    'Uttarakhand': ['Dehradun', 'Haridwar', 'Nainital', 'Rishikesh', 'Almora', 'Haldwani', 'Rudrapur', 'Kashipur', 'Roorkee', 'Pithoragarh', 'Srinagar', 'Kotdwar', 'Ranikhet', 'Mussoorie', 'Tehri'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Asansol', 'Siliguri', 'Bardhaman', 'Malda', 'Habra', 'Kharagpur', 'Ranaghat', 'Haldia', 'Krishnanagar', 'Nabadwip', 'Medinipur', 'Jalpaiguri', 'Balurghat'],
    'Andaman and Nicobar Islands': ['South Andaman', 'North And Middle Andaman', 'Nicobar'],
    'Chandigarh': ['Chandigarh'],
    'Dadra and Nagar Haveli and Daman and Diu': ['Daman', 'Diu', 'Dadra and Nagar Haveli'],
    'Lakshadweep': ['Kavaratti', 'Agatti', 'Amini', 'Andrott', 'Kalpeni', 'Minicoy'],
    'Delhi': ['Central Delhi', 'South Delhi', 'North Delhi', 'East Delhi', 'West Delhi', 'New Delhi', 'North East Delhi', 'North West Delhi', 'South West Delhi', 'South East Delhi'],
    'Puducherry': ['Puducherry', 'Karaikal', 'Yanam', 'Mahe'],
}


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/get_states', methods=['GET'])
def get_states():
    return jsonify({'states': list(states_data.keys())})

@blueprint.route('/get_districts/<state>', methods=['GET'])
def get_districts(state):
    districts = states_data.get(state, [])
    return jsonify({'districts': districts})

# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None



# need on dashboard
# name of crop 
# crop details
# date of sowing
# crop region
# table and dummy data 
    