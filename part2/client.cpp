#include <Arduino.h>
#include <Adafruit_ILI9341.h>
#include <SD.h>
#include "consts_and_types.h"
#include "map_drawing.h"

// the variables to be shared across the project, they are declared here!
shared_vars shared;

Adafruit_ILI9341 tft = Adafruit_ILI9341(clientpins::tft_cs, clientpins::tft_dc);

void setup() {
  // initialize Arduino
  init();

  // initialize zoom pins
  pinMode(clientpins::zoom_in_pin, INPUT_PULLUP);
  pinMode(clientpins::zoom_out_pin, INPUT_PULLUP);

  // initialize joystick pins and calibrate centre reading
  pinMode(clientpins::joy_button_pin, INPUT_PULLUP);
  // x and y are reverse because of how our joystick is oriented
  shared.joy_centre = xy_pos(analogRead(clientpins::joy_y_pin), analogRead(clientpins::joy_x_pin));

  // initialize serial port
  Serial.begin(9600);
  Serial.flush(); // get rid of any leftover bits

  // initially no path is stored
  shared.num_waypoints = 0;

  // initialize display
  shared.tft = &tft;
  shared.tft->begin();
  shared.tft->setRotation(3);
  shared.tft->fillScreen(ILI9341_BLUE); // so we know the map redraws properly

  // initialize SD card
  if (!SD.begin(clientpins::sd_cs)) {
    Serial.println("Initialization has failed. Things to check:");
    Serial.println("* Is a card inserted properly?");
    Serial.println("* Is your wiring correct?");
    Serial.println("* Is the chipSelect pin the one for your shield or module?");

    while (1) {} // nothing to do here, fix the card issue and retry
  }

  // initialize the shared variables, from map_drawing.h
  // doesn't actually draw anything, just initializes values
  initialize_display_values();

  // initial draw of the map, from map_drawing.h
  draw_map();
  draw_cursor();

  // initial status message
  status_message("FROM?");
}

void process_input() {
  // read the zoom in and out buttons
  shared.zoom_in_pushed = (digitalRead(clientpins::zoom_in_pin) == LOW);
  shared.zoom_out_pushed = (digitalRead(clientpins::zoom_out_pin) == LOW);

  // read the joystick button
  shared.joy_button_pushed = (digitalRead(clientpins::joy_button_pin) == LOW);

  // joystick speed, higher is faster
  const int16_t step = 64;

  // get the joystick movement, dividing by step discretizes it
  // currently a far joystick push will move the cursor about 5 pixels
  xy_pos delta(
    // the funny x/y swap is because of our joystick orientation
    (analogRead(clientpins::joy_y_pin)-shared.joy_centre.x)/step,
    (analogRead(clientpins::joy_x_pin)-shared.joy_centre.y)/step
  );
  delta.x = -delta.x; // horizontal axis is reversed in our orientation

  // check if there was enough movement to move the cursor
  if (delta.x != 0 || delta.y != 0) {
    // if we are here, there was noticeable movement

    // the next three functions are in map_drawing.h
    erase_cursor();       // erase the current cursor
    move_cursor(delta);   // move the cursor, and the map view if the edge was nudged
    if (shared.redraw_map == 0) {
      // it looks funny if we redraw the cursor before the map scrolls
      draw_cursor();      // draw the new cursor position
    }
  }
}

void communicate(lon_lat_32 start, lon_lat_32 end){
  // This is the essential part of our code. This communicates betweent the
  // python server and the cpp client.

  //State functions to cycle through different parts of our communication
  enum State {Sending_In, Waiting_N, Sending_A, Waiting_W, Ending};
  // when this function is called we start by sending the stat and end lon and
  // lat values
  State curr_state = Sending_In;
  Serial.println("Starting");
  // Variables needed for this scope
  bool check = false;
  int32_t N_path = 0;
  int path = 0;
  int32_t W_lat_long = 0;
  int count = 1;
  int start_timeout;
  int end_timeout;
  char incomingByte;
  while (true) {
    while (Serial.available() == 0);

    if (curr_state == Ending){
      // this is the last part of the communication. We break outta loop and
      // continue on to the drawing part of this code.
      // we could have a check somewhere else to make sure server is sending
      // 'E' as a confirmation of all the waypoints have been sent.
      // The server is sending this but since everything is working it seems
      // redundant to this now

      Serial.flush();
      break;
    }

    if (curr_state == Waiting_W){
      while(true){
        // we use a while statement to go through all the incoming bytes from
        // the server once the once Serial.read sends '\n' we know that all the
        // info of the waypoints have come in so we store that value and move on
        // either to the next waypoint of to the end state
        incomingByte = Serial.read();
        if (incomingByte == '\n') {
          // marks the end of the incoming data and we then preceed to store
          // values and checks to see if there should be anymore waypoints
          // cominig in by comparing the current loop iteration and the
          // num.waypoints value collected earlier
          if (check){
            // we store longitude as a negative number.
            shared.waypoints[path].lon = -1*W_lat_long;
            path += 1;
              if (path == N_path) {
                curr_state = Ending;
                N_path = 0;
                path = 0;
                check = false;
            }
            Serial.write('A');
            // Sends confirmation to server that we have received the waypoints
            // and ready for the next bit of data
            check = false;
            count = 1;
            W_lat_long = 0;
          }
          break;
        }
        if (incomingByte == -1) continue;
        // if there is nothing in Serial.read we skip over
        if (incomingByte == '%') continue;
        // from python server we send '%' when things don't go perfect in the
        // handshaking process so we have this case to skip over it if it pops up
        if (incomingByte == '-') continue;
        // We deal with the negative longitude in another way at another point
        // so we skip over it in the storing cycle
        if (incomingByte == 'W') {
          // Want to make sure that what is being stored are waypoints
          check = true;
          continue;
        }
        if ((incomingByte == ' ') && (count == 1)) {
          // we ignore the first space and mark it with count that it has happened
          count = 0;
          continue;
        }
        if ((incomingByte == ' ') && (count == 0) && (check)) {
          // this is the second space and marks that we have all the latitude
          // values this waypoint has. we store it and clear our temp out
          count = 2;
          shared.waypoints[path].lat = W_lat_long;
          W_lat_long = 0;
          continue;
        }
        // shifts the numeric values over and adds the next value
        W_lat_long *= 10;
        W_lat_long += (incomingByte - 48);

      }
    }

    if (curr_state == Waiting_N){
      N_path = 0;
      // some reason valuse were being stored into this before this point so
      // we clear it again here
      while (true){
        // we use a while statement to go through all the incoming bytes from
        // the server once the once Serial.read sends '\n' we know that all the
        // info of the waypoints have come in so we store that value and move on
        // either to the next waypoint of to the end state
        incomingByte = Serial.read();
        if (incomingByte == '\n') {
          // marks the end of the incoming data and we then preceed to store
          // values and checks to see if we have value needed and the correct
          // number of paths
          if (check){
            if (N_path == 0){
              // if we have the case of no paths we skip to the end of the state
              // machine with nothing being stored and nothing will be drawn
              curr_state = Ending;
              Serial.write('A'); // python server needs something sent for it to proceed
              N_path = 0;
              check = false;
              break;
            }
            else {
              curr_state = Waiting_W;
              if (N_path > 499) {
                // too many paths
                Serial.write('A'); // python server needs something sent for it to proceed
                curr_state = Ending;
                break;
              }
              shared.num_waypoints = N_path;
              Serial.write('A');

              // Sends confirmation to server that we have received the waypoints
              // and ready for the next bit of data
              check = false;
            }
          }
          break;
        }
        if (incomingByte == -1) continue;
        // if there is nothing in Serial.read we skip over
        if (incomingByte == '%') continue;
        // from python server we send '%' when things don't go perfect in the
        // handshaking process so we have this case to skip over it if it pops up
        if (incomingByte == 'N') {
          // Want to make sure that what is being stored are waypoints
          check = true;
          continue;
        }
        if (incomingByte == ' ') continue;  // skip over space
        // shifts the numeric values over and adds the next value
        N_path *= 10;
        N_path += (incomingByte - 48);
        end_timeout = millis() - start_timeout;
        if (end_timeout > 10000) {
         // timeout if more than 10 seconds pass
         curr_state = Ending;
        }


      }

    }

    if (curr_state == Sending_In){
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
      curr_state = Waiting_N;
      start_timeout = millis();
      // move onto the next state
    }

  }

}

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
        if (incoming == (-1 || '%' || ' ')) {
          continue; // if nothing in serial read
          // or if handshaking is weird or to skip over spaces
        }

        if (incoming == 'N') {
          got_waypoints = true; // make sure got num_waypoints
          continue;
        }

        if (incoming == '\n') {
          // end of the line for incoming data so need to send A

          if (got_waypoints) {

            if ((n_waypoints != 0) && n_waypoints <= 499) {
              current_state = Wait4W; // if range of waypoints O.K. continue to next state
              shared.num_waypoints = n_waypoints; // get the 'N' thing from server i think?
              Serial.write('A');
              got_waypoints = false; // reset the checker thingy so doesn't mess up
            }

            if (n_waypoints > 499) { // too many paths, then treat as no waypoints/path
              Serial.write('A');
              current_state = Done;
              break;
            }

            if ((n_waypoints == 0) || (n_waypoints > 499)) { // if N == 0 or > 499
              Serial.write('A');
              current_state = Done;

              if (n_waypoints == 0) {
                n_waypoints = 0;
                got_waypoints = false;
              }
              break;
            } // end of else

          }
          break; // IDK WHY THO
        }

        // n_waypoints *= 10;
        // n_waypoints += (incoming - 48);
        n_waypoints = (n_waypoints*10) + incoming - 48; // IDK WHAT THIS IS

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

void drawingPath(lon_lat_32 start, lon_lat_32 end){
//added code
//draw line from start to first Wave(if they are in the display)
int32_t starty = latitude_to_y(shared.map_number,start.lat)-shared.map_coords.y;
int32_t startx = longitude_to_x(shared.map_number,start.lon)-shared.map_coords.x;
int32_t endy = latitude_to_y(shared.map_number,shared.waypoints[0].lat)-shared.map_coords.y;
int32_t endx = longitude_to_x(shared.map_number,shared.waypoints[0].lon)-shared.map_coords.x;


//contraints
starty = constrain(starty, 0, 216);
endy = constrain(endy,0,216);


  shared.tft-> drawLine(longitude_to_x(shared.map_number, start.lon)-shared.map_coords.x,
  latitude_to_y(shared.map_number,start.lat)-shared.map_coords.y,
  longitude_to_x(shared.map_number,shared.waypoints[0].lon)-shared.map_coords.x,
  latitude_to_y(shared.map_number, shared.waypoints[0].lat)-shared.map_coords.y,ILI9341_BLUE);


//Draw lines in between the wavepoints
for(int k = 0; k < (shared.num_waypoints-1);k++){
  //calling these a seperate variable so don't have to keep wrting these entire lines
  int32_t startwavey = latitude_to_y(shared.map_number,shared.waypoints[k].lat)-shared.map_coords.y;
  int32_t startwavex = longitude_to_x(shared.map_number,shared.waypoints[k].lon)-shared.map_coords.x;
  int32_t endwavey = latitude_to_y(shared.map_number,shared.waypoints[k+1].lat)-shared.map_coords.y;
  int32_t endwavex = longitude_to_x(shared.map_number,shared.waypoints[k+1].lon)-shared.map_coords.x;
  // startwavey = constrain(startwavey, 0, 216);
  // endwavey = constrain(endwavey,0,216);


  //if the 2 Wavepoints are is in the same screen as the display(shared.map_coords is the top left of the display)
  //We add 320 as x spams to the width of the display and add 216 becuase the y spams to (240-24)becuase of the
  //message prompt

  shared.tft-> drawLine(startwavex,startwavey,endwavex,endwavey,ILI9341_BLUE);
}

//Draw last line between last wavepoint and destination, if in the display range
starty = latitude_to_y(shared.map_number,shared.waypoints[shared.num_waypoints-1].lat)-shared.map_coords.y;
startx = longitude_to_x(shared.map_number,shared.waypoints[shared.num_waypoints-1].lon)-shared.map_coords.x;
endy = latitude_to_y(shared.map_number,end.lat)-shared.map_coords.y;
endx = longitude_to_x(shared.map_number,end.lon)-shared.map_coords.x;

starty = constrain(starty, 0, 216);
endy = constrain(endy,0,216);
  shared.tft-> drawLine(startx,starty,endx,endy,ILI9341_BLUE);

}

int main() {
  setup();

  // very simple finite state machine:
  // which endpoint are we waiting for?
  enum {WAIT_FOR_START, WAIT_FOR_STOP} curr_mode = WAIT_FOR_START;

  // the two points that are clicked
  lon_lat_32 start, end;

  while (true) {
    // clear entries for new state
    shared.zoom_in_pushed = 0;
    shared.zoom_out_pushed = 0;
    shared.joy_button_pushed = 0;
    shared.redraw_map = 0;

    // reads the three buttons and joystick movement
    // updates the cursor view, map display, and sets the
    // shared.redraw_map flag to 1 if we have to redraw the whole map
    // NOTE: this only updates the internal values representing
    // the cursor and map view, the redrawing occurs at the end of this loop
    process_input();

    // if a zoom button was pushed, update the map and cursor view values
    // for that button push (still need to redraw at the end of this loop)
    // function zoom_map() is from map_drawing.h
    if (shared.zoom_in_pushed) {
      zoom_map(1);
      shared.redraw_map = 1;
    }
    else if (shared.zoom_out_pushed) {
      zoom_map(-1);
      shared.redraw_map = 1;
    }

    // if the joystick button was clicked
    if (shared.joy_button_pushed) {

      if (curr_mode == WAIT_FOR_START) {
        // if we were waiting for the start point, record it
        // and indicate we are waiting for the end point
        start = get_cursor_lonlat();
        curr_mode = WAIT_FOR_STOP;
        status_message("TO?");
        //Serial.print("I read the start point (lon,lat) ");
        //Serial.print(start.lon);
        //Serial.print(",");
        //Serial.print(start.lat);
        //Serial.print(" which is in map coords(x,y): ");
        //Serial.print(longitude_to_x(shared.map_number, start.lon));
        //Serial.print(",");
        //Serial.println(latitude_to_y(shared.map_number,start.lat));
        // wait until the joystick button is no longer pushed
        while (digitalRead(clientpins::joy_button_pin) == LOW) {}
      }
      else {
        // if we were waiting for the end point, record it
        // and then communicate with the server to get the path
        end = get_cursor_lonlat();
        // TODO: communicate with the server to get the waypoints
        //Serial.print("I read the end point (lon,lat) ");
        //Serial.print(end.lon);
        //Serial.print(",");
        //Serial.print(end.lat);
        //Serial.print(" which is in map coords(x,y): ");
        //Serial.print(longitude_to_x(shared.map_number, end.lon));
        //Serial.print(",");
        //Serial.println(latitude_to_y(shared.map_number,end.lat));

        status_message("Recieving Wavepoints...");
        //Serial.print("This is map: ");
        //Serial.println(shared.map_number);

        //SERVER HERE WILL MAKE AN ARRAY
        //and assign values to shared.num_waypoints
        //and shared.waypoints[]
        //Ex of the form:
        //shared.num_waypoints = 9;
        //shared.waypoints[0].lat = 5340149;
        //shared.waypoints[0].lon = -11329527;
        //etc....

        //communicate(start, end);
        talk(start, end);
        draw_map(); //gets rid of previously drawn paths
        draw_cursor();
        drawingPath(start,end);  //where drawing of map occurs
        status_message("From?");

        // now we have stored the path length in
        // shared.num_waypoints and the waypoints themselves in
        // the shared.waypoints[] array, switch back to asking for the
        // start point of a new request


        //LEAVE THIS START
        curr_mode = WAIT_FOR_START;
        // wait until the joystick button is no longer pushed
        while (digitalRead(clientpins::joy_button_pin) == LOW) {}
      }
    }


    if (shared.redraw_map) {
      // redraw the status message
      //Serial.print("top left of screen x coord: ");
      //Serial.println(shared.map_coords.x);
      //Serial.print("top left of screen y coor: ");
      //Serial.println(shared.map_coords.y);
      if (curr_mode == WAIT_FOR_START) {
        status_message("FROM?");
      }
      else {
        status_message("TO?");
      }

      // redraw the map and cursor
      draw_map();
      draw_cursor();

      drawingPath(start,end);  // will draw map if next part of screen


    }

  }

  Serial.flush();
  return 0;
}
