#include <AFMotor.h>
#define SPEED 150

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

void motors_stop(){

 
  motor1.setSpeed(0);
  motor2.setSpeed(0);
  motor3.setSpeed(0);
  motor4.setSpeed(0);
 
 motor1.run(RELEASE);
 motor2.run(RELEASE);
 motor3.run(RELEASE);
 motor4.run(RELEASE);
}

void motors_forward(){
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);

  motor1.setSpeed(SPEED);  
  motor2.setSpeed(SPEED);  
  motor3.setSpeed(SPEED);  
  motor4.setSpeed(SPEED); 

    delay(10);
}


void motors_backward(){
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);

  motor1.setSpeed(SPEED);  
  motor2.setSpeed(SPEED);  
  motor3.setSpeed(SPEED);  
  motor4.setSpeed(SPEED);
}

void motors_left(){
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD);

    motor1.setSpeed(SPEED);  
    motor2.setSpeed(SPEED);  
    motor3.setSpeed(SPEED);  
    motor4.setSpeed(SPEED);  
    delay(10);
}

void motors_right(){
    motor1.run(BACKWARD);
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor4.run(FORWARD);
  
    motor1.setSpeed(SPEED);  
    motor2.setSpeed(SPEED);  
    motor3.setSpeed(SPEED);  
    motor4.setSpeed(SPEED); 
    delay(10);
}