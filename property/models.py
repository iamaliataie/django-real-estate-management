from django.db import models
# Create your models here.


def path_generator(instance, filename):
    return f'properties/{instance}/{filename}'

class Property(models.Model):
    type = models.ForeignKey('PropertyType', on_delete=models.DO_NOTHING, related_name='properties')
    owner = models.CharField(max_length=50)
    agent = models.ForeignKey('account.User', on_delete=models.CASCADE, null=True, related_name='agent_properties')
    title = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    size = models.CharField(max_length=50)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    features = models.TextField(null=True, blank=True)
    floor = models.IntegerField(null=True, blank=True)
    hall = models.IntegerField(null=True, blank=True)
    bathroom = models.IntegerField(null=True, blank=True)
    bedroom = models.PositiveIntegerField(null=True, blank=True)
    parking = models.IntegerField(null=True, blank=True)
    basement = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    deal = models.BooleanField(default=False)
    deal_date = models.DateField(null=True, blank=True)
    marker_color = models.CharField(max_length=20, null=True, blank=True)
    type_color = models.CharField(max_length=20, null=True, blank=True)
    type_title = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    def __str__(self) -> str:
        if self.type.title == 'Residential':
            self.marker_color = 'green'
            self.type_color = 'success'
            self.type_title = 'Residential'
        elif self.type.title == 'Commercial':
            self.marker_color = 'red'
            self.type_color = 'danger'
            self.type_title = 'Commercial'
        elif self.type.title == 'Rental':
            self.marker_color = 'yellow'
            self.type_color = 'warning'
            self.type_title = 'Rental'
        self.save()
        return self.title

    def get_features(self):
        return self.features.strip().split(',')
    
    def get_type_colors(self):
        if self.type == 'Commercial':
            return 'red', 'danger'
        return 'yellow', 'warning'
    
    def get_features(self):
        features = list()
        if self.floor:
            features.append('Floor: ' + str(self.floor))
        if self.hall:
            features.append('Hall: ' + str(self.hall))
        if self.bathroom:
            features.append('Bathroom: ' + str(self.bathroom))
        if self.bedroom:
            features.append('Bedroom: ' + str(self.bedroom))
        if self.parking:
            features.append('Parking: ' + str(self.parking))
        if self.basement:
            features.append('Basement')
        return features
    
    
class Image(models.Model):
    property= models.ForeignKey(
        Property, on_delete=models.CASCADE, null=True
        , related_name='images')
    image = models.ImageField(blank=True, upload_to=path_generator)

    def __str__(self):
        return self.property.title


class PropertyType(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to='property_types/', null=True)
    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'
    
    def __str__(self) -> str:
        return self.title
