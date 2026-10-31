"""Host-side checks for the ATmega328P Timer1 frequency calculations."""

F_CPU = 16_000_000


def timer_top(requested_hz: int) -> int:
    return (F_CPU + requested_hz // 2) // requested_hz - 1


def actual_frequency(top: int) -> int:
    return F_CPU // (top + 1)


def test_exact_40_khz():
    top = timer_top(40_000)
    assert top == 399
    assert actual_frequency(top) == 40_000


def test_frequency_range_quantization_is_small():
    for requested in range(38_000, 42_001, 100):
        generated = actual_frequency(timer_top(requested))
        relative_error = abs(generated - requested) / requested
        assert relative_error < 0.003


def test_top_and_half_duty_are_valid():
    for requested in (38_000, 40_000, 42_000):
        top = timer_top(requested)
        compare = (top - 1) // 2
        duty = (compare + 1) / (top + 1)
        assert 380 <= top <= 421
        assert abs(duty - 0.5) < 0.002

