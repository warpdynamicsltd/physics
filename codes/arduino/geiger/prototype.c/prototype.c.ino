#include <stdlib.h>
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);
#define STOPPER_PIN 5
#define interrupt0Pin 2
#define interrupt1Pin 3
#define interrupt0_location "2-UP"
#define interrupt1_location "3-DOWN"
#define STEP 100

unsigned long  i = 0;
unsigned long t = 0;
long t0 = 0;
long t1 = 0;

#define UP 1
#define DOWN 0

#define ON 1
#define OFF 0
struct S
{
  //byte input_state:1;
  byte stopper_state:1;
  byte stopper_button:1;
};

char buff[17];

S state;

/*
void report(int k)
{
  Serial.print("TIME: ");
  Serial.print(micros());
  Serial.print(" ");
  Serial.print("\n");
  Serial.print("INT: ");
  Serial.print(k);
  Serial.print("\n");
  Serial.print("PIN2: ");
  Serial.print(digitalRead(interrupt0Pin));
  Serial.print("\n");
  Serial.print("PIN3: ");
  Serial.print(digitalRead(interrupt1Pin));
  Serial.print("\n");
  Serial.print("INT0_STATE: ");
  Serial.print(state.int0_state);
  Serial.print("\n");
  Serial.print("INT1_STATE: ");
  Serial.print(state.int1_state);
  Serial.print("\n");
  Serial.print("***");
  Serial.print("\n");
}*/

void lcd_time(const unsigned long &t)
{
  sprintf(buff, "WD        %6ld", (long) (t/1000), (int) ((t%1000)/10));
  lcd.print(buff);
}

void lcd_count(const unsigned long &i, const unsigned long &t)
{
  double t_sec = ((double) t)/1000;
  double v = t_sec!=0?((double) i)/t_sec:0;
  
  sprintf(buff, "%6lu %4lu.%04lu", (unsigned long) i, (unsigned long) v, (unsigned long) (round(10000*v)) % 10000);
  lcd.print(buff);
}

void report(const char *s, const long &dt)
{
  Serial.print(s);
  Serial.print(", ");
  Serial.print(dt);
  Serial.print("\n");
}

void int0()
{
  t0 = (long) micros();
  if (t0 - t1 < STEP)
  {
    if (state.stopper_state == ON) i++;
    report(interrupt0_location, t0 - t1);
  }
}

void int1()
{
  t1 = (long) micros();
  if (t1 - t0 < STEP)
  {
    if (state.stopper_state == ON) i++;
    report(interrupt1_location, t1 - t0);
  }  
}
 
void setup() {
  lcd.begin(16, 2);

  //pinMode(INPUT_PIN, INPUT_PULLUP);
  pinMode(STOPPER_PIN, INPUT_PULLUP);

  pinMode(interrupt0Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interrupt0Pin), int0, RISING);

  pinMode(interrupt1Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interrupt1Pin), int1, RISING);

  //state.input_state = UP;
  state.stopper_button = UP;
  state.stopper_state = OFF;
  t = 0;
  i = 0;
  t0 = 0;
  t1 = 0;

  Serial.begin(9600);
}

void loop() 
{
  lcd.setCursor(0, 1);

  /*if(digitalRead(INPUT_PIN) == LOW && state.input_state == UP)
  {
    if (state.stopper_state == ON) i++;
    state.input_state = DOWN;
  }
  if (digitalRead(INPUT_PIN) == HIGH && state.input_state == DOWN)
  {
    state.input_state = UP;
  }*/

  if (digitalRead(STOPPER_PIN) == LOW && state.stopper_button == UP)
  {
    state.stopper_state = 1 - state.stopper_state;
    state.stopper_button = DOWN;

    if (state.stopper_state == ON)
    {
      //Init ON
      lcd.setCursor(0,0);
      lcd.clear();
      i = 0;
      t = millis();
    }

    if (state.stopper_state == OFF)
    {
      //Init OFF
      t = millis()-t;
    }
  }

  if (digitalRead(STOPPER_PIN) == HIGH && state.stopper_button == DOWN)
  {
    state.stopper_button = UP;
  }

  if (state.stopper_state == ON)
  {
    lcd.setCursor(0,0);
    lcd_time(millis()-t);
    lcd.setCursor(0, 1);
    lcd_count(i, millis() - t);
  }
  else
  {
    lcd.setCursor(0,0);
    lcd_time(t);
    lcd.setCursor(0, 1);
    lcd_count(i, t);
  }
  
  lcd.setCursor(0, 1);
  //lcd_count(i, t);
}
