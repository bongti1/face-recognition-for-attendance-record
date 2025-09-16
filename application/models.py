from django.db import models
class Data_student(models.Model):
    label = models.IntegerField()
    std_id = models.CharField(max_length=18 )
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)
    dob = models.DateField()
    tel = models.CharField(max_length=12)
    batch = models.IntegerField()
    major = models.CharField(max_length=10)
    class Meta:
        db_table = "student"
        
    
        
    
    
    
