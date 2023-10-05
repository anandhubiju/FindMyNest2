from django.shortcuts import render, redirect
from django.urls import reverse
from requests import Request
from django.http import JsonResponse
from .models import Property,Image,PropertyView,Feedback,Wishlist
from .forms import PropertyForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property, Image 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect


@login_required
def addproperty(request):
    if request.method == 'POST':
        print(request.POST)
        
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            
            property_instance = form.save(commit=False)  # Don't save it immediately

           
            property_instance.user = request.user 

            
            selected_features = form.cleaned_data['features']
            features_str = ', '.join(selected_features)
            property_instance.features = features_str
            
            selected_nearby_place = form.cleaned_data['nearby_place']
            nearby_place_str = ', '.join(selected_nearby_place)
            property_instance.nearby_place = nearby_place_str

           
            property_instance.save()

           
            images = request.FILES.getlist('images')
            for image in images:
                
                Image.objects.create(property=property_instance, images=image)

           
            return redirect('/')
    else:
        form = PropertyForm()

    context = {
        'form': form,
        
    }
    return render(request, 'addproperty.html', context)



def submit_comment(request):
    if request.method == 'POST':
        # Check if the user is logged in and has a user profile
        if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
            userprofile = request.user.userprofile
        else:
            userprofile = None

        first_name = request.POST['first_name']
        email = request.POST['email']
        message = request.POST['message']
        property_id = request.POST['property_id']

        # Create a new Feedback instance and save it to the database
        feedback = Feedback(
            userprofile=userprofile,  # Associate feedback with the user's profile
            property_id=property_id,
            first_name=first_name,
            email=email,
            message=message,
        )
        feedback.save()

        # Optionally, you can add a success message
        # messages.success(request, 'Your comment has been posted successfully.')

        # Redirect to the property_single page with the property_id
        return redirect('property_single', property_id=property_id)

    return render(request, 'property-single.html')
    
def add_wishlist(request, property_id):
    # Get the Property object based on the property_id
    property = get_object_or_404(Property, id=property_id)

    # Create a Wishlist object for the current user and the property
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, property=property)
        if created:
            message = f'The property "{property.address}" has been added to your wishlist.'
        else:
            message = f'The property "{property.address}" is already in your wishlist.'
    else:
        # Handle the case where the user is not authenticated
        message = 'You need to be logged in to add properties to your wishlist.'

    # You can pass the message to your template or use it as needed
    # For now, we'll just redirect back to the propertylist view
    return redirect('propertylist')

def delete_wishlist(request, property_id):
    wishlist_item = get_object_or_404(Wishlist, property_id=property_id, user=request.user)
    wishlist_item.delete()
    return redirect('propertylist')

def wishlist_view(request):
    if request.user.is_authenticated:
        # Retrieve the wishlist items for the logged-in user
        wishlist_items = Wishlist.objects.filter(user=request.user)
        # Extract the properties from the wishlist items
        wishlist_properties = [item.property for item in wishlist_items]
        return render(request, 'wishlist.html', {'wishlist_properties': wishlist_properties})
    else:
        # Handle the case when the user is not logged in
        # You can redirect them to the login page or display a message
        return render(request, 'wishlist.html', {'wishlist_properties': None})

def propertylist(request):
    properties = Property.objects.all() 
    property_types = Property.objects.values_list('property_type', flat=True).distinct()
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_property_ids = wishlist_items.values_list('property_id', flat=True)  # Get a list of property IDs = wishlist_items.values_list('property_id', flat=True)  # Get a list of property IDs
    
    print(wishlist_items)
    
    return render(request,'propertylist.html', {'properties': properties,'property_types':property_types,'wishlist_items':wishlist_items,'wishlist_property_ids':wishlist_property_ids})


def property_list_by_type(request, property_type):
   
    properties = Property.objects.filter(property_type=property_type)
    
    context = {
        'properties': properties,
        'selected_property_type': property_type,
        'property_types': property_type
    }
    
    return render(request, 'propertylist_by_type.html', context)


def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)

    if request.user == property.user:
        property.active = False
        property.save()
    
    return redirect('propertylist')

def add_remove_from_wishlist(request):
    property_id = request.POST.get('property_id')
    user = request.user

    try:
        wishlist_item = Wishlist.objects.get(user=user, property_id=property_id)
        wishlist_item.delete()
        added = False
    except Wishlist.DoesNotExist:
        Wishlist.objects.create(user=user, property_id=property_id)
        added = True

    return JsonResponse({'added': added})


def edit_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        
        form = PropertyForm(request.POST, request.FILES, instance=property)
    
        if form.is_valid():
            updated_property = form.save(commit=False)
            
            
            selected_features = form.cleaned_data['features']
            features_str = ', '.join(selected_features)
            updated_property.features = features_str
            
            selected_nearby_place = form.cleaned_data['nearby_place']
            nearby_place_str = ', '.join(selected_nearby_place)
            updated_property.nearby_place = nearby_place_str

            images = request.FILES.getlist('images')
            if images:
                
                Image.objects.filter(property=updated_property).delete()
                
                for image in images:
                    property_image = Image(property=updated_property, images=image)
                    property_image.save()

            updated_property.save()

            return redirect('propertylist') 
    else:
        form = PropertyForm(instance=property)

    return render(request, 'edit_property.html', {'form': form, 'property': property })




def propertysingle(request, property_id):
    
    user=request.user
    property = get_object_or_404(Property, id=property_id)
    feedbacks = Feedback.objects.filter(property=property).order_by('-comment_date')
    
    if request.user != property.user:
        # Increment the view count
        property.view_count += 1
        property.save()

        # Record the user's view
        if request.user.is_authenticated:
            PropertyView.objects.get_or_create(property=property, user=request.user)
        
    images = Image.objects.filter(property=property)
    excluded_property_types = ['Commercial', 'Office', 'Garage']
    features = property.features.split(', ') if property.features else []
    nearby_place = property.nearby_place.split(', ') if property.nearby_place else []
    
    return render(request, 'property-single.html', {'property': property, 'images': images ,user:user,
    'features': features,'nearby_place': nearby_place,'excluded_property_types':excluded_property_types,'feedbacks': feedbacks,})
    


def viewcontact(request, property_id):
    user = request.user
    property = get_object_or_404(Property, id=property_id)
    
    # Assuming you have a function send_welcome_email that sends the welcome email
    send_welcome_email(property.whatsapp_no, user.email, property.owner_name)
    
    # Return an empty HttpResponse with a success message
    
    return HttpResponseRedirect(reverse('property_single', args=[property_id]) + '?alert=Details_Emailed')

def send_welcome_email(whatsapp_no, email, owner_name):
    subject = 'Welcome to FindMyNest'
    message = f"Hello {email},\n\n"
    message += f"Welcome to FindMyNest, your platform for finding your dream property. We are excited to have you join us!\n\n"
    message += f"Here are the contact details of the property owner:\n\n"
    message += f"Owner Name: {owner_name}\n"
    message += f"WhatsApp No: {whatsapp_no}\n\n"
    message += "Please feel free to contact the property owner for more information or to schedule a viewing of the property.\n\n"
    message += "Thank you for choosing FindMyNest. We wish you the best in your property search!\n\n"
    message += "Warm regards,\nThe FindMyNest Team\n\n"
    
    from_email = 'findmynest.info@gmail.com'  # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    
    
    
def like_feedback(request, feedback_id):
    # Check if the request is a POST request
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has already liked the feedback
            if feedback.likes.filter(id=request.user.id).exists():
                # User has already liked, so unlike
                feedback.likes.remove(request.user)
                liked = False
            else:
                # User hasn't liked yet, so like
                feedback.likes.add(request.user)
                liked = True

            # Return a JSON response with the updated like status and count
            return JsonResponse({'liked': liked, 'likes_count': feedback.likes.count()})

    # Return a JsonResponse with an error message if the request is not valid
    return JsonResponse({'error': 'Invalid request'}, status=400)



def update_property(request, property_id):
    
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        
        form = PropertyForm(request.POST, request.FILES, instance=property)
    
        if form.is_valid():
            updated_property = form.save(commit=False)
            
            
            selected_features = form.cleaned_data['features']
            features_str = ', '.join(selected_features)
            updated_property.features = features_str
            
            selected_nearby_place = form.cleaned_data['nearby_place']
            nearby_place_str = ', '.join(selected_nearby_place)
            updated_property.nearby_place = nearby_place_str

            images = request.FILES.getlist('images')
            if images:
                
                Image.objects.filter(property=updated_property).delete()
                
                for image in images:
                    property_image = Image(property=updated_property, images=image)
                    property_image.save()

            updated_property.save()

            return redirect('editprofile') 
    else:
        form = PropertyForm(instance=property)

    return render(request, 'update_property.html', {'form': form, 'property': property })






