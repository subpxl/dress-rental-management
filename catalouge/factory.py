import factory
from django.contrib.auth.models import User
from .models import Category
from factory.faker import faker
from seller.models import Branch
    # name = models.CharField(max_length=100)
    # branch = models.ForeignKey(Branch,on_delete=models.CASCADE)


FAKE = faker.Faker()
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model  = Category

    name=factory.Faker("sentence",nb_words=12)
    branch= factory.SubFactory(Branch)

    @factory.lazy_attribute
    def content(self):
        x=""
        for _ in range(0,5):
            x +="\n"+FAKE.paragraph(nb_sentences=30)+"\n"
        return x