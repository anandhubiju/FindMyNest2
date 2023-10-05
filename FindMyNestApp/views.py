from django.shortcuts import render, redirect
from UserApp.models import CustomUser
from Customer.models import Property
from .models import Subscription,Payment
from django.urls import reverse
from django.views import View
from django.contrib.auth import get_user_model
from .forms import SubscriptionForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
import razorpay
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest



User = get_user_model()

def index(request):
    # Check if the user is authenticated and logged in with Google
    if request.user.is_authenticated:
        if request.user.user_type == CustomUser.ADMIN:
            return redirect(reverse('admindashboard'))
        elif not request.user.phone_no:
            return render(request, 'profile_completion.html', {'user': request.user})

    # Get the 5 most recently added properties based on the 'created_at' field
    recent_properties = Property.objects.order_by('-created_at')[:5]

    # Retrieve subscription features from a specific Subscription instance
    # # You may want to retrieve a specific subscription
    subscription = Subscription.objects.values().first()
    payment = Payment.objects.filter(payment_status=Payment.PaymentStatusChoices.SUCCESSFUL)
# Load the first subscription

    if subscription:
        features_str = subscription['features']  # Get the 'features' field as a string
        features = features_str.split(',') if features_str else []
    else:
        features = []

    # Get unique property types
    property_types = Property.objects.values_list('property_type', flat=True).distinct()

    # For Razorpay integration
    

    # Retrieve subscription data
    subscriptions = Subscription.objects.all()

    # Prepare the context data
    context = {
        'user': request.user,
        'recent_properties': recent_properties,
        'property_types': property_types,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'subscriptions': subscriptions,
        'features': features,# Add features to the context
        'payment':payment
    }

    return render(request, 'index.html', context=context)

def payment(request, sub_id):
    # Use get_object_or_404 to get the Subscription object based on sub_id
        # Retrieve subscription features from a specific Subscription instance
    # You may want to retrieve a specific subscription
    subscriptions = Subscription.objects.all()
    
    sub_type = Subscription.objects.get(pk=sub_id)

    if sub_type:
        features_str = sub_type.features  # Get the 'features' field as a string
        features = features_str.split(',') if features_str else []
    else:
        features = []

    # Get unique property types
    property_types = Property.objects.values_list('property_type', flat=True).distinct()

    # For Razorpay integration
    currency = 'INR'
    amount = sub_type.price  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'  # Define your callback URL here


    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
    )
    payment.sub_type.add(sub_type)

    # Prepare the context data
    context = {
        'user': request.user,
        'property_types': property_types,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'subscriptions': subscriptions,
        'features': features,  # Add features to the context
        'sub_type': sub_type,
    }

    return render(request, 'Payment.html', context)



def about(request):
    property_types = Property.objects.values_list('property_type', flat=True).distinct()
    return render(request,'about.html',{'property_types': property_types})


def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            sub_type = form.cleaned_data['sub_type']
            price = form.cleaned_data['price']
            validity = form.cleaned_data['validity']
            features_list = form.cleaned_data['features'].split(',')
            features_csv = ','.join(features_list)
            

            if Subscription.objects.filter(
                sub_type=sub_type,
                price=price,
                validity=validity,
                features=features_csv
            ).exists():
                
                form.add_error(None, "A subscription with the same data already exists.")
            else:
               
                subscription = form.save(commit=False)
                subscription.features = features_csv
                subscription.save()
                return redirect('admindashboard')
    else:
        form = SubscriptionForm()
    
    return render(request, 'add_subscription.html', {'form': form})
 # Replace 'search.html' with your template

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            if result is not None:
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                amount = int(payment.amount * 100)  # Convert Decimal to paise
                try:
                    # capture the payment
                    razorpay_client.payment.capture(payment_id, amount)
                    payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

                    # Update the order with payment ID and change status to "Successful"
                    payment.payment_id = payment_id
                    payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
                    payment.save()
                    
                    send_welcome_email(payment.user.username, payment.sub_type, payment.amount, payment.user.email)
                    # render success page on successful capture of payment
                    return render(request, 'index.html')
                except:
                    # if there is an error while capturing payment.
                    payment.payment_status = Payment.PaymentStatusChoices.FAILED
                    return render(request, 'paymentfail.html')
            else:
                # if signature verification fails.
                payment.payment_status = Payment.PaymentStatusChoices.FAILED
                return render(request, 'paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
    
def send_welcome_email(username, sub_type, amount, email):
    subject = 'Welcome to FindMyNest'
    message = f"Hello {email},\n\n"
    message += f"Welcome to FindMyNest, your platform for finding your dream property. We are excited to have you join us!\n\n"
    
    # Retrieve the associated subscription object
    subscription = sub_type.first()  # Assuming sub_type is a ManyToMany field

    if subscription:
        message += f"You have subscribed to the {subscription.sub_type} plan, which is valid for {subscription.validity}.\n\n"
    
    message += "Please feel free to contact the property owner for more information or to schedule a viewing of the property.\n\n"
    message += "Thank you for choosing FindMyNest. We wish you the best in your property search!\n\n"
    message += "Warm regards,\nThe FindMyNest Team\n\n"
    
    from_email = 'findmynest.info@gmail.com'  # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
@login_required
def search_property(request):
    query = request.GET.get('query')
    print("Query:", query)

   
    if query:
        properties = Property.objects.filter(
            Q(property_type__icontains=query) | Q(Town__icontains=query) | Q(state__icontains=query) 
        )
    else:
       
        properties = []
    property_data = []
    
    for property in properties:
        
        property_dict = {
            'id': property.pk,
            'thumbnail': property.thumbnail.url,
            'address':  property.address,
            'property_type':  property.property_type,
            'bathrooms':  property.bathrooms,
            'bedrooms':  property.bedrooms,
            'price':  property.price,
            'area':  property.area,
        }
        property_data.append(property_dict)

    return JsonResponse({'property': property_data})