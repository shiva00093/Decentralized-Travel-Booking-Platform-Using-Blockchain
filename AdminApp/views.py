from django.shortcuts import render
import base64
import Database
from Blockchain import *
from Block import *
from PIL import Image
from io import BytesIO
import pickle
from django.core.files.storage import FileSystemStorage
import random


# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def home(request):
    return render(request,'AdminApp/AdminHome.html')
def RegisterAction(request):
    name = request.POST['fname']
    email = request.POST['email']
    mobile = request.POST['mobile']
    username = request.POST['username']
    password = request.POST['password']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from provider where  email='" + email + "' and mobile='" + mobile + "'")
    d = cur.fetchone()
    if d is not None:
        context = {'msg': 'Already Exist These Details...!!'}
        return render(request, 'AdminApp/Login.html', context)
    else:
        cur = con.cursor()
        cur.execute(
            "insert into provider values(null,'" + name + "','" + email + "','" + mobile + "','" + username + "','" + password + "')")
        con.commit()
        context = {'msg': 'Successfully Registered Service Provider Details...!!'}
        return render(request, 'AdminApp/Login.html', context)


def LogAction(request):
    uname = request.POST['username']
    pwd = request.POST['password']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from provider where username='" + uname + "' and password='" + pwd + "'")
    d = cur.fetchone()
    if d is not None:
        request.session['sid'] = d[0]
        request.session['name'] = d[1]
        request.session['email'] = d[2]
        return render(request, 'AdminApp/AdminHome.html')
    else:
        context = {'msg': 'Login Failed...!!'}
        return render(request, 'AdminApp/Login.html', context)

def AddProducts(request):
    return render(request, 'AdminApp/AddProducts.html')

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def ProductAction(request):
    if request.method=='POST':
        category = request.POST['category']
        s_category = request.POST['sub_category']
        p_name = request.POST['p_name']
        p_price = request.POST['p_price']
        p_desc = request.POST['p_desc']
        image = request.FILES['image']
        filename = request.FILES['image'].name
        sid = request.session['sid']

        db_image = request.FILES['image'].read()

        fs = FileSystemStorage()
        fs.save('./Static/Products/' +filename, image)
        pid = random.randint(1000,9999)

        data = "AddProducts#"+str(pid)+"#"+ category + "#" + s_category + "#" + p_name+"#"+p_price+"#"+p_desc+"#"+filename+"#"+str(sid)
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), 'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain) - 1]
        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into products values(%s,%s,%s,%s,%s,%s,%s,%s)", (pid,category,s_category, p_name, p_price, p_desc,db_image,sid))
        con.commit()

        context = {'msg': 'Product Successfully Added','ph':str(b.previous_hash),'bno':str(b.index),'ch':str(b.hash)}
        return render(request, 'AdminApp/AddProducts.html', context)

def AddHotels(request):
    return render(request, 'AdminApp/AddHotels.html')

def HotelAction(request):
    if request.method=='POST':
        category = request.POST['category']
        h_name = request.POST['h_name']
        h_price = request.POST['h_price']
        h_desc = request.POST['h_desc']
        image = request.FILES['image']
        filename = request.FILES['image'].name
        sid = request.session['sid']

        db_image = request.FILES['image'].read()

        fs = FileSystemStorage()
        fs.save('./Static/Hotels/' + filename, image)
        hid = random.randint(1000, 9999)
        data = "AddHotels#"+str(hid)+"#" + category + "#"+ h_name + "#" + h_price + "#" + h_desc + "#" + filename + "#" + str(sid)
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), 'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain) - 1]
        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into hotels values(%s,%s,%s,%s,%s,%s,%s)", (hid,category, h_name, h_price, h_desc,db_image,sid))
        con.commit()

        context = {'msg': 'Hotel Successfully Added','ph':str(b.previous_hash),'bno':str(b.index),'ch':str(b.hash)}
        return render(request, 'AdminApp/AddHotels.html', context)

def FlightAction(request):
    if request.method=='POST':
        c_name = request.POST['c_name']
        travel_from = request.POST['travel_from']
        travel_to = request.POST['travel_to']
        price = request.POST['price']
        sid = request.session['sid']
        fid = random.randint(1000, 9999)
        data = "AddFlights#" + str(fid) + "#" + c_name + "#" + travel_from + "#" + travel_to + "#" + price +"#" + str(sid)
        enc = blockchain.encrypt(str(data))
        enc = str(base64.b64encode(enc), 'utf-8')
        blockchain.add_new_transaction(enc)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain) - 1]
        blockchain.save_object(blockchain, 'blockchain_contract.txt')

        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into flights values(%s,%s,%s,%s,%s,%s)", (str(fid),c_name, travel_from, travel_to, price,str(sid)))
        con.commit()

        context = {'msg': 'Flight Successfully Added','ph':str(b.previous_hash),'bno':str(b.index),'ch':str(b.hash)}
        return render(request, 'AdminApp/AddHotels.html', context)

def ViewAllRequests(request):
    return render(request, 'AdminApp/ViewAllRequests.html')

def ProductsRequest(sid):

    table = "<table>"
    table += "<tr><th>Customer ID</th>"
    table += "<th>Product ID</th>"
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
    cur.execute("select * from p_booking pb, products p where pb.p_id=p.id and pb.s_id='"+sid+"'")
    data = cur.fetchall()
    for d in data:
        status =d[6]
        if status == 'waiting':
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[12] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td><a href=/AcceptPRequest?id=" + str(d[0]) + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[12] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td>" + d[6] + "</td>"
            table += "</tr>"

    table += "</table>"
    return table

def ViewProductsRequest(request):
    sid = str(request.session['sid'])
    table = ProductsRequest(sid)
    context = {'data': table}
    return render(request, 'AdminApp/ViewProductsRequest.html',context)
def AcceptPRequest(request):
    id= request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update p_booking set status='Accepted' where id='"+str(id)+"'")
    con.commit()
    sid = str(request.session['sid'])
    table = ProductsRequest(sid)
    context = {'data': table}
    return render(request, 'AdminApp/ViewProductsRequest.html', context)

def HotelsRequest(sid):
    table = "<table>"
    table += "<tr><th>Hotel ID</th>"
    table += "<th>Customer ID</th>"
    table += "<th>Hotel</th>"
    table += "<th>Name</th>"
    table += "<th>Price</th>"
    table += "<th>Description</th>"
    table += "<th>Date of Book</th>"
    table += "<th>Status</th>"
    table += "</tr>"
    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from h_booking hb, hotels h where hb.p_id=h.id and hb.s_id='"+sid+"'")
    data = cur.fetchall()
    for d in data:
        status=d[6]
        if status =='waiting':
            table += "<tr>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td><a href=/AcceptHRequest?id=" + str(d[0]) + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td>" + d[6] + "</td>"
            table += "</tr>"

    table += "</table>"
    return table

def ViewHotelsRequest(request):
    sid = str(request.session['sid'])
    print(sid)
    table = HotelsRequest(sid)
    context = {'data': table}
    return render(request, 'AdminApp/ViewHotelsRequest.html',context)

def AcceptHRequest(request):
    id= request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update H_booking set status='Accepted' where id='"+str(id)+"'")
    con.commit()
    sid = str(request.session['sid'])
    table = HotelsRequest(sid)
    context = {'data': table}
    return render(request, 'AdminApp/ViewHotelsRequest.html', context)

def FlightsRequests(sid):
    table = "<table>"
    table += "<tr><th>Flight ID</th>"
    table += "<th>Passenger ID</th>"
    table += "<th>From</th>"
    table += "<th>To</th>"
    table += "<th>Price</th>"
    table += "<th>Date of Book</th>"
    table += "<th>Status</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from f_booking fb, flights f where fb.f_id=f.id  and f.sid='"+sid+"'")
    data = cur.fetchall()
    for d in data:
        status = d[6]
        if status == 'waiting':
            table += "<tr>"
            table += "<td>" + d[3] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td><a href=/AcceptFRequest?id=" + str(d[0]) + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[3] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "<td>" + d[6] + "</td>"
            table += "</tr>"

    table += "</table>"
    return table
def ViewFlightsRequests(request):
    sid = str(request.session['sid'])
    table = FlightsRequests(sid)
    context={'data':table}
    return render(request, 'AdminApp/ViewFlightsRequest.html', context)

def AcceptFRequest(request):
    id = request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update f_booking set status='Accepted' where id='" + str(id) + "'")
    con.commit()
    sid = str(request.session['sid'])
    table = FlightsRequests(sid)
    context = {'data': table}
    return render(request, 'AdminApp/ViewFlightsRequest.html', context)
