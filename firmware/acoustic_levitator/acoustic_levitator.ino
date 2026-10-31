/*
 * Concave 36+36 acoustic levitator controller for ATmega328P at 16 MHz.
 * Timer1 generates synchronized 38-42 kHz waveforms on OC1A (D9) and
 * OC1B (D10). Each output drives one TB6612FNG bridge input and a 74HC14
 * supplies the complementary input. D8 controls the bridge STBY pin.
 */

#include <Arduino.h>
#include <util/atomic.h>

#if F_CPU != 16000000UL
#error "This controller requires an ATmega328P clocked at 16 MHz"
#endif

namespace {
constexpr uint8_t kEnablePin = 8;
constexpr uint8_t kBankAPin = 9;
constexpr uint8_t kBankBPin = 10;
constexpr uint32_t kDefaultFrequencyHz = 40000UL;
constexpr uint32_t kMinFrequencyHz = 38000UL;
constexpr uint32_t kMaxFrequencyHz = 42000UL;
constexpr size_t kCommandBufferSize = 32;

char commandBuffer[kCommandBufferSize];
size_t commandLength = 0;
bool discardLine = false;
uint32_t frequencyHz = kDefaultFrequencyHz;
bool phaseInverted = false;
bool outputEnabled = false;

uint16_t timerTopForFrequency(uint32_t requestedHz) {
  return static_cast<uint16_t>((F_CPU + requestedHz / 2UL) / requestedHz - 1UL);
}

uint32_t actualFrequencyForTop(uint16_t top) {
  return F_CPU / (static_cast<uint32_t>(top) + 1UL);
}

void setOutputEnable(bool enabled) {
  outputEnabled = enabled;
  digitalWrite(kEnablePin, enabled ? HIGH : LOW);
}

void configureTimer(uint32_t requestedHz, bool invertBankB) {
  // Keep the larger capacitive banks disabled while changing timer timing.
  const bool restoreEnable = outputEnabled;
  setOutputEnable(false);
  const uint16_t top = timerTopForFrequency(requestedHz);
  const uint16_t halfDuty = (top - 1U) / 2U;

  ATOMIC_BLOCK(ATOMIC_RESTORESTATE) {
    // Disconnect outputs while changing TOP and compare modes.
    TCCR1A = _BV(WGM11);
    TCCR1B = _BV(WGM13) | _BV(WGM12);
    TCNT1 = 0;
    ICR1 = top;
    OCR1A = halfDuty;
    OCR1B = halfDuty;

    // Fast PWM, TOP=ICR1, no prescaler. Bank A is non-inverting.
    // Bank B can be non-inverting (0 deg) or inverting (180 deg).
    TCCR1A = _BV(WGM11) | _BV(COM1A1) |
             (invertBankB ? (_BV(COM1B1) | _BV(COM1B0)) : _BV(COM1B1));
    TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS10);
  }

  frequencyHz = actualFrequencyForTop(top);
  phaseInverted = invertBankB;
  setOutputEnable(restoreEnable);
}

void printStatus() {
  Serial.print(F("frequency_hz="));
  Serial.print(frequencyHz);
  Serial.print(F(" phase_deg="));
  Serial.print(phaseInverted ? 180 : 0);
  Serial.print(F(" enabled="));
  Serial.println(outputEnabled ? 1 : 0);
}

void printHelp() {
  Serial.println(F("Commands:"));
  Serial.println(F("  F <38000..42000>  set frequency in Hz"));
  Serial.println(F("  P <0|180>          set bank B phase relative to A"));
  Serial.println(F("  E <0|1>            disable/enable bridge"));
  Serial.println(F("  S                  print status"));
  Serial.println(F("  H                  print help"));
}

void handleCommand(char *line) {
  while (*line == ' ' || *line == '\t') {
    ++line;
  }
  if (*line == '\0') return;
  const char command = toupper(static_cast<unsigned char>(*line++));
  while (*line == ' ' || *line == '\t') {
    ++line;
  }
  char *end = nullptr;
  const unsigned long value = strtoul(line, &end, 10);
  if (command == 'F' || command == 'P' || command == 'E') {
    if (*line < '0' || *line > '9') {
      Serial.println(F("ERR expected unsigned integer"));
      return;
    }
    while (*end == ' ' || *end == '\t') ++end;
    if (*end != '\0') {
      Serial.println(F("ERR trailing characters"));
      return;
    }
  }


  switch (command) {
    case 'F':
      if (end == line || value < kMinFrequencyHz || value > kMaxFrequencyHz) {
        Serial.println(F("ERR frequency range is 38000..42000 Hz"));
        return;
      }
      configureTimer(value, phaseInverted);
      printStatus();
      break;
    case 'P':
      if (end == line || (value != 0UL && value != 180UL)) {
        Serial.println(F("ERR phase must be 0 or 180 degrees"));
        return;
      }
      configureTimer(frequencyHz, value == 180UL);
      printStatus();
      break;
    case 'E':
      if (end == line || value > 1UL) {
        Serial.println(F("ERR enable must be 0 or 1"));
        return;
      }
      setOutputEnable(value == 1UL);
      printStatus();
      break;
    case 'S':
      printStatus();
      break;
    case 'H':
    case '?':
      printHelp();
      break;
    default:
      Serial.println(F("ERR unknown command; use H for help"));
  }
}
}  // namespace

void setup() {
  pinMode(kEnablePin, OUTPUT);
  digitalWrite(kEnablePin, LOW);  // Hardware-safe state before timer setup.
  pinMode(kBankAPin, OUTPUT);
  pinMode(kBankBPin, OUTPUT);
  digitalWrite(kBankAPin, LOW);
  digitalWrite(kBankBPin, LOW);

  Serial.begin(115200);
  configureTimer(kDefaultFrequencyHz, false);
  Serial.println(F("Concave 36+36 controller ready; bridge disabled."));
  printStatus();
  printHelp();
}

void loop() {
  while (Serial.available() > 0) {
    const char incoming = static_cast<char>(Serial.read());
    if (incoming == '\r') {
      continue;
    }
    if (incoming == '\n') {
      commandBuffer[commandLength] = '\0';
      if (!discardLine && commandLength > 0) {
        handleCommand(commandBuffer);
      }
      commandLength = 0;
      discardLine = false;
      continue;
    }
    if (discardLine) continue;
    if (commandLength < kCommandBufferSize - 1) {
      commandBuffer[commandLength++] = incoming;
    } else {
      commandLength = 0;
      discardLine = true;
      Serial.println(F("ERR command too long"));
    }
  }
}

