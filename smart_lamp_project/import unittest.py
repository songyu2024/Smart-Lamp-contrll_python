import unittest
from unittest.mock import patch, MagicMock
from gpio_control import GPIOController, RELAY_PIN

class TestGPIOController(unittest.TestCase):
    @patch("gpio_control.GPIO")  # Mock OPi.GPIO module
    def test_turn_on_relay(self, mock_gpio):
        # Arrange: Mock GPIO methods
        mock_gpio.output = MagicMock()

        # Act: Create GPIOController instance and call turn_on
        controller = GPIOController()
        controller.turn_on()

        # Assert: Check if relay was turned on
        mock_gpio.output.assert_called_with(RELAY_PIN, mock_gpio.HIGH)

if __name__ == "__main__":
    unittest.main()