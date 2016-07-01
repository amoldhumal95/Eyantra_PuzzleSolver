/*
*
* Team Id: 		PS1 301
* Author List: 		Dharini, Arohi, Vivek, Vishnu		
* Filename: 		Robot Navigation
* Theme: 		eyrc+ ps1
*
*/
	


#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include <math.h> //included to support power function
#include "lcd.c"
#include "display.c"

void port_init();
void timer5_init();
void velocity(unsigned char, unsigned char);
void motors_delay();

unsigned char data; //to store received data from UDR1
unsigned char ADC_Conversion(unsigned char);
unsigned char ADC_Value;
unsigned char flag = 0;
unsigned char Left_white_line = 0;
unsigned char Center_white_line = 0;
unsigned char Right_white_line = 0;


//Function To Initialize UART1
// desired baud rate:9600
// actual baud rate:9600 (error 0.0%)
// char size: 8 bit
// parity: Disabled
void uart1_init(void)
{
 UCSR1B = 0x00; //disable while setting baud rate
 UCSR1A = 0x00;
 UCSR1C = 0x06;
 UBRR1L = 0x5F; //set baud rate lo
 UBRR1H = 0x00; //set baud rate hi
 UCSR1B = 0x98;
}


//Function to configure LCD port
void lcd_port_config (void)
{
 DDRC = DDRC | 0xF7; //all the LCD pin's direction set as output
 PORTC = PORTC & 0x80; // all the LCD pins are set to logic 0 except PORTC 7
}

//ADC pin configuration
void adc_pin_config (void)
{
 DDRF = 0x00; 
 PORTF = 0x00;
 DDRK = 0x00;
 PORTK = 0x00;
}


void buzzer_on (void)
{
 unsigned char port_restore = 0;
 port_restore = PINC;
 port_restore = port_restore | 0x08;
 PORTC = port_restore;
}

void buzzer_off (void)
{
 unsigned char port_restore = 0;
 port_restore = PINC;
 port_restore = port_restore & 0xF7;
 PORTC = port_restore;
}



// Timer 5 initialized in PWM mode for velocity control
// Prescale:256
// PWM 8bit fast, TOP=0x00FF
// Timer Frequency:225.000Hz
void timer5_init()
{
	TCCR5B = 0x00;	//Stop
	TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT5L = 0x01;	//Counter lower 8-bit value to which OCR5xH value is compared with
	OCR5AH = 0x00;	//Output compare register high value for Left Motor
	OCR5AL = 0xFF;	//Output compare register low value for Left Motor
	OCR5BH = 0x00;	//Output compare register high value for Right Motor
	OCR5BL = 0xFF;	//Output compare register low value for Right Motor
	OCR5CH = 0x00;	//Output compare register high value for Motor C1
	OCR5CL = 0xFF;	//Output compare register low value for Motor C1
	TCCR5A = 0xA9;	/*{COM5A1=1, COM5A0=0; COM5B1=1, COM5B0=0; COM5C1=1 COM5C0=0}
 					  For Overriding normal port functionality to OCRnA outputs.
				  	  {WGM51=0, WGM50=1} Along With WGM52 in TCCR5B for Selecting FAST PWM 8-bit Mode*/
	
	TCCR5B = 0x0B;	//WGM12=1; CS12=0, CS11=1, CS10=1 (Prescaler=64)
}

void adc_init()
{
	ADCSRA = 0x00;
	ADCSRB = 0x00;		//MUX5 = 0
	ADMUX = 0x20;		//Vref=5V external --- ADLAR=1 --- MUX4:0 = 0000
	ACSR = 0x80;
	ADCSRA = 0x86;		//ADEN=1 --- ADIE=1 --- ADPS2:0 = 1 1 0
}

//Function For ADC Conversion
unsigned char ADC_Conversion(unsigned char Ch) 
{
	unsigned char a;
	if(Ch>7)
	{
		ADCSRB = 0x08;
	}
	Ch = Ch & 0x07;  			
	ADMUX= 0x20| Ch;	   		
	ADCSRA = ADCSRA | 0x40;		//Set start conversion bit
	while((ADCSRA&0x10)==0);	//Wait for conversion to complete
	a=ADCH;
	ADCSRA = ADCSRA|0x10; //clear ADIF (ADC Interrupt Flag) by writing 1 to it
	ADCSRB = 0x00;
	return a;
}

//Function To Print Sesor Values At Desired Row And Coloumn Location on LCD
void print_sensor(char row, char coloumn,unsigned char channel)
{
	
	ADC_Value = ADC_Conversion(channel);
	lcd_print(row, coloumn, ADC_Value, 3);
}

//Function for velocity control
void velocity (unsigned char left_motor, unsigned char right_motor)
{
	OCR5AL = (unsigned char)left_motor;
	OCR5BL = (unsigned char)right_motor;
}

//Function used for setting motor's direction
void motion_set (unsigned char Direction)
{
 unsigned char PortARestore = 0;

 Direction &= 0x0F; 		// removing upper nibbel for the protection
 PortARestore = PORTA; 		// reading the PORTA original status
 PortARestore &= 0xF0; 		// making lower direction nibbel to 0
 PortARestore |= Direction; // adding lower nibbel for forward command and restoring the PORTA status
 PORTA = PortARestore; 		// executing the command
}


unsigned long int ShaftCountLeft = 0; //to keep track of left position encoder 
unsigned long int ShaftCountRight = 0; //to keep track of right position encoder
unsigned int Degrees; //to accept angle in degrees for turning

//Function to configure ports to enable robot's motion
void motion_pin_config (void) 
{
 DDRA = DDRA | 0x0F;
 PORTA = PORTA & 0xF0;
 DDRL = DDRL | 0x18;   //Setting PL3 and PL4 pins as output for PWM generation
 PORTL = PORTL | 0x18; //PL3 and PL4 pins are for velocity control using PWM.
}

//Function to configure INT4 (PORTE 4) pin as input for the left position encoder
void left_encoder_pin_config (void)
{
 DDRE  = DDRE & 0xEF;  //Set the direction of the PORTE 4 pin as input
 PORTE = PORTE | 0x10; //Enable internal pull-up for PORTE 4 pin
}

//Function to configure INT5 (PORTE 5) pin as input for the right position encoder
void right_encoder_pin_config (void)
{
 DDRE  = DDRE & 0xDF;  //Set the direction of the PORTE 4 pin as input
 PORTE = PORTE | 0x20; //Enable internal pull-up for PORTE 4 pin
}

void buzzer_pin_config (void)
{
 DDRC = DDRC | 0x08;		//Setting PORTC 3 as output
 PORTC = PORTC & 0xF7;		//Setting PORTC 3 logic low to turnoff buzzer
}

//Function to initialize ports
void port_init()
{
 buzzer_pin_config();
 motion_pin_config(); //robot motion pins config
 left_encoder_pin_config(); //left encoder pin config
 right_encoder_pin_config(); //right encoder pin config	
}

void left_position_encoder_interrupt_init (void) //Interrupt 4 enable
{
 cli(); //Clears the global interrupt
 EICRB = EICRB | 0x02; // INT4 is set to trigger with falling edge
 EIMSK = EIMSK | 0x10; // Enable Interrupt INT4 for left position encoder
 sei();   // Enables the global interrupt 
}

void right_position_encoder_interrupt_init (void) //Interrupt 5 enable
{
 cli(); //Clears the global interrupt
 EICRB = EICRB | 0x08; // INT5 is set to trigger with falling edge
 EIMSK = EIMSK | 0x20; // Enable Interrupt INT5 for right position encoder
 sei();   // Enables the global interrupt 
}

SIGNAL(SIG_USART1_RECV) 		// ISR for receive complete interrupt
{
	//buzzer_on();

	data = UDR1; 				//making copy of data from UDR1 in 'data' variable 

	UDR1 = data; 				//echo data back to PC
	

		if(data == 0x46) //ASCII value of F
		{
			array[s]='F';  //forward
			array++;
		}

		if(data == 0x4C) //ASCII value of L
		{
			array[s]='L'; //back
			array++;
		}

		if(data == 0x52) //ASCII value of R
		{
			array[s]='R';  
			array++;		
		}

		if(data == 0x55) //ASCII value of U
		{
			array[s]='U';
			array++;
		}

		if(data == 0x42) //ASCII value of B
		{
			array[s]='B';
			array++;
		}

}




//ISR for right position encoder
ISR(INT5_vect)  
{
 ShaftCountRight++;  //increment right shaft position count
}


//ISR for left position encoder
ISR(INT4_vect)
{
 ShaftCountLeft++;  //increment left shaft position count
}



void forward (void) //both wheels forward
{
  motion_set(0x06);
}

void back (void) //both wheels backward
{
  motion_set(0x09);
}

void left (void) //Left wheel backward, Right wheel forward
{
  motion_set(0x05);
}

void right (void) //Left wheel forward, Right wheel backward
{
  motion_set(0x0A);
}

void stop (void)
{
  motion_set(0x00);
}

void angle_rotate(unsigned int Degrees)
{
 float ReqdShaftCount = 0;
 unsigned long int ReqdShaftCountInt = 0;

 ReqdShaftCount = (float) Degrees/ 4.090; // division by resolution to get shaft count
 ReqdShaftCountInt = (unsigned int) ReqdShaftCount;
 ShaftCountRight = 0; 
 ShaftCountLeft = 0; 

 while (1)
 {
  if((ShaftCountRight >= ReqdShaftCountInt) | (ShaftCountLeft >= ReqdShaftCountInt))
  break;
 }
 stop(); //Stop robot
}

//Function used for moving robot forward by specified distance

void linear_distance_mm(unsigned int DistanceInMM)
{
 float ReqdShaftCount = 0;
 unsigned long int ReqdShaftCountInt = 0;

 ReqdShaftCount = DistanceInMM / 5.338; // division by resolution to get shaft count
 ReqdShaftCountInt = (unsigned long int) ReqdShaftCount;
  
 ShaftCountRight = 0;
 while(1)
 {
  if(ShaftCountRight > ReqdShaftCountInt)
  {
  	break;
  }
 } 
 stop(); //Stop robot
}

void forward_mm(unsigned int DistanceInMM)
{
 forward();
 linear_distance_mm(DistanceInMM);
}

void back_mm(unsigned int DistanceInMM)
{
 back();
 linear_distance_mm(DistanceInMM);
}

void left_degrees(unsigned int Degrees) 
{
// 88 pulses for 360 degrees rotation 4.090 degrees per count
 left(); //Turn left
 angle_rotate(Degrees);
}



void right_degrees(unsigned int Degrees)
{
// 88 pulses for 360 degrees rotation 4.090 degrees per count
 right(); //Turn right
 angle_rotate(Degrees);
}







void init_devices (void)
{
 	cli(); //Clears the global interrupts
	port_init();
	adc_init();
	timer5_init();
	left_position_encoder_interrupt_init();
    right_position_encoder_interrupt_init();
 	sei();   //Enables the global interrupts
}

init_devices();
	int s=0;
	int array[1024]={0}; //Initializing array of 1024 which will store values from data; 
	while(1);
	if data=='B'
	{
		break;  //after receiving terminating character, we break
	}
void correction(void){
								while(1)
	                   {

		Left_white_line = ADC_Conversion(3);	//Getting data of Left WL Sensor
		Center_white_line = ADC_Conversion(2);	//Getting data of Center WL Sensor
		Right_white_line = ADC_Conversion(1);	//Getting data of Right WL Sensor


		
		

		if(Center_white_line>=12 && Center_white_line<=80)
		{
			
			forward();
			velocity(200,200);
		}

		else if((Center_white_line>80)) //if node
		{  
		stop(); 
		
		break;
		}

		else if((Left_white_line>=12) && (Left_white_line<=200))
		{
			forward();
			velocity(0,100);
		}

		else if((Right_white_line>=12) && (Right_white_line<=200))
		{
			forward();
			velocity(100,0);
		}

		else if(Center_white_line<12 && Left_white_line<12 && Right_white_line<12)
		{    
		   forward();
		   velocity(200,200);
		}	
		
        else 
		{
		forward();
		velocity(200,200);
		}

	
		}


	             }

//Main Function
int main()
{
	init_devices();
	lcd_set_4bit();
	lcd_init();
    
	
	for(i=0;i<123;i++)   /////MOTHER LOOP
	{
	     Left_white_line = ADC_Conversion(3);	//Getting data of Left WL Sensor
		Center_white_line = ADC_Conversion(2);	//Getting data of Center WL Sensor
		Right_white_line = ADC_Conversion(1);	//Getting data of Right WL Sensor

		//flag=0;

		
			
		if((Center_white_line>0))	///NODE DETECTED
		{	

			
			PORTA=0x00; 
			buzzer_on();
		    _delay_ms(50);		//delay
		    buzzer_off();
		
			forward_mm(75);
            velocity(200,200);
			PORTA=0x00; 
			
			if (array[i]=='F')
		    {
				correction();	
            }
			else if(array[i]=='L')
			{
				left_degrees(98); //Rotate robot left by 90 degrees
		        stop();
				Left_white_line = ADC_Conversion(3);	//Getting data of Left WL Sensor
		Center_white_line = ADC_Conversion(2);	//Getting data of Center WL Sensor
		Right_white_line = ADC_Conversion(1);
		if (Center_white_line<12 && Left_white_line<12 && Right_white_line<12){
			back_mm(15);
			correction();
		}
		else{
			correction();
		}
				
											
       }
		else if(array[i]=='R')
			{
				right_degrees(104); //Rotate robot left by 90 degrees
		        stop();
		Left_white_line = ADC_Conversion(3);	//Getting data of Left WL Sensor
		Center_white_line = ADC_Conversion(2);	//Getting data of Center WL Sensor
		Right_white_line = ADC_Conversion(1);
		if (Center_white_line<12 && Left_white_line<12 && Right_white_line<12){
			back_mm(15);
			correction();
		}
		else{
			correction();
		}

	             }
       
	else if(array[i]=='U')
			{
				right_degrees(201); //Rotate robot left by 90 degrees
		        stop();
									correction();
       }
	 else if(array[i]=='1')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_one();
		led_on();
						
		correction();
		
	 }
	 else if (array[i]=='2'){
		 stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_two();
		led_on();
		correction();				
		
		
	 }
		 
	 
	  else if(array[i]=='3')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_three();
		led_on();
		correction();
		
		
	 }
	  else if(array[i]=='4')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_four();
		led_on();
					correction();


	             }
		
		
	 
	  else if(array[i]=='5')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_five();
		led_on();
					correction();

	             }
		
		
	 
	  else if(array[i]=='6')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_six();
		led_on();
						correction();
		
		
	 }
	  else if(array[i]=='7')
	 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_seven();
		led_on();
			correction();			


	             }
		
		
	 
	 else if(array[i]=='8')
		 {
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_eight();
		led_on();
	correction();
		
		
	 }
	else if(array[i]=='9')
		{
		stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();	
		
		print_nine();
		led_on();
				correction();
		
	 }
	 else if(array[i]=='D')
	 {
		 stop();
		back_mm(190);   //Moves robot backward 100mm
		stop();
		deposit();
		led_off();
		
		buzzer_on();
		_delay_ms(1000);
		buzzer_off();
		
		

			correction();
		
		
		 
	 }
	 else if(array[i]=='B'){
	 stop();
		back_mm(45);
		buzzer_on();
		_delay_ms(5000);  
stop();
buzzer_off();
_delay_ms(1000000000000000); //Moves robot backward 100mm
		
		


	 }
	 }
	
	}
			
	}


