import base64

from django.shortcuts import render
import Database
from Blockchain import *
from Block import *
from PIL import Image
from io import BytesIO
import pickle
from django.templatetags.static import static


# Create your views here.
def login(request):
    return render(request,'CustomerApp/Login.html')

def RegisterAction(request):
    name = request.POST['fname']
    email = request.POST['email']
    mobile = request.POST['mobile']
    username = request.POST['username']
    password = request.POST['password']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from customer where  email='" + email + "' and mobile='" + mobile + "'")
    d = cur.fetchone()
    if d is not None:
        context = {'msg': 'Already Exist These Details...!!'}
        return render(request, 'CustomerApp/Login.html', context)
    else:
        cur = con.cursor()
        cur.execute(
            "insert into customer values(null,'" + name + "','" + email + "','" + mobile + "','" + username + "','" + password + "')")
        con.commit()
        context = {'msg': 'Successfully Registered Your Details...!!'}
        return render(request, 'CustomerApp/Login.html', context)

def LogAction(request):
    uname = request.POST['username']
    pwd = request.POST['password']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from customer where username='" + uname + "' and password='" + pwd + "'")
    d = cur.fetchone()
    if d is not None:
        request.session['userid'] = d[0]
        request.session['name'] = d[1]
        request.session['email'] = d[2]
        return render(request, 'CustomerApp/CustomerHome.html')
    else:
        context = {'msg': 'Login Failed...!!'}
        return render(request, 'CustomerApp/Login.html', context)

def home(request):
    return render(request, 'CustomerApp/CustomerHome.html')


def products(request):
    return render(request, 'CustomerApp/SearchProducts.html')

# def fetch_image_blob(id):
#     connection = Database.connect()
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT image FROM products WHERE id=%s", [id])
#         row = cursor.fetchone()
#     return row[0] if row else None

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def viewproducts(category,sub_category):
    output = ""
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'AddProducts' and arr[2]==category and arr[3]==sub_category:
                output += "<div class ='col-lg-4 col-md-4 col-sm-6'>"
                output += "<div class ='tm-home-box-1 tm-home-box-1-2 tm-home-box-1-center'>"
                image_url = static(f'Products/{arr[7]}')
                output += f"<img src='{image_url}' style = 'height:350px;' class ='img-responsive'>"

                output += "<div class ='tm-green-gradient-bg tm-city-price-container'>"
                output += f"<span><a href=/customer/bookproduct?id=" + str(arr[1]) + "&sid="+str(arr[8])+" style='color:white';>Book</a></span>"
                output += "</div>"
                output += f"Product ID: {arr[1]}<br>"
                output += f"Name: {arr[4]}<br> "
                output += f"Model: {arr[5]}<br>"
                output += f"Description: {arr[6]}"

                output += "</div>"
                output += "</div>"
    return output


def SearchAction(request):
    category=request.POST['category']
    sub_category = request.POST['sub_category']

    table = viewproducts(category, sub_category)
    context={'data':table}
    return render(request,'CustomerApp/ViewProducts.html',context)

def bookproduct(request):
    id=str(request.GET['id'])
    sid = str(request.GET['sid'])
    userid=request.session['userid']
    name=request.session['name']

    con=Database.connect()
    cur=con.cursor()
    cur.execute("insert into p_booking values(null,'"+str(userid)+"','"+id+"','"+str(sid)+"','"+name+"',now(),'waiting')")
    con.commit()

    context={'msg':"Product Booked Successfully...!!"}
    return render(request,'CustomerApp/CustomerHome.html',context)


# def fetch_himage_blob(id):
#     connection = Database.connect()
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT image FROM hotels WHERE id=%s", [id])
#         row = cursor.fetchone()
#     return row[0] if row else None

def hotels(request):
    output = ""
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            data = base64.b64decode(data)
            decrypt = blockchain.decrypt(data)
            decrypt = decrypt.decode("utf-8")
            arr = decrypt.split("#")
            if arr[0] == 'AddHotels':
                output += "<div class ='col-lg-4 col-md-4 col-sm-6'>"
                output += "<div class ='tm-home-box-1 tm-home-box-1-2 tm-home-box-1-center'>"
                image_url = static(f'Hotels/{arr[6]}')
                output += f"<img src='{image_url}' style = 'height:350px;' class ='img-responsive'>"

                output += "<div class ='tm-green-gradient-bg tm-city-price-container'>"
                output += f"<span><a href=/customer/bookHotel?id=" + str(arr[1]) + "&sid="+str(arr[7])+" style='color:white';>Book</a></span>"
                output += "</div>"
                output += f"Product ID: {arr[1]}<br>"
                output += f"Category: {arr[2]}<br>"
                output += f"Name: {arr[3]}<br> "
                output += f"Price: {arr[4]}<br>"
                output += f"Description: {arr[5]}"

                output += "</div>"
                output += "</div>"
    context={'data':output}
    return render(request,'CustomerApp/ViewHotels.html',context)

def bookHotel(request):
    id=str(request.GET['id'])
    sid=str(request.GET['sid'])
    userid=request.session['userid']
    name=request.session['name']

    con=Database.connect()
    cur=con.cursor()
    cur.execute("insert into h_booking values(null,'"+str(userid)+"','"+id+"','"+sid+"','"+name+"',now(),'waiting')")
    con.commit()

    context={'msg':"Hotel Booked Successfully...!!"}
    return render(request,'CustomerApp/CustomerHome.html',context)

def flights(request):
    from_flight = ""
    to_flight = ""
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select distinct travel_from from flights")
    data = cur.fetchall()
    for d in data:
        from_flight += "<option>" + d[0] + "</option>"
    from_flight += ""
    cur.execute("select distinct travel_to from flights")
    data = cur.fetchall()
    for d in data:
        to_flight += "<option>" + d[0] + "</option>"

    to_flight += ""

    context = {'from_flight': from_flight,'to_flight':to_flight}
    return render(request, 'CustomerApp/SearchFlights.html',context)

def ViewFlightAction(request):
    from_loc=request.POST['from_loc']
    to_loc = request.POST['to_loc']

    table = "<table>"
    table += "<tr><th>Company Name</th>"
    table += "<th>From Location</th>"
    table += "<th>To Location</th>"
    table += "<th>Price</th>"
    table += "<th>Book</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from flights where travel_from='"+from_loc+"' and travel_to='"+to_loc+"'")
    data = cur.fetchall()
    for d in data:

        table += "<tr>"
        table += "<td>" + d[1] + "</td>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[3] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += "<td><a href=/customer/bookFlight?id=" + str(d[0]) + "&sid="+str(d[5])+">Book</a></td>"
        table += "</tr>"
    table += "</table>"
    context={'data':table}
    return render(request,'CustomerApp/ViewFlights.html',context)

def bookFlight(request):
    id = str(request.GET['id'])
    userid = request.session['userid']
    name = request.session['name']
    sid = request.session['sid']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("insert into f_booking values(null,'" + str(userid) + "','" + id + "','"+str(sid)+"','" + name + "',now(),'waiting')")
    con.commit()

    context = {'msg': "Flight Booked Successfully...!!"}
    return render(request, 'CustomerApp/CustomerHome.html', context)

def ViewBProducts(request):
    iid=str(request.session['userid'])
    table = "<table>"
    table += "<tr><th>Product ID</th>"
    table += "<th>Product Category</th>"
    table += "<th>Sub_Category</th>"
    table += "<th>Name</th>"
    table += "<th>Price</th>"
    table += "<th>Description</th>"
    table += "<th>Date of Book</th>"
    table += "<th>Status</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from p_booking pb, products p where pb.userid='"+iid+"' and pb.p_id=p.id")
    data = cur.fetchall()
    for d in data:
        table += "<tr>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[7] + "</td>"
        table += "<td>" + d[8] + "</td>"
        table += "<td>" + d[9] + "</td>"
        table += "<td>" + d[10] + "</td>"
        table += "<td>" + d[11] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += "<td>" + d[5] + "</td>"
        table += "</tr>"
    table += "</table>"
    context = {'data': table}
    return render(request, 'CustomerApp/ViewBProducts.html', context)

def ViewBHotels(request):
    iid = str(request.session['userid'])
    table = "<table>"
    table += "<tr><th>Hotel ID</th>"
    table += "<th>Hotel</th>"
    table += "<th>Name</th>"
    table += "<th>Price</th>"
    table += "<th>Description</th>"
    table += "<th>Date of Book</th>"
    table += "<th>Status</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from h_booking hb, hotels h where hb.userid='" + iid + "' and hb.p_id=h.id")
    data = cur.fetchall()
    for d in data:
        table += "<tr>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[7] + "</td>"
        table += "<td>" + d[8] + "</td>"
        table += "<td>" + d[9] + "</td>"
        table += "<td>" + d[10] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += "<td>" + d[5] + "</td>"
        table += "</tr>"
    table += "</table>"
    context = {'data': table}
    return render(request, 'CustomerApp/ViewBHotel.html', context)
def ViewBFlights(request):
    iid = str(request.session['userid'])
    table = "<table>"
    table += "<tr><th>Flight ID</th>"
    table += "<th>From</th>"
    table += "<th>To</th>"
    table += "<th>Price</th>"
    table += "<th>Date of Book</th>"
    table += "<th>Status</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from f_booking fb, flights f where fb.userid='" + iid + "' and fb.f_id=f.id")
    data = cur.fetchall()
    for d in data:
        table += "<tr>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[8] + "</td>"
        table += "<td>" + d[9] + "</td>"
        table += "<td>" + d[10] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += "<td>" + d[5] + "</td>"
        table += "</tr>"
    table += "</table>"
    context = {'data': table}
    return render(request, 'CustomerApp/ViewBFlight.html', context)
