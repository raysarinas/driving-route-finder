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

            else { // if N == 0 or > 499
              Serial.write('A')
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
        incomingByte = Serial.read();

        if (incoming == (-1 || '%' || '-')) {
          continue; // if nothing in serial read
          // or if handshaking is weird or to skip over spaces
        }

        if (incoming == 'W') { // DO WE NEED THIS CHECK????
          // make sure got data
          got_waypoints = true;
          continue;
        }

        if ((incomingByte == ' ') && (check1)) {
          // we ignore the first space and mark it with count that it has happened
          check1 = false;
          check2 = true;
          continue;
        }
        if ((incomingByte == ' ') && (check2) && (check)) {
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

    ''' might be able to remove this because redundant'''
    if (current_state == Done) {
      // if communication done break loop and draw lines
      // and whatever other crap apparently
      // APPARENTLY THIS MIGHT BE REDUNDANT CODE BUT WHOMSDT KNOWS
      Serial.flush();
      break;
    }
  }

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

        //******************* SERIAL MON TEST:
        Serial.print("START POINT: ")
        Serial.print(start.lon);
        Serial.print(", ");
        Serial.println(start.lat);
        Serial.print("START POINT COORDS ON MAP COORDS");
        Serial.print(longitude_to_x(shared.map_number, start.lon));
        Serial.print(", ");
        Serial.println(latitude_to_y(shared.map_number,start.lat));
        //******************** END


        // wait until the joystick button is no longer pushed
        while (digitalRead(clientpins::joy_button_pin) == LOW) {}
      }
      else {
        // if we were waiting for the end point, record it
        // and then communicate with the server to get the path
        end = get_cursor_lonlat();

        //******************* SERIAL MON TEST:
        Serial.print("ENDPOINT: ")
        Serial.print(end.lon);
        Serial.print(", ");
        Serial.println(end.lat);
        Serial.print("ENDPOINT COORDS ON MAP COORDS");
        Serial.print(longitude_to_x(shared.map_number, end.lon));
        Serial.print(", ");
        Serial.println(latitude_to_y(shared.map_number, end.lat));
        //******************** END

        // TODO: communicate with the server to get the waypoints
        talk(start, end);

        // now we have stored the path length in
        // shared.num_waypoints and the waypoints themselves in
        // the shared.waypoints[] array, switch back to asking for the
        // start point of a new request
        curr_mode = WAIT_FOR_START;

        // wait until the joystick button is no longer pushed
        while (digitalRead(clientpins::joy_button_pin) == LOW) {}
      }
    }

    if (shared.redraw_map) {
      // redraw the status message
      if (curr_mode == WAIT_FOR_START) {
        status_message("FROM?");
      }
      else {
        status_message("TO?");
      }

      // redraw the map and cursor
      draw_map();
      draw_cursor();

      // TODO: draw the route if there is one
    }
  }

  Serial.flush();
  return 0;
}
