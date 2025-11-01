from django.db import models

# Create your models here.
class UserModel(models.Model):
    username=models.CharField(max_length=200)
    email=models.EmailField()
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Income(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    date=models.DateField()
    amount=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}-{self.amount}"
    
class Expense(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    name=models.CharField(max_length=250)
    date=models.DateField()
    amount=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}-{self.amount}"
    
