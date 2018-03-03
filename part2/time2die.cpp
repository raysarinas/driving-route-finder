void communicate(lon_lat_32 start, lon_lat_32 end){
  // This is the essential part of our code. This communicates betweent the
  // python server and the cpp client.

  //State functions to cycle through different parts of our communication
  enum State {Begin, Wait4N, SendA, Wait4W, Done};
  // when this function is called we start by sDone the stat and end lon and
  // lat values
  State current_state = Begin;
  Serial.println("Starting");
  // Variables needed for this scope
  bool check = false;
  int32_t n_waypoints = 0;
  int path = 0;
  int32_t w_coord = 0;
  int count = 1;
  int start_timeout;
  int end_timeout;
  char incoming;
  while (true) {
    while (Serial.available() == 0);

    if (current_state == Wait4W){
      while(true){
        // we use a while statement to go through all the incoming bytes from
        // the server once the once Serial.read sends '\n' we know that all the
        // info of the waypoints have come in so we store that value and move on
        // either to the next waypoint of to the end state
        incoming = Serial.read();
        if (incoming == '\n') {
          // marks the end of the incoming data and we then preceed to store
          // values and checks to see if there should be anymore waypoints
          // cominig in by comparing the current loop iteration and the
          // num.waypoints value collected earlier
          if (check){
            // we store longitude as a negative number.
            shared.waypoints[path].lon = -1*w_coord;
            path += 1;
              if (path == n_waypoints) {
                current_state = Done;
                n_waypoints = 0;
                path = 0;
                check = false;
            }
            Serial.write('A');
            // Sends confirmation to server that we have received the waypoints
            // and ready for the next bit of data
            check = false;
            count = 1;
            w_coord = 0;
          }
          break;
        }
        if (incoming == -1) continue;
        // if there is nothing in Serial.read we skip over
        if (incoming == '%') continue;
        // from python server we send '%' when things don't go perfect in the
        // handshaking process so we have this case to skip over it if it pops up
        if (incoming == '-') continue;
        // We deal with the negative longitude in another way at another point
        // so we skip over it in the storing cycle
        if (incoming == 'W') {
          // Want to make sure that what is being stored are waypoints
          check = true;
          continue;
        }
        if ((incoming == ' ') && (count == 1)) {
          // we ignore the first space and mark it with count that it has happened
          count = 0;
          continue;
        }
        if ((incoming == ' ') && (count == 0) && (check)) {
          // this is the second space and marks that we have all the latitude
          // values this waypoint has. we store it and clear our temp out
          count = 2;
          shared.waypoints[path].lat = w_coord;
          w_coord = 0;
          continue;
        }
        // shifts the numeric values over and adds the next value
        w_coord *= 10;
        w_coord += (incoming - 48);

      }
    }

    if (current_state == Wait4N){
      n_waypoints = 0;
      // some reason valuse were being stored into this before this point so
      // we clear it again here
      while (true){
        // we use a while statement to go through all the incoming bytes from
        // the server once the once Serial.read sends '\n' we know that all the
        // info of the waypoints have come in so we store that value and move on
        // either to the next waypoint of to the end state
        incoming = Serial.read();
        if (incoming == '\n') {
          // marks the end of the incoming data and we then preceed to store
          // values and checks to see if we have value needed and the correct
          // number of paths
          if (check){
            if (n_waypoints == 0){
              // if we have the case of no paths we skip to the end of the state
              // machine with nothing being stored and nothing will be drawn
              current_state = Done;
              Serial.write('A'); // python server needs something sent for it to proceed
              n_waypoints = 0;
              check = false;
              break;
            }
            else {
              current_state = Wait4W;
              if (n_waypoints > 499) {
                // too many paths
                Serial.write('A'); // python server needs something sent for it to proceed
                current_state = Done;
                break;
              }
              shared.num_waypoints = n_waypoints;
              Serial.write('A');

              // Sends confirmation to server that we have received the waypoints
              // and ready for the next bit of data
              check = false;
            }
          }
          break;
        }
        if (incoming == -1) continue;
        // if there is nothing in Serial.read we skip over
        if (incoming == '%') continue;
        // from python server we send '%' when things don't go perfect in the
        // handshaking process so we have this case to skip over it if it pops up
        if (incoming == 'N') {
          // Want to make sure that what is being stored are waypoints
          check = true;
          continue;
        }
        if (incoming == ' ') continue;  // skip over space
        // shifts the numeric values over and adds the next value
        n_waypoints *= 10;
        n_waypoints += (incoming - 48);
        end_timeout = millis() - start_timeout;
        if (end_timeout > 10000) {
          // timeout if more than 10 seconds pass
          current_state = Done;
        }

      }

    }

    if (current_state == Begin){
      // we send over start and end waypoints
      Serial.print("R ");
      Serial.print(start.lat);
      Serial.print(" ");
      Serial.print(start.lon);
      Serial.print(" ");
      Serial.print(end.lat);
      Serial.print(" ");
      Serial.println(end.lon);
      Serial.flush();
      current_state = Wait4N;
      start_timeout = millis();
      // move onto the next state
    }

    if (current_state == Done) {

      Serial.flush();
      break;
    }

  }

}
