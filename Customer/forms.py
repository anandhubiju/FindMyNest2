from tkinter import Widget
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    
    features = forms.MultipleChoiceField(
    choices=Property.FEATURES_CHOICES,
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    required=False
    )
    
    nearby_place= forms.MultipleChoiceField(
    choices=Property.PLACE_CHOICES,
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    required=False
)
        
    class Meta:
        model = Property
        fields = ['thumbnail', 'video', 'owner_name', 'property_type', 'status', 'price', 'area', 'bedrooms',
                  'bathrooms', 'rooms', 'garage', 'address', 'Town', 'state', 'zipcode', 'description',
                  'bulding_age','near_supermarket','near_hospital','major_road', 'floor','floor_no','floor_plan', 'last_renovated', 'whatsapp_no','nearby_place','features']
        widgets = {
            'thumbnail': forms.FileInput(attrs={
                "class": "form-control",
                'id':"thumbnail",
                'onkeyup':"validateImageFile(thumbnailInput)",
                'placeholder': 'Upload Thumbnail'
            }),
            'video': forms.FileInput(attrs={
                "class": "form-control ",
                'id':"video",
                'onkeyup':"validateVideoFile()",
                'placeholder': 'Upload Video',
                'required': False  
            }),
            'floor_plan': forms.FileInput(attrs={
                "class": "form-control",
                'id': "floor_plan",
                'onkeyup': "validateImageFile(floorPlanInput)",
                'placeholder': 'Upload Video',  # Added a comma here
                'required': False  # Changed 'false' to 'False'
            }),
            'owner_name': forms.TextInput(attrs={
                "class": "form-control ",
                'id':"name",
                'placeholder': 'Enter Owner Name'
            }),
            'area': forms.TextInput(attrs={
                "class": "form-control ",
                'id':"area",
                'placeholder': 'Enter Area in Square Feet eg(2000sf|22 lack sf)'
            }),
            'address': forms.TextInput(attrs={
                "class": "form-control ",
                'id':"address",
                'placeholder': 'Enter Owner Name'
            }),
            'Town': forms.TextInput(attrs={
               "class": "form-control ",
                'id':"town",
                'placeholder': 'Enter City'
            }),
             'whatsapp_no': forms.NumberInput(attrs={
                "class": "form-control ",
                'id':"whatsapp_no",
                'onkeyup':"validatePhoneNumber()",
                'placeholder': 'Enter phone number ',
                'min': '0'
            }),
            'price': forms.NumberInput(attrs={
                "class": "form-control ",
                'id':"amount",
                'placeholder': 'Enter Price',
                'min': '0'
            }),
             'zipcode': forms.NumberInput(attrs={
                "class": "form-control",
                'id':"zipcode",
                'placeholder': 'Enter Price'
            }),
             'description': forms.Textarea(attrs={
                "class": "form-control h-120",
                'id':"description",
                'placeholder': 'Enter description'
            }),
            'property_type': forms.Select(attrs={
                "class": "form-control ",
                'id':'propertyType',
                'onchange':'toggleFields()'
            }),
            'status': forms.Select(attrs={
                "class": "form-control ",
                'id':'status'
            }),
            'bathrooms': forms.Select(attrs={
                "class": "form-control ",
                'id':'bathrooms'
            }),
            'bedrooms': forms.Select(attrs={
                "class": "form-control ",
                'id':'bedrooms',
                
            }),
            'rooms': forms.Select(attrs={
                "class": "form-control ",
                'id':'rooms',
                'required': False  
            }),
            'garage': forms.Select(attrs={
                "class": "form-control ",
                'id':'garage',
                'required': False  
            }),
            'state': forms.Select(attrs={
                "class": "form-control ",
                'id':'state'
            }),
            'floor': forms.Select(attrs={
                "class": "form-control ",
                'id':'floor'
            }),
             'floor_no': forms.Select(attrs={
                "class": "form-control ",
                'id':'floor_no'
            }),
            'last_renovated': forms.Select(attrs={
                "class": "form-control ",
                'id':'last_renovated'
            }),
            'bulding_age': forms.Select(attrs={
                "class": "form-control",
                'id':'building_age'
            }),
             'major_road': forms.Select(attrs={
                "class": "form-control",
                'id':'building_age'
            }),
              'near_hospital': forms.Select(attrs={
                "class": "form-control",
                'id':'building_age'
            }),
               'near_supermarket': forms.Select(attrs={
                "class": "form-control",
                'id':'building_age'
            }),
            
            
        }
        


            
            
       