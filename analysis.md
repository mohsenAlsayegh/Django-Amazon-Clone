Products:
    Data: ---> models
        -Name
        -Flag(new,sale)
        -Price
        -Image
        -Reviews 
            -name
            -image
            -review
            -date
            -rate
        -Brand :
            -images
            -name
            -item count 
        -SKU
        -Images
        -Subtitle
        -Tags
        -discription

    Functions: ---> views
        - List 
        - Detail
        - Brand list
        - Brand detail
        - Search
        - Filter
        - Add to cart
        - Add to wishlist
    
Users:
        -Data:
            - username
            - email
            - images
            - contact numbers
                -type(primary,secondary)
                -number
            -address 
                -type: (home,office,business,academy,other)
                -address

        -Functions:
            - Auth
            - Dashboard
            - Profile
            - Edit profile
_____________________________

    App Orders:
    -address
    -product
    -brand
    -qunatity
    -price
    -order_time
    -delivery_time
    -order_id
    - total_item
    -discount
    -delivery fee
    -status =['Recieved', 'Processed', 'Shipped']
