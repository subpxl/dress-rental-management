class Config:
    Male ="Male"
    Female="Female"
    Other="Other"
    GENDER = (
        ('Male', Male),
        ('Female', Female),
        ('Other', Other),
    )
    Available = "Available"
    Booked = 'Booked'
    NotAvailable = 'Not Available'
    Returned="Returned"
    STATUS = (
        ('Available', Available),
        ('Booked', Booked),
        ('Not Available',NotAvailable ),
        ('Returned',Returned)
    )
    rajgharana_jaora ='rajgharana jaora'
    SHOP = (
        # ('rajgharana jaora':rajgharana_jaora)
    )

    # roles
    ShopAdmin='ShopAdmin'
    Manager='ShopManager'
    Staff='ShopStaff'

    ROLE_CHOICES = [
        ('ShopAdmin', ShopAdmin),
        ('Manager', Manager),
        ('Staff', Staff),
    ]
