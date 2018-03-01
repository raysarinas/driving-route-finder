




    with Serial("/dev/ttyACM0", baudrate=9600, timeout=0.1) as ser:
        while True: # infinite loop
            line = ser.readline() # reading from serial thing
            if not line: #if blank line, timeout and restart the loop
                print("timeout, restarting...")
                continue #
            line_string = line.decode("ASCII") # turns 8 bit crap to ASCII stuff
            stripped = line_string.rstrip("\r\n") # remove the \r?
            print(stripped) # first request input line thing
            if stripped[0] == 'R':
                received = stripped.split() # same as processing input from process_input
                v1 = nearest_vertices(location, (received[1], received[2])) # start
                v2 = nearest_vertices(location, (received[3], received[4])) # end
                path = [] # get empty list
                path = least_cost_path(edmonton, v1, v2, cost) # get the least cost path
                if not path: # if empty, then say there is no path
                    a = "N 0\n" # empty stuff
                    encoded = a.encode("ASCII") # encode to garbage
                    ser.write(encoded)  # garge writes to serial thingy
                else: # if not empty
                    a = "N " + str(len(path)) + "\n" # get number of waypoints
                    encoded = a.encode("ASCII") # encode
                    ser.write(encoded) # send garbage to serial
                    continue # loop again
            elif stripped[0] == 'A': # if there is a valid response
                if path: # if there is a path, print out W thing
                    waypoint = location[path.pop(0)]
                    a = "W " + str(waypoint[0]) + " " + str(waypoint[1]) + "\n"
                else: # print E when gone through all waypoints
                    a = "E \n"

                encoded = a.encode("ASCII") # encode
                ser.write(encoded) # send garbage
                continue # re-loop
            else: # what is this ??? MAYBE FOR PROCESSING ERRORS/INVALID
                out_line = "%"
                encoded = out_line.encode("ASCII")
                ser.write(encoded)

            sleep(2)
    return 0
