type reg8 = bits 8
type flag = enum {OFF=0, ON=1}
const MAX = 10

func blink led_pin def {
  loop (var i = 0; i < MAX; i = i + 1) {
    if (i & 1 == 1) {
      {
        instruction: "0x10",
        field: led_pin,
        field: ON
      }
    } else {
      {
        instruction: "0x11",
        field: led_pin,
        field: OFF
      }
    }
  }
}

func main def {
  blink(3)
}
