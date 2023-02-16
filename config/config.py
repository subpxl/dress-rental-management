class Config:
    Male ="Male"
    Female="Female"
    Other="Other"
    Morning=1
    Evening=3
    Afternoon=2
    GENDER = (
        ('Male', Male),
        ('Female', Female),
        ('Other', Other),
    )
    DayTime = (
        ('Morning',Morning),
        ('Evening',Evening),
        ('Afternoon',Afternoon),
    )
    Available = "Available"
    Booked = 'Booked'
    NotAvailable = 'Not Available'
    Returned="Returned"
    Maintainance="Maintainance"
    STATUS = (
        ('Available', Available),
        ('Booked', Booked),
        ('Not Available',NotAvailable ),
        ('Returned',Returned),
        ('Maintainance',Maintainance),
    )
    rajgharana_jaora ='rajgharana jaora'
    SHOP = (
        # ('rajgharana jaora':rajgharana_jaora)
    )

    # roles
    ShopOwner='ShopOwner'
    Manager='ShopManager'
    Staff='ShopStaff'

    ROLE_CHOICES = [
        ('ShopOwner', ShopOwner),
        ('Manager', Manager),
        ('Staff', Staff),
    ]
