#define interrupt0Pin 2
#define interrupt1Pin 3
#define interrupt0_location "2-DOWN"
#define interrupt1_location "3-UP"

#define STEP 100

long t0 = 0;
long t1 = 0;

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
    report(interrupt0_location, t0 - t1);
  }
}

void int1()
{
  t1 = (long) micros();
  if (t1 - t0 < STEP)
  {
    report(interrupt1_location, t1 - t0);
  }  
}
 
void setup() {
  pinMode(interrupt0Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interrupt0Pin), int0, RISING);

  pinMode(interrupt1Pin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interrupt1Pin), int1, RISING);

  t0 = 0;
  t1 = 0;

  Serial.begin(9600);
}

void loop() 
{}
