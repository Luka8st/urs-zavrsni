/*
 * RFID.cpp
 *
 * Created: 7/31/2018 12:03:28 AM
 * Author : Xiu
 */ 

#include <stdio.h>


#include "RFID.h"

void sendz(uint8_t c)
{
	while(bit_is_clear(UCSRA,UDRE));// doi den khi bit UDRE = 1
	UDR = c;
}
void SPI_MasterInit(void)
{
	DDRB |= (1<<SCK_PIN)|(1<<MOSI_PIN)|(1<<SS);
	//PORTB|=(1<<MISO_PIN);
	SPCR |=	(1<<SPE)|(1<<MSTR)|(1<<SPR0);
	sbi(PORTB,SS);
}


void _SendString(char str[])
{
	int i =0;
	
	while (str[i] != 0x00)
	{
		sendz(str[i]);
		i++;
	}
}

MFRC522 abc(4,0);

int main(void)
{
	DDRA = 0xff;
	PORTA = 0xff;
	
	SPI_MasterInit();
	
	UBRRL = 103;
	UCSRC =	(1<<URSEL)|(1 << UCSZ1) | (1 << UCSZ0); // k chon UBRRch va chon mode 8bit
	UCSRB = (1 << TXEN); //EN rx,tx,ngat
	DDRA = 0xff;
	abc.begin();
	_SendString("START");
	int count = 0;
	while(1)
	{
		
		uint8_t status;
		uint8_t data[MAX_LEN];
		
		status = abc.requestTag(MF1_REQIDL, data);
		//sendz(status);
		if (status == MI_OK) {
			PORTA = 0xfe;
			_delay_ms(1000);
			
			PORTA = 0xff;

			status = abc.antiCollision(data);
			
			for (int i = 0; i < 5; i++) {
				sendz(data[i]);
						
			switch(data[i])
			{
				case 0x85:
				count++;
				break;
				
				case 0xA8:
				count++;
				break;
				
				case 0x13:
				count++;
				break;
				
				case 0xAB:
				count++;
				break;
				
				case 0x95:
				count++;
				break;
			}
		}
			if(count == 5)
			{
				sbi(PORTA,0);
				count=0;
			}
			else
			{
				 count = 0;
				 cbi(PORTA,0);
			}
			abc.selectTag(data);

			// Stop the tag and get ready for reading a new tag.
			abc.haltTag();
			
			/*PORTA = 0xfe;
			_delay_ms(1000);
			
			PORTA = 0xff;*/
		}
	
	}
}

