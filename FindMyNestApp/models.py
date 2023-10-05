from django.db import models
from UserApp.models import CustomUser,UserProfile
from Customer.models import Property
from django.utils import timezone

# Create your models here.

VALIDITY_CHOICES = [
        ('1 MONTH', '1 MONTH'),
        ('2 MONTH', '2 MONTH'),
        ('3 MONTH', '3 MONTH'),
        ('4 MONTH', '4 MONTH'),
        ('5 MONTH', '5 MONTH'),
        ('6 MONTH', '6 MONTH'),
        ('7 MONTH', '7 MONTH'),
        ('8 MONTH', '8 MONTH'),
        ('9 MONTH', '9 MONTH'),
        ('10 MONTH', '10 MONTH'),
        ('11 MONTH', '11 MONTH'),
        ('12 MONTH', '12 MONTH'),
    ]

class Subscription(models.Model):  
    sub_type = models.CharField(max_length=40, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    validity = models.CharField(max_length=40, choices=VALIDITY_CHOICES, blank=True, null=True) 
    features = models.CharField(max_length=255 , default='',) 

    def __str__(self):
        return f"{self.sub_type} Subscription"
    
class Payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
        
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link the payment to a user
    razorpay_order_id = models.CharField(max_length=255)  # Razorpay order ID
    payment_id = models.CharField(max_length=255)  # Razorpay payment ID
    amount = models.DecimalField(max_digits=8, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=3)  # Currency code (e.g., "INR")
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp of the payment
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    sub_type = models.ManyToManyField(Subscription)

    def str(self):
        return f"Order for {self.user.username}"

    class Meta:
        ordering = ['-timestamp']

#Update Status not implemented
    def update_status(self):
        # Calculate the time difference in minutes
        time_difference = (timezone.now() - self.timestamp).total_seconds() / 60

        if self.payment_status == self.PaymentStatusChoices.PENDING and time_difference > 1:
            # Update the status to "Failed"
            self.payment_status = self.PaymentStatusChoices.FAILED
            self.save()
    
    

