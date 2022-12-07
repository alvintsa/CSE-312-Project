from flask import Flask, render_template, send_file, request, url_for, redirect, abort, make_response
from pymongo import MongoClient

app = Flask(__name__)

#just making sure framework is installed properly
#execute python app.py
#may need to update interpreter to venv

client = MongoClient("mongo")
mydatabase = client['db']

auction_db = mydatabase['auctions']
listing_db = mydatabase['listings']

def escapeHTML(input):
    return input.replace('&', "&amp;").replace('<', "&lt").replace('>', "&gt")

@app.route('/')
def home_page():
    return render_template('home.html')
@app.route('/home.css')
def home_css():
    return send_file('templates/home.css',mimetype="text/css")
@app.route('/logo.png')
def send_logo():
    return send_file('images/logo.png')

@app.route('/auctions')
def auction_page():
    auctions_vals = list(auction_db.find({}))
    if(auctions_vals != []):
        auctions_vals = list(auction_db.find({}))
        return render_template('auctions/auction.html', auctions_vals=auctions_vals)
    else:
        return render_template('auctions/auction.html')





@app.route('/image-upload', methods=('GET', 'POST'))
def image_load():
    if request.method == 'POST':
        #make sure you escape HTML for all these
        #need to make sure users can't access a different file using /../.
        image_name = 'images/' + request.files['upload'].filename
        request.files['upload'].save(image_name)
        time = escapeHTML(request.form['End_Time'])
        description = escapeHTML(request.form['Description'])
        item_name = escapeHTML(request.form['Item_Name'])

        auction_db.insert_one({'image_name': image_name, 'time': time, 'description': description, 'item_name': item_name}) #insert into database

    return redirect(url_for('auction_page'), code=302)

@app.route('/auctions/<image_name>')
def display_image(image_name):
    return send_file('images/' + image_name, mimetype="image/gif")

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login.css')
def login_css():
    return send_file('templates/login.css',mimetype="text/css")

@app.route('/dog.jpg')
def ret_dog():
    return send_file("images/dog.jpg",mimetype="image/gif")

@app.route('/backdrop.jpg')
def ret_backdrop():
    return send_file("images/backdrop.jpg",mimetype="image/gif")

@app.route('/okabe.jpg')
def ret_okabe():
   return send_file("images/okabe.jpg", mimetype="image/gif")

@app.route('/kurisu.jpg')
def ret_kurisu():
   return send_file("images/kurisu.jpg", mimetype="image/gif")

@app.route('/auction.css')
def auction_css():
   return send_file('templates/auctions/auction.css', mimetype="text/css")

@app.route('/listings')
def listing_page():
    all_listings = listing_db.find({},{"_id":0})
    if all_listings:
        return render_template("listings/all_listings.html", listing_vals=all_listings)
    else:
        return render_template("listings/all_listings.html")
@app.route('/listings.css')
def listing_css():
    return send_file("templates/listings/all_listings.css")
@app.route('/create-listing', methods=('GET','POST'))
def new_listing():
    if request.method == 'POST':
        item_name = request.form["Name"]
        if not item_name:
            return redirect(url_for('listing_page'), code=302)
        item_name = item_name.replace("&","&amp")
        item_name = item_name.replace("<","&lt")
        item_name = item_name.replace(">","&gt")
        item_name = item_name.replace("/", " ")
        item_name = item_name.replace(' ', '-')
        item_description = request.form["Description"]
        if not item_description:
            item_description = "No Description"
        item_description = item_description.replace("&","&amp")
        item_description = item_description.replace("<","&lt")
        item_description = item_description.replace(">","&gt")
        item_price = request.form["Price"]
        if not item_price:
            return redirect(url_for('listing_page'), code=302)
        price_alphabet = ['0','1','2','3','4','5','6','7','8','9','0','.']
        for char in item_price:
            if char not in price_alphabet:
                return redirect(url_for('listing_page'), code=302)
        if not request.files["Image"]:
            return redirect(url_for('listing_page'), code=302)
        else:
            image_name = "images/" + item_name + ".jpg"
            request.files["Image"].save(image_name)
        listing_db.insert_one({"Name":item_name, "Description":item_description, "Price":item_price})
    return redirect(url_for('listing_page'), code=302)
@app.route('/listing/<itemname>')
def listing_image(itemname):
    listing_record = listing_db.find_one({"Name":itemname.replace(".jpg","")})
    if listing_record:
        image_path = "images/" + itemname
        return send_file(image_path,mimetype="image/jpg")
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')