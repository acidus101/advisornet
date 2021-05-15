# Deployed API
    - https://advisornet.herokuapp.com/
    
# list of apis according to given structure
    i) admin
        1)AdvisorSetAPI
    ii) user
        1)RegisterAPI
        2)LoginAPI
        3)AdvisorViewAPI
        4)MakeBookingAPI
        5)ViewBookingsAPI
    Note: also added few apis
        -view users (UserAPI)
        -logout users(LogoutAPI)

# dummy data
    i) admin
        1) {
                 "name":"kokika sharma",
                    "picture_url" : "https://static.coindesk.com/wp-content/uploads/2021/04/dogecoin-345x222.jpg"
            }
    ii) user
        1){
               "name": "g",
                "email":"g@test.com",
                "password":"test@123"
            }
        2){
                "email":"g@test.com",
                "password":"test@123"
            }
        3)AdvisorViewAPI(none)
        4)  pre-request script = var current_timestamp = new Date();
                                postman.setEnvironmentVariable("current_timestamp", current_timestamp.toISOString());
            dummy data = {
                "bookingDateTime" : "{{current_timestamp}}"
            }   
        5)ViewBookingsAPI(None)
    Note: also added few apis
        -UserAPI(None)
        -LogoutAPI(None)
