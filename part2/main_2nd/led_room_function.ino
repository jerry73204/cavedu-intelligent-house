
// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}

void colorWipe_living(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip_living.numPixels(); i++) {
    strip_living.setPixelColor(i, c);
    strip_living.show();
    delay(wait);
  }
}

void colorWipe_escape(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip_escape.numPixels(); i++) {
    strip_escape.setPixelColor(i, c);
    strip_escape.show();
    delay(wait);
  }
}
