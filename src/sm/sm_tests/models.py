from django.db import models

class MentalTest(models.Model):
    """
        Mental Test class
    """
    owner = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING)
    name  = models.CharField(max_length=255)
    description =  models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MentalTestFieldType(models.Model):
    """
        Mental Test Field Type class, stores the field types for mental tests.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class MentalTestField(models.Model):
    """
        Mental Test Field class, stores the field for mental tests.
    """
    test = models.ForeignKey(MentalTest, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    field_type = models.ForeignKey(MentalTestFieldType, related_name='fieldtypes',
                                   on_delete=models.DO_NOTHING)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class MentalTestResult(models.Model):
    """
        Mental Test Resutl class, stores the results
    """
    test = models.ForeignKey(MentalTest, on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', related_name='mentaltests', on_delete=models.DO_NOTHING)
    test_field = models.ForeignKey(MentalTestField, related_name='mentaltestfieldtypes',
                                   on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=5)

    def __str__(self):
        return self.test_field.name + " :: " + self.user.name
