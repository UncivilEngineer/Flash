//Stream Code V0.3
//by Uncivil_Engineer
//Copywrite 2015
//can only be used for personal use, not for commercial sale.

//The purpose of this sketch is to allow an Adruino Uno to take serial input
//over usb, and display it on Williams system 3 to 6 displays.  All input
//must be wrapped in < > to be valid.  
//Player 1 score format is: <P1XXXXXX>
//Player 2 score format is: <P2XXXXXX> and so on.
//the displays on the main driver board are referred to as 
// displays M1 and M2 in this code.
//where XXXXXXX is the score to be displayed.  'B' can be sent in place of 
//a character to create a blank display.
//Also, invalid input will be displayed as a Blank space.
//refer to the system 3 wiring diagram and schematics for an explenation 
// of the outputs for the board.
//To start the board, a <G> must be sent to enable the displays.
//All displays can be disabled by sending <B> over the USB.
//a word of caution on using Serial.println statments, they severly
//slow the board down, and should only be left on for debugging.

//output assignments for the BCD generators, reffered to as 
//IC 5 and IC7 in the System 3 schematics of the main display driver
//These are pin assignments for Adruino Uno
const int ic5_aPin = 2;
const int ic5_bPin = 3;
const int ic5_cPin = 4;
const int ic5_dPin = 5;

const int ic7_aPin = 7;
const int ic7_bPin = 8;
const int ic7_cPin = 9;
const int ic7_dPin = 10;

//Output for blanking
const int blanking = 6;

const int latchPin = 12;//Pin connected to ST_CP of 74HC595 No. 1
const int clockPin = 13;//Pin connected to SH_CP of 74HC595 No. 1
const int dataPin = 11; //Pin connected to DS of 74HC595 N0. 1

//setup the variable used to store incoming data until it is parsed
//out to the indiviual variable for each display

const byte numChars = 100;
char receivedChars[numChars];

//used in the recvWithStartEndMarkers() function
boolean newData = false;

//here are the character inputs for each display digit
char p1_units = '0';
char p1_tens = '0';
char p1_hundreds = '0';
char p1_thousands = '0';
char p1_10thousands = '0';
char p1_100thousands = '0';

char p2_units = '0';
char p2_tens = '0';
char p2_hundreds = '0';
char p2_thousands = '0';
char p2_10thousands = '0';
char p2_100thousands = '0';

char p3_units = '0';
char p3_tens = '0';
char p3_hundreds = '0';
char p3_thousands = '0';
char p3_10thousands = '0';
char p3_100thousands = '0';

char p4_units = '0';
char p4_tens = '0';
char p4_hundreds = '0';
char p4_thousands = '0';
char p4_10thousands = '0';
char p4_100thousands = '0';

char m1_units = '0';
char m1_tens = '0';
char m2_units = '0';
char m2_tens = '0';

 //needed to keep the code running at 60 hz.  without the delay, the
 //board runs at about 200 hertz
 unsigned long msDelay = 150;

//master flag for display on or off
boolean displayOn = false;


void setup(){
  //initialize the Serial Port
 Serial.begin(9600); 
 
//                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             inputString.reserve(200); 
//setup the output pins
 
 pinMode(ic5_aPin, OUTPUT);
 pinMode(ic5_bPin, OUTPUT);
 pinMode(ic5_cPin, OUTPUT);
 pinMode(ic5_dPin, OUTPUT);
 
 pinMode(ic7_aPin, OUTPUT);
 pinMode(ic7_bPin, OUTPUT);
 pinMode(ic7_cPin, OUTPUT);
 pinMode(ic7_dPin, OUTPUT);
 
 pinMode(dataPin, OUTPUT);       
 pinMode(latchPin, OUTPUT);
 pinMode(clockPin, OUTPUT);
 
 pinMode(blanking, OUTPUT);
 digitalWrite(blanking, LOW);// Start out with displays off
 
 //make sure all strobes start out as low
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 0);
  shiftOut(dataPin, clockPin, MSBFIRST, 0);
  digitalWrite(latchPin, HIGH);
 
// Serial.println("Setup Complete"); 
}

//the main loop
void loop(){
  
  //First we check for new serial stream data
  if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
 
//check to see if displays are active
//if so we start the strobes
if(displayOn){
 
 ///TAKE STROBE 1 LOW VIA REGISTER SHIFT
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);//this byte goes to register shift 2
  shiftOut(dataPin, clockPin, MSBFIRST, 254);//this byte goes to register shift 1
  digitalWrite(latchPin, HIGH); 
  
 //write out player 1 100thousands
  IC5output(p1_100thousands); 
  
  //write out player 3 100thousands
  IC7output(p3_100thousands);
  //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
 
 //TAKE STROBE 1 HIGH, AND SET 2 STROBE  LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 253);
  digitalWrite(latchPin, HIGH);  
  
  //next write P1 10thoutsands
  IC5output(p1_10thousands);
  //write out player 3 101thousands
  IC7output(p3_10thousands);
 
 //we now check for new input again
 //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
  //TAKE STROBE 2 HIGH, AND SET STROBE 3 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 251);
  digitalWrite(latchPin, HIGH);  
  
  //next write P1 thoutsands
  IC5output(p1_thousands);
  //write out player 3 1thousands
  IC7output(p3_thousands);
 
 //we now check for new input again
 //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
 //TAKE STROBE 3 HIGH, AND SET STROBE 4 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 247);
  digitalWrite(latchPin, HIGH); 
  
   //next write P1 hundreds
  IC5output(p1_hundreds);
  //write out player 3 hundreds
  IC7output(p3_hundreds);
  
   //we now check for new input again
 //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
   
//TAKE STROBE 4 HIGH, AND SET STROBE 5 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 239);
  digitalWrite(latchPin, HIGH);  
 
   //next write P1 tens
  IC5output(p1_tens);
  //write out player 3 tens
  IC7output(p3_tens);
  
    //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
   
  //TAKE STROBE 5 HIGH, AND SET STROBE 6 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 223);
  digitalWrite(latchPin, HIGH);
  
   //next write P1 units
  IC5output(p1_units);
  //write out player 3 units
  IC7output(p3_units);

 //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}

 //TAKE STROBE 6 HIGH, AND SET STROBE 7 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 191);
  digitalWrite(latchPin, HIGH);  
  
  // write M2 tens
  IC5output(m2_tens);
  
   //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
//TAKE STROBE 7 HIGH, AND SET STROBE 8 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  shiftOut(dataPin, clockPin, MSBFIRST, 127);
  digitalWrite(latchPin, HIGH);  

  // write M2 units
  IC5output(m2_units);
  
  //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
  
  //half way through the loop, check for input again
   recvWithStartEndMarkers();
  //TAKE STROBE 8 HIGH, AND SET STROBE 9 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 254);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);  
  
  //next write P2 100thousands
  IC5output(p2_100thousands);
  //write out player 4 100thousands
  IC7output(p4_100thousands);
  
    //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
 //TAKE STROBE 9 HIGH, AND SET STROBE 10 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 253);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);

//next write P2 10thousands
  IC5output(p2_10thousands);
  //write out player 4 10thousands
  IC7output(p4_10thousands);
  
    //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
 
  //TAKE STROBE 10 HIGH, AND SET STROBE 11 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 251);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH); 
  
  //next write P2 thousands
  IC5output(p2_thousands);
  //write out player 4 thousands
  IC7output(p4_thousands);
  
    //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
   //TAKE STROBE 11 HIGH, AND SET STROBE 12 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 247);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);
  
  //next write P2 hundreds
  IC5output(p2_hundreds);
  //write out player 4 thousands
  IC7output(p4_hundreds);
  
   //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
    //TAKE STROBE 12 HIGH, AND SET STROBE 13 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 239);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);
  
   //next write P2 tens
  IC5output(p2_tens);
  //write out player 4 tens
  IC7output(p4_tens);
  
  //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
   //TAKE STROBE 13 HIGH, AND SET STROBE 14 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 223);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);
  
    //next write P2 units
  IC5output(p2_units);
  //write out player 4 units
  IC7output(p4_units);
  
   //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
  //TAKE STROBE 14 HIGH, AND SET STROBE 15 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 191);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);
  
  //write master 1 tens
  IC5output(m1_tens);
  
    //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
  //TAKE STROBE 15 HIGH, AND SET STROBE 16 LOW
 digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 127);
  shiftOut(dataPin, clockPin, MSBFIRST, 255);
  digitalWrite(latchPin, HIGH);
  
  //write master 1 units
  IC5output(m1_units);
  
   //we now check for new input again
if (Serial.available() > 0) {
  recvWithStartEndMarkers();
  }
  else{delayMicroseconds(msDelay);}
  
  //end of ouput updates
  
}// end of display on loop
  
}//end of main loop


//This is the routine that gets the input from the USB bus
void recvWithStartEndMarkers(){
  static boolean recvInProgress = false;
	static byte ndx = 0;
	char startMarker = '<';
	char endMarker = '>';
	char rc;

if (Serial.available() > 0) {
  
//Serial.println("Serial called");
 rc = Serial.read();
//are we adding to the existing string?
if (recvInProgress == true) {
  //if so, look for the  end marker
	if (rc != endMarker) {
	receivedChars[ndx] = rc;
	ndx++;
         //is the string too long (over 50 characters)                       
	if (ndx >= numChars) {
	ndx = numChars - 1;
	}
			}//end of look for end marker

                        // if you get an end marker, it terminate the string....
			else {
				receivedChars[ndx] = '\0'; // terminate the string
				recvInProgress = false;
				ndx = 0;
				newData = true;
			}//end of else statement

		}//end of recieved in progress true?

		else if (rc == startMarker) {
			recvInProgress = true;
		}



	}//end of serial avalaible

//check to see if input data came through

if(newData){// So we now have new data to parse

//debugging lines
//Serial.print("Data Recieved :");
//Serial.println(receivedChars);
  
  //Player 1 score parser
  if(receivedChars[0] == 'P' && receivedChars[1] == '1'){
   p1_100thousands = receivedChars[2];
   p1_10thousands = receivedChars[3];
   p1_thousands = receivedChars[4];
   p1_hundreds = receivedChars[5];
   p1_tens = receivedChars[6];
   p1_units = receivedChars[7];
   
   newData = false;
 
 }//end of P1 parcer
 
 //Player 2 score parser
 else if(receivedChars[0] == 'P' && receivedChars[1] == '2'){
   p2_100thousands = receivedChars[2];
   p2_10thousands = receivedChars[3];
   p2_thousands = receivedChars[4];
   p2_hundreds = receivedChars[5];
   p2_tens = receivedChars[6];
   p2_units = receivedChars[7];
   
   newData = false;
   
 }//end of P2 Parcer
 
 //Player 3 score parser
 else if(receivedChars[0] == 'P' && receivedChars[1] == '3'){
   p3_100thousands = receivedChars[2];
   p3_10thousands = receivedChars[3];
   p3_thousands = receivedChars[4];
   p3_hundreds = receivedChars[5];
   p3_tens = receivedChars[6];
   p3_units = receivedChars[7];
   
   newData = false;
   
 }//end of P3 Parcer
 
 //player 4 score parser
else if(receivedChars[0] == 'P' && receivedChars[1] == '4'){
   p4_100thousands = receivedChars[2];
   p4_10thousands = receivedChars[3];
   p4_thousands = receivedChars[4];
   p4_hundreds = receivedChars[5];
   p4_tens = receivedChars[6];
   p4_units = receivedChars[7];
   
   newData = false;
 }//end of P4 Parcer
 
 //Master display 1 parser
 else if(receivedChars[0] == 'M' && receivedChars[1] == '1'){
   m1_tens = receivedChars[2];
   m1_units = receivedChars[3];
   
   newData = false;
 
  } // end of Master 1

//Master display 2 parser  
  else if(receivedChars[0] == 'M' && receivedChars[1] == '2'){
   m2_tens = receivedChars[2];
   m2_units = receivedChars[3];
   
   newData = false;
  }//end of master 2
  
  //This signal needs to come first to activate the displays
  else if(receivedChars[0] == 'G'){
   // Serial.println("All Displays on called");
    digitalWrite(blanking, HIGH);//Blanking has to be high for the displays to run
    newData = false;
    displayOn = true;
  }
  //shutsdown all displays
  
  else if(receivedChars[0] == 'B'){
    Serial.println("All displays down called");
    digitalWrite(blanking, LOW);
    newData = false;
    displayOn = false;
    
    // pulls all strobes low
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, MSBFIRST, 0);
  shiftOut(dataPin, clockPin, MSBFIRST, 0);
  digitalWrite(latchPin, HIGH); 
    
  }
  
  //this is a catchall for bad data.
  else{
    Serial.print("Bad data received :");
    Serial.println(receivedChars);
    newData = false;
  }
  
}//end of newData check

}// end of recvStartEndMark function    

//This function sets the BCD inputs based on the digit recieved.  There are tow
//funcitons, one for input to IC 5, and one for IC 7.
void IC5output(char inputNumber){
  
 // Serial.println("IC5output called");
  //Serial.println("inputNumber is:");
  //Serial.println(inputNumber);
  switch (inputNumber){
 
    
    case 'B': //creates a blank unit in the display
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, HIGH);
    break;
    
   case '0':
    digitalWrite(ic5_aPin, LOW);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, LOW);
    break;
  
   case '1':
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, LOW);
    break;
  
  case '2':
    digitalWrite(ic5_aPin, LOW);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, LOW);
    break;
    
  case '3':
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, LOW);
    break;
    
  case '4':
    digitalWrite(ic5_aPin, LOW);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, LOW);
    break;
    
 case '5':
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, LOW);
    break;
  
 case '6':
    digitalWrite(ic5_aPin, LOW);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, LOW);
    break;

case '7':
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, LOW);
    break;
  
  case '8':
    digitalWrite(ic5_aPin, LOW);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, HIGH);
    break;
  
  case '9':
    digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, LOW);
    digitalWrite(ic5_cPin, LOW);
    digitalWrite(ic5_dPin, HIGH);
    break;
    
    default: // if bad input gets through, it will put up a blank
   // Serial.println("error in ic5 routine");
     digitalWrite(ic5_aPin, HIGH);
    digitalWrite(ic5_bPin, HIGH);
    digitalWrite(ic5_cPin, HIGH);
    digitalWrite(ic5_dPin, HIGH);
    break;
  }// end of switch statement
  
}// end of function


//the routine for lighting up IC7 based on the number given
void IC7output(char inputNumber){
  //Serial.println("IC7output called");
  //Serial.println("inputNumber is:");
  //Serial.println(inputNumber);
  
  
  switch (inputNumber){
 
   case 'B':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, HIGH);
    break;
    
   case '0':
    digitalWrite(ic7_aPin, LOW);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, LOW);
    break;
  
   case'1':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, LOW);
    break;
  
  case '2':
    digitalWrite(ic7_aPin, LOW);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, LOW);
    break;
    
  case '3':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, LOW);
    break;
    
  case '4':
    digitalWrite(ic7_aPin, LOW);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, LOW);
    break;
 case '5':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, LOW);
    break;
  
 case '6':
    digitalWrite(ic7_aPin, LOW);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, LOW);
    break;

case '7':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, LOW);
    break;
  
  case '8':
    digitalWrite(ic7_aPin, LOW);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, HIGH);
    break;
  
  case '9':
    digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, LOW);
    digitalWrite(ic7_cPin, LOW);
    digitalWrite(ic7_dPin, HIGH);
    break;
    
    default:
    //Serial.println("error in ic7 routine");
     digitalWrite(ic7_aPin, HIGH);
    digitalWrite(ic7_bPin, HIGH);
    digitalWrite(ic7_cPin, HIGH);
    digitalWrite(ic7_dPin, HIGH);
    break;
  }// end of switch statement
  
}// end of ic7 function

