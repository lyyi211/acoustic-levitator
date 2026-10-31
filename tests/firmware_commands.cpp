#include <cassert>
#include "../firmware/acoustic_levitator/acoustic_levitator.ino"
void send(const std::string &line) { Serial.input=line; loop(); }
int main() {
 setup(); assert(!outputEnabled);
 send("   \n"); assert(!outputEnabled);
 send(std::string(32,'x')+"E 1\n"); assert(!outputEnabled);
 send("E 1junk\n"); assert(!outputEnabled);
 send("E -0\n"); assert(!outputEnabled);
 send("E 1\n"); assert(outputEnabled);
 enableWrites.clear(); send("F 41000\n");
 assert(outputEnabled && enableWrites.size()==2 && enableWrites[0]==LOW && enableWrites[1]==HIGH);
 auto frequency=frequencyHz;send("F 40000junk\n");assert(frequencyHz==frequency);
 send("P 180\n"); assert(phaseInverted);
 send("E 0\n"); assert(!outputEnabled);
 send("E 1\r\n"); assert(outputEnabled);
}
