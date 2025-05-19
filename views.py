from django.shortcuts import render
import base64
import Database


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

def ProductAction(request):
    if request.method=='POST':
        category = request.POST['category']
        s_category = request.POST['sub_category']
        p_name = request.POST['p_name']
        p_price = request.POST['p_price']
        p_desc = request.POST['p_desc']
        image = request.FILES['image'].read()

        sid = request.session['sid']

        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into products values(null,%s,%s,%s,%s,%s,%s,%s)", (category,s_category, p_name, p_price, p_desc,image,str(sid)))
        con.commit()

        context = {'msg': 'Product Successfully Added'}
        return render(request, 'AdminApp/AddProducts.html', context)

def AddHotels(request):
    return render(request, 'AdminApp/AddHotels.html')

def HotelAction(request):
    if request.method=='POST':
        category = request.POST['category']
        h_name = request.POST['h_name']
        h_price = request.POST['h_price']
        h_desc = request.POST['h_desc']
        image = request.FILES['image'].read()

        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into hotels values(null,%s,%s,%s,%s,%s)", (category, h_name, h_price, h_desc,image))
        con.commit()

        context = {'msg': 'Hostel Successfully Added'}
        return render(request, 'AdminApp/AddHotels.html', context)

def FlightAction(request):
    if request.method=='POST':
        c_name = request.POST['c_name']
        travel_from = request.POST['travel_from']
        travel_to = request.POST['travel_to']
        price = request.POST['price']


        con = Database.connect()
        cur = con.cursor()
        cur.execute("insert into flights values(null,%s,%s,%s,%s)", (c_name, travel_from, travel_to, price))
        con.commit()

        context = {'msg': 'Flight Successfully Added'}
        return render(request, 'AdminApp/AddHotels.html', context)

def ViewAllRequests(request):
    return render(request, 'AdminApp/ViewAllRequests.html')

def ProductsRequest():
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
    cur.execute("select * from p_booking pb, products p where pb.p_id=p.id")
    data = cur.fetchall()
    for d in data:
        status =d[5]
        if status == 'waiting':
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[7] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[11] + "</td>"
            table += "<td>" + d[4] + "</td>"
            table += "<td><a href=/AcceptPRequest?id=" + d[2] + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
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
    return table

def ViewProductsRequest(request):
    table = ProductsRequest()
    context = {'data': table}
    return render(request, 'AdminApp/ViewProductsRequest.html',context)
def AcceptPRequest(request):
    id= request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update p_booking set status='Accepted' where p_id='"+str(id)+"'")
    con.commit()
    table = ProductsRequest()
    context = {'data': table}
    return render(request, 'AdminApp/ViewProductsRequest.html', context)

def HotelsRequest():
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
    cur.execute("select * from h_booking hb, hotels h where hb.p_id=h.id")
    data = cur.fetchall()
    for d in data:
        status=d[5]
        if status =='waiting':
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[7] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[4] + "</td>"
            table += "<td><a href=/AcceptHRequest?id=" + d[2] + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[7] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[4] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "</tr>"

    table += "</table>"
    return table

def ViewHotelsRequest(request):
    table = HotelsRequest()
    context = {'data': table}
    return render(request, 'AdminApp/ViewHotelsRequest.html',context)

def AcceptHRequest(request):
    id= request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update H_booking set status='Accepted' where p_id='"+str(id)+"'")
    con.commit()
    table = HotelsRequest()
    context = {'data': table}
    return render(request, 'AdminApp/ViewHotelsRequest.html', context)

def FlightsRequests():
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
    cur.execute("select * from f_booking fb, flights f where fb.f_id=f.id")
    data = cur.fetchall()
    for d in data:
        status = d[5]
        if status == 'waiting':
            table += "<tr>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[4] + "</td>"
            table += "<td><a href=/AcceptFRequest?id=" + d[2] + ">Accept</a></td>"
            table += "</tr>"
        else:
            table += "<tr>"
            table += "<td>" + d[2] + "</td>"
            table += "<td>" + d[1] + "</td>"
            table += "<td>" + d[8] + "</td>"
            table += "<td>" + d[9] + "</td>"
            table += "<td>" + d[10] + "</td>"
            table += "<td>" + d[4] + "</td>"
            table += "<td>" + d[5] + "</td>"
            table += "</tr>"

    table += "</table>"
    return table
def ViewFlightsRequests(request):
    table = FlightsRequests()
    context={'data':table}
    return render(request, 'AdminApp/ViewFlightsRequest.html', context)

def AcceptFRequest(request):
    id = request.GET['id']
    con = Database.connect()
    cur = con.cursor()
    cur.execute("update f_booking set status='Accepted' where f_id='" + str(id) + "'")
    con.commit()
    table = FlightsRequests()
    context = {'data': table}
    return render(request, 'AdminApp/ViewFlightsRequest.html', context)
