from django.db import models

class MentalTest(models.Model):
    """
        Mental Test class
    """
    owner = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    name  = models.CharField(max_length=255)
    description =  models.TextField(blank=True, null=True)
    alias =  models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MentalTestFieldType(models.Model):
    """
        Mental Test Field Type class, stores the field types for mental tests.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    initial_label = models.CharField(max_length=255)
    final_label = models.CharField(max_length=255)
    initial_range = models.IntegerField(default=0)
    final_range = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MentalTestField(models.Model):
    """
        Mental Test Field class, stores the field for mental tests.
    """
    test = models.ForeignKey(MentalTest, related_name='mental_test_fields', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    field_type = models.ForeignKey(MentalTestFieldType, related_name='fieldtypes',
                                   on_delete=models.DO_NOTHING)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class MentalTestResult(models.Model):
    """
        Mental Test Result class, stores the results
    """
    test = models.ForeignKey(MentalTest, related_name='test', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', related_name='user', on_delete=models.DO_NOTHING)
    test_field = models.ForeignKey(MentalTestField, related_name='test_field',
                                   on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=5)

    def __str__(self):
        return self.test_field.name + " :: " + self.user.username

class MentalTestDiagnosis(models.Model):
    """
        Mental Test Diagnosis class, stores the results of the tests
    """
    test = models.ForeignKey(MentalTest, related_name='diagnosis_test', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', related_name='diagnosis_user', on_delete=models.DO_NOTHING)
    value = models.IntegerField(default=0)
    max_value = models.IntegerField(default=0)

    def __str__(self):
        return self.test.name + " :: " + self.user.username + "::" + str(self.value)


class Company(models.Model):
    """
        Users are part of companies
    """
    owner = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    name  = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    postal_code = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    description =  models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
        Employee 
    """
    company = models.ForeignKey(Company, related_name='company', on_delete=models.DO_NOTHING)
    user = models.OneToOneField('auth.User', related_name='employee', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username + " :: " + self.company.name

