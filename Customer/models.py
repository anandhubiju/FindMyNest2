from django.db import models
from UserApp.models import CustomUser,UserProfile

# Create your models here.



class Property(models.Model):
    
    STATE_CHOICES = [
        ('', 'Select an option'),
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    ]
    
    TYPE_CHOICES = [
        ('', 'Select an option'),
        ('Houses', 'Houses'),
        ('Apartment', 'Apartment'),
        ('Villas', 'Villas'),
        ('Commercial', 'Commercial'),
        ('Garage', 'Garage'),
    ]
    
    STATUS_CHOICES = [
        ('', 'Select an option'),
        ('For Sale', 'For Sale'),
    ]
    
    BEDROOM_CHOICES = [
        ('', 'Select an option'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('More than 5', 'More than 5'),
    ]
    
    BATHROOM_CHOICES = [
        ('', 'Select an option'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('More than 5', 'More than 5'),
    ]
    
    FLOOR_CHOICES = [
        ('', 'Select an option'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4')
    ]
    
    AFLOOR_CHOICES = [
    ('', 'Select an option'),
    ('Ground Floor', 'Ground Floor'),
    ('1 Floor', '1 Floor'),
    ('2 Floor', '2 Floor'),
    ('3 Floor', '3 Floor'),
    ('4 Floor', '4 Floor'),
    ('5 Floor', '5 Floor'),
    ('6 Floor', '6 Floor'),
    ('7 Floor', '7 Floor'),
    ('8 Floor', '8 Floor'),
    ('9 Floor', '9 Floor'),
    ('10 Floor', '10 Floor'),
    ('11 Floor', '11 Floor'),
    ('12 Floor', '12 Floor'),
    ('13 Floor', '13 Floor'),
    ('14 Floor', '14 Floor'),
    ('15 Floor', '15 Floor'),
    ('16 Floor', '16 Floor'),
    ('17 Floor', '17 Floor'),
    ('18 Floor', '18 Floor'),
    ('19 Floor', '19 Floor'),
    ('20 Floor', '20 Floor'),
    ('21 Floor', '21 Floor'),
    ('22 Floor', '22 Floor'),
    ('23 Floor', '23 Floor'),
    ('24 Floor', '24 Floor'),
    ('25 Floor', '25 Floor'),
    ('26 Floor', '26 Floor'),
    ('27 Floor', '27 Floor'),
    ('28 Floor', '28 Floor'),
    ('29 Floor', '29 Floor'),
    ('30 Floor', '30 Floor'),
    ('31 Floor', '31 Floor'),
    ('32 Floor', '32 Floor'),
    ('33 Floor', '33 Floor'),
    ('34 Floor', '34 Floor'),
    ('35 Floor', '35 Floor'),
    ('36 Floor', '36 Floor'),
    ('37 Floor', '37 Floor'),
    ('38 Floor', '38 Floor'),
    ('39 Floor', '39 Floor'),
    ('40 Floor', '40 Floor'),
    ('41 Floor', '41 Floor'),
    ('42 Floor', '42 Floor'),
    ('43 Floor', '43 Floor'),
    ('44 Floor', '44 Floor'),
    ('45 Floor', '45 Floor'),
    ('46 Floor', '46 Floor'),
    ('47 Floor', '47 Floor'),
    ('48 Floor', '48 Floor'),
    ('49 Floor', '49 Floor'),
    ('50 Floor', '50 Floor'),
    ('51 Floor', '51 Floor'),
    ('52 Floor', '52 Floor'),
    ('53 Floor', '53 Floor'),
    ('54 Floor', '54 Floor'),
    ('55 Floor', '55 Floor'),
    ('56 Floor', '56 Floor'),
    ('57 Floor', '57 Floor'),
    ('58 Floor', '58 Floor'),
    ('59 Floor', '59 Floor'),
    ('60 Floor', '60 Floor'),
    ('61 Floor', '61 Floor'),
    ('62 Floor', '62 Floor'),
    ('63 Floor', '63 Floor'),
    ('64 Floor', '64 Floor'),
    ('65 Floor', '65 Floor'),
    ('66 Floor', '66 Floor'),
    ('67 Floor', '67 Floor'),
    ('68 Floor', '68 Floor'),
    ('69 Floor', '69 Floor'),
    ('70 Floor', '70 Floor'),
    ('71 Floor', '71 Floor'),
    ('72 Floor', '72 Floor'),
    ('73 Floor', '73 Floor'),
    ('74 Floor', '74 Floor'),
    ('75 Floor', '75 Floor'),
    ('76 Floor', '76 Floor'),
    ('77 Floor', '77 Floor'),
    ('78 Floor', '78 Floor'),
    ('79 Floor', '79 Floor'),
    ('80 Floor', '80 Floor'),
    ('81 Floor', '81 Floor'),
    ('82 Floor', '82 Floor'),
    ('83 Floor', '83 Floor'),
    ('84 Floor', '84 Floor'),
    ('85 Floor', '85 Floor'),
    ('86 Floor', '86 Floor'),
    ('87 Floor', '87 Floor'),
    ('88 Floor', '88 Floor'),
    ('89 Floor', '89 Floor'),
    ('90 Floor', '90 Floor'),
]

    
    
    
    AGE_CHOICES = [
        ('', 'Select an option'),
        ('Less than one year', 'Less than one year'),
        ('1-5 Year', '1-5 Year'),
        ('5-10 Years', '5-10 Years'),
        ('More than 10 Years', 'More than 10 Years')
    ]
    
    RENOVATED_CHOICES = [
        ('', 'Select an option'),
        ('Not Yet Renovated', 'Not Yet Renovated'),
        ('1-5 Year Before', '1-5 Year Before'),
        ('5-10 Years Before', '5-10 Years Before'),
        ('More than 10 Years Before', 'More than 10 Years Before')
    ]
    
    KM_CHOICES = [
        ('', 'Select an option'),
        ('Less than 1 Kilometer', 'Less than 1 Kilometer'),
        ('1-5 Kilometer near', '1-5 Kilometer'),
        ('5-10 Kilometer', '5-10 Kilometer'),
        ('More than 10 Kilometer', 'More than 10 Kilometer')
    ]
    
    GARAGE_CHOICES = [
        ('', 'Select an option'),
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('More than 2', 'More than 2')
        
    ]
    
    ROOM_CHOICES = [
        ('', 'Select an option'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('More than 8', 'More than 8'),
    ]
    
    FEATURES_CHOICES = [
    ('Air Condition', 'Air Condition'),
    ('Playing Area', 'Playing Area'),
    ('Well(Water Availability)', 'Well(Water Availability)'),
    ('Balcony ', 'Balcony '),
    ('Parking', 'Parking'),
    ('Concrete Flooring', 'Concrete Flooring'),
    ('Garden', 'Garden'),
    ('Internet ', 'Internet'),
    ('Furnished', 'Furnished'),
    ('Fireplace', 'Fireplace'),
    ('Security System', 'Security System'),
]
    PLACE_CHOICES = [
    ('Schools', 'Schools'),
    ('Hospitals Facilities', 'Hospitals Facilities'),
    ('Well(Water Availability)', 'Well(Water Availability)'),
    ('Shopping Centers', 'Shopping Centers'),
    ('Public Transportation', 'Public Transportation'),
    ('Restaurants and Dining', 'Restaurants and Dining'),
    ('Fitness Centers', 'Fitness Centers'),
    ('Major Roads and Highways', 'Major Roads and Highways'),
    ('Employment Centers', 'Employment Centers'),
    ('Beach', 'Beach:'),
    ('Shopping Complex', 'Shopping Complex'),
     ('Parks', 'Parks'),
    ('Transportation Hubs', 'Transportation Hubs'),
    ('Cinema Centers', 'Cinema Centers'),

]
    
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    thumbnail = models.FileField(upload_to='thumbnail/')
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    owner_name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    Town = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    description = models.CharField(max_length=500)
    floor_plan = models.FileField(upload_to='floorplan/', default='',null=True, blank=True)
    whatsapp_no = models.IntegerField()
    nearby_place = models.CharField(max_length=255, default='',null=True, blank=True)
    features = models.CharField(max_length=255,default='',)
    price = models.IntegerField()
    area = models.CharField(max_length=100)
    property_type = models.CharField(max_length=40, choices=TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, blank=True, null=True)
    bedrooms = models.CharField(max_length=40, choices=BEDROOM_CHOICES, blank=True, null=True)
    bathrooms = models.CharField(max_length=40, choices=BATHROOM_CHOICES, blank=True, null=True)
    rooms = models.CharField(max_length=40, choices=ROOM_CHOICES, blank=True, null=True)
    state = models.CharField(max_length=40, choices=STATE_CHOICES, blank=True, null=True)
    garage = models.CharField(max_length=40, choices=GARAGE_CHOICES, blank=True, null=True)
    major_road = models.CharField(max_length=40, choices=KM_CHOICES, blank=True, null=True)
    near_hospital = models.CharField(max_length=40, choices=KM_CHOICES, blank=True, null=True,)
    near_supermarket = models.CharField(max_length=40, choices=KM_CHOICES, blank=True, null=True)
    bulding_age = models.CharField(max_length=40, choices=AGE_CHOICES, blank=True, null=True)
    floor = models.CharField(max_length=40, choices=FLOOR_CHOICES, blank=True, null=True)
    floor_no = models.CharField(max_length=40, choices=AFLOOR_CHOICES, blank=True, null=True)
    last_renovated = models.CharField(max_length=40, choices=RENOVATED_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    

    def __str__(self):
        return f"Property ID {self.pk}"

    


class Image(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='property_images/', blank=True)  

    def __str__(self):
        return f"Image for {self.property.owner_name}" 
    
class PropertyView(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Feedback(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_feedbacks', blank=True)

    def __str__(self):
        return self.first_name
    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')

    def __str__(self):
        return f'{self.user.username} - {self.property.address}'

    
