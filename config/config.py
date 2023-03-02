class Config:
    Male ="Male"
    Female="Female"
    Other="Other"
    Morning='Morning'
    Evening='Evening'
    Afternoon='Afternoon'
    GENDER = (
        ('Male', Male),
        ('Female', Female),
        ('Other', Other),
    )
    DayTime = (
        ('1',Morning),
        ('2',Afternoon),
        ('3',Evening),
    )
    Available = "Available"
    Booked = 'Booked'
    NotAvailable = 'Not Available'
    Returned="Returned"
    Maintainance="Maintainance"
    PickedUp="Picked Up"
    STATUS = (
        ('Available', Available),
        ('Booked', Booked),
        ('Not Available',NotAvailable ),
        ('Returned',Returned),
        ('Maintainance',Maintainance),
        ('Picked Up',PickedUp)
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
