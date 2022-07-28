import 'package:flutter/services.dart';

class RangeEnforcer extends TextInputFormatter {
  RangeEnforcer(
      this.minRange,
      this.maxRange,
      ) : assert(
  minRange < maxRange,
  );

  final int minRange;
  final int maxRange;

  @override
  TextEditingValue formatEditUpdate(
      TextEditingValue oldValue, TextEditingValue newValue) {
    var value = int.parse(newValue.text);
    if (value < minRange) {
      return TextEditingValue(text: minRange.toString());
    } else if (value > maxRange) {
      if (value.toInt() % 10 == 0) {
        return TextEditingValue(text: 1.toString());
      }

      return TextEditingValue(text: (value.toInt() % 10).toString());

    }
    return newValue;
  }
}