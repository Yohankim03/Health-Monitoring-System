from requests import post, get, put, delete

url = "http://127.0.0.1:5000/"

while True:
    inp = input("Enter number: \n\t1. Auth \n\t2. Data Reading \n\t3. Device Interface \n\t4. Reports\n\t5. Notification\n\t6. User Management\n\t7. Quit\n")
    if inp == '7':
        break

    match inp:
        # Auth
        case '1':
            while True:
                inp_auth = input("Enter number: \n\t1. UserRegistration \n\t2. UserLogin(WIP) \n\t3. Quit\n")
                if inp_auth == '3':
                    break  # Break out of the auth menu loop, back to the main menu

                match inp_auth:
                    case '1':
                        username = input("Enter username: ")
                        email = input("Enter email: ")
                        password = input("Enter password: ")

                        try:
                            print(post(url+"registration", json={"username": username, "email": email, "password": password}))
                        except Exception as e:
                            print(f"ERROR: Failed to add user {username}:", e)
                            
                    case '2':
                        pass
                    
        case '2':
            while True:
                inp_read = input("Enter number: \n\t1. POST \n\t2. GET \n\t3. Quit\n")
                if inp_read == '3':
                    break
                
                match inp_read:
                    case '1':
                        userid = input("Enter user id: ")
                        type = input("Enter measurement type: ")
                        value = input("Enter measurement value: ")
                        unit = input("Enter measurement unit: ")
                        
                        try:
                            print(post(url+"measurements", json={"user_id": userid, "type":type, "value": value, "unit": unit}))
                        except Exception as e:
                            print(f"ERROR: Failed to add measurment for {userid}:", e)
                            
                    case '2':
                        userid = input("Enter user id: ")
                        print(get(url+"users/"+userid+"/measurements").json())
        
        case '3':
            while True:
                inp_interface = input("Enter number: \n\t1. AddDevice(POST) \n\t2. AssignDevice(POST) \n\t3. UpdateDeviceStatus(PUT) \n\t4. ListDevices(GET) \n\t5. Quit\n")
                if inp_interface == '5':
                    break
                
                match inp_interface:
                    case '1':
                        device_name = input("Enter device name: ")
                        
                        try:
                            print(post(url+"devices", json={"name": device_name}))
                        except Exception as e:
                            print(f"ERROR: Failed to add device: {device_name}", e)
                            
                    case '2':
                        patient_id = input("Enter user id to assign device to: ")
                        device_id = input("Enter device id to asssign user to: ")
                        
                        try:
                            print(post(url+"devices/assign", json={"patient_id": patient_id, "device_id": device_id}))
                        except Exception as e:
                            print(f"ERROR: Failed to add device {device_id} to user {patient_id}.", e)
                
                    case '3':
                        device_id = input("Enter device id: ")
                        status = input("Enter new device status: ")
                        
                        try:
                            print(put(url+"/devices/"+device_id+"/status", json={"status":status}))
                        except Exception as e:
                            print(f"ERROR: Failed to change device {device_id} status.", e)
                        
                    case '4':
                        print(get(url+"devices").json())
                        
        case '4':
            while True:
                inp_report = input("Enter number: \n\t1. CreateReport(POST) \n\t2. ListReports(POST) \n\t3. GetReport(PUT) \n\t4. Quit\n")
                if inp_report == '4':
                    break
                
                match inp_report:
                    case '1':
                        generated_by = input("Enter report creator id: ")
                        patient_id = input("Enter report's patient id: ")
                        
                        try:
                            print(post(url+"reports", json={"generated_by": generated_by, "patient_id": patient_id}))
                        except Exception as e:
                            print(f"ERROR: Failed to create report for patient {patient_id}.", e)
                            
                    case '2':
                        print(get(url+"reports").json())
                    
                    case '3':
                        report_id = input("Enter report id: ")
                        
                        try:
                            print(get(url+"reports/"+report_id).json())
                        except Exception as e:
                            print(f"ERROR: Failed to get report id: {report_id}.", e)
                    
        case '5':
            while True:
                inp_noti = input("Enter number: \n\t1. POST \n\t2. GET \n\t3. Quit\n")
                if inp_noti == '3':
                    break  # Break out of the auth menu loop, back to the main menu
                
                match inp_noti:
                    case '1':
                        userid = input("Enter user id: ")
                        message = input("Enter message: ")
                        
                        try:
                            print(post(url+"notification", json={"user_id": userid, "message": message}))
                        except Exception as e:
                            print(f"ERROR: Failed send {userid} notification:", e)
                            
                    case '2':
                        userid = input("Enter user id: ")
                        
                        if userid=='':
                            try:
                                print(get(url+"notification").json())
                            except Exception as e:
                                print(f"ERROR: Failed to get {userid} notificaiton:", e)
                        else:
                            try:
                                print(get(url+"notification/"+userid).json())
                            except Exception as e:
                                print(f"ERROR: Failed to get {userid} notificaiton:", e)
                                
                                
        case '6':
            while True:
                inp_man = input("Enter number: \n\t1. GetUser(GET) \n\t2. DeleteUser(DELETE) \n\t3. Quit\n")
                if inp_man == '3':
                    break
                
                match inp_man:
                    case '1':
                        print(get(url+"users").json())
                        
                    case '2':
                        userid = input("Enter the id you want to delete: ")
                        delete(url+ "users/" +userid+ "/delete")
                        
            