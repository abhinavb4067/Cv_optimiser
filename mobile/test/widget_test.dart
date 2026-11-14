import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:career_assistant_app/main.dart';

void main() {
  testWidgets('App boots and shows a splash/login state', (WidgetTester tester) async {
    await tester.pumpWidget(const CareerAssistantApp());
    await tester.pump();

    expect(find.byType(Scaffold), findsOneWidget);
  });
}
