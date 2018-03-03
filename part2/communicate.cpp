void talk(lon_lat_32 start, lon_lat_32 end) {
  // this fun stuff is what allows for communication between
  // the arduino/client and python server to happen I guess

  // state machine unfortunately
  enum State {Begin, Wait4N, Wait4W, Done};
  // dont need SendA state?

  State current_state = Begin;
  Serial.println("beginning/starting whatever u wanna call it");

  // variables apparently
  int32_t n_waypoints;
  int32_t waypoint;
  bool got_waypoints;
  int timeout;
  char incoming;
  bool check1 = true;
  bool check2 = false;


  int path = 0;
  int32_t W_lat_long = 0;
  int count = 1;


  while (true) { // infinite loopy loop
    while (Serial.available() == 0);

    if (current_state == Begin) {
      // send the start and end waypoints?
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
      timeout = millis();
      // move onto next state? idk why
    }

    if (current_state == Wait4N) {
      n_waypoints = 0;
      // set to zero just in case

      while (true) {
        // read incoming bytes from server once we get '\n'
        // so we know the number of waypoints / information have been stored
        // something something idk
        incoming = Serial.read(); // read the incoming byte(s)

        // can we use a SWITCH thing to make this better or nah?
        if (incoming == -1) {
          continue; // if nothing in serial read
          // or if handshaking is weird or to skip over spaces
        }

        if (incoming == '%') { continue; }
        if (incoming == ' ') { continue; }

        if (incoming == 'N') {
          got_waypoints = true; // make sure got num_waypoints
          continue;
        }

        if (incoming == '\n') {
          // end of the line for incoming data so need to send A

          if (got_waypoints) {

            if (n_waypoints == 0) { // if N == 0 or > 499
              Serial.write('A');
              current_state = Done;
              n_waypoints = 0;
              got_waypoints = false;
              break;
            }

            else {
              current_state = Wait4W; // if range of waypoints O.K. continue to next state
              if (n_waypoints > 499) {
                Serial.write('A');
                current_state = Done;
                break;
              }
              shared.num_waypoints = n_waypoints; // get the 'N' thing from server i think?
              Serial.write('A');
              got_waypoints = false; // reset the checker thingy so doesn't mess up
            }

          }
          break; // IDK WHY THO
        }

        // n_waypoints *= 10;
        // n_waypoints += (incoming - 48);
        n_waypoints = (n_waypoints2*10) + incoming - 48; // IDK WHAT THIS IS

        if ((millis() - timeout) > 10000) {
          current_state = Done; // time out I guess but idk when it would
        }
      }
    }

    if (current_state == Wait4W) {
      while (true) { // anotha one so know to store all crap?
        incoming = Serial.read();

        if (incoming == (-1 || '%' || '-')) {
          continue; // if nothing in serial read
          // or if handshaking is weird or to skip over spaces
        }

        if (incoming == 'W') { // DO WE NEED THIS CHECK????
          // make sure got data
          got_waypoints = true;
          continue;
        }

        if ((incoming == ' ') && (check1)) {
          // we ignore the first space and mark it with count that it has happened
          check1 = false;
          check2 = true;
          continue;
        }
        if ((incoming == ' ') && (check2) && (got_waypoints)) {
          // this is the second space and marks that we have all the latitude
          // values this waypoint has. we store it and clear our temp out
          check1 = false;
          check2 = false;
          shared.waypoints[path].lat = W_lat_long;
          waypoint = 0;
          continue;
        }

        // something something numeric value crap
        waypoint = (waypoint*10) + incoming - 48;


      }
    }

    // ''' might be able to remove this because redundant'''
    if (current_state == Done) {
      // if communication done break loop and draw lines
      // and whatever other crap apparently
      // APPARENTLY THIS MIGHT BE REDUNDANT CODE BUT WHOMSDT KNOWS
      Serial.flush();
      break;
    }
  }

}
