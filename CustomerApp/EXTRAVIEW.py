import base64

from django.shortcuts import render
import Database

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

def fetch_image_blob(id):
    connection = Database.connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM products WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None
def viewproducts(category,sub_category):
    table = "<table>"
    table += "<tr><th>Category</th><th>Sub_Category</th>"
    table += "<th>Product Name</th>"
    table += "<th>Price</th>"
    table += "<th>Description</th>"
    table += "<th>Image</th>"
    table += "<th>Book</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from products where category='" + category + "'and sub_category='" + sub_category + "'")
    data = cur.fetchall()
    for d in data:
        iid = str(d[0])
        image_blob = fetch_image_blob(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')

        table += "<tr>"
        table += "<td>" + d[1] + "</td>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[3] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += "<td>" + d[5] + "</td>"
        table += f"<td><img src='data:images/png;base64,{image_base64}'></td>"
        table += "<td><a href=/customer/bookproduct?id=" + str(d[0]) + ">Book</a></td>"
        table += "</tr>"
    table += "</table>"
    return table
def SearchAction(request):
    category=request.POST['category']
    sub_category = request.POST['sub_category']
    table = viewproducts(category, sub_category)
    context={'data':table}
    return render(request,'CustomerApp/ViewProducts.html',context)

def bookproduct(request):
    id=str(request.GET['id'])
    userid=request.session['userid']
    name=request.session['name']

    con=Database.connect()
    cur=con.cursor()
    cur.execute("insert into p_booking values(null,'"+str(userid)+"','"+id+"','"+name+"',now(),'waiting')")
    con.commit()

    context={'msg':"Product Booked Successfully...!!"}
    return render(request,'CustomerApp/CustomerHome.html',context)


def fetch_himage_blob(id):
    connection = Database.connect()
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM hotels WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None

def hotels(request):
    table = "<table>"
    table += "<tr><th>Category</th>"
    table += "<th>Product Name</th>"
    table += "<th>Price</th>"
    table += "<th>Description</th>"
    table += "<th>Image</th>"
    table += "<th>Book</th>"
    table += "</tr>"

    con = Database.connect()
    cur = con.cursor()
    cur.execute("select * from hotels")
    data = cur.fetchall()
    for d in data:
        iid = str(d[0])
        image_blob = fetch_himage_blob(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')

        table += "<tr>"
        table += "<td>" + d[1] + "</td>"
        table += "<td>" + d[2] + "</td>"
        table += "<td>" + d[3] + "</td>"
        table += "<td>" + d[4] + "</td>"
        table += f"<td><img src='data:images/png;base64,{image_base64}' width='200' height='200'></td>"
        table += "<td><a href=/customer/bookHotel?id=" + str(d[0]) + ">Book</a></td>"
        table += "</tr>"
    table += "</table>"
    context={'data':table}
    return render(request,'CustomerApp/ViewHotels.html',context)

def bookHotel(request):
    id=str(request.GET['id'])
    userid=request.session['userid']
    name=request.session['name']

    con=Database.connect()
    cur=con.cursor()
    cur.execute("insert into h_booking values(null,'"+str(userid)+"','"+id+"','"+name+"',now(),'waiting')")
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
        table += "<td><a href=/customer/bookFlight?id=" + str(d[0]) + ">Book</a></td>"
        table += "</tr>"
    table += "</table>"
    context={'data':table}
    return render(request,'CustomerApp/ViewFlights.html',context)

def bookFlight(request):
    id = str(request.GET['id'])
    userid = request.session['userid']
    name = request.session['name']

    con = Database.connect()
    cur = con.cursor()
    cur.execute("insert into f_booking values(null,'" + str(userid) + "','" + id + "','" + name + "',now(),'waiting')")
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
