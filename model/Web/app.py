from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

def prediction(lst):
    filename = 'model/best.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    pred = '0'
    if request.method == 'POST':
        ram = int(request.form['ram'])
        weight = float(request.form['weight'])
        company = request.form['company'].lower()
        type = request.form['type'].lower()
        os = request.form['os'].lower() if 'os' in request.form else ''
        cpu = request.form['cpu'].lower()
        gpu = request.form['gpu'].lower()
        touchscreen = 1 if request.form.get('touchscreen') == 'on' else 0
        ips = 1 if request.form.get('ips') == 'on' else 0
        k = 1 if request.form.get('k') == 'on' else 0

        feature_list = [ram, weight, touchscreen, ips, k]
        
        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi']
        type_list = ['2in1', 'gaming', 'notebook', 'ultrabook', 'netbook', 'workstation']
        os_list = ['android', 'chrome os', 'linux', 'mac os x', 'no os', 'windows 10', 'windows 10 s', 'windows 7', 'macos']
        cpu_list = ['amd', 'intel', 'i3', 'i5', 'i7']
        gpu_list = ['amd', 'intel', 'nvidia', 'other']

        feature_list.extend([1 if item == company else 0 for item in company_list])
        feature_list.extend([1 if item == type else 0 for item in type_list])
        os_match = [1 if item == os else 0 for item in os_list]
        feature_list.extend(os_match)
        feature_list.extend([1 if item == cpu else 0 for item in cpu_list])
        feature_list.extend([1 if item == gpu else 0 for item in gpu_list])

        feature_list.extend([0, 0, 0, 0, 0, 0, 0])
        
        pred = prediction(feature_list)*320
        
    return render_template("index.html", pred=pred)

if __name__ == '__main__':
    app.run(debug=True)
