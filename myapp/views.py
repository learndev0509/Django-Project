from django.shortcuts import render,redirect
from .models import User,Contact,Product,Wishlist,Cart,Transaction,Subscribe,Reviews
from django.conf import settings
from django.core.mail import send_mail
import random
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):	
	reviews=Reviews.objects.all()
	try:
		user=User.objects.get(email=request.session['email'])
		if user.usertype=="user":
			return render(request,'index.html')
		else:
			return render(request,'seller_index.html')
	except:
		return render(request,'index.html',{'reviews':reviews})


def about(request):
	return render(request,'about.html')

def more_about(request):
	return render(request,'more_about.html')

def computer(request):
	return render(request,'computer.html')

def contact(request):
	if request.method=="POST":
		contact=Contact.objects.create(
				name=request.POST['name'],
				email=request.POST['email'],
				mobile=request.POST['mobile'],
				message=request.POST['message']
			)
		subject = 'Contact To CLA'
		message = 'Hello '+contact.name+',' + '\n We noticed that you recently ran a query that took a while to return results in CLA- sorry for the wait! \nWe are reaching out to let you know that we have taken note of this query and we will do what we can to make it faster in future.' + '\n \n In the meantime , feel free to reach out to us if you countinue to see not responsed by any department of CLA, We will take a action soon.' +'\nThanks For Coordinate.'+ '\n-Team Developer2022'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [request.POST['email'], ]
		send_mail( subject, message, email_from, recipient_list )

		msg="Contact saved Successfully"
		return render(request,'contact.html',{'msg':msg})

	else:
		return render(request,'contact.html')


def laptop(request):
	return render(request,'laptop.html')

def product(request):
	return render(request,'product.html')

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(
				email=request.POST['email'],
				password=request.POST['password']
				)
			if user.usertype=="user":
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['address']=user.address
				request.session['profile_pic']=user.profile_pic.url
				wishlist=Wishlist.objects.filter(user=user)
				request.session['wishlist_count']=len(wishlist)
				cart=Cart.objects.filter(user=user,payment_status=False)
				request.session['cart_count']=len(cart)
				return render(request,'index.html')
			else:
				request.session['email']=user.email
				request.session['fname']=user.fname
				request.session['profile_pic']=user.profile_pic.url
				return render(request,'seller_index.html')
		except:
			msg="Email or Password Is Incorrect"
			return render(request,'login.html',{'msg':msg})

	else:
		return render(request,'login.html')

def signup(request):
	if request.method=="POST":
		try:
			User.objects.get(email=request.POST['email'])
			msg="Email Is Already Registered"
			return render(request,'signup.html',{'msg':msg})
		except:
			if request.POST['password']==request.POST['cpassword']:

				User.objects.create(
						usertype=request.POST['usertype'],
						fname=request.POST['fname'],
						lname=request.POST['lname'],
						email=request.POST['email'],
						mobile=request.POST['mobile'],
						address=request.POST['address'],
						password=request.POST['password'],
						profile_pic=request.FILES['profile_pic']

					)
				msg="You Have SignUp Successfully"
				return render(request,'login.html',{'msg':msg})
			else:
				msg="Password & Confirm Password Does Not Matched"
				return render(request,'signup.html',{'msg':msg})
	else:
		return render(request,'signup.html')


def logout(request):
	try:
		del request.session['email']
		del request.session['fname']
		del request.session['profile_pic']
		return render(request,'login.html')
	except:
		return render(request,'login.html')


def change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				del request.session['email']
				del request.session['fname']
				del request.session['profile_pic']
				msg="Your Password Has Been Changed"
				return render(request,'login.html',{'msg':msg})
				
			else:
				msg="Your New Password & Confirm Password Does Not Matched"
				return render(request,'change_password.html',{'msg':msg})
		else:
			msg="Your Old Password Does Not Matched"
			return render(request,'change_password.html',{'msg':msg})
	else:
		return render(request,'change_password.html')

def seller_change_password(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		if user.password==request.POST['old_password']:
			if request.POST['new_password']==request.POST['cnew_password']:
				user.password=request.POST['new_password']
				user.save()
				del request.session['email']
				del request.session['fname']
				del request.session['profile_pic']
				msg="Your Password Has Been Changed"
				return render(request,'login.html',{'msg':msg})
				
			else:
				msg="Your New Password & Confirm Password Does Not Matched"
				return render(request,'seller_change_password.html',{'msg':msg})
		else:
			msg="Your Old Password Does Not Matched"
			return render(request,'seller_change_password.html',{'msg':msg})
	else:
		return render(request,'seller_change_password.html')


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			otp=random.randint(1000,9999)
			subject = 'OTP For Forgot Password'
			message = 'Hello '+user.fname+', Your OTP-' +str(otp)+ ' Is For Forgot Password Verification. ' + '\nThanks For Support.'+ '\n- Team Devloper2022'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			return render(request,'otp.html',{'otp':otp,'email':user.email})

		except:
			msg="Email is Not Registered"
			return render(request,'forgot_password.html',{'msg':msg})

	else:
		return render(request,'forgot_password.html')


def verify_otp(request):
	otp=request.POST['otp']
	uotp=request.POST['uotp']
	email=request.POST['email']

	if otp==uotp:
		return render(request,'new_password.html',{'email':email})

	else:
		msg="Invalid OTP"
		return render(request,'otp.html',{'email':email,'otp':otp,'msg':msg})


def new_password(request):
	email=request.POST['email']
	np=request.POST['new_password']
	cnp=request.POST['cnew_password']

	if np==cnp:
		user=User.objects.get(email=email)
		user.password=np
		user.save()
		msg="Password Updated Successfully"
		return render(request,'login.html',{'msg':msg})

	else:
		msg="Password & Confirm Password Does Not Matched"
		return render(request,'new_password.html',{'msg':msg,'email':email})

def profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Profile Updated Successfully"
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'profile.html',{'user':user,'msg':msg})
	else:
		
		return render(request,'profile.html',{'user':user})
	
def seller_profile(request):
	user=User.objects.get(email=request.session['email'])
	if request.method=='POST':
		user.fname=request.POST['fname']
		user.lname=request.POST['lname']
		user.mobile=request.POST['mobile']
		user.address=request.POST['address']
		try:
			user.profile_pic=request.FILES['profile_pic']
		except:
			pass
		user.save()
		msg="Profile Updated Successfully"
		request.session['profile_pic']=user.profile_pic.url
		return render(request,'seller_profile.html',{'user':user,'msg':msg})
	else:
		
		return render(request,'seller_profile.html',{'user':user})
	
def seller_home(request):
	return render(request,'seller_index.html')

def seller_add_product(request):
	seller=User.objects.get(email=request.session['email'])

	if request.method=="POST":
		Product.objects.create(
			seller=seller,
			product_category=request.POST['product_category'],
			product_name=request.POST['product_name'],
			product_price=request.POST['product_price'],
			product_desc=request.POST['product_desc'],
			product_image=request.FILES['product_image'],
			product_discount=request.POST['product_discount']
			)

		msg="Product Added Successfully"
		return render(request,'seller_add_product.html',{'msg':msg})
	else:
		return render(request,'seller_add_product.html')

def seller_view_product(request):
	seller=User.objects.get(email=request.session['email'])

	products=Product.objects.filter(seller=seller)
	return render(request,'seller_view_product.html',{'products':products})

def seller_product_details(request,pk):
	product=Product.objects.get(pk=pk)
	return render(request,'seller_product_details.html',{'product':product})

def seller_edit_product(request,pk):
	product=Product.objects.get(pk=pk)
	if request.method=="POST":
		product.product_category=request.POST['product_category']
		product.product_name=request.POST['product_name']
		product.product_price=request.POST['product_price']
		product.product_desc=request.POST['product_desc']
		product.product_discount=request.POST['product_discount']
		try:
			product.product_image=request.FILES['product_image']
		except:
			pass
		product.save()
		msg="Product Details Is Updated Successfully"
		return render(request,'seller_edit_product.html',{'product':product,'msg':msg})
	else:
		return render(request,'seller_edit_product.html',{'product':product})


def seller_delete_product(request,pk):
	product=Product.objects.get(pk=pk)
	product.delete()
	msg="Product Deleted Successfully"
	return redirect('seller_view_product')


def product_filter(request,pc):
	products=Product.objects.filter(product_category=pc)
	return render(request,'view_product.html',{'products':products,'pc':pc})


def product_details(request,pk):
	wishlist_flag=False
	cart_flag=False
	product=Product.objects.get(pk=pk)
	reviews=Reviews.objects.filter(product=product)
	try:
		user=User.objects.get(email=request.session['email'])
		Wishlist.objects.get(user=user,product=product)
		wishlist_flag=True
	except:
		pass	

	try:
		user=User.objects.get(email=request.session['email'])
		Cart.objects.get(user=user,product=product,payment_status=False)
		cart_flag=True
	except:
		pass	

	return render(request,'product_details.html',{'product':product,'wishlist_flag':wishlist_flag,'cart_flag':cart_flag,'reviews':reviews})

def add_to_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Wishlist.objects.create(product=product,user=user)
	return redirect('wishlist')

def wishlist(request):
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.filter(user=user)
	request.session['wishlist_count']=len(wishlist)
	return render(request,'wishlist.html',{'wishlist':wishlist})


def remove_from_wishlist(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	wishlist=Wishlist.objects.get(product=product,user=user)
	wishlist.delete()
	return redirect('wishlist')


def add_to_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	Cart.objects.create(product=product,
			user=user,
			product_price=product.product_price,
			total_price=product.product_price
			
			)
	return redirect('cart')


def cart(request):
	net_price=0
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=False)
	
	for i in cart:
		net_price=net_price+i.total_price

	request.session['cart_count']=len(cart)
	return render(request,'cart.html',{'cart':cart,'net_price':net_price})

def remove_from_cart(request,pk):
	product=Product.objects.get(pk=pk)
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.get(product=product,user=user)
	cart.delete()
	return redirect('cart')


def change_qty(request,pk):
	cart=Cart.objects.get(pk=pk)
	cart.product_qty=int(request.POST['product_qty'])
	cart.total_price=cart.product_price*int(request.POST['product_qty'])
	cart.save()
	return redirect('cart')


def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    try:
        
        amount = int(request.POST['amount'])
        
    except:
        return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()
    cart=Cart.objects.filter(user=user,payment_status=False)
    for i in cart:
    	i.payment_status=True
    	i.save()
    cart=Cart.objects.filter(user=user,payment_status=False)
    request.session['cart_count']=len(cart)
    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)


def my_order(request):
	user=User.objects.get(email=request.session['email'])
	cart=Cart.objects.filter(user=user,payment_status=True)
	return render(request,'my_order.html',{'cart':cart,'user':user})


def validate_email(request):
	email=request.GET.get('email')
	print(email)
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)


def subscribe(request):
	if request.method=="POST":
		subscribe=Subscribe.objects.create(
			email=request.POST['email']
			)
		try:
			subject = 'Subscribe To CLA'
			message = 'Dear Customer,'+'\nThanks for the subscribing our site.'+'\nNow onwards you will be notified by our site with the attractive offers on Computers and Lapotops.' +'\n\nThanks For Support.'+'\nPowered by The-CLA'+ '\n-Team Developer2022'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [subscribe.email, ]
			send_mail( subject, message, email_from, recipient_list )
		except:
			pass
		return render(request,'index.html')
	else:
		pass


def reviews(request,pk):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		product=Product.objects.get(pk=pk)
		Reviews.objects.create(
			reviews=request.POST['reviews'],
			user=user,
			product=product
			)
		return render(request,'index.html')
	else:
		pass