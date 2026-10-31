#pragma once
#include <cstdint>
#include <cstdlib>
#include <cctype>
#include <string>
#include <vector>
#define F_CPU 16000000UL
#define F(x) x
#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define _BV(x) (1U << (x))
enum {WGM11,WGM13,WGM12,COM1A1,COM1B1,COM1B0,CS10};
unsigned TCCR1A,TCCR1B,TCNT1,ICR1,OCR1A,OCR1B;
std::vector<int> enableWrites;
void pinMode(int,int) {}
void digitalWrite(int pin,int value) { if(pin==8) enableWrites.push_back(value); }
struct FakeSerial {
 std::string input;
 void begin(int) {}
 int available() { return input.size(); }
 char read() {char c=input.front();input.erase(0,1);return c;}
 template<class T> void print(T) {}
 template<class T> void println(T) {}
} Serial;
